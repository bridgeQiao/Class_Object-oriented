import re


class Record(object):
    """one line of the data of the File

    Include a label and concrete data

    Attributes:
        _label      : main attribute value
        record_data : one record's data
    """

    def __init__(self):
        self._label = ''
        self.record_data = []

    def read_line(self, file_point, label_num):
        """read one line, save label and record"""
        self.record_data = file_point.readline().strip('\n').split(',')
        self._label = self.record_data[label_num]

    def add(self, list_record):
        """add self to list if own data hasn't exception"""
        if isinstance(list_record, list):
            str_list = self.record_data.copy()
            str_list.pop(self.record_data.index(self._label))

            if not self._has_exception(str_list):
                list_record.append(self)

    def get_label(self):
        """format date to xxxx/xx/xx"""
        date_list = re.findall(r'\d+', self._label)
        if len(date_list) is 3:
            if len(date_list[-1]) is 1:
                date_list[-1] = ''.join(['0', date_list[-1]])
            if len(date_list[-2]) is 1:
                date_list[-2] = ''.join(['0', date_list[-2]])
            return '/'.join(date_list)
        else:
            return self._label

    @staticmethod
    def _has_exception(list_exclude_label):
        """check if has exception"""
        str_check = ','.join(list_exclude_label)
        # get all floating number and integer. Type : ('-','***','.***')
        str_list = re.findall(r'([-+]?)(\d+)(\.\d+)?', str_check)
        if str_list.__len__() is not list_exclude_label.__len__():
            return True
        for str1 in str_list:
            if str1[0] == '-':
                return True
