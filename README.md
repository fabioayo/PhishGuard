# 🛡️ PhishGuard — AI Phishing Detector

PhishGuard is a full-stack phishing detection application built with **Python, Django, Django REST Framework, React, and Scikit-learn**.

It analyzes emails, URLs, and messages using machine learning, rule-based security checks, and VirusTotal URL analysis.

## ✨ Features

- Email, URL, and message analysis
- Machine-learning phishing detection
- Rule-based threat detection
- VirusTotal URL reputation checks
- Risk level and risk score
- Prediction confidence
- Explainable detection reasons
- Responsive React interface
- Scan history using browser `localStorage`
- Clear scan history

## 🧰 Tech Stack

**Backend**
- Python
- Django
- Django REST Framework
- Scikit-learn
- Pandas
- Joblib

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Security**
- VirusTotal API
- Rule-based phishing analysis

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/fabioayo/ai-phishing-detector.git
cd ai-phishing-detector
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your VirusTotal API key:

```env
VT_API_KEY=your_api_key_here
```

Run Django:

```bash
python manage.py migrate
python manage.py runserver
```

Open a **second terminal**, then start React:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite address shown in the terminal, usually:

```text
http://localhost:5173/
```

> Keep both Django and React running during development.

## 🔌 API Endpoint

```http
POST /api/analyze/
```

Example request:

```json
{
  "text": "Urgent! Verify your account immediately."
}
```

## 📁 Project Structure

```text
ai-phishing-detector/
├── core/
├── scanner/
│   ├── ml/
│   ├── api.py
│   └── serializers.py
├── frontend/
│   └── src/
├── manage.py
├── requirements.txt
└── README.md
```

## 🔐 Security Note

Do not upload your `.env` file or VirusTotal API key to GitHub. PhishGuard provides automated security assessments and should support—not replace—careful security judgment.

## 🔮 Future Improvements

- WHOIS and SSL checks
- Domain-age analysis
- User authentication
- Database-backed scan history
- Automated testing
- Production deployment

## 👨‍💻 Author

**fabioayo77**