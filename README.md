# 🔴 PhishGuard — Phishing Email Detector

> AI-powered phishing email detection using Machine Learning. Red & Black cybersecurity theme.

![Python](https://img.shields.io/badge/Python-3.8%2B-red?style=flat-square&logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0%2B-red?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-red?style=flat-square)
![Accuracy](https://img.shields.io/badge/Accuracy-94.12%25-brightgreen?style=flat-square)

---

## ✨ Features

- **Real-time Detection** — Paste any email and get instant phishing/safe classification
- **Confidence Score** — See how confident the model is in its decision
- **Red Flag Analysis** — Specific threat indicators identified in the email
- **Probability Meters** — Visual phishing risk and safe score bars
- **Model Statistics** — Accuracy, ROC-AUC, Confusion Matrix displayed live
- **ML Pipeline Diagram** — Visual representation of the processing pipeline

## 🤖 Machine Learning

| Property | Value |
|----------|-------|
| Algorithm | Random Forest Classifier |
| Accuracy | **94.12%** |
| ROC-AUC | **1.000** |
| Cross-Validation (5-fold) | **89.63% ± 12%** |
| Features | 3000 TF-IDF + 10 hand-crafted |
| Training Samples | 135 curated emails |

### Features Extracted
- TF-IDF bigrams (3000 dimensions)
- URL count and suspicious TLD detection
- Urgency word frequency
- Financial/money lure keywords
- Phishing phrase detection
- Exclamation mark count
- Capital letter ratio
- IP-address URL detection

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/phishguard.git
cd phishguard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the model
```bash
python train_model.py
```

### 4. Start the web server
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

## 📁 Project Structure

```
phishing-detector/
├── app.py                 # Flask web server & REST API
├── train_model.py         # ML training script
├── requirements.txt       # Python dependencies
├── model/
│   ├── classifier.pkl     # Trained Random Forest model
│   ├── tfidf.pkl          # Fitted TF-IDF vectorizer
│   └── metrics.json       # Model performance metrics
├── templates/
│   └── index.html         # Main HTML page
└── static/
    ├── css/style.css      # Red/black cyberpunk styling
    └── js/main.js         # Frontend logic & API calls
```

## 🌐 API Endpoints

### `POST /api/predict`
Classify an email as phishing or safe.

**Request:**
```json
{
  "email": "URGENT: Your account has been suspended..."
}
```

**Response:**
```json
{
  "prediction": "PHISHING",
  "is_phishing": true,
  "confidence": 96.5,
  "phishing_probability": 96.5,
  "safe_probability": 3.5,
  "red_flags": [
    "Urgency language: urgent, immediately, suspended",
    "Suspicious domain extension detected (.xyz)"
  ]
}
```

### `GET /api/metrics`
Returns model performance statistics.

## ⚙️ Tech Stack

- **ML:** Scikit-learn, NumPy, Pandas
- **Backend:** Flask, Flask-CORS
- **Frontend:** Vanilla HTML/CSS/JS
- **Fonts:** Orbitron, Rajdhani, Share Tech Mono

 

---

Made by : Vishal Jangid
