# auth.py
# Security concepts demonstrated:
#   1.  Password Hashing          (PBKDF2-SHA256 / scrypt via Werkzeug)
#   2.  Credential Storage        (users.json)
#   3.  Authentication            (verify_user)
#   4.  Account Recovery          (security question + answer hashing)
#   5.  Audit Trail               (activity_log.json with IP logging)
#   6.  Account Lockout           (MAX_FAILED_ATTEMPTS → timed lock)
#   7.  Rate Limiting             (per-IP in-memory tracking)
#   8.  Password Complexity       (server-side enforcement)
#   9.  User Management           (admin can delete users)     ← NEW
#   10. Multi-Factor Auth (MFA)   (admin PIN after password)   ← NEW

import json
import os
import re
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = "users.json"
LOG_FILE   = "activity_log.json"

# ─────────────────────────────────────────
# Account Lockout Configuration
# ─────────────────────────────────────────
MAX_FAILED_ATTEMPTS = 5       # lock account after this many consecutive failures
LOCKOUT_MINUTES     = 15      # how long the lock lasts

# In-memory rate limiter: { ip_address: [datetime, ...] }
_rate_store = {}
RATE_LIMIT_WINDOW  = 60    # seconds
RATE_LIMIT_MAX_REQ = 10    # max login attempts per IP per window


# ─────────────────────────────────────────
# Load / Save users
# ─────────────────────────────────────────
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


# ─────────────────────────────────────────
# Migration helper
# Upgrades old plain-string entries to dict format
# ─────────────────────────────────────────
def _migrate_users():
    users   = load_users()
    changed = False
    for username, data in users.items():
        if isinstance(data, str):
            users[username] = {
                "password":          data,
                "security_question": "What city were you born in?",
                "security_answer":   generate_password_hash("changeme"),
                "registered_at":     "2024-01-01 00:00:00",
                "failed_attempts":   0,
                "locked_until":      None
            }
            changed = True
        else:
            if "failed_attempts" not in data:
                data["failed_attempts"] = 0
                changed = True
            if "locked_until" not in data:
                data["locked_until"] = None
                changed = True
    if changed:
        save_users(users)

_migrate_users()


# ─────────────────────────────────────────
# Load / Save activity log
# ─────────────────────────────────────────
def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def write_log(event_type, username, note="", ip=None):
    """
    Appends one entry to activity_log.json.
    Demonstrates: Audit Trail + IP Logging
    """
    log = load_log()
    log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event":     event_type,
        "username":  username,
        "note":      note,
        "ip":        ip or "unknown"
    })
    save_log(log)


# ─────────────────────────────────────────
# Rate Limiter (per IP, in-memory)
# Demonstrates: Rate Limiting / Brute Force Protection
# ─────────────────────────────────────────
def is_rate_limited(ip):
    """Returns True if this IP has exceeded the allowed request rate."""
    now          = datetime.now()
    window_start = now - timedelta(seconds=RATE_LIMIT_WINDOW)
    timestamps   = _rate_store.get(ip, [])
    timestamps   = [t for t in timestamps if t > window_start]
    _rate_store[ip] = timestamps
    if len(timestamps) >= RATE_LIMIT_MAX_REQ:
        return True
    timestamps.append(now)
    _rate_store[ip] = timestamps
    return False


# ─────────────────────────────────────────
# Password Complexity Checker (server-side)
# Demonstrates: Password Policy Enforcement
# ─────────────────────────────────────────
def check_password_complexity(password):
    """Returns (True, '') on pass, or (False, reason) on fail."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*()\-_=+\[\]{};:\'",.<>?\/\\|`~]', password):
        return False, "Password must contain at least one special character."
    return True, ""


# ─────────────────────────────────────────
# Register new user
# ─────────────────────────────────────────
def register_user(username, password, security_question, security_answer):
    """
    Saves new user with hashed password and hashed security answer.
    Demonstrates: Credential Storage + Password Hashing + Complexity Enforcement
    """
    if not username or not password:
        return False, "Username and password are required."
    if not security_question or not security_answer:
        return False, "Security question and answer are required."
    if len(username) < 3:
        return False, "Username must be at least 3 characters."

    ok, reason = check_password_complexity(password)
    if not ok:
        return False, reason

    users = load_users()
    if username in users:
        return False, "Username already exists. Please choose another."

    users[username] = {
        "password":          generate_password_hash(password),
        "security_question": security_question,
        "security_answer":   generate_password_hash(security_answer.strip().lower()),
        "registered_at":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "failed_attempts":   0,
        "locked_until":      None
    }
    save_users(users)
    write_log("REGISTER", username)
    return True, "Account created successfully!"


# ─────────────────────────────────────────
# Verify login (with lockout)
# ─────────────────────────────────────────
def verify_user(username, password, ip=None):
    """
    Verifies credentials against stored hash.
    Locks account after MAX_FAILED_ATTEMPTS consecutive failures.
    Demonstrates: Authentication + Audit Trail + Account Lockout
    """
    if not username or not password:
        return False, "credentials_missing"

    users = load_users()
    if username not in users:
        write_log("LOGIN_FAILED", username, "Username not found", ip)
        return False, "invalid"

    user    = users[username]
    pw_hash = user["password"] if isinstance(user, dict) else user

    # ── Lockout check ──────────────────────────────────
    locked_until = user.get("locked_until") if isinstance(user, dict) else None
    if locked_until:
        lock_time = datetime.strptime(locked_until, "%Y-%m-%d %H:%M:%S")
        if datetime.now() < lock_time:
            remaining = int((lock_time - datetime.now()).total_seconds() // 60) + 1
            write_log("LOGIN_FAILED", username,
                      f"Account locked — {remaining}m remaining", ip)
            return False, f"locked:{remaining}"
        else:
            user["failed_attempts"] = 0
            user["locked_until"]    = None
            users[username] = user
            save_users(users)

    # ── Password check ─────────────────────────────────
    if check_password_hash(pw_hash, password):
        if isinstance(user, dict):
            user["failed_attempts"] = 0
            user["locked_until"]    = None
            users[username] = user
            save_users(users)
        write_log("LOGIN_SUCCESS", username, "", ip)
        return True, "ok"
    else:
        if isinstance(user, dict):
            user["failed_attempts"] = user.get("failed_attempts", 0) + 1
            if user["failed_attempts"] >= MAX_FAILED_ATTEMPTS:
                user["locked_until"] = (
                    datetime.now() + timedelta(minutes=LOCKOUT_MINUTES)
                ).strftime("%Y-%m-%d %H:%M:%S")
                users[username] = user
                save_users(users)
                write_log("ACCOUNT_LOCKED", username,
                          f"Locked {LOCKOUT_MINUTES}m after {MAX_FAILED_ATTEMPTS} failures", ip)
                return False, f"locked:{LOCKOUT_MINUTES}"
            users[username] = user
            save_users(users)
        write_log("LOGIN_FAILED", username, "Wrong password", ip)
        return False, "invalid"


# ─────────────────────────────────────────
# Admin PIN — Multi-Factor Authentication
# Demonstrates: MFA (something you know × 2)
# ─────────────────────────────────────────

# The admin PIN is stored as a hash inside users.json under the "admin" key.
# Default PIN is 1234 — admin SHOULD change it via the dashboard.
# PIN is stored as: users["admin"]["admin_pin"] = generate_password_hash("1234")

ADMIN_DEFAULT_PIN = "1234"

def ensure_admin_pin():
    """
    Makes sure admin account has a PIN hash stored.
    Called automatically on app start.
    If no PIN exists yet, creates one using the default.
    """
    users = load_users()
    if "admin" not in users:
        return   # admin account doesn't exist yet — nothing to do
    user = users["admin"]
    if not isinstance(user, dict):
        return
    if "admin_pin" not in user or not user["admin_pin"]:
        user["admin_pin"] = generate_password_hash(ADMIN_DEFAULT_PIN)
        users["admin"] = user
        save_users(users)

def verify_admin_pin(pin):
    """
    Checks the entered PIN against the stored hash for admin.
    Returns True if correct, False otherwise.
    Demonstrates: Multi-Factor Authentication (second factor check)
    """
    if not pin:
        return False
    users = load_users()
    if "admin" not in users:
        return False
    user = users["admin"]
    if not isinstance(user, dict):
        return False
    stored_pin = user.get("admin_pin", "")
    if not stored_pin:
        # No PIN set — allow with default
        return pin == ADMIN_DEFAULT_PIN
    return check_password_hash(stored_pin, pin)

def update_admin_pin(new_pin):
    """
    Allows admin to change their PIN from the dashboard.
    New PIN is hashed before saving.
    """
    if not new_pin or len(new_pin) != 4 or not new_pin.isdigit():
        return False, "PIN must be exactly 4 digits."
    users = load_users()
    if "admin" not in users or not isinstance(users["admin"], dict):
        return False, "Admin account not found."
    users["admin"]["admin_pin"] = generate_password_hash(new_pin)
    save_users(users)
    write_log("PIN_CHANGED", "admin")
    return True, "PIN updated successfully."


# ─────────────────────────────────────────
# Forgot Password helpers
# ─────────────────────────────────────────
def get_security_question(username):
    users = load_users()
    if username not in users:
        return None
    user = users[username]
    if isinstance(user, dict):
        return user.get("security_question", None)
    return None

def verify_security_answer(username, answer):
    users = load_users()
    if username not in users:
        return False
    user = users[username]
    if isinstance(user, dict):
        stored = user.get("security_answer", "")
        return check_password_hash(stored, answer.strip().lower())
    return False

def reset_password(username, new_password):
    ok, reason = check_password_complexity(new_password)
    if not ok:
        return False, reason
    users = load_users()
    if username not in users:
        return False, "User not found."
    user = users[username]
    if isinstance(user, dict):
        user["password"]        = generate_password_hash(new_password)
        user["failed_attempts"] = 0
        user["locked_until"]    = None
        users[username] = user
        save_users(users)
        write_log("PASSWORD_RESET", username)
        return True, "Password reset successfully!"
    return False, "Account format error."


# ─────────────────────────────────────────
# Admin: get all users data
# ─────────────────────────────────────────
def get_all_users():
    """Returns all users with status info. Excludes admin account itself."""
    users  = load_users()
    result = []
    for username, data in users.items():
        if username == "admin":
            continue
        locked_until = data.get("locked_until") if isinstance(data, dict) else None
        is_locked    = False
        if locked_until:
            lock_time = datetime.strptime(locked_until, "%Y-%m-%d %H:%M:%S")
            is_locked = datetime.now() < lock_time
        result.append({
            "username":          username,
            "registered_at":     data.get("registered_at", "N/A") if isinstance(data, dict) else "N/A",
            "security_question": data.get("security_question", "—") if isinstance(data, dict) else "—",
            "failed_attempts":   data.get("failed_attempts", 0)    if isinstance(data, dict) else 0,
            "is_locked":         is_locked,
            "locked_until":      locked_until if is_locked else None
        })
    return result

def get_activity_log():
    """Returns full activity log."""
    return load_log()

def unlock_user(username):
    """Admin action: manually unlock a locked account."""
    users = load_users()
    if username not in users or not isinstance(users[username], dict):
        return False, "User not found."
    users[username]["failed_attempts"] = 0
    users[username]["locked_until"]    = None
    save_users(users)
    write_log("ACCOUNT_UNLOCKED", username, "Manually unlocked by admin")
    return True, f"{username} has been unlocked."


# ─────────────────────────────────────────
# Delete User (NEW)
# Demonstrates: User Management / Access Revocation
# Admin can permanently remove a registered user.
# The deletion is logged in activity_log.json for audit trail.
# ─────────────────────────────────────────
def delete_user(username):
    """
    Permanently removes a user from users.json.
    Admin account itself can never be deleted.
    Demonstrates: Access Revocation + Audit Trail
    """
    if username == "admin":
        return False, "Admin account cannot be deleted."

    users = load_users()
    if username not in users:
        return False, "User not found."

    del users[username]
    save_users(users)
    write_log("USER_DELETED", username, "Deleted by admin")
    return True, f"User '{username}' has been permanently deleted."