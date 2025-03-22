# app/services/call_quality.py

import os
import json
from typing import Dict, List

def calculate_overtalk_and_silence(folder_path: str) -> Dict[str, Dict[str, float]]:
    results = {}
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            
            call_id = filename
            total_duration = 0
            overtalk_duration = 0
            silence_duration = 0
            
            for i in range(len(data) - 1):
                curr_speaker = data[i]["speaker"].lower()
                next_speaker = data[i + 1]["speaker"].lower()
                curr_end = data[i]["etime"]
                next_start = data[i + 1]["stime"]
                
                total_duration = max(total_duration, data[i]["etime"])
                
                # Overtalk: If two speakers overlap
                if curr_speaker != next_speaker and next_start < curr_end:
                    overtalk_duration += curr_end - next_start
                
                # Silence: If gap exists between two speakers
                elif next_start > curr_end:
                    silence_duration += next_start - curr_end
            
            if total_duration > 0:
                overtalk_percentage = (overtalk_duration / total_duration) * 100
                silence_percentage = (silence_duration / total_duration) * 100
            else:
                overtalk_percentage = silence_percentage = 0
            
            results[call_id] = {
                "overtalk_percentage": round(overtalk_percentage, 2),
                "silence_percentage": round(silence_percentage, 2)
            }
    
    return results
