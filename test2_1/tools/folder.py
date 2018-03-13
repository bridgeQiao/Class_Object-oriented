import os
import csv
from tools.file import File


class Folder(object):
    """get all File to a list

    some operate of File

    Attributes:
        file_path   : folder name
        files       : get all File object
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.files = []
        for f in os.listdir(self.file_path):
            self.files.append(File(''.join([self.file_path, os.sep, f])))

    def file_new(self, file_name):
        self._write_first_row(file_name)

        # write the rest row
        attribute = self.files[0].get_attribute()
        row = attribute.__len__() - 1
        col = self.files.__len__() + 2
        # index save record's column in StrMatrix
        index = [i for i in range(2, col)]

        while self._has_next():
            record_list = []
            # read one date of five files
            for f in self.files:
                f.get_record(record_list)

            date_tmp = self._get_label(record_list)
            if date_tmp is not None:
                # print(date_tmp, end=' ')
                # save records to StrMatrix
                one_date_set = StrMatrix(row, col)
                one_date_set.fill_one_point(0, 0, date_tmp)
                one_date_set.fill_one_col(1, attribute[1:])

                record_list = [i.record_data[1:] for i in record_list]
                one_date_set.fill_cols(index, record_list)
                # write one_date_set ot File
                one_date_set.write_lines(file_name)

    def _write_first_row(self, file_name):
        """write first line attribute"""
        with open(file_name, 'w', encoding='utf-8', newline='') as file_tmp:
            csv_writer = csv.writer(file_tmp, dialect='excel')

            first_row = ['date', 'features']
            for f in self.files:
                first_row.append(
                    f.file_name.split(os.sep)[-1].split('.')[0])
            csv_writer.writerow(first_row)

    def _has_next(self):
        """when all the files have been read, the loop is closed."""
        for f in self.files:
            if not f.has_next():
                return False
        return True

    def _get_label(self, record_list):
        # if The number of rows read into the file is less than
        # the number of files or dates are not equal, date_tmp is None
        if len(record_list) is not len(self.files):
            return
        date_tmp = record_list[0].get_label()
        for record in record_list:
            if record.get_label() != date_tmp:
                date_tmp = None
                return date_tmp
        return date_tmp


class StrMatrix(object):
    """two dimensional string array

    Attributes:
        row     : number of rows
        col     : number of cols
        row_set : data of StrMatrix
    """

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.row_set = []
        self._prep()

    def _prep(self):
        # Generating a two dimensional string array
        for i in range(self.row):
            tmp_list = []
            for j in range(self.col):
                tmp_list.append('')
            self.row_set.append(tmp_list.copy())

    def fill_one_point(self, x, y, value):
        if x not in range(self.row) or y not in range(self.col):
            return

        self.row_set[x][y] = value

    def fill_one_col(self, col_num, str_list):
        if col_num not in range(self.col) \
                or len(str_list) is not self.row:
            return

        for i in range(self.row):
            self.row_set[i][col_num] = str_list[i]

    def fill_cols(self, col_num_list, str_list_list):
        if len(col_num_list) != len(str_list_list):
            return

        for i in range(len(col_num_list)):
            self.fill_one_col(col_num_list[i], str_list_list[i])

    def write_lines(self, file_name):
        with open(file_name, 'a+', encoding='utf-8', newline='') as file_tmp:
            csv_writer = csv.writer(file_tmp, dialect='excel')
            csv_writer.writerows(self.row_set)


if __name__ == '__main__':
    # test the function
    file = Folder('../data')
