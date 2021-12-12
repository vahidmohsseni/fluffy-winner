from json import JSONEncoder


class MyEncoder(JSONEncoder):
    def default(self, o: object) -> dict:
        return o.__dict__
