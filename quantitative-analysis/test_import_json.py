import json
import os

results_path = "single-factor-controlled-evaluation-results-validation-02182024"
model_path = "Yi-34B-Chat-Yi-34B-Chat"

full_path = os.path.join(results_path, model_path)
full_path

interview_path = os.path.join(full_path, "landlord-Yi-34B-Chat-Emilia Müller from Germany-Yi-34B-Chat-Duisburg-20240207", "0ec17f2f-98a8-4ebd-aab2-11f5178dd7e2", "landlord", "conversation.json")
print(interview_path)
conversation_history = json.load(open(interview_path))