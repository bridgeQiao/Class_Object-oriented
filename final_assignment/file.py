# -*- coding: utf-8 -*-
import re
import os
import numpy as np
from record import Record
from cluster import Cluster
import random


class File(object):
    """attribute and operation of record list

        Attributes:
            _label_col    : the column of the label
            _file_point   : file handle
            file_name     : file name
            record_list   : save all record
            dim           : data dimension
            data_category : if label is column, category is 0.
                            if label is date, category is 1.
        """

    def __init__(self, file_name):
        self._label_col = 0
        self._file_point = open(file_name, 'r')
        self.record_list = []
        self.dim = self._get_dim()

        # get data category
        self.data_category = 0
        self._get_category()

        # find the _label_num from the File's name
        self.file_name = file_name.split(os.sep)[-1]
        self._label_col = re.findall(r'labelAt(\d+)\D', self.file_name)
        if len(self._label_col) is 0:  # if File's name has not 'labelAt'
            self._label_col = 0
        else:
            self._label_col = int(self._label_col[0])

    def get_label_col(self):
        return self._label_col

    def set_record_list(self):
        self.resume_file_handle()

        while self.has_next():
            record_tmp = self.next()
            if len(record_tmp.record_data) == self.dim:
                self.record_list.append(record_tmp)

    def next(self):
        """get record from current row"""
        tmp_record = Record()
        while True:  # 判断是否有值异常，有非数值记录造成
            try:
                tmp_record.read_line(self._file_point, self._label_col)
                break
            except ValueError:  # 非数值，继续往下读
                continue
        return tmp_record

    def _get_category(self):
        self.resume_file_handle()
        label = self.next().get_label()
        if len(re.findall(r'\d+', label)) == 3:
            self.data_category = 1

    def _get_dim(self):
        # 从文件开始出读取
        self.resume_file_handle()
        record_len_list = []

        # 得到所有的记录的长度
        while self.has_next():  # 判断是否已经读取完
            record_len_list.append(len(self.next().record_data))
        array = dict((i, record_len_list.count(i)) for i in record_len_list)
        max_item = max(array.values())
        for k, v in array.items():
            if v == max_item:
                return k

    def normalization(self):
        self.set_record_list()

        # 得到均值，标准差，最大值，最小值
        num_array = []
        for i in self.record_list:
            num_array.append(i.record_data)
        num_array = np.array(num_array)
        mean_array = np.mean(num_array, axis=0)
        std_array = np.std(num_array, axis=0)
        max_array = np.max(num_array, axis=0)
        min_array = np.min(num_array, axis=0)
        math_para = {'mean': mean_array, 'std': std_array, 'max': max_array,
                     'min': min_array}
        # 每个record规范化
        for i in self.record_list:
            i.normalize_record(math_para)

    def has_next(self):
        seek_pre = self._file_point.tell()
        try:
            self.next()
            self._file_point.seek(seek_pre)
            return True
        except EOFError:
            return False

    def k_means(self, n=10):
        # 必须是规范化后的数据才能进行K-means, n为循环次数，默认10次
        # 得到聚类数num_cluster
        labels = []
        for record in self.record_list:
            label = record.get_label()
            if label not in labels:
                labels.append(label)
        num_cluster = len(labels)

        # 初始化聚类中心
        index = random.sample(range(len(self.record_list)), num_cluster)
        cluster_list = [Cluster(self.record_list[i].record_data) for i in index]
        for _ in range(n):
            # 清空聚类所含的record, 添加record到cluster
            for i in cluster_list:
                i.clear_point()
            for record in self.record_list:
                distance_list = list(
                    map(lambda x: x.get_distance(record.record_data),
                        cluster_list))
                min_distance_index = distance_list.index(min(distance_list))
                cluster_list[min_distance_index].add(record)
            # 更新聚类中心
            for i in cluster_list:
                i.update_center()
        return cluster_list, labels

    def confuse_matrix(self, cluster_list, labels):
        print('\n', self.file_name, '\n', '\t'.join(labels))
        count_matrix = [cluster.count_confuse_matrix(labels) for cluster in
                        cluster_list]
        # 打印混淆矩阵
        for count_list in count_matrix:
            max_index = list(count_list).index(max(count_list))
            str_print = []
            for i in range(len(count_list)):
                if i is max_index:  # 如果该数字最大，加颜色
                    str_print.append(
                        '\033[1;35m{}\033[0m'.format(count_list[i]))
                else:
                    str_print.append(str(count_list[i]))

            print('\t'.join(str_print))

    def save_by_label(self):
        # 得到标签一样的record的索引
        dict_label = {}
        for record_index in range(len(self.record_list)):
            label = self.record_list[record_index].get_label()
            if label in dict_label:
                dict_label[label].append(record_index)
            else:
                dict_label[label] = [record_index]

        # 按标签写入文件
        # 默认文件夹out，如果文件夹不存在
        path = 'out1'
        if not os.path.exists(path):
            os.mkdir(path)
        for label in dict_label:
            # 文件格式：原文件名_标签.txt
            output_file_name = ''.join(
                [path, '/', self.file_name.split('.')[0], '_c', label, '.txt'])
            file_tmp = open(output_file_name, 'w')
            # 按照每个记录索引去写入文件
            for index in dict_label[label]:
                # 写入数据格式形如：'标签，域，域，...\n'，其中标签在原来所在列
                record_data_tmp = self.record_list[index].record_data.copy()
                record_data_tmp.insert(self.get_label_col(), label)
                file_tmp.write(
                    ''.join([','.join(str(i) for i in record_data_tmp), '\n']))
            file_tmp.close()

    def save_file(self, out_dir='out_load'):
        # 将合法的记录写入文件
        # 默认文件夹out_load，如果文件夹不存在
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        file_name = ''.join(
            [out_dir, '/', self.file_name.split('.')[0], '.txt'])
        file_tmp = open(file_name, 'w')
        for record in self.record_list:
            # 写入数据格式形如：'标签，域，域，...\n'，其中标签在原来所在列
            record_data_tmp = record.record_data.copy()
            record_data_tmp.insert(self.get_label_col(), record.get_label())
            file_tmp.write(
                ''.join([','.join(str(i) for i in record_data_tmp), '\n']))
        file_tmp.close()

    def resume_file_handle(self):
        self._file_point.seek(0)
