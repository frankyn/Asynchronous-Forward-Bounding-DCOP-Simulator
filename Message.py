import copy

class Message:
    def __init__(self, type, timestamp, src, destination, payload):
        self._type = copy.deepcopy(type)
        self._timestamp = copy.deepcopy(timestamp)
        self._source = copy.deepcopy(src)
        self._destination = copy.deepcopy(destination)
        self._payload = copy.deepcopy(payload)

    def get_type(self):
        return self._type

    def get_destination(self):
        return self._destination

    def get_source(self):
        return self._source

    def get_timestamp(self):
        return self._timestamp

    def get_payload(self):
        return self._payload

    def __str__(self):
        return "Type: %s, Timestamp: %s, Source: %d, Destination: %d"%(self._type,
                                                                    str(self._timestamp),
                                                                    self._source,
                                                                    self._destination)


