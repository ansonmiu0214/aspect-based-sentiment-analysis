from models import QueryParser, Query


class SimpleParser(QueryParser):
    '''
    Basic query parser, assumes space-separated parameters in the order of <entity> <attribute?> ...
    '''

    def parse_query(self, text):
        entity, *rest = text.strip().split()
        attribute = rest[0] if rest else None
        return Query(entity, attribute, None)
