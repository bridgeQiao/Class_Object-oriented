import numpy as np
import csv
import os
from tools.file_factory import FileFactory

debug = 1

def test1():
    files = FileFactory('data', 'txt').search()
    for file in files:
        print('{} 的维度是\t{}'.format(file.file_name.split(os.sep)[-1], file.count_dim()))
        file.file_save('tmp')

        file.check_raise()


def gen_matrix_str(row, col):
    row_set = []
    for i in range(row):
        tmp_list = []
        for j in range(col):
            tmp_list.append('')
        row_set.append(tmp_list.copy())

    # fill the first two lines
    row_set[0][0] = least_date
    for i in range(row):
        row_set[i][1] = record_attribute[1 + i]

    return row_set


if __name__ == '__main__':
    files = [file for file in FileFactory('data', 'csv').search()]

    # indexs : indicate which row has read
    # lengths : the length of the file
    # record_sets : save ordered record_data
    # record_attribute : all record attribute
    # loop_index : determine whether over the loop
    # sum_csv_file : the sum of all csv file
    indexs = np.zeros(len(files), dtype=np.int)
    lengths = [file.record_set_length - 1 for file in files]
    record_sets = [file.sort_date() for file in
                   files]  # len(files) * file.record_set_length * record_length, exclude attribute
    record_attribute = files[0].record_set[0].record_data
    loop_index = 0
    sum_csv_file = len(files)

    with open('test2.csv', 'w', encoding='utf-8', newline='') as csv_file_tmp:
        csv_writer = csv.writer(csv_file_tmp, dialect='excel')

        # write the first row
        first_row = ['date', 'features']
        for file in files:
            first_row.append(file.file_name.split(os.sep)[-1].split('.')[0])
        csv_writer.writerow(first_row)

        # write the rest row
        while loop_index is not sum_csv_file:
            loop_index = 0

            # 1. find least date
            # 2. write the record_data that has same date to csv file
            # 3. then add the index of the record_data
            least_date = None

            # get an exit date, avoid out of list
            for i in range(sum_csv_file):
                if indexs[i] < lengths[i]:
                    least_date = record_sets[i][indexs[i]].get_date()
                    break
            # get the least date
            for i in range(sum_csv_file):
                if indexs[i] < lengths[i] and record_sets[i][indexs[i]].get_date() < least_date:
                    least_date = record_sets[i][indexs[i]].get_date()

            # for debug, print least date
            if debug:
                print(least_date, end=' ')

            # save write lines. Two-dimensional, at test2 is 6 * 7
            one_date_set = gen_matrix_str(len(record_attribute) - 1, sum_csv_file + 2)

            # has same date, increase indexs[j]
            for j in range(sum_csv_file):
                if indexs[j] < lengths[j] and record_sets[j][indexs[j]].get_date() == least_date:
                    for c in range(len(record_attribute) - 1):
                        one_date_set[c][j + 2] = record_sets[j][indexs[j]].record_data[c + 1]
                    indexs[j] += 1

            csv_writer.writerows(one_date_set)

            for i in range(sum_csv_file):  # when all the files have been read, the loop is closed.
                if indexs[i] == lengths[i]:
                    loop_index += 1
