import pandas as pd
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)

    def fit(self, data):
        # Assuming numeric columns only for simplicity
        numeric_data = data.select_dtypes(include=['float64', 'int64'])
        self.model.fit(numeric_data)

    def detect_anomalies(self, data):
        numeric_data = data.select_dtypes(include=['float64', 'int64'])
        anomalies = self.model.predict(numeric_data)
        data['anomaly'] = anomalies
        return data[data['anomaly'] == -1]  # Return rows flagged as anomalies
