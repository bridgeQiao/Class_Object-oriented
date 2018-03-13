# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 12:34:24 2017

@author: jwang
"""
import csv
import re
import os
import random
import time
import numpy as np
from tools.record import Record


class File(object):
    def __init__(self, file_name):
        self._label_num = 0
        self._file_point = open(file_name, 'r')
        # find the _label_num from the File's name
        self.file_name = file_name.split(os.sep)[-1]
        self._label_num = re.findall(r'labelAt(\d+)\D', self.file_name)
        if len(self._label_num) is 0:  # if File's name has not 'labelAt'
            self._label_num = 0
        else:
            self._label_num = int(self._label_num[0])

    def add_record(self, list_record):
        """get record from current row,
        if record has exception, it won't add to list_record"""
        flag_add = False  # 判断是否已经加入list_record
        tmp_record = Record()
        while not flag_add:
            tmp_record.read_line(self._file_point, self._label_num)
            flag_add = tmp_record.add(list_record)

    def get_attribute(self):
        # default : the File's attribute at the first line
        tmp_list = None
        seek_pre = self._file_point.tell()
        self._file_point.seek(0)
        tmp_list = self._file_point.readline().strip().split(',')
        self._file_point.seek(seek_pre)
        return tmp_list

    def has_next(self):
        seek_pre = self._file_point.tell()
        self._file_point.readline()
        if self._file_point.tell() == seek_pre:
            self._file_point.close()
            return False
        else:
            self._file_point.seek(seek_pre)
            return True

    def save(self, file_dir, file_type='txt'):
        operate_name = {1: 'Z_score_scaling',
                        2: 'Dividing_standard_deviation',
                        3: '0_1_scaling',
                        4: 'Dividing_each_value_by_the_range'}

        record_list = []
        # 得到所有的记录，并根据标签排序
        while self.has_next():
            self.add_record(record_list)
        sorted(record_list, key=lambda x: x.get_label())
        # 剔除维数不相等的记录
        dim = list(map(lambda x: len(x.record_data), record_list))
        dim = int(round(np.mean(dim)))
        dim_err_record = []
        for i in record_list:
            if (len(i.record_data)) != dim:
                dim_err_record.append(i)
        for i in dim_err_record:
            record_list.remove(i)

        # 得到均值，标准差，最大值，最小值
        max_precision_list = self._get_max_precision(
            record_list)
        num_array = []
        for i in record_list:
            num_array.append(list(map(self._sym_to_num, i.record_data)))
        num_array = np.array(num_array)
        mean_array = np.mean(num_array, axis=0)
        std_array = np.std(num_array, axis=0)
        max_array = np.max(num_array, axis=0)
        min_array = np.min(num_array, axis=0)
        math_para = {'mean': mean_array, 'std': std_array, 'max': max_array,
             'min': min_array}
        # 保存进文件
        for i in record_list:
            [norm_list, key] = i.normalization(math_para)
            i.save(norm_list, operate_name[key], file_dir)

    @staticmethod
    def _get_max_precision(record_list):
        precision_array = []
        for i in record_list:
            precision_array.append(
                list(map(lambda x: len(x.split('.')[-1]), i.record_data)))

        precision_array = np.array(precision_array)
        return np.max(precision_array, axis=0)

    @staticmethod
    def _sym_to_num(str_1):
        if isinstance(str_1, str):
            if str_1.isdigit():
                return int(str_1)
            else:
                return float(str_1)
