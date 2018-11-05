import abc


class ExtractorService(abc.ABC):
    @abc.abstractmethod
    def extract(self, doc):
        '''

        :param doc:
        :return: (Document, [{ 'entity': String, 'attributes': [{ 'attribute': String, 'expression': String }]] }])
        '''
        pass
