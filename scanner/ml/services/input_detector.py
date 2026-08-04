import re

class InputDetector:

    URL_PATTERN = r"https?://[^\s]+"

    EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    def detect(self, text):

        text = text.strip()

        # Entire input is a URL
        url_pattern = (
            r"^(?:https?://)?"
            r"(?:www\.)?"
            r"(?:[a-zA-Z0-9-]+\.)+"
            r"[a-zA-Z]{2,}"
            r"(?::\d+)?"
            r"(?:/[^\s]*)?$"
            )
        if re.match(url_pattern, text.strip(), re.IGNORECASE):
            return "url"

        # Looks like an email message
        if (
            re.search(self.EMAIL_PATTERN, text)
            or "subject:" in text.lower()
            or "from:" in text.lower()
        ):
            return "email"

        # Default
        return "sms"