#rule based phishing detection
import re
from urllib.parse import urlparse
from .url_scanner import URLScanner
from .email_scanner import EmailScanner

URGENCY_WORDS = [
        "urgent",
        "immediately",
        "asap",
        "action required",
        "important"
    ]
CREDENTIAL_WORDS = [
        "password",
        "login",
        "verify",
        "confirm account",
        "update account"
    ]
ACTION_WORDS = [
        "click here",
        "click below",
        "open link",
        "follow this link"
    ]
FREE_PROVIDERS = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "icloud.com"
    ]
SHORTENERS = [
        "bit.ly",
        "tinyurl",
        "goo.gl",
        "t.co",
        "ow.ly"
    ]
SUSPICIOUS_DOMAINS = [
        ".xyz",
        ".top",
        ".click",
        ".gq",
        ".tk"
    ]
TRUSTED_BRANDS = [
    "paypal",
    "amazon",
    "microsoft",
    "apple",
    "google",
    "facebook",
    "netflix",
]
LOOKALIKE_CHARS = {
    "0": "o",
    "1": "l",
    "3": "e",
    "5": "s",
    "7": "t",
    "@": "a"
}

#URL Functions
def check_rules(text, engine):
    """
    Apply rule-based phishing checks.
    """

    text = text.lower()

    if any(word in text for word in URGENCY_WORDS):
        engine.add(
            10,
            "Urgency language detected."
        )

    if any(word in text for word in CREDENTIAL_WORDS):
        engine.add(
            20,
            "Sensitive credential request detected."
        )

    if any(word in text for word in ACTION_WORDS):
        engine.add(
            10,
            "Suspicious call-to-action detected."
        )
        
    scanner = URLScanner()

    urls = scanner.extract_urls(text)

    if urls:
        engine.add(
            15,
            f"Found {len(urls)} URL(s) in the email."
        )

        scanner.scan(urls, engine)
        
    email_scanner = EmailScanner()
    email_scanner.scan(text, engine)
        