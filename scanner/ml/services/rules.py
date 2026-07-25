#rule based phishing detection
import re
from urllib.parse import urlparse

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
def extract_urls(text):
    """
    Extract all URLs from the email text.
    """
    pattern = r'https?://[^\s]+'
    return re.findall(pattern, text)

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
    
    urls = extract_urls(text)
    if urls:
        engine.add(
            15,
            f"Found {len(urls)} URL(s) in the email."
        )
        
        check_urls(urls, engine)
        
    emails = extract_emails(text)
    if emails:
        engine.add(
            10,
            f"Found {len(emails)} email address(es)."
            )
        check_email_addresses(emails, engine)
        
def extract_emails(text):
    """
    Extract email addresses from the email text.
    """
    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    return re.findall(pattern, text)

def check_email_addresses(emails, engine):
    """
    Analyze extracted email addresses.
    """
    for email in emails:

        email_lower = email.lower()

        # Company name + free email provider
        if any(company in email_lower for company in TRUSTED_BRANDS):
            if any(provider in email_lower for provider in FREE_PROVIDERS):

                engine.add(
                    20,
                    f"Possible impersonation email: {email}"
                )

def check_urls(urls, engine):
    """
    Check extracted URLs for suspicious characteristics.
    """
    
    for url in urls:

        # URL shortener
        if any(site in url for site in SHORTENERS):
            engine.add(
                20,
                f"Shortened URL detected: {url}"
            )

        # Suspicious TLD
        if any(url.endswith(tld) for tld in SUSPICIOUS_DOMAINS):
            engine.add(
                15,
                f"Suspicious domain detected: {url}"
            )
        if is_ip_url(url):
            engine.add(25,
                       f"URL uses an IP address instead of a domain: {url}"
                       )
        check_lookalike_domain(url, engine)

def is_ip_url(url):
    """
    Check whether a URL uses an IP address instead of a domain.
    """
    pattern = r'https?://(?:\d{1,3}\.){3}\d{1,3}'
    return re.match(pattern, url) is not None

def normalize_word(word):
    """
    Replace common lookalike characters.
    """

    for fake, real in LOOKALIKE_CHARS.items():
        word = word.replace(fake, real)

    return word

def get_substitutions(word):
    """
    Return the character substitutions found in a word.

    Example:
        paypa1.com -> ["1 → l"]
        micr0soft.com -> ["0 → o"]
    """

    substitutions = []

    for fake, real in LOOKALIKE_CHARS.items():
        if fake in word:
            substitutions.append(f"{fake} → {real}")

    return substitutions

def check_lookalike_domain(url, engine):
    """
    Detect domains that imitate trusted brands.
    """

    domain = urlparse(url).netloc.lower()
    normalized = normalize_word(domain)

    for brand in TRUSTED_BRANDS:

        if brand in normalized and brand not in domain:

            substitutions = get_substitutions(domain)

            message = (
                f"Possible lookalike domain: '{domain}' may be impersonating "
                f"'{brand}.com'."
            )

            if substitutions:
                message += (
                    f" Detected substitution(s): {', '.join(substitutions)}."
                )

            engine.add(25, message)