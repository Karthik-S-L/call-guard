# Call Guard Backend

## 📌 Project Overview

Call Guard Backend is a **Python-based system** for analyzing **debt collection call recordings** to detect:

- **Profanity & Compliance Violations** (using Regex & ML/LLM approaches)
- **Privacy Violations** (using Hugging Face API)
- **Call Quality Metrics** (Silence & Overtalk Percentage)
- **Visualizations** (Streamlit Dashboard for insights)

Built using **FastAPI** for backend processing and **Streamlit** for UI visualization.

---

## ⚙️ Tech Stack

- **Backend**: FastAPI
- **ML Models**: Hugging Face API
- **Frontend**: Streamlit
- **Database**: (Optional) SQLite/PostgreSQL
- **Deployment**: Docker (optional)

---

## 🏗️ Project Structure

```
your_project/
│── app/
│   ├── main.py               # FastAPI app entry point
│   ├── api/
│   │   ├── v1/               # API versioning
│   │   │   ├── endpoints/
│   │   │   │   ├── profanity.py        # Profanity detection APIs
│   │   │   │   ├── compliance.py       # Privacy violation detection APIs
│   │   │   │   ├── call_quality.py     # Call quality metrics APIs
│   ├── services/
│   │   ├── profanity.py       # Regex & ML-based profanity detection logic
│   │   ├── compliance_ml.py   # Privacy violation detection logic
│   │   ├── call_quality.py    # Call silence & overtalk calculations
│── call_quality_dashboard.py  # Streamlit dashboard for call quality
│── requirements.txt           # Dependencies
│── README.md                  # Project documentation
```

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/call-guard-backend.git
cd call-guard-backend
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv call_guard_env
source call_guard_env/bin/activate   # For Linux/macOS
call_guard_env\Scripts\activate      # For Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

Create a **.env** file in the root folder:

```ini
HF_API_KEY=your_huggingface_api_key
```

### 5️⃣ Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

API will be available at: **http://127.0.0.1:8000/docs**

---

## 🔌 API Endpoints

### 📍 **1. Profanity Detection**

- **Regex-based Detection:** `POST /detect/profanity/regex`
- **ML-based Detection:** `POST /detect/profanity/ml`

### 📍 **2. Privacy Violation Detection**

- **ML-based Detection:** `POST /detect/privacy-violation/ml`

### 📍 **3. Call Quality Metrics**

- **Silence & Overtalk Calculation:** `GET /call-quality`

---

## 📊 Running Streamlit Dashboard

```bash
streamlit run call_quality_dashboard.py
```

The dashboard visualizes **silence and overtalk percentages per call**.

---

## 🛠️ Future Enhancements

- Integrate a local ML model for **privacy violation detection**.
- Store **analysis results in a database** for long-term tracking.
- Extend **compliance checks** for legal guidelines.

---

## 🤝 Contributing

Feel free to fork the repo, submit issues, and make pull requests!

📧 Contact: your.email@example.com
