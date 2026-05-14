# genomic_risk_pipeline.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from collections import Counter
import warnings
warnings.filterwarnings("ignore")
import os # Added for PLINK file loading

# Import the comprehensive nutrition dataset
try:
    from nutrition_dataset import NUTRITION_DATABASE, AGE_RECOMMENDATIONS, EXERCISE_GUIDELINES, get_nutrition_plan
    NUTRITION_DATA_AVAILABLE = True
    print("✅ Comprehensive nutrition database loaded successfully")
except ImportError:
    NUTRITION_DATA_AVAILABLE = False
    print("⚠️ Comprehensive nutrition database not available, using basic recommendations")


def load_user_genome(path):
    """Load user genome data from various formats"""
    try:
        if path.endswith('.txt') or path.endswith('.csv'):
            # Load from text/csv file
            if path.endswith('.csv'):
                df = pd.read_csv(path)
            else:
                df = pd.read_csv(path, sep='\t')
            
            # Check if it's a simple SNP list
            if len(df.columns) >= 2 and 'rs' in str(df.iloc[0, 0]).lower():
                # Assume format: SNP_ID, genotype
                snps = df.iloc[:, 0].astype(str).tolist()
                print(f"📊 Loaded {len(snps)} SNPs from {path}")
                return snps
            
        elif path.endswith('.ped') and path.endswith('.map'):
            # Load from PLINK format
            map_path = path.replace('.ped', '.map')
            if os.path.exists(map_path):
                map_df = pd.read_csv(map_path, sep='\t', header=None)
                snps = map_df.iloc[:, 1].astype(str).tolist()
                print(f"📊 Loaded {len(snps)} SNPs from PLINK format")
                return snps
        
        # Fallback: try to read as simple text file with SNP IDs
        with open(path, 'r') as f:
            lines = f.readlines()
            snps = []
            for line in lines:
                line = line.strip()
                if line and ('rs' in line.lower() or line.startswith('chr')):
                    snps.append(line)
            
            if snps:
                print(f"📊 Loaded {len(snps)} SNPs from text file")
                return snps
        
        raise ValueError(f"❌ Could not parse genome file: {path}")
        
    except Exception as e:
        print(f"❌ Error loading genome file: {e}")
        # Return some test SNPs for demonstration
        test_snps = [
            'rs1799966', 'rs10757274', 'rs7903146', 'rs429358', 
            'rs9939609', 'rs1378942', 'rs1800947', 'rs2981582'
        ]
        print(f"⚠️ Using test SNPs for demonstration: {len(test_snps)} SNPs")
        return test_snps


def load_bed_subset(prefix, target_snps):
    """Load genotype data from PLINK binary files"""
    # This function is now deprecated as load_user_genome handles basic file formats
    # and pandas_plink is removed.
    # If you need to load PLINK files, you'll need to re-implement this using a different library
    # or rely on the user to provide the correct file format.
    # For now, we'll raise an error as pandas_plink is not available.
    raise ImportError("pandas_plink is required for PLINK file loading. Please ensure it's installed or use a different file format.")

# ------------------------------------------------------
# IMPORTANT NOTE FOR MERGE LOCATIONS
# Anywhere you currently have code like:
# merged = pd.merge(gwas_df, user_df, on=["rsid", "chromosome", "position"])
# or merging on multiple keys including chromosome/position,
# you MUST replace it with:
# merged = pd.merge(gwas_df, user_df, on="rsid")
# ------------------------------------------------------

# ... [rest of your functions remain unchanged] ...


def load_clinvar_variant_summary(path):
    """Load ClinVar variant summary data without restrictive filters"""
    try:
        required_cols = ['RS# (dbSNP)', 'PhenotypeList', 'ClinicalSignificance', 'Assembly', 'Type']
        df = pd.read_csv(path, sep='\t', usecols=required_cols, compression='gzip', low_memory=False)
        df.columns = df.columns.str.strip()

        # Keep ALL assemblies and ALL clinical significance values
        df['RS# (dbSNP)'] = df['RS# (dbSNP)'].astype(str).str.strip().str.lower()
        df['RS# (dbSNP)'] = df['RS# (dbSNP)'].apply(lambda x: 'rs' + x if not x.startswith('rs') else x)

        # Drop rows missing rsid or phenotype
        df = df[['RS# (dbSNP)', 'PhenotypeList']].dropna().drop_duplicates()

        print(f"✅ ClinVar: {len(df)} SNPs loaded (no filters applied).")
        return df
    except FileNotFoundError:
        print(f"⚠️ Warning: {path} not found. Creating empty DataFrame.")
        return pd.DataFrame(columns=['RS# (dbSNP)', 'PhenotypeList'])
    except Exception as e:
        print(f"⚠️ Error loading ClinVar data: {e}")
        return pd.DataFrame(columns=['RS# (dbSNP)', 'PhenotypeList'])


def load_gwas(path, p=1.0, top=None):
    """Load ALL GWAS data without truncation"""
    try:
        df = pd.read_csv(path, sep='\t', low_memory=False)
        df['SNPS'] = df['SNPS'].astype(str).str.strip().str.lower()

        df = df[['SNPS', 'DISEASE/TRAIT', 'P-VALUE']].dropna()

        # Apply optional p-value filter
        if p < 1.0:
            df = df[df['P-VALUE'] < p]

        # Apply optional row limit
        if top:
            df = df.head(top)

        print(f"✅ GWAS: {len(df)} SNPs loaded (filters: p<{p}, top={top}).")
        return df
    except FileNotFoundError:
        print(f"⚠️ Warning: {path} not found. Creating empty DataFrame.")
        return pd.DataFrame(columns=['SNPS', 'DISEASE/TRAIT', 'P-VALUE'])
    except Exception as e:
        print(f"⚠️ Error loading GWAS data: {e}")
        return pd.DataFrame(columns=['SNPS', 'DISEASE/TRAIT', 'P-VALUE'])


def load_pharmgkb(path, top=None):
    """Load ALL PharmGKB variant-drug associations"""
    try:
        df = pd.read_csv(path, sep='\t')

        if 'Chemical' not in df.columns and 'Drugs' in df.columns:
            df.rename(columns={'Drugs': 'Chemical'}, inplace=True)
        if 'Variant/Haplotypes' in df.columns:
            df.rename(columns={'Variant/Haplotypes': 'Variant'}, inplace=True)

        expected_cols = ['Variant', 'Chemical', 'Phenotype Category']
        available_cols = [col for col in expected_cols if col in df.columns]

        if not available_cols:
            print(f"⚠️ No expected columns found. Available: {df.columns.tolist()}")
            return pd.DataFrame(columns=['Variant'])

        df = df[available_cols].dropna()

        if top:
            df = df.head(top)

        if 'Variant' in df.columns:
            df['Variant'] = df['Variant'].astype(str).str.strip().str.lower()

        print(f"✅ PharmGKB: {len(df)} variant-drug pairs loaded (top={top}).")
        return df
    except FileNotFoundError:
        print(f"⚠️ Warning: {path} not found. Creating empty DataFrame.")
        return pd.DataFrame(columns=['Variant'])
    except Exception as e:
        print(f"⚠️ Error loading PharmGKB data: {e}")
        return pd.DataFrame(columns=['Variant'])


def genotype_str_to_dosage(geno):
    """Convert genotype string to dosage (0,1,2)"""
    if isinstance(geno, str):
        geno = geno.upper().strip()
        if geno in ["AA", "CC", "GG", "TT"]:
            return 0  # Homozygous Reference
        elif geno in ["AC", "CA", "AG", "GA", "TC", "CT", "TG", "GT", "AT", "TA", "CG", "GC"]:
            return 1  # Heterozygous
        elif len(set(geno)) == 1 and len(geno) == 2:  # Other homozygous
            return 2  # Homozygous Alternate
    return np.nan

def label_risk(geno_df, pathogenic_snps):
    """Label disease risk from SNPs (robust to duplicate rsIDs)"""
    # clean and de-duplicate (preserve order)
    cleaned = [str(s).lower().strip() for s in pathogenic_snps if pd.notna(s)]
    cleaned = list(dict.fromkeys(cleaned))

    # overlap, also unique
    overlap = [s for s in cleaned if s in geno_df.columns]
    overlap = list(dict.fromkeys(overlap))

    print(f"🧬 Total SNPs in genotype: {len(geno_df.columns)}")
    print(f"🧬 Overlapping SNPs: {len(overlap)}")

    if not overlap:
        print("⚠️ No overlapping SNPs found. Using first 5 SNPs as fallback.")
        overlap = geno_df.columns[:5].tolist()

    # convert genotype strings to numeric dosage
    for col in overlap:
        geno_df[col] = geno_df[col].apply(genotype_str_to_dosage)

    # use .loc to avoid length/key alignment issues
    geno_df.loc[:, overlap] = geno_df.loc[:, overlap].fillna(0)

    scores = geno_df[overlap].sum(axis=1)

    # with tiny samples, avoid qcut issues
    if len(geno_df) < 3 or scores.nunique() < 2:
        geno_df['risk_label'] = "Medium"
        return geno_df, overlap

    try:
        bins = pd.qcut(scores, q=3, labels=["Low", "Medium", "High"], duplicates='drop')
        geno_df['risk_label'] = bins
    except Exception:
        p33, p66 = scores.quantile(0.33), scores.quantile(0.66)
        geno_df['risk_label'] = pd.cut(
            scores, bins=[-np.inf, p33, p66, np.inf],
            labels=["Low", "Medium", "High"], include_lowest=True
        )
    return geno_df, overlap

def get_matched_diseases(clinvar_df, matched_snps):
    """Get matched diseases from SNPs with more specific condition names"""
    if not matched_snps:
        return [("Genetic variant of unknown significance", 0)]
    
    # Expanded disease categories with more specific names
    disease_categories = {
        "cardiovascular disease": {
            "terms": ["heart", "cardiac", "cardiovascular", "coronary", "myocardial", "atrial", "ventricular", "hypertension", "blood pressure"],
            "specific_names": ["Coronary Artery Disease", "Hypertension", "Atrial Fibrillation", "Heart Failure", "Cardiovascular Risk"]
        },
        "type 2 diabetes": {
            "terms": ["diabetes", "diabetes mellitus", "t2d", "glucose", "insulin", "metabolic"],
            "specific_names": ["Type 2 Diabetes", "Insulin Resistance", "Metabolic Syndrome", "Glucose Metabolism Issues"]
        },
        "alzheimer's disease": {
            "terms": ["alzheimer", "dementia", "neurodegenerative", "cognitive", "memory", "brain"],
            "specific_names": ["Alzheimer's Disease", "Cognitive Decline", "Memory Loss", "Brain Health Risk"]
        },
        "obesity": {
            "terms": ["obesity", "overweight", "body mass", "bmi", "weight", "metabolic"],
            "specific_names": ["Obesity", "Weight Management Issues", "Metabolic Disorder", "Body Composition Risk"]
        },
        "breast cancer": {
            "terms": ["breast", "mammary", "carcinoma", "brca", "estrogen receptor", "cancer"],
            "specific_names": ["Breast Cancer", "BRCA Mutation", "Hormone Receptor Positive Cancer", "Breast Health Risk"]
        },
        "colorectal cancer": {
            "terms": ["colorectal", "colon", "rectal", "intestinal", "digestive"],
            "specific_names": ["Colorectal Cancer", "Colon Cancer", "Intestinal Cancer", "Digestive Health Risk"]
        },
        "lung cancer": {
            "terms": ["lung", "pulmonary", "respiratory", "airway"],
            "specific_names": ["Lung Cancer", "Pulmonary Cancer", "Respiratory Cancer", "Lung Health Risk"]
        },
        "prostate cancer": {
            "terms": ["prostate", "prostatic", "male reproductive"],
            "specific_names": ["Prostate Cancer", "Prostatic Cancer", "Male Reproductive Health Risk"]
        },
        "autoimmune disease": {
            "terms": ["autoimmune", "rheumatoid", "lupus", "inflammatory", "immune"],
            "specific_names": ["Autoimmune Disorder", "Inflammatory Condition", "Immune System Disorder", "Inflammation Risk"]
        },
        "osteoporosis": {
            "terms": ["osteoporosis", "bone density", "fracture", "bone", "skeletal"],
            "specific_names": ["Osteoporosis", "Low Bone Density", "Bone Health Issues", "Skeletal Health Risk"]
        },
        "hypertension": {
            "terms": ["hypertension", "high blood pressure", "blood pressure", "cardiovascular"],
            "specific_names": ["Hypertension", "High Blood Pressure", "Blood Pressure Issues", "Cardiovascular Risk"]
        },
        "lactose intolerance": {
            "terms": ["lactose", "dairy", "milk", "digestive", "intolerance"],
            "specific_names": ["Lactose Intolerance", "Dairy Sensitivity", "Milk Intolerance", "Digestive Sensitivity"]
        },
        "vitamin d deficiency": {
            "terms": ["vitamin d", "rickets", "bone density", "calcium", "sunlight"],
            "specific_names": ["Vitamin D Deficiency", "Bone Health Issues", "Calcium Absorption Problems", "Nutrient Deficiency"]
        },
        "inflammation": {
            "terms": ["inflammation", "inflammatory", "crp", "cytokine", "immune response"],
            "specific_names": ["Chronic Inflammation", "Inflammatory Response", "Immune System Activation", "Inflammation Risk"]
        },
        "oxidative stress": {
            "terms": ["oxidative", "free radical", "antioxidant", "stress", "cellular damage"],
            "specific_names": ["Oxidative Stress", "Free Radical Damage", "Cellular Stress", "Antioxidant Deficiency"]
        }
    }
    
    # Known disease-specific SNPs with more comprehensive list
    known_snps = {
        "breast cancer": ["rs1799966", "rs1799950", "rs144848", "rs8176318", "rs4986850", 
                         "rs206075", "rs766173", "rs13281615", "rs3803662", "rs889312", 
                         "rs2981582", "rs1219648", "rs2420946", "rs704010", "rs10995190", 
                         "rs8170", "rs4973768", "rs10941679", "rs2107425", "rs3817198", 
                         "rs13387042", "rs2046210", "rs12662670", "rs999737", "rs1045485"],
        "cardiovascular disease": ["rs10757274", "rs1333049", "rs2383206", "rs10757278", 
                                 "rs501120", "rs17465637", "rs12190287", "rs599839", 
                                 "rs646776", "rs1746048", "rs4977574", "rs17464857", 
                                 "rs9818870", "rs17228212", "rs16996148", "rs46522"],
        "type 2 diabetes": ["rs7903146", "rs12255372", "rs4506565", "rs7754840", 
                           "rs10811661", "rs5219", "rs13266634", "rs1801282", 
                           "rs4402960", "rs7756992", "rs1111875", "rs7923837", 
                           "rs864745", "rs12779790", "rs7961581", "rs4607103"],
        "alzheimer's disease": ["rs429358", "rs7412", "rs744373", "rs3851179", 
                               "rs3764650", "rs6656401", "rs3818361", "rs610932", 
                               "rs6733839", "rs10948363", "rs3865444", "rs670139", 
                               "rs1049296", "rs2075650", "rs4420638"],
        "obesity": ["rs9939609", "rs1421085", "rs17817449", "rs3751812", "rs8044769",
                   "rs6548238", "rs17782313", "rs17700633", "rs6265", "rs1801133"],
        "hypertension": ["rs1378942", "rs16948048", "rs11191548", "rs17367504", "rs3184504",
                        "rs633185", "rs2681472", "rs1813353", "rs4387287", "rs1799945"],
        "inflammation": ["rs1800947", "rs1205", "rs1130864", "rs1417938", "rs1800629",
                        "rs361525", "rs1800750", "rs1800896", "rs1800871", "rs1800872"]
    }
    
    # Create SNP to phenotype mapping
    snp_disease_map = {}
    if not clinvar_df.empty and 'RS# (dbSNP)' in clinvar_df.columns and 'PhenotypeList' in clinvar_df.columns:
        snp_disease_map = clinvar_df.set_index('RS# (dbSNP)')['PhenotypeList'].to_dict()
    
    # Separate counters so we can enforce stricter evidence thresholds
    disease_counter_known = Counter()    # from curated known SNP lists
    disease_counter_clinvar = Counter()  # from ClinVar phenotype term matches
    matched_snp_details = []

    print(f"🔍 Analyzing {len(matched_snps)} matched SNPs for disease associations")
    
    # ALWAYS check for known disease-specific SNPs first (this is the key fix!)
    for disease, snps in known_snps.items():
        matches = [snp for snp in matched_snps if snp in snps]
        if matches:
            disease_counter_known[disease] += len(matches)
            print(f"  ✅ Found {len(matches)} known {disease} SNPs: {matches}")
            for snp in matches:
                matched_snp_details.append(f"{snp} -> {disease} (known)")
    
    # Then check ClinVar phenotype descriptions if available
    if snp_disease_map:
        for snp in matched_snps:
            diseases = snp_disease_map.get(snp, "")
            if diseases:
                print(f"  📋 SNP {snp} associated with: {diseases}")
                diseases_lower = diseases.lower()
                
                # Check for matches with disease categories
                for main_disease, category_info in disease_categories.items():
                    if any(term in diseases_lower for term in category_info["terms"]):
                        disease_counter_clinvar[main_disease] += 1
                        matched_snp_details.append(f"{snp} -> {main_disease} (ClinVar term)")
                        continue
                        
                # Also check individual disease terms
                for d in diseases.split(';'):
                    d_clean = d.strip().lower()
                    for disease, category_info in disease_categories.items():
                        if any(term in d_clean for term in category_info["terms"]):
                            disease_counter_clinvar[disease] += 1
                            matched_snp_details.append(f"{snp} -> {disease} (ClinVar term: {d_clean})")

    # If no specific diseases found, try to infer from SNP patterns
    if not disease_counter_known and not disease_counter_clinvar:
        print("  🔍 No specific disease matches found, analyzing SNP patterns...")
        # Check for common SNP patterns that might indicate general health risks
        if len(matched_snps) >= 5:
            disease_counter_clinvar["general health risk"] = len(matched_snps)
            print(f"  ⚠️ Found {len(matched_snps)} SNPs indicating general health risk")

    # Merge counters and apply stricter evidence thresholds:
    # - Keep diseases with at least 2 curated known SNPs, OR
    # - Keep diseases with at least 3 ClinVar-supported term hits
    combined = Counter()
    for disease, cnt in disease_counter_known.items():
        if cnt >= 2:
            combined[disease] += cnt
    for disease, cnt in disease_counter_clinvar.items():
        if cnt >= 3 or (disease in disease_counter_known and disease_counter_known[disease] >= 2):
            combined[disease] += cnt

    # Convert to specific disease names
    result = []
    for disease, count in combined.most_common():
        if count >= 1:
            specific_names = disease_categories.get(disease, {}).get("specific_names", [disease.title()])
            if count >= 3:
                specific_name = specific_names[0]
            elif count >= 2:
                specific_name = specific_names[1] if len(specific_names) > 1 else specific_names[0]
            else:
                specific_name = specific_names[0] if specific_names else disease.title()
            result.append((specific_name, count))

    # Limit to top K most strongly supported diseases to avoid overwhelming lists
    TOP_K_DISEASES = 2
    result = result[:TOP_K_DISEASES]
    
    # Debug: Print matched diseases
    if result:
        print("🔍 Matched Specific Conditions:")
        for disease, count in result:
            print(f"  ✅ {disease} ({count} SNPs)")
        
        print("🔍 SNP-Disease Mapping Details:")
        for detail in matched_snp_details[:10]:  # Show first 10 details
            print(f"    {detail}")
    else:
        print("🔍 No specific disease matches found in our database")
        if matched_snps:
            result = [("Genetic variant of unknown significance", len(matched_snps))]
    
    return result

def predict_demo(model, feature_cols):
    """Predict demo case"""
    if model is None or not feature_cols:
        print("⚠️ No model or features available for demo prediction")
        return
    
    user = pd.DataFrame([np.random.choice([0,1,2], size=len(feature_cols))], columns=feature_cols)
    print("\n🧬 Synthetic user risk:", model.predict(user)[0])

def integrate_nutrition_plan(disease_results, age):
    """Generate nutrition plans for each identified disease risk with consistent risk calculation"""
    nutrition_plans = {}
    
    # Calculate overall risk consistently
    total_snps = sum(count for _, count in disease_results)
    if total_snps >= 10:
        overall_risk = "High"
    elif total_snps >= 5:
        overall_risk = "Medium"
    else:
        overall_risk = "Low"
    
    for disease, count in disease_results:
        # Use consistent risk calculation based on SNP count
        if count >= 5:
            risk_level = "High"
        elif count >= 2:
            risk_level = "Medium"
        else:
            risk_level = "Low"
            
        # Generate nutrition plan for this disease
        nutrition_plans[disease] = generate_nutrition_plan(disease, age, risk_level, overall_risk)
        
    return nutrition_plans

def generate_nutrition_plan(disease, age, risk_level, overall_risk="Medium"):
    """Generate comprehensive nutrition and exercise plan for specific disease"""
    
    # Determine age group
    if age < 18:
        age_group = "adolescent"
    elif age < 30:
        age_group = "young_adult"
    elif age < 50:
        age_group = "middle_aged"
    else:
        age_group = "senior"
    
    # Use comprehensive nutrition database if available
    if NUTRITION_DATA_AVAILABLE:
        # Get the comprehensive nutrition plan
        comprehensive_plan = get_nutrition_plan(disease, age_group)
        
        # Compile the complete nutrition and exercise plan
        complete_plan = {
            "disease": disease,
            "age_group": age_group,
            "risk_level": risk_level,
            "overall_risk": overall_risk,
            "general_advice": comprehensive_plan["general_advice"],
            "foods_to_include": comprehensive_plan["foods_to_include"]["all"] + comprehensive_plan["foods_to_include"][age_group],
            "foods_to_avoid": comprehensive_plan["foods_to_avoid"]["all"] + comprehensive_plan["foods_to_avoid"][age_group],
            "meal_pattern": f"{comprehensive_plan['meal_pattern']['all']}. {comprehensive_plan['meal_pattern'][age_group]}.",
            "supplements": comprehensive_plan["supplements"]["all"] + comprehensive_plan["supplements"][age_group],
            "exercise_plan": comprehensive_plan["exercise_plan"],
            "age_recommendations": AGE_RECOMMENDATIONS.get(age_group, {}),
            "disclaimer": "This nutrition and exercise plan is for informational purposes only. Please consult with a healthcare provider or registered dietitian before making significant dietary or exercise changes."
        }
        
        return complete_plan
    
    # Fallback to basic recommendations if comprehensive database not available
    # Comprehensive nutrition and exercise database
    comprehensive_plans = {
        "coronary artery disease": {
            "general_advice": "Focus on heart-healthy nutrition with emphasis on reducing inflammation and improving cardiovascular function.",
            "foods_to_include": {
                "all": ["fatty fish", "leafy greens", "berries", "nuts and seeds", "olive oil", "whole grains", "legumes", "avocado"],
                "adolescent": ["lean proteins", "dairy products", "colorful vegetables"],
                "young_adult": ["omega-3 rich foods", "antioxidant-rich fruits", "plant proteins"],
                "middle_aged": ["fiber-rich foods", "potassium-rich foods", "heart-healthy fats"],
                "senior": ["easily digestible proteins", "soft fruits", "cooked vegetables"]
            },
            "foods_to_avoid": {
                "all": ["trans fats", "excessive sodium", "processed meats", "refined sugars", "saturated fats"],
                "adolescent": ["sugary beverages", "fast food", "processed snacks"],
                "young_adult": ["excessive alcohol", "ultra-processed foods", "high-sodium meals"],
                "middle_aged": ["red meat", "full-fat dairy", "refined carbohydrates"],
                "senior": ["high-sodium foods", "difficult-to-chew items", "excessive portions"]
            },
            "meal_pattern": {
                "all": "Mediterranean-style eating pattern with emphasis on plant-based foods",
                "adolescent": "3 balanced meals with heart-healthy snacks",
                "young_adult": "Regular meals focusing on anti-inflammatory foods",
                "middle_aged": "Portion-controlled Mediterranean diet",
                "senior": "4-5 smaller, nutrient-dense meals throughout day"
            },
            "supplements": {
                "all": ["omega-3", "vitamin d", "magnesium"],
                "adolescent": ["multivitamin", "calcium"],
                "young_adult": ["coenzyme q10", "vitamin e"],
                "middle_aged": ["fish oil", "garlic extract", "hawthorn"],
                "senior": ["vitamin b12", "potassium", "fiber supplement"]
            },
            "exercise_plan": {
                "cardio": "30-45 minutes moderate cardio 5 days/week (walking, cycling, swimming)",
                "strength": "2-3 days/week resistance training focusing on major muscle groups",
                "flexibility": "Daily stretching and yoga for stress reduction",
                "intensity": "Moderate intensity, avoid high-intensity intervals if high risk",
                "precautions": "Monitor heart rate, avoid exercise in extreme temperatures"
            }
        },
        "type 2 diabetes": {
            "general_advice": "Focus on blood sugar management through balanced nutrition and regular physical activity.",
            "foods_to_include": {
                "all": ["complex carbohydrates", "fiber-rich foods", "lean proteins", "healthy fats", "non-starchy vegetables"],
                "adolescent": ["growth-supporting proteins", "calcium-rich foods", "iron sources"],
                "young_adult": ["nutrient-dense whole foods", "varied protein sources"],
                "middle_aged": ["low-glycemic foods", "antioxidant-rich foods"],
                "senior": ["easily digestible proteins", "hydrating foods", "nutrient-dense options"]
            },
            "foods_to_avoid": {
                "all": ["refined sugars", "white bread", "sugary beverages", "processed foods", "high-glycemic fruits"],
                "adolescent": ["candy", "soda", "white pasta", "sweetened cereals"],
                "young_adult": ["alcohol", "fast food", "desserts"],
                "middle_aged": ["refined grains", "sweetened beverages", "high-fat foods"],
                "senior": ["high-sugar foods", "difficult-to-digest items", "large portions"]
            },
            "meal_pattern": {
                "all": "Consistent meal timing with balanced macronutrients",
                "adolescent": "3 structured meals with protein-rich snacks",
                "young_adult": "Regular meals with emphasis on protein and fiber",
                "middle_aged": "Smaller, frequent meals to maintain blood sugar",
                "senior": "4-5 smaller meals with consistent timing"
            },
            "supplements": {
                "all": ["chromium", "magnesium", "vitamin d"],
                "adolescent": ["multivitamin", "calcium"],
                "young_adult": ["berberine", "alpha-lipoic acid"],
                "middle_aged": ["cinnamon", "fenugreek", "biotin"],
                "senior": ["vitamin b12", "fiber supplement", "probiotics"]
            },
            "exercise_plan": {
                "cardio": "150 minutes/week moderate cardio (walking, swimming, cycling)",
                "strength": "2-3 days/week resistance training to improve insulin sensitivity",
                "flexibility": "Daily stretching and balance exercises",
                "intensity": "Moderate intensity, monitor blood sugar before/after exercise",
                "precautions": "Check blood sugar before exercise, carry glucose tablets"
            }
        },
        "obesity": {
            "general_advice": "Focus on sustainable weight management through balanced nutrition and increased physical activity.",
            "foods_to_include": {
                "all": ["lean proteins", "fiber-rich vegetables", "whole grains", "healthy fats", "low-calorie fruits"],
                "adolescent": ["growth-supporting proteins", "calcium-rich foods", "iron sources"],
                "young_adult": ["nutrient-dense whole foods", "varied protein sources"],
                "middle_aged": ["anti-inflammatory foods", "antioxidant-rich foods"],
                "senior": ["easily digestible proteins", "hydrating foods", "nutrient-dense options"]
            },
            "foods_to_avoid": {
                "all": ["highly processed foods", "excessive sugar", "trans fats", "refined carbohydrates", "sugary beverages"],
                "adolescent": ["sugary beverages", "highly processed snacks", "fast food"],
                "young_adult": ["excessive alcohol", "ultra-processed foods", "large portions"],
                "middle_aged": ["excessive sodium", "refined carbohydrates", "high-calorie foods"],
                "senior": ["high-sodium foods", "difficult-to-chew items", "excessive portions"]
            },
            "meal_pattern": {
                "all": "Portion-controlled meals with emphasis on protein and fiber",
                "adolescent": "3 structured meals with healthy snacks",
                "young_adult": "Regular meals focusing on satiety and nutrition",
                "middle_aged": "Smaller, frequent meals to maintain metabolism",
                "senior": "4-5 smaller, nutrient-dense meals throughout day"
            },
            "supplements": {
                "all": ["multivitamin", "vitamin d", "omega-3"],
                "adolescent": ["calcium", "iron"],
                "young_adult": ["protein powder", "green tea extract"],
                "middle_aged": ["conjugated linoleic acid", "garcinia cambogia"],
                "senior": ["vitamin b12", "calcium", "fiber supplement"]
            },
            "exercise_plan": {
                "cardio": "300 minutes/week moderate cardio for weight loss (walking, cycling, swimming)",
                "strength": "3-4 days/week resistance training to build muscle mass",
                "flexibility": "Daily stretching and mobility work",
                "intensity": "Mix of moderate and high-intensity intervals",
                "precautions": "Start slowly, focus on consistency, avoid overtraining"
            }
        },
        "alzheimer's disease": {
            "general_advice": "Focus on brain-healthy nutrition with emphasis on antioxidants and anti-inflammatory foods.",
            "foods_to_include": {
                "all": ["fatty fish", "berries", "leafy greens", "nuts and seeds", "olive oil", "whole grains", "turmeric", "dark chocolate"],
                "adolescent": ["omega-3 rich foods", "antioxidant-rich fruits", "brain-supporting proteins"],
                "young_adult": ["nutrient-dense whole foods", "varied protein sources"],
                "middle_aged": ["anti-inflammatory foods", "antioxidant-rich foods"],
                "senior": ["easily digestible proteins", "hydrating foods", "nutrient-dense options"]
            },
            "foods_to_avoid": {
                "all": ["trans fats", "excessive sugar", "processed foods", "refined carbohydrates", "alcohol"],
                "adolescent": ["sugary beverages", "highly processed snacks", "artificial sweeteners"],
                "young_adult": ["excessive alcohol", "ultra-processed foods", "high-sugar foods"],
                "middle_aged": ["excessive sodium", "refined carbohydrates", "inflammatory foods"],
                "senior": ["high-sodium foods", "difficult-to-chew items", "excessive portions"]
            },
            "meal_pattern": {
                "all": "MIND diet pattern combining Mediterranean and DASH diets",
                "adolescent": "3 balanced meals with brain-healthy snacks",
                "young_adult": "Regular meals focusing on cognitive support",
                "middle_aged": "Anti-inflammatory meal pattern",
                "senior": "4-5 smaller, nutrient-dense meals throughout day"
            },
            "supplements": {
                "all": ["omega-3", "vitamin d", "b-complex vitamins"],
                "adolescent": ["multivitamin", "calcium"],
                "young_adult": ["acetyl-l-carnitine", "phosphatidylserine"],
                "middle_aged": ["ginkgo biloba", "curcumin", "resveratrol"],
                "senior": ["vitamin b12", "vitamin e", "coenzyme q10"]
            },
            "exercise_plan": {
                "cardio": "150 minutes/week moderate cardio to improve blood flow to brain",
                "strength": "2-3 days/week resistance training for cognitive benefits",
                "flexibility": "Daily stretching and balance exercises",
                "intensity": "Moderate intensity with focus on consistency",
                "precautions": "Include cognitive challenges, social interaction during exercise"
            }
        },
        "breast cancer": {
            "general_advice": "Focus on anti-inflammatory nutrition and maintaining healthy body weight.",
            "foods_to_include": {
                "all": ["cruciferous vegetables", "berries", "fatty fish", "whole grains", "legumes", "green tea", "turmeric", "garlic"],
                "adolescent": ["growth-supporting proteins", "calcium-rich foods", "antioxidant-rich fruits"],
                "young_adult": ["nutrient-dense whole foods", "varied protein sources"],
                "middle_aged": ["anti-inflammatory foods", "antioxidant-rich foods"],
                "senior": ["easily digestible proteins", "hydrating foods", "nutrient-dense options"]
            },
            "foods_to_avoid": {
                "all": ["processed meats", "excessive alcohol", "refined sugars", "trans fats", "charred foods"],
                "adolescent": ["sugary beverages", "highly processed snacks", "artificial sweeteners"],
                "young_adult": ["excessive alcohol", "ultra-processed foods", "high-sugar foods"],
                "middle_aged": ["excessive sodium", "refined carbohydrates", "inflammatory foods"],
                "senior": ["high-sodium foods", "difficult-to-chew items", "excessive portions"]
            },
            "meal_pattern": {
                "all": "Plant-forward diet with emphasis on anti-inflammatory foods",
                "adolescent": "3 balanced meals with healthy snacks",
                "young_adult": "Regular meals focusing on cancer prevention",
                "middle_aged": "Anti-inflammatory meal pattern",
                "senior": "4-5 smaller, nutrient-dense meals throughout day"
            },
            "supplements": {
                "all": ["vitamin d", "omega-3", "antioxidants"],
                "adolescent": ["multivitamin", "calcium"],
                "young_adult": ["curcumin", "green tea extract"],
                "middle_aged": ["resveratrol", "indole-3-carbinol"],
                "senior": ["vitamin b12", "vitamin e", "selenium"]
            },
            "exercise_plan": {
                "cardio": "150 minutes/week moderate cardio to maintain healthy weight",
                "strength": "2-3 days/week resistance training for bone health",
                "flexibility": "Daily stretching and yoga for stress reduction",
                "intensity": "Moderate intensity with focus on consistency",
                "precautions": "Avoid excessive exercise, focus on stress reduction"
            }
        }
    }
    
    # Convert disease to lowercase and find closest match
    disease_lower = disease.lower()
    matched_disease = None
    
    # Direct match
    if disease_lower in comprehensive_plans:
        matched_disease = disease_lower
    else:
        # Try to find a partial match
        for key in comprehensive_plans.keys():
            if key in disease_lower or disease_lower in key:
                matched_disease = key
                break
                
    # Default to general recommendations if no match
    if not matched_disease:
        matched_disease = "genetic variant of unknown significance"
        comprehensive_plans[matched_disease] = {
            "general_advice": "Focus on a balanced diet with diverse nutrients to support overall health.",
            "foods_to_include": {
                "all": ["variety of fruits and vegetables", "whole grains", "lean proteins", "healthy fats"],
                "adolescent": ["growth-supporting foods", "calcium-rich foods", "iron sources"],
                "young_adult": ["nutrient-dense whole foods", "varied protein sources"],
                "middle_aged": ["anti-inflammatory foods", "antioxidant-rich foods"],
                "senior": ["easily digestible proteins", "hydrating foods", "nutrient-dense options"]
            },
            "foods_to_avoid": {
                "all": ["highly processed foods", "excessive sugar", "trans fats"],
                "adolescent": ["sugary beverages", "highly processed snacks"],
                "young_adult": ["excessive alcohol", "ultra-processed foods"],
                "middle_aged": ["excessive sodium", "refined carbohydrates"],
                "senior": ["high-sodium foods", "difficult-to-chew items"]
            },
            "meal_pattern": {
                "all": "Regular balanced meals with variety of nutrients",
                "adolescent": "3 structured meals with nutrient-dense snacks",
                "young_adult": "Regular meals focusing on diverse nutrient intake",
                "middle_aged": "Mediterranean-style eating pattern",
                "senior": "4-5 smaller, nutrient-dense meals throughout day"
            },
            "supplements": {
                "all": ["multivitamin"],
                "adolescent": ["vitamin d", "calcium"],
                "young_adult": ["vitamin d"],
                "middle_aged": ["vitamin d", "omega-3"],
                "senior": ["vitamin b12", "vitamin d", "calcium"]
            },
            "exercise_plan": {
                "cardio": "150 minutes/week moderate cardio for general health",
                "strength": "2-3 days/week resistance training",
                "flexibility": "Daily stretching and mobility work",
                "intensity": "Moderate intensity with focus on consistency",
                "precautions": "Start slowly, focus on consistency"
            }
        }
    
    plan = comprehensive_plans[matched_disease]
    
    # Compile the complete nutrition and exercise plan
    complete_plan = {
        "disease": disease,
        "age_group": age_group,
        "risk_level": risk_level,
        "overall_risk": overall_risk,
        "general_advice": plan["general_advice"],
        "foods_to_include": plan["foods_to_include"]["all"] + plan["foods_to_include"][age_group],
        "foods_to_avoid": plan["foods_to_avoid"]["all"] + plan["foods_to_avoid"][age_group],
        "meal_pattern": f"{plan['meal_pattern']['all']}. {plan['meal_pattern'][age_group]}.",
        "supplements": plan["supplements"]["all"] + plan["supplements"][age_group],
        "exercise_plan": plan["exercise_plan"],
        "disclaimer": "This nutrition and exercise plan is for informational purposes only. Please consult with a healthcare provider or registered dietitian before making significant dietary or exercise changes."
    }
    
    return complete_plan