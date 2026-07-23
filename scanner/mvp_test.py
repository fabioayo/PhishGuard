import re

SUSPICIOUS_KEYWORDS = [
    "urgent",
    "immediately",
    "verify your account",
    "confirm your identity",
    "password",
    "login",
    "click here",
    "account suspended",
    "security alert",
    "bank",
    "limited time",
    "update your information",
    "unusual activity",
    "payment failed",
    "invoice",
    "free gift",
    "claim your prize",
    "reset your password",
    "act now",
    "confidential"
]

SUSPICIOUS_DOMAINS = [
    "bit.ly",
    "tinyurl",
    "grabify",
]

def detect_phishing(text):
    text_lower = text.lower()

    score = 0
    reasons = []

    # 1. Keyword check
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in text_lower:
            score += 1
            reasons.append(f"Suspicious keyword detected: '{keyword}'")

    # 2. URL extraction
    urls = re.findall(r"https?://[^\s]+", text_lower)

    for url in urls:
        for domain in SUSPICIOUS_DOMAINS:
            if domain in url:
                score += 2
                reasons.append(f"Suspicious shortener/known risky domain: {domain}")

        if "@" in url or "-" in url:
            score += 1
            reasons.append(f"Unusual URL structure: {url}")

    # 3. Urgency patterns
    if "24 hours" in text_lower or "today only" in text_lower:
        score += 1
        reasons.append("Urgency-based social engineering detected")

    # 4. Decision logic
    
    if score >= 5:
        result = "HIGH RISK (Phishing likely)"
    elif score >= 3:
        result = "MEDIUM RISK (Suspicious)"
    else:
        result = "LOW RISK (Likely safe)"

    return {
        "result": result,
        "score": score,
        "reasons": reasons,
        "urls_found": urls
    }
    
# Example of phishing email text for testing
      
# Subject: URGENT: Your Bank Account Will Be Suspended in 24 Hours!

# Dear Customer,

# We have detected unusual activity on your account. Failure to verify your account immediately will result in permanent suspension.

# Click the link below to verify your account:

# http://secure-bank-login-verify-account.xyz

# Please provide:

# * Username
# * Password
# * Debit Card Number
# * PIN

# This action must be completed within 24 hours to avoid account closure.

# Thank you,

# Security Verification Team
# Global Bank Support
