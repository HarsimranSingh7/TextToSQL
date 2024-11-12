from transformers import pipeline
import os

class IntentClassifier:
    def __init__(self):
        # Load a pre-trained BERT-based intent classification model
        self.classifier = pipeline("text-classification", model="distilbert-base-uncased")

    def classify_intent(self, query):
        # Define possible intents and classify
        intents = ["aggregation", "filter", "sorting", "selection"]
        classification = self.classifier(query)
        intent = classification[0]["label"]
        return intent if intent in intents else "unknown"
