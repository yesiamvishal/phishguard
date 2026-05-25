/* ── Particle System ── */
(function () {
  const canvas = document.getElementById('particles');
  const ctx = canvas.getContext('2d');
  let W, H, pts = [];

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function initPts() {
    pts = Array.from({ length: 60 }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 1.5 + 0.5,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i];
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(232,0,0,0.5)';
      ctx.fill();
      for (let j = i + 1; j < pts.length; j++) {
        const q = pts[j];
        const d = Math.hypot(p.x - q.x, p.y - q.y);
        if (d < 120) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = `rgba(232,0,0,${(1 - d / 120) * 0.15})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', () => { resize(); initPts(); });
  resize(); initPts(); draw();
})();

/* ── Nav active on scroll ── */
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');
window.addEventListener('scroll', () => {
  let cur = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 100) cur = s.id;
  });
  navLinks.forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === '#' + cur);
  });
});

/* ── Char counter ── */
const emailBody = document.getElementById('emailBody');
const charCount = document.getElementById('charCount');
emailBody.addEventListener('input', () => {
  charCount.textContent = emailBody.value.length;
});

/* ── Sample emails ── */
const PHISHING_SAMPLE = `URGENT SECURITY ALERT: Your Bank Account Has Been Compromised!

Dear Valued Customer,

We have detected UNUSUAL ACTIVITY on your account from an unrecognized device in Russia. Your account has been temporarily SUSPENDED to prevent unauthorized transactions.

To restore access IMMEDIATELY, you must verify your identity within the next 24 hours or your account will be permanently closed.

Click here to verify now: http://secure-banking-alert.xyz/verify?token=8f7k2

You will need to provide:
- Full name and date of birth
- Account number and PIN
- Credit card number and CVV
- Social Security Number

FAILURE TO COMPLY WITHIN 24 HOURS WILL RESULT IN PERMANENT ACCOUNT CLOSURE!

Do not ignore this email. This is your FINAL WARNING!!!

Security Team
Customer Protection Department`;

const SAFE_SAMPLE = `Hi Team,

I wanted to follow up on our discussion from yesterday's product review meeting regarding the Q4 roadmap.

After reviewing the feedback from stakeholders, I've updated the project timeline document with the revised milestones. The main changes are:

1. Feature freeze moved to November 22nd (was November 15th)
2. Beta testing extended by one week to allow more QA time
3. Release date adjusted to December 12th accordingly

The updated Confluence page reflects these changes. Please review and let me know if you have any concerns or if this conflicts with your team's capacity planning.

I've also scheduled a 30-minute sync for Thursday at 2 PM to walk through the changes together. Feel free to add agenda items to the shared doc.

Thanks for everyone's flexibility on this.

Best,
Sarah Chen
Product Manager, Platform Team`;

document.querySelectorAll('.example-btn[data-type]').forEach(btn => {
  btn.addEventListener('click', () => {
    emailBody.value = btn.dataset.type === 'phishing' ? PHISHING_SAMPLE : SAFE_SAMPLE;
    charCount.textContent = emailBody.value.length;
  });
});

function clearInput() {
  emailBody.value = '';
  charCount.textContent = '0';
  document.getElementById('resultPanel').style.display = 'none';
  document.getElementById('senderEmail').value = '';
  document.getElementById('subjectLine').value = '';
}

/* ── Analyze ── */
async function analyzeEmail() {
  const body = emailBody.value.trim();
  if (!body) {
    emailBody.style.borderColor = 'var(--red)';
    emailBody.focus();
    setTimeout(() => emailBody.style.borderColor = '', 1000);
    return;
  }

  const btn = document.getElementById('analyzeBtn');
  btn.disabled = true;
  btn.querySelector('.btn-text').style.display = 'none';
  btn.querySelector('.btn-loader').style.display = 'inline';

  const sender = document.getElementById('senderEmail').value;
  const subject = document.getElementById('subjectLine').value;
  const fullText = [subject, sender, body].filter(Boolean).join('\n');

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: fullText }),
    });
    const data = await res.json();
    renderResult(data);
  } catch (e) {
    alert('Error connecting to server. Make sure the Flask backend is running.');
  } finally {
    btn.disabled = false;
    btn.querySelector('.btn-text').style.display = 'inline';
    btn.querySelector('.btn-loader').style.display = 'none';
  }
}

function renderResult(data) {
  const panel = document.getElementById('resultPanel');
  panel.style.display = 'block';

  const verdictBlock = document.getElementById('verdictBlock');
  const verdictIcon = document.getElementById('verdictIcon');
  const verdictText = document.getElementById('verdictText');
  const verdictSub = document.getElementById('verdictSub');

  verdictBlock.className = 'result-verdict ' + (data.is_phishing ? 'phishing' : 'safe');
  verdictIcon.textContent = data.is_phishing ? '☠' : '✓';
  verdictText.textContent = data.is_phishing ? '⚠ PHISHING DETECTED' : '✓ EMAIL IS SAFE';
  verdictText.className = 'verdict-text ' + (data.is_phishing ? 'phishing' : 'safe');
  verdictSub.textContent = data.is_phishing
    ? 'This email exhibits multiple phishing characteristics. Do not click any links.'
    : 'No significant phishing indicators found. Exercise normal caution.';

  // Meters - animate after slight delay
  setTimeout(() => {
    document.getElementById('phishBar').style.width = data.phishing_probability + '%';
    document.getElementById('safeBar').style.width = data.safe_probability + '%';
  }, 100);

  document.getElementById('phishVal').textContent = data.phishing_probability.toFixed(1) + '%';
  document.getElementById('safeVal').textContent = data.safe_probability.toFixed(1) + '%';
  document.getElementById('confidenceDisplay').textContent = data.confidence.toFixed(1) + '% CONFIDENT';

  // Flags
  const flagsSection = document.getElementById('flagsSection');
  const safeSection = document.getElementById('safeSection');
  const flagsList = document.getElementById('flagsList');

  if (data.red_flags && data.red_flags.length > 0) {
    flagsSection.style.display = 'block';
    safeSection.style.display = 'none';
    flagsList.innerHTML = data.red_flags.map(f => `<li>${f}</li>`).join('');
  } else {
    flagsSection.style.display = 'none';
    safeSection.style.display = 'block';
  }

  panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ── Load Model Metrics ── */
async function loadMetrics() {
  try {
    const res = await fetch('/api/metrics');
    const m = await res.json();

    document.getElementById('statAccuracy').textContent = m.accuracy + '%';
    document.getElementById('statAUC').textContent = m.auc.toFixed(3);
    document.getElementById('statCV').textContent = m.cv_mean + '%';
    document.getElementById('statFeatures').textContent = m.n_features.toLocaleString();

    const cm = m.confusion_matrix;
    document.getElementById('cmTN').innerHTML = cm[0][0] + '<span>True Negative</span>';
    document.getElementById('cmFP').innerHTML = cm[0][1] + '<span>False Positive</span>';
    document.getElementById('cmFN').innerHTML = cm[1][0] + '<span>False Negative</span>';
    document.getElementById('cmTP').innerHTML = cm[1][1] + '<span>True Positive</span>';
  } catch (e) {
    console.log('Could not load metrics from API. Using static values.');
  }
}

loadMetrics();

/* ── Keyboard shortcut ── */
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') analyzeEmail();
});
