import re
import random
import numpy as np
import time
import os


class Record(object):
    """one line of the data of the File

    Include a label and concrete data

    Attributes:
        _label      : main attribute value
        record_data : one record's data without label
    """

    def __init__(self):
        self._label = ''
        self.record_data = []
        self._file_name = ''

    def read_line(self, file_point, label_num):
        """read one line, save label and record"""
        self.record_data = file_point.readline().split()
        if len(self.record_data) is 1:
            self.record_data = self.record_data[0].split(',')
        self._label = self.record_data[label_num]
        self.record_data.pop(label_num)
        self._file_name = file_point.name.split(os.sep)[-1]

    def add(self, list_record):
        """add self to list and return True if own data hasn't exception,
           return False if has exception"""
        if isinstance(list_record, list):
            if self._has_exception():
                return False
            else:
                list_record.append(self)
                return True

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

    def save(self, norm_list, operate_name, file_dir, file_type='txt'):
        # 保存进文件
        str_list = list(map(str, norm_list))
        str_write = ','.join(str_list)
        str_write += '\n'

        # 文件名为exit_file
        file_name = self._file_name.split('.')[0]
        name_list = [file_name, operate_name, self.get_label()]
        # 判断文件是否已经存在
        name_tmp = self._file_exits(file_dir, name_list)
        # 如果不存在
        if not name_tmp:
            exit_file = '-'.join(name_list)
            time_now = time.strftime("%Y_%m_%d-%H_%M_%S", time.localtime())
            exit_file = ''.join([exit_file, '-', time_now, '.', file_type])
        else:
            exit_file = name_tmp

        with open(file_dir + '/' + exit_file, 'a+') as file_tmp:
            file_tmp.write(str_write)

    # Normalization method
    def normalization(self, math_para):
        """数据没有异常，规则化数组后保存，否则不作改变"""
        num_list = list(map(self._sym_to_num, self.record_data))
        num_array = np.array(num_list)
        # 产生随机数1-4后，选择规范化方法进行处理
        key = random.randint(1, 4)
        operate = {1: self._z_score_scaling,
                   2: self._dividing_standard_deviation,
                   3: self._0_1_scaling,
                   4: self._dividing_each_value_by_the_range}
        return [operate[key](num_array, math_para), key]

    @staticmethod
    def _z_score_scaling(num_array, math_para):
        return (num_array - math_para['mean']) / math_para['std']

    @staticmethod
    def _dividing_standard_deviation(num_array, math_para):
        return num_array / math_para['std']

    @staticmethod
    def _0_1_scaling(num_array, math_para):
        return (num_array - math_para['min']) / (
            math_para['max'] - math_para['min'])

    @staticmethod
    def _dividing_each_value_by_the_range(num_array, math_para):
        return num_array / (math_para['max'] - math_para['min'])

    def _has_exception(self):
        """check if has exception"""
        str_check = ','.join(self.record_data)
        # check has character
        str_list = re.findall(r'[a-zA-Z]', str_check)
        if len(str_list) != 0:
            return True
        if len(self._file_name.split('label')) != 1:
            return False
        # get all floating number and integer. Type : ('-','***','.***')
        str_list = re.findall(r'([-+]?)(\d+)(\.\d+)?', str_check)
        if str_list.__len__() is not self.record_data.__len__():
            return True
        for str1 in str_list:
            if str1[0] == '-':
                return True

    @staticmethod
    def _sym_to_num(str_1):
        if isinstance(str_1, str):
            if str_1.isdigit():
                return int(str_1)
            else:
                return float(str_1)

    @staticmethod
    def _file_exits(file_dir, name_list):
        for f in os.listdir(file_dir):
            count = 0
            feature = f.split('-')
            for i in range(len(name_list)):
                if feature[i] == name_list[i]:
                    count += 1
                if count == len(name_list):
                    return f
        return False
