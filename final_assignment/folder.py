# -*- coding: utf-8 -*-
import os
import random
from file import File


class Folder(object):
    """get all File to a list

    some operate of File

    Attributes:
        file_path   : folder name
        files       : get all File object
    """

    def __init__(self, file_path, file_list=None):
        self.file_path = file_path
        self.files = []
        if file_list is None:
            for f in os.listdir(self.file_path):
                self.files.append(File(''.join([self.file_path, os.sep, f])))
        else:
            self.files = file_list

    def save_combine(self, file_name):

        record_list = []
        record_all = []
        # 从n个文件中读取相同label的记录
        while self._get_same_label(record_list):
            record_all.append(record_list.copy())
            record_list = []
        record_all = sorted(record_all, key=lambda x: x[0].get_label())
        # 保存进文件
        file_tmp = open(file_name, 'w')
        for records in record_all:
            for record in records:
                str_save = ''.join(
                    [record.get_label(), ',',
                     ','.join(str(i) for i in record.record_data), '\n'])
                file_tmp.write(str_save)
        file_tmp.close()

    def _get_same_label(self, record_list):
        # 每个文件都读一行，将label保存到labels里，如果读不到返回False
        labels = []
        flag_same = 0

        if not self._has_next():
            return False

        for i in range(len(self.files)):
            record_list.append(self.files[i].next())
            labels.append(record_list[i].get_label())

        # 如果标签不一样，则读一行，更新record_list，直到标签一样
        while flag_same != len(labels):
            # 得到最大的标签
            flag_same = 0
            label_max = labels[0]
            for label in labels:
                if label > label_max:
                    label_max = label

            for i in range(len(labels)):
                if not labels[i] == label_max:
                    if not self.files[i].has_next():
                        return False
                    record_list[i] = self.files[i].next()
                    labels[i] = record_list[i].get_label()
                else:
                    flag_same += 1
        return True

    def _has_next(self):
        # 文件夹下的文件是否有读完的情况
        for f in self.files:
            if not f.has_next():
                return False
        return True


#
# 以下是主控代码
#
def data_load(in_dir, out_dir='out_load'):
    print('数据正在装载...')
    folder = Folder(in_dir)
    # 将label字段值相同的记录输出到一个文件x
    for file in folder.files:
        # 由于日期文件的label每个都不同，输出文件太多而忽略
        if file.data_category == 0:
            file.set_record_list()
            file.save_by_label()
            file.save_file(out_dir)

    print('数据装载已完成')
    return out_dir


def data_merge(in_dir, out_dir, category=1):
    data_load(in_dir, out_dir)
    print('数据合并中...')
    if category is 1:
        out_dir = in_dir
    folder = Folder(out_dir)
    # 选出同类型的文件
    filter_file = [i for i in folder.files if i.data_category == category]
    # 随机选择n个文件
    n = random.randint(1, len(filter_file))
    random_index = random.sample(range(len(filter_file)), n)
    random_index.sort()
    random_files = [filter_file[i] for i in random_index]
    print('随机选择了类别为{}的{}个文件，分别是{}'.format(category, n, list(
        map(lambda x: x.file_name, random_files))))
    # 对文件初始化后，新建Folder对象
    for x in random_files:
        x.resume_file_handle()
    folder2 = Folder(out_dir, random_files)
    # 保存
    file_name = 'combination.txt'
    folder2.save_combine(file_name)
    print('数据已合并')


def data_standardization(in_dir, out_dir):
    # 选0对A产生的out_load目录下的文件处理，选1对B产生的combination文件处理
    method = {0: data_load, 1: data_merge}
    method_rand = random.randint(0, 1)
    method[method_rand](in_dir, out_dir)
    method_rand = 0
    if method_rand is 0:
        folder = Folder(out_dir)
        for file in folder.files:
            file.normalization()
        return method_rand, folder
    if method_rand is 1:
        file = File('combination.txt')
        file.normalization()
        return method_rand, file


def k_means(in_dir, out_dir):
    key, data_standardized = data_standardization(in_dir, out_dir)
    if key is 0:
        for file in data_standardized.files:
            cluster_list, labels = file.k_means(100)
            file.confuse_matrix(cluster_list, labels)
    if key is 1:
        cluster_list, labels = data_standardized.k_means(1)
        data_standardized.confuse_matrix(cluster_list, labels)


if __name__ == '__main__':
    in_dir = 'data'
    out_dir = 'out_load'
    k_means('data', 'out_load')
