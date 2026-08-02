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
        pattern =  (
            r'(?i)'
            r'(?:https?://)?'
            r'(?:www\.)?'
            r'(?:[a-z0-9-]+\.)+'
            r'[a-z]{2,}'
            r'(?::\d+)?'
            r'(?:/[^\s<>"\']*)?'
        )
        
        matches=re.findall(pattern,text)
        
        return [
            self.prepare_url(url)
            for url in matches
            if url
        ]
    
    def prepare_url(self, url):

        url = url.strip()

        # Remove punctuation that may appear after a URL in a sentence.
        url = url.rstrip(".,!?;:)]}>\"'")

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url

    def get_domain(self, url):
        try:
            url = url.strip()
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
                
            parsed = urlparse(url)
            
            domain = parsed.hostname
            
            if domain:
                return domain.lower()
            
            return None
        
        except ValueError as error:
            print(f"URL parsing error: {url} -> {error}")

        return None   

    def is_ip_url(self,url):
        domain = self.get_domain(url)
        if not domain: 
            return False
        
        pattern = r'https?://(?:\d{1,3}\.){3}\d{1,3}'
        return re.fullmatch(pattern, domain) is not None

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

        domain = self.get_domain(url)

        if not domain:
            engine.add(
                20,
                f"Malformed or invalid URL detected: {url}"
            )
            return

        normalized = self.normalize_word(domain)

        for brand in TRUSTED_BRANDS:

            if brand in normalized and brand not in domain:

                substitutions = self.get_substitutions(domain)

                message = (
                    f"Possible lookalike domain: '{domain}' may be "
                    f"impersonating '{brand}.com'."
                )

                if substitutions:

                    message += (
                        f" Detected substitution(s): "
                        f"{', '.join(substitutions)}."
                    )

                engine.add(25, message)

    def scan(self,urls, engine):
        
        vt= VirusTotalScanner()
        
        for url in urls:
            
            url=self.prepare_url(url)
            
            domain=self.get_domain(url)
            if not domain:
                engine.add(
                    20,
                    f"Malformed or invalid URL detected: {url}"
                )
                continue
            
            if any(
                domain==shortener 
                or domain.endswith(f".{shortener}")
                for shortener in SHORTENERS
            ):
                engine.add(
                    20,
                    f"Shortened URL detected: {url}"
                )

            # if any(site in url for site in SHORTENERS):
            #     engine.add(
            #         20,
            #         f"Shortened URL detected: {url}"
            #     )
            # domain = urlparse(url).netloc.lower()

            if any(domain.endswith(tld) for tld in SUSPICIOUS_DOMAINS):
                engine.add(
                    15,
                    f"Suspicious domain detected: {domain}"
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