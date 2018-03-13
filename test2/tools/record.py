import re


class Record(object):
    """record_data one line of the TXT data

    Include a label and concrete data

    Attributes:
        record : one line of the file
        length : one record_data's length
    """

    def __init__(self, record_data):
        self.record_data = record_data
        self.length = len(record_data)

    def check_not_match(self, dim):
        """determine whether the record_data's column numbers is right"""
        if dim != self.length:
            return True
        else:
            return False

    def check_has_not_number(self, label_num):
        """determine whether the record_data has data anomalies"""
        record = self.record_data
        record.pop(label_num)

        if len(re.findall(r'[a-zA-Z]', ''.join(record))) is not 0:
            return True
        else:
            return False

    def check_has_negative(self):
        """check negative"""
        if len(re.findall(r'-', ''.join(self.record_data[1:6]))) is not 0:
            return True
        else:
            return False

    def check_not_float(self):
        """check float"""
        if len(re.findall(r'\.', ''.join(self.record_data[1:6]))) is not 5:
            return True
        else:
            return False

    def check_has_black(self):
        """check black string"""
        if '' in self.record_data[1:6]:
            return True
        else:
            return False

    def get_date(self):
        """format date to xxxx/xx/xx"""
        date_list = re.findall(r'\d+', self.record_data[0])
        if len(date_list[-1]) is 1:
            date_list[-1] = ''.join(['0', date_list[-1]])
        if len(date_list[-2]) is 1:
            date_list[-2] = ''.join(['0', date_list[-2]])
        return '/'.join(date_list)


if __name__ == '__main__':
    record = Record(['1962/1/2'])
    print(record.get_date())
