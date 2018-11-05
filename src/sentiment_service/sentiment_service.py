import abc


class SentimentService(abc.ABC):
    @abc.abstractmethod
    def compute_sentiment(self, text):
        '''

        :param text:
        :return:
        '''
        pass
