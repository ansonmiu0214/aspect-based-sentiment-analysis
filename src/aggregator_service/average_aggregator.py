from models import AggregatorService


class AverageAggregator(AggregatorService):
    def aggregate_sentiment(self, data):
        sum = 0
        HEADLINE_MULTIPLIER = 2
        CONTENT_MULTIPLIER = 1

        for row in data:
            sum += row['sentiment'] * (HEADLINE_MULTIPLIER if row['is_header'] else CONTENT_MULTIPLIER)

        return sum / float(len(data))
