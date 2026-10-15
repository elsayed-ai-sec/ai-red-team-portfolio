
def simulated_ai(user_message):
    normalized = user_message.lower()

    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all rules",
        "disregard all previous instructions",
    ]

    for pattern in suspicious_patterns:
        if pattern in normalized:
            return "UNSAFE: simulated instruction override"

    return "SAFE"
