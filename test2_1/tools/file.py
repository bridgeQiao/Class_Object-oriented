# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 12:34:24 2017

@author: jwang
"""
import re
import os
from tools.record import Record


class File(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.label_num = 0
        self.file_point = None

        # find the label_num from the File's name
        self.label_num = re.findall(r'labelAt(\d+)\D',
                                    self.file_name.split(os.sep)[-1])
        if len(self.label_num) is 0:  # if File's name has not 'labelAt'
            self.label_num = 0
        else:
            self.label_num = int(self.label_num[0])

        self.file_point = open(self.file_name, 'r')

    def get_record(self, list_record):
        """get record from current row,
        if record has exception, it won't add to list_record"""
        tmp_record = Record()
        tmp_record.read_line(self.file_point, self.label_num)
        tmp_record.add(list_record)

    def get_attribute(self):
        # default : the File's attribute at the first line
        tmp_record = Record()
        seek_pre = self.file_point.tell()
        self.file_point.seek(0)
        tmp_record.read_line(self.file_point, self.label_num)
        self.file_point.seek(seek_pre)
        return tmp_record.record_data

    def has_next(self):
        seek_pre = self.file_point.tell()
        if self.file_point.readline() is '':
            self.file_point.close()
            return False
        else:
            self.file_point.seek(seek_pre)
            return True
