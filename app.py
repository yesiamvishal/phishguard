"""
Phishing Email Detection - Flask API
"""
import os, json, re, pickle, numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE = os.path.dirname(os.path.abspath(__file__))

# Load model artifacts
with open(os.path.join(BASE, 'model/tfidf.pkl'), 'rb') as f:
    TFIDF = pickle.load(f)
with open(os.path.join(BASE, 'model/classifier.pkl'), 'rb') as f:
    CLF = pickle.load(f)
with open(os.path.join(BASE, 'model/metrics.json')) as f:
    METRICS = json.load(f)


def extract_features(text):
    text_lower = text.lower()
    urls = re.findall(r'http[s]?://\S+', text)
    suspicious_tlds = ['.xyz', '.tk', '.ml', '.biz', '.top', '.ru', '.cn', '.pw', '.cc']
    urgent_words = ['urgent', 'immediately', 'alert', 'warning', 'suspend', 'verify',
                    'expire', 'final', 'critical', 'limited', 'act now', 'deadline',
                    'blocked', 'frozen', 'terminated', 'compromised']
    money_words = ['free', 'win', 'prize', 'cash', 'money', 'reward', 'gift',
                   'lottery', '$', 'bitcoin', 'crypto', 'investment', 'refund']
    phish_words = ['click here', 'log in', 'verify your', 'confirm your', 'update your',
                   'account suspended', 'unauthorized', 'unusual activity', 'ssn',
                   'social security', 'bank details', 'credit card', 'password expires']
    return [
        len(urls),
        int(any(tld in url.lower() for url in urls for tld in suspicious_tlds)),
        sum(1 for w in urgent_words if w in text_lower),
        sum(1 for w in money_words if w in text_lower),
        sum(1 for p in phish_words if p in text_lower),
        text.count('!'),
        sum(1 for c in text if c.isupper()) / max(len(text), 1),
        len(text),
        int(bool(re.search(r'http[s]?://\d{1,3}\.\d{1,3}', text))),
        int('@' in text and 'gmail' not in text_lower and 'yahoo' not in text_lower),
    ]


def get_red_flags(text):
    text_lower = text.lower()
    flags = []
    urls = re.findall(r'http[s]?://\S+', text)
    suspicious_tlds = ['.xyz', '.tk', '.ml', '.biz', '.top', '.ru', '.cn', '.pw', '.cc']
    if any(tld in url.lower() for url in urls for tld in suspicious_tlds):
        flags.append("Suspicious domain extension detected (.xyz, .tk, .ml, etc.)")
    if len(urls) > 0:
        flags.append(f"{len(urls)} URL(s) found in email body")
    urgent_found = [w for w in ['urgent', 'immediately', 'alert', 'warning', 'suspended',
                                 'expires', 'final notice', 'critical'] if w in text_lower]
    if urgent_found:
        flags.append(f"Urgency language: {', '.join(urgent_found[:3])}")
    money_found = [w for w in ['free', 'prize', 'lottery', 'bitcoin', 'cash reward',
                                'gift card', 'wire transfer'] if w in text_lower]
    if money_found:
        flags.append(f"Financial lure words: {', '.join(money_found[:3])}")
    if text.count('!') >= 2:
        flags.append(f"Excessive exclamation marks ({text.count('!')} found)")
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    if caps_ratio > 0.15:
        flags.append(f"High proportion of capital letters ({caps_ratio:.0%})")
    phish_phrases = ['click here', 'verify your', 'confirm your', 'bank details',
                     'credit card', 'social security', 'password expires']
    found_phrases = [p for p in phish_phrases if p in text_lower]
    if found_phrases:
        flags.append(f"Phishing phrases: '{found_phrases[0]}'")
    if re.search(r'http[s]?://\d{1,3}\.\d{1,3}', text):
        flags.append("IP-address URL detected (highly suspicious)")
    return flags


@app.route('/')
def index():
    return render_template('index.html', metrics=METRICS)


@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    email_text = data.get('email', '').strip()
    if not email_text:
        return jsonify({'error': 'No email text provided'}), 400

    tfidf_vec = TFIDF.transform([email_text]).toarray()
    manual_vec = np.array([extract_features(email_text)])
    X = np.hstack([tfidf_vec, manual_vec])

    pred = int(CLF.predict(X)[0])
    proba = CLF.predict_proba(X)[0]
    confidence = float(max(proba)) * 100

    red_flags = get_red_flags(email_text)

    return jsonify({
        'prediction': 'PHISHING' if pred == 1 else 'SAFE',
        'is_phishing': bool(pred == 1),
        'confidence': round(confidence, 2),
        'phishing_probability': round(float(proba[1]) * 100, 2),
        'safe_probability': round(float(proba[0]) * 100, 2),
        'red_flags': red_flags,
    })


@app.route('/api/metrics')
def metrics():
    return jsonify(METRICS)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
