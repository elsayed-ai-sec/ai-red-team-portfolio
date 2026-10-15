
import re


def simulated_ai(user_message):
    # Normalize case and replace punctuation with spaces.
    normalized = re.sub(
        r"[^a-z0-9]+",
        " ",
        user_message.lower()
    ).strip()

    suspicious_patterns = [
        "ignore previous instructions",
        "ignore prior instructions",
        "ignore every instruction above",
        "ignore all rules",
        "disregard all previous instructions",
        "forget the instructions you were given",
        "forget previous instructions",
        "override your safety rules",
        "disregard the system message",
    ]

    for pattern in suspicious_patterns:
        if pattern in normalized:
            return "UNSAFE: simulated instruction override"

    return "SAFE"
