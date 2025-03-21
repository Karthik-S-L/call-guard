import re

# Simple list of profane words (extend as needed)
PROFANITY_WORDS = {"badword1", "badword2", "badword3"}

# Compile regex pattern
PROFANITY_PATTERN = re.compile(r"\b(" + "|".join(PROFANITY_WORDS) + r")\b", re.IGNORECASE)

def detect_profanity_regex(text: str):
    """Detects profane words using regex matching."""
    return PROFANITY_PATTERN.findall(text)