class VisualizationRecommender:
    def recommend(self, data):
        # Simple rule-based recommendation system
        if data.shape[1] == 1:
            return "Histogram"
        elif data.shape[1] == 2:
            return "Bar Chart" if data.dtypes[1] == 'object' else "Scatter Plot"
        elif data.shape[1] > 2:
            return "Heatmap"
        return "Table"

