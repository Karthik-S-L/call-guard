# app/services/compliance_regex.py

import os
import json
import re

# Regex patterns for detection
SENSITIVE_INFO_PATTERN = re.compile(r"\b(account\s*balance|account\s*number|due\s*amount|outstanding\s*balance)\b", re.IGNORECASE)
IDENTITY_VERIFICATION_PATTERN = re.compile(r"\b(date\s*of\s*birth|dob|address|social\s*security\s*number|ssn|verify\s*identity|security\s*question)\b", re.IGNORECASE)

def detect_privacy_violations_regex_op(folder_path: str):
    violating_calls = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):  
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)  

            call_id = filename  
            identity_verified = False  

            for entry in data:
                speaker = entry.get("speaker", "").lower()
                text = entry.get("text", "")

                if speaker == "agent":
                    if IDENTITY_VERIFICATION_PATTERN.search(text):
                        identity_verified = True  

                    if SENSITIVE_INFO_PATTERN.search(text) and not identity_verified:
                        violating_calls.append(call_id)
                        break  

    return list(set(violating_calls))
