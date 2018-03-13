class Record(object):
    """record one line of the TXT data

    Include a label and concrete data

    Attributes:
        record : one line of the file
        length : one record's length
    """

    def __init__(self, record):
        self.record = record
        self.length = len(record)
