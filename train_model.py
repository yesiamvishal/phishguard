"""
Phishing Email Detection Model
Trains a Random Forest classifier on a synthetic + pattern-based dataset
and saves the model + vectorizer for use by the Flask API.
"""

import numpy as np
import pandas as pd
import pickle
import json
import re
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, roc_auc_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# ── Dataset ──────────────────────────────────────────────────────────────────

PHISHING_EMAILS = [
    "URGENT: Your account has been suspended! Click here immediately to verify your identity at http://secure-bank-login.xyz/verify",
    "Congratulations! You've won $1,000,000 lottery prize. Send your bank details to claim@prize-winner.net now!",
    "Dear customer, your PayPal account will be closed unless you verify at http://paypal-secure.tk/login within 24 hours",
    "ALERT: Unusual activity detected on your account. Login immediately: http://amazon-security.ml/signin",
    "Your Apple ID has been locked. Verify your information now at http://apple-id-verify.xyz or lose access forever",
    "IRS TAX REFUND: You are eligible for a $3,200 refund. Provide SSN and banking info to claim@irs-refund.net",
    "FINAL WARNING: Your email account will be deactivated. Click http://email-verify.top/activate to keep access",
    "Dear winner, you have been selected for a $500 gift card. Claim at http://free-giftcard.biz/claim",
    "Your Netflix subscription has expired. Update payment at http://netflix-billing.xyz/update immediately",
    "Security breach detected! Your password was compromised. Reset now: http://secure-reset.tk/password",
    "Urgent bank transfer required. Your account shows suspicious activity. Verify: http://bank-alert.ml/check",
    "You have a pending package delivery. Pay $2.99 fee at http://delivery-tracking.xyz/pay to release it",
    "Microsoft account blocked for security reasons. Unlock at http://microsoft-support.tk/unlock immediately",
    "FREE iPhone 15 Pro! You are our lucky winner. Claim prize at http://iphone-winner.biz within 1 hour",
    "Dear valued customer, confirm your credit card details at http://card-verify.xyz or service will be suspended",
    "ALERT: Your social security number has been suspended. Call 1-800-555-FAKE or visit http://ssa-alert.ml",
    "Crypto investment opportunity! Double your Bitcoin in 24 hours. Send funds to wallet: 1FakeWallet123ABC",
    "Your Gmail password expires today. Renew at http://gmail-renew.xyz/password or lose all emails",
    "Bank of America: Account verification required. Login http://bofa-secure.tk/verify - expires in 2 hours",
    "Phishing test: click here to steal your credentials http://totally-not-malware.ru/login?track=yes",
    "You owe back taxes! IRS immediate action required. Pay at http://irs-payment.xyz or face arrest",
    "Your insurance claim approved! Collect $8,500 at http://claim-money.ml/collect - 24hr deadline",
    "WINNER! Amazon Prime lucky draw winner selected. Claim $200 voucher: http://amazon-prize.tk/claim",
    "Ransomware alert: Your files encrypted. Pay 2 BTC to decrypt@hacker.net within 48 hours or lose data",
    "Verify your identity for Wells Fargo account at http://wellsfargo-verify.xyz - account frozen",
    "Your student loan forgiveness approved! Claim $20,000 at http://loan-forgive.tk/claim now",
    "CRITICAL: Virus detected on your computer! Call 1-800-FAKE-HELP or visit http://antivirus-fix.xyz",
    "DHL delivery failed. Reschedule delivery fee $1.99 at http://dhl-redelivery.xyz/pay",
    "Your Venmo account limited. Verify at http://venmo-secure.ml/verify to restore full access",
    "Investment opportunity: 500% returns guaranteed! Wire $1000 to profit@investment-fake.com now",
    "Chase bank: Unusual login attempt. Secure account at http://chase-alert.xyz/protect immediately",
    "Your COVID relief payment ready. Claim $1,400 at http://covid-relief.tk/claim - limited time",
    "Warning: Your computer has been hacked! Fix it now at http://computer-fix.biz or lose all data",
    "Exclusive offer: Work from home earn $5000/week! Apply: http://easy-money.xyz/apply - no experience",
    "Your subscription renewal failed. Update billing at http://subscription-billing.ml/update",
    "EMERGENCY: Family member in hospital needs $2000 wire transfer immediately to help@emergency.net",
    "Sweepstakes winner notification: Claim $50,000 prize at http://sweepstakes-winner.xyz - act fast",
    "Your Spotify premium expired. Reactivate free at http://spotify-renew.tk/free - today only",
    "LinkedIn: Your profile viewed by recruiters. Unlock views at http://linkedin-premium.xyz/unlock",
    "Tax refund available: $4,200 waiting for you at http://taxrefund-claim.ml - submit SSN to collect",
    "Unauthorized access to your account from Russia. Secure now: http://account-secure.xyz/lockdown",
    "PRIZE NOTIFICATION: You won a luxury cruise! Claim at http://cruise-winner.biz - pay $99 processing",
    "Your phone number won $5,000 cash! Collect at http://cash-prize.tk/collect before midnight tonight",
    "Bitcoin trading bot: Earn $1000 daily automatically. Install at http://crypto-bot.xyz - free trial",
    "Medical alert: Important health information requires immediate verification at http://health-verify.ml",
]

SAFE_EMAILS = [
    "Hi team, please find attached the quarterly report for Q3 2024. Let me know if you have any questions.",
    "Meeting reminder: Project standup tomorrow at 10am in Conference Room B. Agenda attached.",
    "Thank you for your purchase! Your order #12345 has been confirmed and will ship within 2-3 business days.",
    "Hi Sarah, just following up on our conversation from last week about the marketing campaign timeline.",
    "Newsletter: Top 10 productivity tips for remote workers this month. Unsubscribe at any time.",
    "Your flight booking confirmation for Flight AA1234 on December 15th. Boarding pass attached.",
    "Happy birthday! Wishing you a wonderful day filled with joy and celebration from all of us.",
    "Reminder: Your dentist appointment is scheduled for Tuesday, November 5th at 2:30 PM.",
    "GitHub notification: Pull request #456 has been merged into main branch by johndoe.",
    "Welcome to our team! Here's your onboarding guide and first week schedule. Excited to have you.",
    "Your monthly bank statement for October 2024 is now available in your online banking portal.",
    "Recipe of the week: Classic Italian Carbonara - ingredients and steps inside. Enjoy cooking!",
    "Meeting notes from today's product review: Action items assigned, next steps documented.",
    "Your Amazon order has been delivered. We hope you enjoy your purchase! Leave a review.",
    "IT maintenance scheduled Sunday 2-4 AM. Services may be briefly unavailable during this window.",
    "Congratulations on completing the Python course! Your certificate is attached to this email.",
    "Team lunch this Friday at 12:30 PM at The Garden Bistro. Please RSVP by Thursday afternoon.",
    "Your invoice #INV-2024-0892 is due on November 30th. Payment details in the attached PDF.",
    "Book club reminder: This month we're reading 'The Midnight Library'. Discussion on Saturday.",
    "Software update available for your app. New features include dark mode and improved performance.",
    "Your subscription renewal is coming up next month. No action needed unless you want to cancel.",
    "Feedback request: How would you rate your recent customer service experience? Takes 2 minutes.",
    "Weekly digest: Top stories in technology, science, and business for the week of Nov 4-10.",
    "Your Google Workspace storage is at 80%. Consider upgrading or deleting old files.",
    "Project update: Phase 2 development complete. QA testing starts Monday, release planned for Dec.",
    "LinkedIn: John Smith accepted your connection request. You now have 342 connections.",
    "HR announcement: New vacation policy effective January 1st. Please review the updated handbook.",
    "Your library books are due in 3 days. Renew online at the library website if needed.",
    "Slack notification: @channel - all hands meeting moved to 3 PM today due to schedule conflict.",
    "Annual performance review scheduled for next week. Self-evaluation form due by Friday EOD.",
    "Weather alert: Light rain expected tomorrow morning. Temperatures around 65°F in your area.",
    "Your podcast subscription includes 5 new episodes this week. Happy listening!",
    "Expense report approved. Reimbursement of $234.50 will appear in your next paycheck.",
    "New comment on your blog post: 'Great article! Really helpful for beginners learning ML.'",
    "Security tip: Enable two-factor authentication on all your accounts for better protection.",
    "Your gym membership renews automatically on the 15th. Visit in-person to make any changes.",
    "Conference registration confirmed. Workshop materials will be emailed one week before the event.",
    "Happy holidays from our team! Offices will be closed December 24-26. Enjoy the break!",
    "Your code review has been approved. Ready to merge when you are. Great work on the refactor.",
    "Reminder: Submit your timesheet by 5 PM Friday. Contact HR if you have any payroll questions.",
    "Photography club: Next meetup at Riverside Park, Saturday 7 AM for sunrise shots. Bring tripod.",
    "Your renewal for domain yourwebsite.com is due in 30 days. Renew in your hosting dashboard.",
    "Customer support ticket #789 has been resolved. Please rate your experience with our team.",
    "New research paper published in Nature: Breakthrough in renewable energy storage efficiency.",
    "Quarterly team outing: Escape room booked for December 10th at 6 PM. All are welcome!",
    "Your Spotify Wrapped is ready! You listened to 45,000 minutes of music this year. Top genre: Jazz.",
    "Board meeting agenda for Q4 review attached. Please prepare your department's KPI summary.",
    "Internship offer extended to 3 candidates from our fall recruiting cycle. Start date January 15.",
    "Your manuscript submission has been received. Review process takes 6-8 weeks. Thank you.",
    "Class assignment reminder: Final project due Sunday midnight. Submit via the course portal.",
]

def build_dataset():
    """Create a balanced, augmented dataset."""
    emails = []
    labels = []

    # Core samples
    for e in PHISHING_EMAILS:
        emails.append(e)
        labels.append(1)
    for e in SAFE_EMAILS:
        emails.append(e)
        labels.append(0)

    # Augmentation: light variations
    phishing_aug = [
        "URGENT ACTION REQUIRED: Verify your account details or face immediate suspension.",
        "You have been selected for exclusive rewards. Click to claim your prize now!",
        "Account security alert: Suspicious login detected. Immediate verification needed.",
        "Final notice: Unpaid invoice requires immediate payment to avoid legal action.",
        "Confirm your personal information at the link below or your account will be terminated.",
        "Limited time offer: Claim your free gift card before it expires tonight at midnight.",
        "WARNING: Your computer is infected with viruses. Call our helpline immediately.",
        "Your beneficiary has sent you a wire transfer. Verify your bank account to receive funds.",
        "Exclusive investment: Guaranteed 300% returns in 30 days. Limited spots available.",
        "Your social media account has been compromised. Reset credentials at fake-link.xyz now.",
        "Delivery notice: Package held at customs. Pay clearance fee of $4.99 to release.",
        "Your email storage full. Upgrade now at email-upgrade.xyz or lose your messages.",
        "Legal notice: You are being sued. Respond immediately to avoid court appearance.",
        "Password expiry notice: Your password expires in 24 hours. Update via link below.",
        "Cryptocurrency wallet verification required. Confirm details or lose your funds.",
        "Remote job offer: Earn $8000/month from home. No experience needed. Apply today!",
        "Your card was charged $499. Dispute at refund-claim.xyz if you did not authorize this.",
        "Inheritance notification: You are a beneficiary of $2.3M. Provide details to claim.",
        "CLICK IMMEDIATELY: Security certificate expired. Visit http://fix-ssl.xyz to resolve.",
        "Gift card scam: Purchase $500 iTunes cards and send codes to manager@company-fake.com",
    ]
    safe_aug = [
        "Good morning! Here are your action items from yesterday's strategy session.",
        "Please review the attached proposal and share your feedback by end of week.",
        "Reminder: The company picnic is next Saturday. Bring your family and enjoy the day.",
        "Your recent payment of $49.99 has been processed. Thank you for your business.",
        "New comment on your pull request: Looks good, minor suggestion on line 42.",
        "Congratulations on your promotion to Senior Engineer! Well deserved achievement.",
        "Office supplies order received. Items will be at the front desk by Monday morning.",
        "Training session on new HR software is scheduled for Thursday at 2 PM in Room A.",
        "Your article has been published on our blog. Great writing on machine learning basics.",
        "Thank you for attending our webinar. Recording and slides sent to registered attendees.",
        "Please complete the anonymous employee satisfaction survey by December 1st.",
        "Invitation: Join us for the annual charity fundraiser gala on November 20th.",
        "Your travel reimbursement has been approved and processed to your direct deposit.",
        "Code deployment successful. All tests passed. Production environment stable.",
        "Reminder: Please update your emergency contact information in the HR portal this week.",
        "New feature request added to backlog. Will be reviewed in next sprint planning.",
        "Coffee chat with the CEO scheduled for Friday at 11 AM. Casual Q&A format.",
        "Your professional certification exam is booked for December 8th at the testing center.",
        "Monthly newsletter: Company updates, employee spotlight, and upcoming events inside.",
        "System backup completed successfully. All data secured and verified. No issues found.",
    ]
    for e in phishing_aug:
        emails.append(e)
        labels.append(1)
    for e in safe_aug:
        emails.append(e)
        labels.append(0)

    return pd.DataFrame({'email': emails, 'label': labels})


# ── Feature Engineering ───────────────────────────────────────────────────────

def extract_features(text):
    """Hand-crafted features for email classification."""
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

    return {
        'url_count': len(urls),
        'has_suspicious_tld': int(any(tld in url.lower() for url in urls for tld in suspicious_tlds)),
        'urgent_word_count': sum(1 for w in urgent_words if w in text_lower),
        'money_word_count': sum(1 for w in money_words if w in text_lower),
        'phish_phrase_count': sum(1 for p in phish_words if p in text_lower),
        'exclamation_count': text.count('!'),
        'caps_ratio': sum(1 for c in text if c.isupper()) / max(len(text), 1),
        'text_length': len(text),
        'has_ip_url': int(bool(re.search(r'http[s]?://\d{1,3}\.\d{1,3}', text))),
        'has_at_symbol': int('@' in text and 'gmail' not in text_lower and 'yahoo' not in text_lower),
    }


# ── Training ──────────────────────────────────────────────────────────────────

def train():
    print("🔄 Building dataset...")
    df = build_dataset()
    print(f"   Total samples: {len(df)} | Phishing: {df['label'].sum()} | Safe: {(df['label']==0).sum()}")

    X_text = df['email']
    y = df['label']

    # TF-IDF on text
    tfidf = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1, 2),
        stop_words='english',
        sublinear_tf=True,
        min_df=1
    )

    X_tfidf = tfidf.fit_transform(X_text).toarray()

    # Manual features
    manual_feats = np.array([list(extract_features(t).values()) for t in X_text])
    X_all = np.hstack([X_tfidf, manual_feats])

    X_train, X_test, y_train, y_test = train_test_split(
        X_all, y, test_size=0.25, random_state=42, stratify=y
    )

    print("\n🤖 Training Random Forest classifier...")
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=2,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred).tolist()
    report = classification_report(y_test, y_pred, target_names=['Safe', 'Phishing'], output_dict=True)
    auc = roc_auc_score(y_test, y_prob)

    cv_scores = cross_val_score(clf, X_all, y, cv=5, scoring='accuracy')

    print(f"\n✅ Accuracy      : {acc*100:.2f}%")
    print(f"✅ ROC-AUC       : {auc:.4f}")
    print(f"✅ CV Mean Acc   : {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%")
    print(f"\nConfusion Matrix:\n  TN={cm[0][0]}  FP={cm[0][1]}\n  FN={cm[1][0]}  TP={cm[1][1]}")

    # Save everything
    with open('model/tfidf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    with open('model/classifier.pkl', 'wb') as f:
        pickle.dump(clf, f)

    metrics = {
        'accuracy': round(acc * 100, 2),
        'auc': round(auc, 4),
        'cv_mean': round(cv_scores.mean() * 100, 2),
        'cv_std': round(cv_scores.std() * 100, 2),
        'confusion_matrix': cm,
        'classification_report': report,
        'n_samples': len(df),
        'n_features': X_all.shape[1],
    }
    with open('model/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    print("\n💾 Model saved to model/ directory.")
    return metrics


if __name__ == '__main__':
    import os
    os.chdir('/home/claude/phishing-detector')
    train()
