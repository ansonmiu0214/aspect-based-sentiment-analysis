from src.models import AggregatorService


class AverageAggregator(AggregatorService):
    def aggregate_sentiment(self, sentiments):
        return sum(sentiments) / float(len(sentiments))
