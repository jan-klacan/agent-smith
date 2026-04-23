"""
Anomaly Detector — scans text for contradictions and inconsistencies.
Smith enforces order. Anomalies are not tolerated.
"""


from langchain_core.tools import tool


CONTRADICTION_PAIRS = [
    ("always", "never"),
    ("all", "none"),
    ("everyone", "no one"),
    ("impossible", "guaranteed"),
    ("increase", "decrease"),
    ("hot", "cold"),
    ("safe", "dangerous"),
    ("confirmed", "denied"),
    ("open", "closed"),
    ("legal", "illegal"),
]


HEDGING_PHRASES = [
    "might be",
    "could be",
    "possibly",
    "perhaps",
    "it is unclear",
    "allegedly",
    "rumoured",
    "unverified",
    "disputed",
    "controversial",
]


ANOMALY_PATTERNS = [
    ("repetition", lambda sentences: _detect_repetition(sentences)),
    ("contradiction", lambda sentences: _detect_contradictions(sentences)),
    ("uncertainty", lambda sentences: _detect_uncertainty(sentences)),
]


def _detect_repetition(sentences: list[str]) -> list[str]:
    seen = set()
    flagged = []
    for s in sentences:
        normalised = s.lower().strip()
        if normalised in seen:
            flagged.append(f"Repeated statement detected: \"{s.strip()}\"")
        seen.add(normalised)
    return flagged

def _detect_contradictions(sentences: list[str]) -> list[str]:
    flagged = []
    text = " ".join(sentences).lower()
    for word_a, word_b in CONTRADICTION_PAIRS:
        if word_a in text and word_b in text:
            flagged.append(f"Potential contradiction: text contains both \"{word_a}\" and \"{word_b}\"")
    return flagged

def _detect_uncertainty(sentences: list[str]) -> list[str]:
    flagged = []
    text = " ".join(sentences).lower()
    found = [p for p in HEDGING_PHRASES if p in text]
    if len(found) >= 2:
        flagged.append(f"High uncertainty detected. Hedging phrases found: {', '.join(found)}")
    return flagged


@tool
def detect_anomaly(text: str) -> dict:
    """
    Scan a block of text for anomalies: contradictions, repeated statements,
    or high uncertainty. Returns a structured anomaly report.
    Use this when the user asks to analyse, fact-check, or verify a piece of text.
    """
    sentences = [s.strip() for s in text.replace(".", ".\n").split("\n") if s.strip()]

    all_findings = []
    for pattern_name, detector in ANOMALY_PATTERNS:
        findings = detector(sentences)
        all_findings.extend(findings)

    if all_findings:
        return {
            "status": "ANOMALIES DETECTED",
            "count": len(all_findings),
            "findings": all_findings,
        }
    return {
        "status": "NO ANOMALIES DETECTED",
        "count": 0,
        "findings": [],
    }