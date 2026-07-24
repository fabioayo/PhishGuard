# ai-phishing-detector

# 🛡️ AI Phishing Detector

An AI-powered phishing detection system built with **Python**, **Django**, and **Scikit-learn**. The application analyzes emails and URLs using machine learning and rule-based techniques to identify phishing attempts and explain why they were flagged.

## Features

* Email phishing detection
* URL phishing detection
* Machine Learning (Scikit-learn + TF-IDF)
* Rule-based phishing analysis
* Confidence score
* Explainable detection results
* Web interface built with Django

## Tech Stack

* Python
* Django
* Scikit-learn
* Pandas
* Joblib
* HTML/CSS
* Bootstrap

## Project Structure

```text
ai-phishing-detector/
│── core/
│── scanner/
│   ├── AL/
│   ├── templates/
│   ├── views.py
│   └── urls.py
│── manage.py
│── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/fabioayo/ai-phishing-detector.git
```

Navigate into the project:

```bash
cd ai-phishing-detector
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it (Windows):

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python manage.py migrate
python manage.py runserver
```

## Current Features

* Machine learning email classifier
* Machine learning URL classifier
* Rule-based phishing detection
* Confidence scoring
* Web-based scanning interface

## Planned Improvements

* React frontend
* Django REST API
* VirusTotal integration
* WHOIS & SSL checks
* Domain age analysis
* User authentication
* Scan history
* Threat intelligence dashboard

## Screenshots

*Screenshots will be added in future updates.*

## Author

**fabioayo77**


