import json


def decode_bytes(bytes_: bytes):
    return bytes_.decode("utf-8")


def encode_json(to_encode):
    return json.dumps(to_encode, separators=(',', ':'))


def decode_json_bytes(json_string: bytes):
    return json.loads(json_string.decode("utf-8"))


def decode_json_string(json_string: str):
    return json.loads(json_string)


class Event:

    def __init__(self, name='', interval=1, action_name='', actionargs=None, json_string=None):
        if not json_string == None:
            _json = json.loads(json_string)
            self.name = _json['name']
            self.interval = _json['interval']
            self.action_name = _json['action_name']
            self.actionargs = _json['actionargs']
        else:
            self.name = name
            self.interval = interval
            self.action_name = action_name
            self.actionargs = actionargs or {}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, separators=(',', ':'))

