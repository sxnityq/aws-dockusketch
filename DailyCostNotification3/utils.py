from datetime import datetime
from json import JSONEncoder


class MyJsonEncoder(JSONEncoder):
    
    def default(self, o) -> str:
        if isinstance(o, datetime):
            return str(o)
        return super().default(o)