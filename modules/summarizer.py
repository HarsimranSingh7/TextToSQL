from transformers import pipeline

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, data):
        # Generate a simple summary; adjust for your data context
        text = data.to_string()
        summary = self.summarizer(text, max_length=50, min_length=20, do_sample=False)
        return summary[0]["summary_text"]
