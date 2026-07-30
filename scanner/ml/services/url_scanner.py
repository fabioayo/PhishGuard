from urllib.parse import urlparse
from .virustotal import VirusTotalScanner
import re

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

class URLScanner:
    def extract_urls(self,text):
        pattern = r'https?://[^\s]+'
        return re.findall(pattern, text)

    def is_ip_url(self,url):
        pattern = r'https?://(?:\d{1,3}\.){3}\d{1,3}'
        return re.match(pattern, url) is not None

    def normalize_word(self,word):
        for fake, real in LOOKALIKE_CHARS.items():
            word = word.replace(fake, real)

        return word

    def get_substitutions(self,word):
        
        substitutions = []

        for fake, real in LOOKALIKE_CHARS.items():
            if fake in word:
                substitutions.append(f"{fake} → {real}")

        return substitutions

    def check_lookalike_domain(self,url, engine):

        domain = urlparse(url).netloc.lower()
        normalized = self.normalize_word(domain)

        for brand in TRUSTED_BRANDS:

            if brand in normalized and brand not in domain:

                substitutions = self.get_substitutions(domain)

                message = (
                    f"Possible lookalike domain: '{domain}' may be impersonating "
                    f"'{brand}.com'."
                )

                if substitutions:
                    message += (
                        f" Detected substitution(s): {', '.join(substitutions)}."
                    )

                engine.add(25, message)

    def scan(self,urls, engine):
        
        vt= VirusTotalScanner()
        
        for url in urls:

            if any(site in url for site in SHORTENERS):
                engine.add(
                    20,
                    f"Shortened URL detected: {url}"
                )
            domain = urlparse(url).netloc.lower()

            if any(url.endswith(tld) for tld in SUSPICIOUS_DOMAINS):
                engine.add(
                    15,
                    f"Suspicious domain detected: {url}"
                )
            if self.is_ip_url(url):
                engine.add(25,
                        f"URL uses an IP address instead of a domain: {url}"
                        )
            self.check_lookalike_domain(url, engine)
            
            try:
                result = vt.scan_url(url)
                
                if result["malicious"] > 0:
                    engine.add(
                40,
                f"VirusTotal: {result['malicious']} security vendor(s) flagged this URL as malicious."
            )
                elif result["suspicious"] > 0:
                    engine.add(
                25,
                f"VirusTotal: {result['suspicious']} security vendor(s) marked this URL as suspicious."
            )
            except Exception as e:
                print(f"VirusTotal Error: {e}")
                engine.add(
                    0,
            "VirusTotal lookup could not be completed."
        )

scanner=URLScanner()