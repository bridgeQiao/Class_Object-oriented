import re
import os
from scipy.stats import mode
from tools.record import Record


class FileTxt(object):
    """process txt file

    Attributes:
        file_name : file name
        label_num : the label's position of one record_data
        data : all record_data of txt file
        index : all the index of data
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.label_num = None
        self.data = []
        self.index = []

        self.get_label_num()
        self.get_data()

    def get_label_num(self):
        """find the label_num from the file's name"""
        self.label_num = re.findall(r'labelAt(\d+)\D', self.file_name.split(os.sep)[-1])
        if len(self.label_num) is 0:  # if file's name has not 'labelAt'
            self.label_num = 0
        else:
            self.label_num = int(self.label_num[0])

    def get_data(self):
        """save record_data to data"""
        with open(self.file_name) as txt_tmp:
            f = txt_tmp.readlines()
            for one_line_data in f:
                one_line_data = one_line_data.split()
                if len(one_line_data) is 1:
                    one_line_data = one_line_data[0].split(',')

                str1 = Record(one_line_data)
                self.data.append(str1)

    def count_dim(self):
        """count number of columns in a file"""
        count_num = []
        for i in self.data:
            count_num.append(i.length)
        # get mode of number, exclude index
        return mode(count_num)[0][0] - 1

    def check_raise(self):
        """check abnormalities"""
        count = 0
        dim_include_index = self.count_dim() + 1
        not_match = []
        has_data_anomalies = []

        for record in self.data:  # determine whether there are column numbers and data anomalies
            count += 1
            # match dim
            if record.check_not_match(dim_include_index):
                not_match.append(count)

            if record.check_has_not_number(self.label_num):
                has_data_anomalies.append(count)

        if len(not_match) != 0:
            print('存在列数不等的情况，行数为：', end=' ')
            for i in not_match:
                print(i, end=' ')
            print()

        if len(has_data_anomalies) != 0:
            print('存在数据异常，行数为：', end=' ')
            for i in has_data_anomalies:
                print(i, end=' ')
            print()

    def get_dict_index_to_record(self):
        """ use dict to save data """

        tmp_index = self.data[0].record_data[self.label_num]  # in for loop, represent the previous index
        dict_index_to_record = {tmp_index: [0, []]}  # sum and record_data list

        for record in self.data:
            one_record = record.record_data  # get list
            # determine whether record_data has same index
            if one_record[self.label_num] is tmp_index:
                dict_index_to_record[tmp_index][1].append(one_record)
                dict_index_to_record[tmp_index][0] += 1
            else:
                tmp_index = one_record[self.label_num]

                if tmp_index in dict_index_to_record.keys():  # has same index before
                    dict_index_to_record[tmp_index][0] += 1
                else:
                    dict_index_to_record[tmp_index] = [1, []]
                dict_index_to_record[tmp_index][1].append(one_record)

        self.index = dict_index_to_record.keys()
        return dict_index_to_record

    def file_save(self, file_dir):
        """save file to directory"""
        # if dir is not exit
        path = file_dir.strip().rstrip('\\')
        if not os.path.exists(path):
            os.mkdir(path)

        file_name = self.file_name.split(os.sep)[-1]  # get concrete name
        if isinstance(file_name, str):
            dict_index_to_record = self.get_dict_index_to_record()
            for index in dict_index_to_record.keys():
                with open(''.join([file_dir, os.sep, file_name,
                                   '_c{}_{}'.format(index, dict_index_to_record[index][0]), '.txt']),
                          'w+') as tmp_file:
                    tmp_str = []
                    for i in dict_index_to_record[index][1]:
                        tmp_str.append('\t'.join(i) + '\n')
                    tmp_file.writelines(tmp_str)


if __name__ == '__main__':
    # test
    # file1 = FileTxt('d:\\Documents\\PycharmProjects\\test2\\data\\batch1_labelAt3_missing_column.txt')
    file1 = FileTxt('d:\\Documents\\PycharmProjects\\test2\\data\\batch1_labelAt0.txt')
    print(file1.file_name, file1.label_num)
    print(file1.count_dim())
    print(file1.check_raise())
