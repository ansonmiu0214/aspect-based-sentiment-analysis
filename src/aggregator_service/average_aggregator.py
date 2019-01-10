from models import AggregatorService


class AverageAggregator(AggregatorService):
    HEADLINE_MULTIPLIER = 2
    CONTENT_MULTIPLIER = 1

    def aggregate_sentiment(self, data):
        '''
        Calculates the weighted average of the given sentiment.

        :param data: [{'sentiment': float, 'is_header': bool}]
        :rtype: float
        '''
        sum = 0

        for row in data:
            sum += row['sentiment'] * (HEADLINE_MULTIPLIER if row['is_header'] else CONTENT_MULTIPLIER)

        return sum / float(len(data))
