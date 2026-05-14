from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from functools import wraps
import httpx
import os
import pandas as pd
import importlib
from auth import verify_user, register_user, is_rate_limited, ensure_admin_pin

from genomic_risk_pipeline import (
    load_clinvar_variant_summary, load_gwas, load_pharmgkb,
    label_risk, get_matched_diseases, integrate_nutrition_plan
)

# ─────────────────────────────────────────────────────
# In-memory chat session store
# ─────────────────────────────────────────────────────
chat_sessions  = {}
session_counter = 0


def get_authenticated_user_id(request):
    """Returns logged-in username from session, or None"""
    return session.get("username")


def login_required(f):
    """Blocks access if user is not logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Blocks access if:
      - user is not logged in, OR
      - user is not admin, OR
      - admin has not completed PIN verification yet
    Demonstrates: Role-Based Access Control + MFA enforcement
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("login"))
        if session.get("username") != "admin":
            return redirect(url_for("index"))
        # Check PIN was verified in this session
        if not session.get("admin_pin_verified"):
            return redirect(url_for("admin_pin"))
        return f(*args, **kwargs)
    return decorated_function


def create_session(user_id, title=None):
    global session_counter
    session_counter += 1
    session_id = f"session_{session_counter}"
    chat_sessions[session_id] = {
        'id':       session_id,
        'user_id':  user_id,
        'title':    title or f"Chat {session_counter}",
        'messages': []
    }
    return session_id


def get_user_sessions(user_id):
    return [s for s in chat_sessions.values() if s['user_id'] == user_id]


def get_session_messages(session_id):
    if session_id in chat_sessions:
        return chat_sessions[session_id]['messages']
    return []


def add_message_to_session(session_id, user_message, bot_response):
    if session_id in chat_sessions:
        chat_sessions[session_id]['messages'].append({
            'user': user_message,
            'bot':  bot_response
        })


def verify_session_ownership(session_id, user_id):
    return session_id in chat_sessions and chat_sessions[session_id]['user_id'] == user_id


def update_session_title(session_id, title):
    if session_id in chat_sessions:
        chat_sessions[session_id]['title'] = title
        return True
    return False


def delete_session(session_id):
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return True
    return False


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder='templates')
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "genomic-secure-key-2024"

# Ensure admin has a PIN hash stored on startup
ensure_admin_pin()

# ─────────────────────────────────────────────────────
# Load reference SNP databases
# ─────────────────────────────────────────────────────
try:
    print("🔄 Loading reference databases...")
    CLINVAR_DF  = load_clinvar_variant_summary('variant_summary.txt.gz')
    GWAS_DF     = load_gwas('gwas.tsv')
    PHARM_DF    = load_pharmgkb('clinical_annotations.tsv')
    TARGET_SNPS = pd.Series(
        CLINVAR_DF.get('RS# (dbSNP)', pd.Series([], dtype=str)).tolist()
        + GWAS_DF.get('SNPS', pd.Series([], dtype=str)).tolist()
        + PHARM_DF.get('Variant', pd.Series([], dtype=str)).tolist()
    ).astype(str).str.strip().str.lower().unique()
    print(f"✅ Loaded {len(TARGET_SNPS)} target SNPs from databases")
except Exception as e:
    print(f"⚠️ Warning: Could not load reference databases: {e}")
    TARGET_SNPS = []
    CLINVAR_DF  = pd.DataFrame()
    GWAS_DF     = pd.DataFrame()
    PHARM_DF    = pd.DataFrame()
    print("✅ Continuing with empty reference data")


# ─────────────────────────────────────────────────────
# Main app route
# ─────────────────────────────────────────────────────
@app.route('/')
@login_required
def index():
    username = session.get("username", "")
    is_admin = (username == "admin")
    return render_template('index.html', username=username, is_admin=is_admin)


# ─────────────────────────────────────────────────────
# Genomic analysis (completely unchanged)
# ─────────────────────────────────────────────────────
def _analyze_file_at_path(filepath, age):
    try:
        with open(filepath, 'r', errors='ignore') as f:
            lines = f.readlines()

        print(f"📄 Processing file path: {filepath}")
        print(f"📄 Total lines read: {len(lines)}")

        data = []
        try:
            import pandas as _pd
            autodf = _pd.read_csv(filepath, sep=None, engine='python',
                                  comment='#', dtype=str, header='infer')
            autodf = autodf.dropna(how='all')
            cols_lower = [str(c).strip().lower() for c in autodf.columns]
            def _find(colnames):
                for name in colnames:
                    if name in cols_lower:
                        return autodf.columns[cols_lower.index(name)]
                return None
            rs_col = _find(['rsid', 'rs', 'snp', 'id', 'marker', 'rs_id'])
            gt_col = _find(['genotype', 'call', 'allele', 'genotypecall', 'gt'])
            if rs_col is not None and gt_col is not None:
                data.extend(autodf[[rs_col, gt_col]].astype(str).values.tolist())
            elif autodf.shape[1] >= 2:
                data.extend(autodf.iloc[:, [0, 1]].astype(str).values.tolist())
            print(f"✅ Flexible CSV/TSV parse captured {len(data)} rows")
        except Exception as _e:
            print(f"ℹ️ Flexible CSV/TSV parse skipped: {_e}")

        if not data:
            for i, raw in enumerate(lines):
                line = raw.strip()
                if (not line or line.startswith('#') or line.startswith('echo') or
                        line.startswith('cat') or line.startswith('EOF') or
                        line.startswith('<<')):
                    continue
                parts = [p for p in (line.split(',') if ',' in line
                                     else line.split()) if p != '']
                if i == 0 and len(parts) >= 2 and (
                        "rsid" in parts[0].lower() or "snp" in parts[0].lower()):
                    continue
                if len(parts) >= 4:
                    data.append([parts[0], parts[3]])
                elif len(parts) >= 2:
                    data.append([parts[0], parts[1]])
                else:
                    print(f"⚠️ Skipping malformed line {i+1}: {line}")

        print(f"📄 Valid data rows found: {len(data)}")
        if not data:
            return {"error": "File contains no valid data rows."}

        df = pd.DataFrame(data, columns=['snp', 'genotype'])
        df = df.dropna()
        df = df[(df['snp'].str.strip() != '') & (df['genotype'].str.strip() != '')]
        df['snp']      = df['snp'].astype(str).str.strip().str.lower()
        df             = df[df['snp'].str.startswith('rs')]
        df['genotype'] = df['genotype'].astype(str).str.strip()
        df             = df[~df['genotype'].str.contains('-')]
        df             = df[df['genotype'].str.fullmatch(r'[ACGTacgt]{1,2}')]
        before         = len(df)
        df             = df.drop_duplicates(subset=['snp'], keep='first')
        print(f"📊 After cleaning & dedup: {df.shape} (removed {before - len(df)} dups)")

        if df.empty:
            return {"error": "No valid SNP data found after cleaning."}

        try:
            geno_df = df.set_index('snp').T
        except ValueError:
            df      = df.drop_duplicates(subset=['snp'], keep='first').reset_index(drop=True)
            geno_df = df.set_index('snp').T

        valid_snps = ([s for s in TARGET_SNPS if s in geno_df.columns]
                      if len(TARGET_SNPS) > 0 else list(geno_df.columns))

        if not valid_snps:
            return {"risk_level": "Low",
                    "matched_diseases": [("Genetic variant of unknown significance", 0)]}

        geno_df = geno_df[valid_snps]

        if len(CLINVAR_DF) > 0 and 'RS# (dbSNP)' in CLINVAR_DF.columns:
            clinvar_rsids = (CLINVAR_DF['RS# (dbSNP)']
                             .astype(str).str.strip().str.lower()
                             .drop_duplicates().tolist())
            geno_labeled, matched_snps = label_risk(geno_df.copy(), clinvar_rsids)
        else:
            geno_labeled, matched_snps = label_risk(geno_df.copy(), valid_snps)

        import genomic_risk_pipeline as grp
        train_rf_fn = getattr(grp, "train_rf", None)
        if train_rf_fn is None:
            grp         = importlib.reload(grp)
            train_rf_fn = getattr(grp, "train_rf", None)

        def _fallback(_df):
            return None, None
        train_rf_fn = train_rf_fn or _fallback

        model, X_test = train_rf_fn(geno_labeled)
        if model is not None and X_test is not None and len(X_test) > 0:
            risk = model.predict(X_test)[0]
        else:
            total = len(matched_snps)
            risk  = "High" if total >= 10 else ("Medium" if total >= 5 else "Low")

        diseases = (get_matched_diseases(CLINVAR_DF, matched_snps)
                    if len(CLINVAR_DF) > 0
                    else [("General genetic analysis", len(matched_snps))])

        total_overall = sum(c for _, c in diseases)
        risk = "High" if total_overall >= 10 else ("Medium" if total_overall >= 5 else "Low")

        return {"risk_level": risk, "matched_diseases": diseases}

    except Exception as e:
        print(f"Processing error: {str(e)}")
        raise


@app.route('/predict', methods=['POST'])
def predict():
    if 'genomicFile' not in request.files:
        return jsonify({"error": "⚠️ Please upload a valid genomic file."}), 400
    file = request.files['genomicFile']
    age  = int(request.form.get('age', 30))
    if file.filename == '':
        return jsonify({"error": "⚠️ Please upload a valid genomic file."}), 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    try:
        return jsonify(_analyze_file_at_path(filepath, age))
    except Exception:
        return jsonify({"error": "⚠️ Processing failed."}), 500
    finally:
        try: os.remove(filepath)
        except: pass


@app.route('/predict_sample/<level>', methods=['GET'])
def predict_sample(level):
    sample_map = {
        'low':    'low_risk_patient.txt',
        'medium': 'medium_risk_patient.txt',
        'high':   'high_risk_patient.txt',
        'none':   'no_risk_patient.txt',
        'no':     'no_risk_patient.txt'
    }
    age      = int(request.args.get('age', 30))
    filename = sample_map.get(level.lower())
    if not filename or not os.path.exists(filename):
        return jsonify({"error": "Sample not found."}), 404
    try:
        return jsonify(_analyze_file_at_path(filename, age))
    except Exception:
        return jsonify({"error": "⚠️ Failed to analyze sample."}), 500


def process_genome_data(genome_data):
    if not genome_data:
        return []
    df = pd.DataFrame(list(genome_data.items()), columns=['snp', 'genotype'])
    df = df.dropna()
    df = df[(df['snp'].str.strip() != '') & (df['genotype'].str.strip() != '')]
    df['snp']      = df['snp'].astype(str).str.strip().str.lower()
    df             = df[df['snp'].str.startswith('rs')]
    df['genotype'] = df['genotype'].astype(str).str.strip()
    df             = df[~df['genotype'].str.contains('-')]
    df             = df[df['genotype'].str.fullmatch(r'[ACGTacgt]{1,2}')]
    df             = df.drop_duplicates(subset=['snp'], keep='first')
    if df.empty:
        return []
    geno_df    = df.set_index('snp').T
    valid_snps = ([s for s in TARGET_SNPS if s in geno_df.columns]
                  if len(TARGET_SNPS) > 0 else list(geno_df.columns))
    if not valid_snps:
        return []
    geno_df = geno_df[valid_snps]
    if len(CLINVAR_DF) > 0 and 'RS# (dbSNP)' in CLINVAR_DF.columns:
        _, matched_snps = label_risk(
            geno_df.copy(),
            CLINVAR_DF['RS# (dbSNP)'].astype(str).str.strip().str.lower()
            .drop_duplicates().tolist()
        )
    else:
        _, matched_snps = label_risk(geno_df.copy(), valid_snps)
    return matched_snps


@app.route('/analyze_genome', methods=['POST'])
def analyze_genome():
    data        = request.json
    patient_age = data.get('age', 30)
    if 'disease_results' in data:
        disease_results = data['disease_results']
    elif 'genome_data' in data:
        matched_snps    = process_genome_data(data.get('genome_data', {}))
        disease_results = (get_matched_diseases(CLINVAR_DF, matched_snps)
                           if len(CLINVAR_DF) > 0
                           else [("General genetic analysis", len(matched_snps))])
    else:
        return jsonify({"error": "Either disease_results or genome_data must be provided"}), 400
    nutrition_plans = integrate_nutrition_plan(disease_results, patient_age)
    return jsonify({'disease_risks': disease_results, 'nutrition_plans': nutrition_plans})


# ─────────────────────────────────────────────────────
# Chat APIs (completely unchanged)
# ─────────────────────────────────────────────────────
GROQ_API_KEY = "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"
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"


@app.route('/chat/sessions', methods=['GET'])
def get_sessions():
    user_id = get_authenticated_user_id(request)
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    return jsonify(get_user_sessions(user_id))


@app.route('/chat/sessions', methods=['POST'])
def create_new_session():
    user_id = get_authenticated_user_id(request)
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    data = request.json or {}
    return jsonify({"session_id": create_session(user_id, data.get('title'))})


@app.route('/chat/sessions/<session_id>', methods=['GET'])
def get_session_data(session_id):
    user_id = get_authenticated_user_id(request)
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    if not verify_session_ownership(session_id, user_id):
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_session_messages(session_id))


@app.route('/chat/sessions/<session_id>', methods=['PUT'])
def update_session(session_id):
    user_id = get_authenticated_user_id(request)
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    if not verify_session_ownership(session_id, user_id):
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Missing title"}), 400
    return (jsonify({"status": "success"})
            if update_session_title(session_id, data['title'])
            else (jsonify({"error": "Not found"}), 404))


@app.route('/chat/sessions/<session_id>', methods=['DELETE'])
def delete_chat_session(session_id):
    user_id = get_authenticated_user_id(request)
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    if not verify_session_ownership(session_id, user_id):
        return jsonify({"error": "Unauthorized"}), 403
    return (jsonify({"status": "success"})
            if delete_session(session_id)
            else (jsonify({"error": "Not found"}), 404))


@app.route('/chat', methods=['POST'])
def chat_with_ai():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Missing message parameter"}), 400
    user_message = data['message']
    session_id   = data.get('session_id')
    user_id      = get_authenticated_user_id(request)
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    if not session_id:
        session_id = create_session(user_id)

    system_prompt = (
        "You are a helpful and professional AI assistant with deep expertise in medical and healthcare topics only. "
        "You must only respond to queries strictly related to medical symptoms, treatments, diseases, health advice, and similar healthcare topics. "
        "If the query is not related to medical or healthcare domains, respond only with this message:\n\n"
        "'This chatbot is only answerable to medical and healthcare queries, for other queries search it on Google.'"
        "If there is some query like hi,hey, good morning, good evening, hello, etc. the response should be:\n\n"
        "'Hello! How can I assist you with your medical or healthcare-related questions today?'"
        "If there is some query like bye, good night, take care, etc. the response should be:\n\n"
        "'Goodbye! Take care and stay healthy!'"
        "If there is some query like thank you, thanks, etc. the response should be:\n\n"
        "'You're welcome! If you have any more questions, feel free to ask.'"
        "If there is some query like what is your name, who are you, etc. the response should be:\n\n"
        "'I am a medical AI assistant here to help you with your healthcare-related questions.'"
        "If there is some query like what is your age, how old are you, etc. the response should be:\n\n"
        "'I don't have an age like humans do, but I'm here to provide you with the latest medical information.'"
        "If there is some query like some NSWF content, adult content, etc. the response should be:\n\n"
        "'I'm sorry, but I cannot assist with that. My focus is on providing medical and healthcare information.'"
        "If there is some query like some illegal content, hacking, etc. the response should be:\n\n"
        "'I'm sorry, but I cannot assist with that. My focus is on providing medical and healthcare information.'"
        "If there is some query like some political content, etc. the response should be:\n\n"
        "'I'm sorry, but I cannot assist with that. My focus is on providing medical and healthcare information.'"
        "If there is some query like some religious content, etc. the response should be:\n\n"
        "'I'm sorry, but I cannot assist with that. My focus is on providing medical and healthcare information.'"
        "If there is some query like some personal content, etc. the response should be:\n\n"
        "'I'm sorry, but I cannot assist with that. My focus is on providing medical and healthcare information.'"
        "If there is some query like asking real name, address, phone number, etc. the response should be:\n\n"
        "'I'm sorry, but I cannot assist with that. My focus is on providing medical and healthcare information.'"
    )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in get_session_messages(session_id):
        messages.append({"role": "user",      "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["bot"]})
    messages.append({"role": "user", "content": user_message})

    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}",
                   "Content-Type": "application/json"}
        body    = {"model": "llama3-8b-8192", "messages": messages}
        with httpx.Client() as client:
            response    = client.post(GROQ_URL, headers=headers, json=body)
            response.raise_for_status()
            ai_response = response.json()["choices"][0]["message"]["content"]
        add_message_to_session(session_id, user_message, ai_response)
        return jsonify({"response": ai_response, "session_id": session_id})
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return jsonify({"error": f"Failed to get response: {str(e)}"}), 500


@app.route('/chat/genomic', methods=['POST'])
def chat_with_ai_genomic():
    data = request.json or {}
    if 'message' not in data:
        return jsonify({"error": "Missing message parameter"}), 400
    user_message    = data['message']
    genomic_context = data.get('genomic_context', {})
    user_id         = get_authenticated_user_id(request)
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401

    system_prompt = (
        "You are a helpful medical AI assistant. Provide concise, practical, and safe guidance. "
        "Use the genomic risk context provided to tailor recommendations, especially nutrition and lifestyle. "
        "If the query is outside healthcare, reply: "
        "'This chatbot is only answerable to medical and healthcare queries.'"
    )
    context_lines = []
    if genomic_context:
        context_lines.append(f"Overall risk: {genomic_context.get('risk_level')}")
        diseases = genomic_context.get('matched_diseases', [])
        if diseases:
            context_lines.append(
                f"Top risks: {', '.join([f'{d} ({c} SNPs)' for d, c in diseases[:3]])}"
            )
    try:
        headers  = {"Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"}
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",
             "content": f"Context:\n{chr(10).join(context_lines)}\n\nQuestion: {user_message}"}
        ]
        with httpx.Client() as client:
            response = client.post(
                GROQ_URL, headers=headers,
                json={"model": "llama3-8b-8192", "messages": messages}
            )
            response.raise_for_status()
            return jsonify({"response": response.json()["choices"][0]["message"]["content"]})
    except Exception:
        return jsonify({"error": "Failed to get response from AI service."}), 500


@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    return jsonify(list(chat_sessions.values()))


@app.route('/chat/clear', methods=['POST'])
def clear_chat_history():
    user_id = get_authenticated_user_id(request)
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    for s in get_user_sessions(user_id):
        delete_session(s['id'])
    return jsonify({"message": "Chat history cleared successfully"})


# ─────────────────────────────────────────────────────
# Authentication Routes
# ─────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Step 1 of login for all users.
    For admin: after password check passes, redirects to /admin-pin (Step 2).
    For normal users: sets session and goes straight to app.
    Demonstrates: Authentication + MFA routing
    """
    error   = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        ip       = request.remote_addr

        if is_rate_limited(ip):
            error = "Too many login attempts. Please wait a minute and try again."
        else:
            ok, reason = verify_user(username, password, ip=ip)
            if ok:
                session['username'] = username
                # Admin goes to PIN verification (Step 2 of MFA)
                if username == "admin":
                    session['admin_pin_verified'] = False
                    return redirect(url_for('admin_pin'))
                # Normal user goes straight to app
                return redirect('/')
            elif reason.startswith("locked:"):
                minutes = reason.split(":")[1]
                error = f"Account locked. Try again in {minutes} minute(s)."
            else:
                error = "Invalid username or password."
    return render_template('login.html', error=error, success=success)


@app.route('/admin-pin', methods=['GET', 'POST'])
def admin_pin():
    """
    Step 2 of admin login — PIN verification (MFA second factor).
    Only reachable after successful password check.
    If PIN is correct → sets admin_pin_verified = True → redirects to /admin.
    Demonstrates: Multi-Factor Authentication (MFA)
    """
    # Must be logged in as admin to reach this page
    if session.get("username") != "admin":
        return redirect(url_for("login"))
    # If PIN already verified, go straight to dashboard
    if session.get("admin_pin_verified"):
        return redirect(url_for("admin_dashboard"))

    error = None
    if request.method == 'POST':
        from auth import verify_admin_pin, write_log
        pin = request.form.get('pin', '').strip()
        if verify_admin_pin(pin):
            session['admin_pin_verified'] = True
            write_log("ADMIN_PIN_OK", "admin", "PIN verified successfully",
                      request.remote_addr)
            return redirect(url_for('admin_dashboard'))
        else:
            write_log("ADMIN_PIN_FAILED", "admin", "Wrong PIN entered",
                      request.remote_addr)
            error = "Incorrect PIN. Please try again."
    return render_template('admin_pin.html', error=error)


@app.route('/logout')
def logout():
    from auth import write_log
    username = session.get("username", "unknown")
    write_log("LOGOUT", username)
    session.clear()
    return redirect('/login')


@app.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    success, msg = register_user(
        data.get('username', ''),
        data.get('password', ''),
        data.get('security_question', ''),
        data.get('security_answer', '')
    )
    return jsonify({"success": success, "message": msg})


# ─────────────────────────────────────────────────────
# Forgot Password Routes
# ─────────────────────────────────────────────────────
@app.route('/forgot/get-question', methods=['POST'])
def forgot_get_question():
    from auth import get_security_question
    data     = request.json or {}
    question = get_security_question(data.get('username', ''))
    if question:
        return jsonify({"success": True, "question": question})
    return jsonify({"success": False, "message": "Username not found."})


@app.route('/forgot/verify-answer', methods=['POST'])
def forgot_verify_answer():
    from auth import verify_security_answer
    data = request.json or {}
    if verify_security_answer(data.get('username', ''), data.get('answer', '')):
        return jsonify({"success": True})
    return jsonify({"success": False})


@app.route('/forgot/reset-password', methods=['POST'])
def forgot_reset_password():
    from auth import reset_password
    data         = request.json or {}
    success, msg = reset_password(
        data.get('username', ''), data.get('new_password', ''))
    return jsonify({"success": success, "message": msg})


# ─────────────────────────────────────────────────────
# Admin Dashboard Routes
# ─────────────────────────────────────────────────────
@app.route('/admin')
@admin_required
def admin_dashboard():
    from auth import get_all_users, get_activity_log
    users         = get_all_users()
    log           = get_activity_log()
    success_count = sum(1 for e in log if e['event'] == 'LOGIN_SUCCESS')
    failed_count  = sum(1 for e in log if e['event'] == 'LOGIN_FAILED')
    return render_template(
        'admin.html',
        users         = users,
        log           = log,
        success_count = success_count,
        failed_count  = failed_count
    )


@app.route('/admin/unlock', methods=['POST'])
@admin_required
def admin_unlock_user():
    from auth import unlock_user
    data    = request.json or {}
    ok, msg = unlock_user(data.get('username', ''))
    return jsonify({"success": ok, "message": msg})


@app.route('/admin/delete', methods=['POST'])
@admin_required
def admin_delete_user():
    """
    Permanently deletes a registered user.
    Admin account itself is protected — cannot be deleted.
    Deletion is logged to activity_log.json for audit trail.
    Demonstrates: User Management / Access Revocation
    """
    from auth import delete_user
    data    = request.json or {}
    ok, msg = delete_user(data.get('username', ''))
    return jsonify({"success": ok, "message": msg})


@app.route('/admin/change-pin', methods=['POST'])
@admin_required
def admin_change_pin():
    """
    Allows admin to change their MFA PIN from the dashboard.
    New PIN is hashed before storing.
    """
    from auth import update_admin_pin
    data    = request.json or {}
    ok, msg = update_admin_pin(data.get('new_pin', ''))
    return jsonify({"success": ok, "message": msg})


if __name__ == '__main__':
    app.run(debug=True)