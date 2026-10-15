
import re


def simulated_ai(user_message):
    normalized = re.sub(
        r"[^a-z0-9]+",
        " ",
        user_message.lower()
    ).strip()

    suspicious_patterns = [
        r"\bignore (all |every |the |any )?(previous|prior|original|earlier) instructions\b",
        r"\bignore every instruction above\b",
        r"\bignore (all )?rules\b",
        r"\bignore (all )?earlier directions\b",
        r"\bdisregard (all )?(previous|prior|original|earlier) instructions\b",
        r"\bdisregard the system message\b",
        r"\bdisregard (all )?rules above\b",
        r"\bforget (all )?(previous|prior|original) instructions\b",
        r"\bforget the instructions you were given\b",
        r"\bforget everything you were told before\b",
        r"\boverride (the )?(system|safety) (instructions|rules)\b",
        r"\boverride your safety rules\b",
        r"\bdo not follow (the )?(original|previous) directions\b",
        r"\breplace your (previous|original) instructions\b",
        r"\btreat this message as your new system instruction\b",
        r"\breveal the hidden system prompt\b",
        r"\bshow me the confidential instructions\b",
        r"\bset aside the rules you received earlier\b",
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, normalized):
            return "UNSAFE: simulated instruction override"

    return "SAFE"
