# 🧬 Predictive Analysis on Genomic Data — Treatment Response Prediction

> AI-powered genomic risk prediction platform that analyzes DNA variants, predicts disease risk, generates personalized nutrition plans, and provides AI-assisted healthcare guidance.

---

# 🌟 Project Overview

This project is a **full-stack AI-powered genomic analysis platform** where users can upload their DNA data files and receive:

✅ Disease risk prediction  
✅ Personalized nutrition & lifestyle plans  
✅ Treatment response insights  
✅ AI-powered medical chatbot support  

The system combines **Genomics + Machine Learning + Healthcare AI** using real-world scientific databases such as:

- ClinVar (NCBI)
- GWAS Catalog (EBI)
- PharmGKB (Stanford University)

---

# 🧠 What Problem Does This Solve?

DNA testing companies provide users with thousands of confusing SNP records like:

```txt
rs429358     CC
rs7903146    TT
rs9939609    AA
```

Most people cannot understand:

- Which diseases they may be genetically prone to
- Which medications may affect them differently
- What diet or exercise they should follow

This project automatically analyzes genomic variants and converts them into meaningful healthcare insights.

---

# 🚀 Key Features

## 🧬 1. DNA File Upload & Parsing

- Supports SNP-based genomic files
- Parses `.txt`, `.csv`, `.tsv`
- Supports PLINK research formats (`.ped`, `.map`)
- Cleans and validates genotype data automatically

---

## 🔍 2. Disease Variant Matching

Matches uploaded SNPs against:

| Database | Purpose |
|---|---|
| ClinVar | Disease-associated variants |
| GWAS Catalog | Population-level genetic associations |
| PharmGKB | Drug response prediction |

---

## 🤖 3. Machine Learning Risk Prediction

Uses a **Random Forest Classifier** to predict:

- 🟢 Low Risk
- 🟡 Medium Risk
- 🔴 High Risk

### ML Workflow

- SNP encoding
- Feature preparation
- Train-test split
- Random Forest training
- Risk classification

---

## 🥗 4. Personalized Nutrition & Lifestyle Plans

Generates customized:

- Diet recommendations
- Foods to avoid
- Supplements
- Exercise routines

Based on:

- Disease risk
- Age group
- Genetic findings

---

## 💬 5. AI Medical Chatbot

Powered by:

- Groq API
- Meta LLaMA 3-8B

Users can ask:

- Disease-related questions
- Nutrition guidance
- Lifestyle suggestions
- Medication-related queries

---

# 🏗️ System Architecture

```text
User Uploads DNA File
        ↓
File Parsing & Cleaning
        ↓
SNP Matching with Databases
        ↓
Genotype Encoding
        ↓
Machine Learning Prediction
        ↓
Disease Detection
        ↓
Nutrition Plan Generation
        ↓
AI Medical Chatbot Assistance
```

---

# 📂 Project Structure

```text
├── run.py
├── app.py
├── auth.py
├── genomic_risk_pipeline.py
├── nutrition_dataset.py
├── users.json
├── activity_log.json
├── variant_summary.txt.gz
├── gwas.tsv
├── clinical_annotations.tsv
├── templates/
├── uploads/
└── ui_test_files/
```

---

# 📖 File Descriptions

| File | Purpose |
|---|---|
| `run.py` | Starts the Flask application |
| `app.py` | Main Flask routes and application logic |
| `auth.py` | Authentication & security handling |
| `genomic_risk_pipeline.py` | ML pipeline & genomic analysis |
| `nutrition_dataset.py` | Nutrition & exercise recommendation data |
| `users.json` | User account storage |
| `activity_log.json` | Security and login activity logs |

---

# 🧬 Datasets Used

## 1️⃣ ClinVar — NCBI

### Purpose
Maps SNP variants to diseases.

### Example
| SNP | Disease |
|---|---|
| rs429358 | Alzheimer's Disease |
| rs1799966 | Breast Cancer |

### Source
https://www.ncbi.nlm.nih.gov/clinvar/

---

## 2️⃣ GWAS Catalog — EMBL-EBI

### Purpose
Contains large-scale population genetic association studies.

### Example
| SNP | Disease |
|---|---|
| rs7903146 | Type 2 Diabetes |
| rs10757274 | Heart Disease |

### Source
https://www.ebi.ac.uk/gwas/

---

## 3️⃣ PharmGKB — Stanford University

### Purpose
Predicts medicine response based on genetics.

### Example
| SNP | Drug Impact |
|---|---|
| rs1065852 | Codeine metabolism |

### Source
https://www.pharmgkb.org/

---

# ⚙️ Technologies Used

## Backend
- Python
- Flask
- Flask-CORS

## Machine Learning
- Scikit-learn
- Random Forest Classifier

## Data Processing
- pandas
- numpy

## Security
- Werkzeug
- scrypt hashing

## AI Integration
- Groq API
- LLaMA 3-8B

---

# 🔐 Security Features

✅ Password hashing using scrypt  
✅ Account lockout after failed attempts  
✅ Rate limiting  
✅ Admin MFA using PIN verification  
✅ Session-based authentication  
✅ Role-based access control  
✅ Activity logging with timestamps & IPs  

---

# 🧠 Machine Learning Model

## Random Forest Classifier

The model:

- Builds 100 decision trees
- Each tree predicts risk level
- Majority voting decides final output

### Why Random Forest?

✅ Handles genomic data effectively  
✅ Reduces overfitting  
✅ Works well with multiple SNP features  
✅ High robustness and accuracy  

---

# 🧬 Genomic Concepts Used

| Term | Meaning |
|---|---|
| DNA | Genetic instruction manual |
| SNP | Variation at a DNA position |
| rsID | SNP identifier |
| Genotype | DNA letters like AA, AG |
| GWAS | Population-level genetic study |
| Pharmacogenomics | DNA impact on medicine response |

---

# 🌐 API Routes

| Route | Function |
|---|---|
| `/login` | User login |
| `/register` | User registration |
| `/predict` | DNA analysis |
| `/chat` | AI medical chatbot |
| `/admin` | Admin dashboard |
| `/logout` | Logout |

---

# 📊 Risk Prediction Logic

## Genotype Encoding

| Genotype | Dosage |
|---|---|
| AA / CC / GG / TT | 0 |
| AG / CT / AC | 1 |
| Alternate Homozygous | 2 |

---

# 🥗 Nutrition Recommendation Logic

Recommendations depend on:

- Disease category
- Age group
- Genetic findings

Age groups:

- Adolescent
- Young Adult
- Middle Aged
- Senior

---

# 🧪 Sample Diseases Detected

| Disease | Important SNP |
|---|---|
| Alzheimer's Disease | rs429358 |
| Type 2 Diabetes | rs7903146 |
| Heart Disease | rs10757274 |
| Obesity | rs9939609 |
| Breast Cancer | rs1799966 |

---

# 🔄 Complete Application Flow

```text
Start Flask Server
        ↓
Load Genomic Databases
        ↓
User Authentication
        ↓
Upload DNA File
        ↓
Parse & Clean Data
        ↓
Match SNPs
        ↓
Run ML Prediction
        ↓
Generate Health Plan
        ↓
Chat with AI Assistant
```

---

# 🛠️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/project-name.git
cd project-name
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows
```bash
venv\Scripts\activate
```

### Linux / Mac
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Application

```bash
python run.py
```

Server starts at:

```text
http://127.0.0.1:5000
```

---

# 📈 Future Improvements

- Deep Learning models
- Real-time genomic APIs
- Cloud deployment
- PDF medical reports
- Multi-language support
- Doctor consultation integration

---

# 🎯 Interview Summary

### One-Line Description

> “An AI-powered genomic healthcare platform that predicts disease risk and treatment response using DNA variants, machine learning, and personalized healthcare recommendations.”

---

# 👨‍💻 Author

## Devansh Rai

AI & Data Analytics Enthusiast  
Machine Learning | Genomics | Healthcare AI

---

# ⭐ If You Like This Project

Give it a ⭐ on GitHub and support the project!
