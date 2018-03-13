import csv
from tools.record import Record


class FileCsv(object):
    """deal with csv file

    Attributes:
        file_name : the file's name
        record_set : the file's all row set
        record_set_length : the sum of record_set
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.record_set = []
        self.record_set_length = None

        self._prep()

    def _prep(self):
        """get record_set from file and determine whether there is some abnormalities"""
        with open(self.file_name, encoding='utf-8') as f:
            record = f.readline().strip('\n').split(',')  # read the record_data's attribute
            self.record_set.append(Record(record))
            csv_reader = csv.reader(f)
            for record in csv_reader:
                record_tmp = Record(record)
                # determine whether record_data has negative, not float or black.
                if not record_tmp.check_has_negative() and not record_tmp.check_not_float() \
                        and not record_tmp.check_has_black():
                    self.record_set.append(record_tmp)

            self.record_set_length = len(self.record_set)

    def sort_date(self):
        """sort by time"""
        return sorted(self.record_set[1:], key=lambda x: x.get_date())


if __name__ == '__main__':
    file = FileCsv('d:\\Documents\\PycharmProjects\\test2\\data\\BA.csv')
    print(len(file.record_set))
    date_sort = file.sort_date()
    date_sort = [i.record_data for i in date_sort]
    print(date_sort[:10])
