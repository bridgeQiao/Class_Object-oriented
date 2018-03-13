# -*- coding: utf-8 -*-
import re
import random
import numpy as np


class Record(object):
    """one record of the File

    Include a label and concrete data

    Attributes:
        _label      : main attribute value
        record_data : one record's data without label
    """

    def __init__(self):
        self._label = ''
        self.record_data = []

    def read_line(self, file_point, label_num):
        """If file has next line, read one line, save label and record data.
           If  raise error
        """

        self.record_data = file_point.readline()

        # whether reads the end of the file, raise EOFError
        if self.record_data == '':
            raise EOFError('It has been read to the end of the document.')

        # convert string to list
        self.record_data = self.record_data.split()
        if len(self.record_data) is 1:
            self.record_data = self.record_data[0].split(',')
        self._label = self.record_data[label_num]
        self.record_data.pop(label_num)
        # convert field to float, raise ValueError
        self.record_data = list(map(lambda x: float(x), self.record_data))

    def add(self, record_list):
        if isinstance(record_list, list):
            record_list.append(self)
        else:
            raise TypeError(
                'Excepted list, but get {}'.format(type(record_list)))

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

    # Normalization method
    def normalize_record(self, math_para):
        """数据没有异常，规则化数组后保存，否则不作改变"""
        num_array = np.array(self.record_data)
        # 产生随机数1-4后，选择规范化方法进行处理
        key = random.randint(1, 4)
        operate = {1: self._z_score_scaling,
                   2: self._dividing_standard_deviation,
                   3: self._0_1_scaling,
                   4: self._dividing_each_value_by_the_range}
        self.record_data = operate[key](num_array, math_para)

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
