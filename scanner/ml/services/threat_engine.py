class ThreatEngine:
    def __init__(self):
        self.score = 0
        self.reasons = []

    def add(self, points, reason):
        self.score += points
        self.reasons.append(reason)

    def get_risk(self):
        if self.score >= 80:
            return "HIGH"
        elif self.score >= 50:
            return "MEDIUM"
        elif self.score >= 20:
            return "LOW"
        return "SAFE"

    def build_result(self, ml_prediction=None, ml_confidence=None):
        return {
        "result": ml_prediction,
        "score": min(self.score, 100),
        "risk": self.get_risk(),
        "confidence": ml_confidence,
        "reasons": self.reasons,
    }