# app/services/compliance_regex.py

import os
import json
import re
from typing import List, Tuple

# Regex patterns for detection
SENSITIVE_INFO_PATTERN = re.compile(r"\b(account\s*balance|account\s*number|due\s*amount|outstanding\s*balance)\b", re.IGNORECASE)
IDENTITY_VERIFICATION_PATTERN = re.compile(r"\b(date\s*of\s*birth|dob|address|social\s*security\s*number|ssn|verify\s*identity|security\s*question)\b", re.IGNORECASE)

def detect_privacy_violations_regex_op(folder_path: str) -> Tuple[int, List[str]]:
    """
    Detects privacy violations in call transcripts using regex-based pattern matching.

    A privacy violation occurs if an agent shares sensitive account details without verifying
    the borrower's identity. This function scans multiple JSON files in the provided folder.

    Parameters:
    -----------
    folder_path : str
        The path to the folder containing conversation JSON files.

    Returns:
    --------
    Tuple[int, List[str]]
        - HTTP status code (200 for success, 500 for failure).
        - List of call IDs that contain privacy violations.
    """
    violating_calls = []

    try:
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder '{folder_path}' not found.")

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        data = json.load(file)
                except json.JSONDecodeError:
                    print(f"Warning: Skipping {filename} due to JSON decoding error.")
                    continue  

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

        return 200, list(set(violating_calls))  # Return success status

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        return 500, []  # Return failure status with an empty list