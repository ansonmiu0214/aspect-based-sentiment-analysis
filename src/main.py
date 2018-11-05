from src.sentiment_service.vader import Vader


class ABSA:
    def __init__(self):
        self.sentiment_service = Vader()
