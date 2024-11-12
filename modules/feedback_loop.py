import json

class FeedbackLoop:
    def __init__(self, feedback_file="feedback.json"):
        self.feedback_file = feedback_file

    def record_feedback(self, original_query, generated_sql, is_correct, correction=None):
        feedback_entry = {
            "original_query": original_query,
            "generated_sql": generated_sql,
            "is_correct": is_correct,
            "correction": correction
        }
        with open(self.feedback_file, "a") as f:
            json.dump(feedback_entry, f)
            f.write("\n")
    
    def get_feedback_data(self):
        feedback_data = []
        with open(self.feedback_file, "r") as f:
            for line in f:
                feedback_data.append(json.loads(line))
        return feedback_data
