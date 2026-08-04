import re

FREE_PROVIDERS = ["gmail.com","yahoo.com","hotmail.com","outlook.com","icloud.com"]
  
TRUSTED_BRANDS = ["paypal","amazon","microsoft","apple","google","facebook",
"netflix","linkedin","twitter","dropbox","instagram","ebay","wellsfargo"]

EXTRACT_EMAIL_SCORE =20
EMAIL_SCANNER_SCORE = 10

class EmailScanner:
    def extract_emails(self,text):
        """
        Extract email addresses from the email text.
        """
        pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
        return re.findall(pattern, text)

    def check_email_addresses(self,emails, engine):
        """
        Analyze extracted email addresses.
        """
        for email in emails:

            email_lower = email.lower()

            # Company name + free email provider
            if any(company in email_lower for company in TRUSTED_BRANDS):
                if any(provider in email_lower for provider in FREE_PROVIDERS):

                    engine.add(
                        EXTRACT_EMAIL_SCORE,
                        f"Possible impersonation email: {email}"
                    )
    def scan(self, text, engine):
        emails = self.extract_emails(text)
        if emails:
            engine.add(
                EMAIL_SCANNER_SCORE, f"Found {len(emails)} email address(es)."
        )

        self.check_email_addresses(emails, engine)
                    