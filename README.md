# 🔴 PhishGuard — Phishing Email Detector

> AI-powered phishing email detection using Machine Learning. Red & Black cybersecurity theme.

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-phishguard.onrender.com-e80000?style=for-the-badge)](https://phishguard-6m9w.onrender.com/)

![Python](https://img.shields.io/badge/Python-3.8%2B-red?style=flat-square&logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0%2B-red?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-red?style=flat-square)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render)
![Accuracy](https://img.shields.io/badge/Accuracy-94.12%25-brightgreen?style=flat-square)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)

---

## 🌐 Live Demo

**🔗 [https://phishguard-6m9w.onrender.com/](https://phishguard-6m9w.onrender.com/)**

> Try it instantly — no installation needed. Paste any email and get a real-time phishing verdict with confidence score, risk meters, and threat indicators.

> ⚠️ **Note:** The app is hosted on Render's free tier. If it hasn't been visited recently, it may take **30–60 seconds to wake up** on first load. This is normal — just wait and refresh.

---

## ✨ Features

- **Real-time Detection** — Paste any email and get instant phishing/safe classification
- **Confidence Score** — See how confident the model is in its decision
- **Red Flag Analysis** — Specific threat indicators identified in the email
- **Probability Meters** — Visual phishing risk and safe score bars
- **Model Statistics** — Accuracy, ROC-AUC, Confusion Matrix displayed live
- **ML Pipeline Diagram** — Visual representation of the processing pipeline
- **Quick Examples** — One-click sample phishing and safe emails to test immediately

---

## 🤖 Machine Learning

| Property | Value |
|----------|-------|
| Algorithm | Random Forest Classifier |
| Accuracy | **94.12%** |
| ROC-AUC | **1.000** |
| Cross-Validation (5-fold) | **89.63% ± 12%** |
| Features | 3000 TF-IDF + 10 hand-crafted |
| Training Samples | 135 curated emails |
| Trees in Forest | 200 |

### Features Extracted
- TF-IDF bigrams (3000 dimensions)
- URL count and suspicious TLD detection (`.xyz`, `.tk`, `.ml`, `.biz`, etc.)
- Urgency word frequency
- Financial/money lure keywords
- Phishing phrase detection
- Exclamation mark count
- Capital letter ratio
- IP-address URL detection

---

## 🚀 Run Locally

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

---

## 📁 Project Structure

```
phishing-detector/
├── app.py                 # Flask web server & REST API
├── train_model.py         # ML training script
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment config
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

---

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
Returns live model performance statistics including accuracy, AUC, and confusion matrix.

---

## ☁️ Deployment

This project is deployed on **[Render](https://render.com)** (free tier).

To deploy your own instance:

1. Fork this repo
2. Sign up at [render.com](https://render.com) with GitHub
3. Click **New → Web Service** → connect your fork
4. Render auto-detects settings from `render.yaml`
5. Click **Deploy** — live in ~3 minutes at your own URL

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| ML | Scikit-learn, NumPy, Pandas |
| Backend | Python, Flask, Flask-CORS, Gunicorn |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Hosting | Render (free tier) |
| Fonts | Orbitron, Rajdhani, Share Tech Mono |

---

 

---

Made with ❤️ by Vishal Jangid &nbsp;|&nbsp; [Live Demo](https://phishguard-6m9w.onrender.com/)
