import os
from tools.FileTxt import FileTxt


class FileSave(object):
    """get index, sum and data of the file

    Attributes:
        _file : file name
        dict_index_to_record : data saved as dict, key : index, value : [sum, list]
    """

    def __init__(self, file):
        self._file = file
        self.dict_index_to_record = {}
        self.get_dict_index_to_record()

    def get_dict_index_to_record(self):
        """save data in dect"""
        f = FileTxt(self._file)

        tmp_index = f.data[0].record[f.label_num]  # in for loop, represent the previous index
        dict_index_to_record = {tmp_index: [0, []]}  # sum and record list

        for record in f.data:
            one_record = record.record  # get list
            # determine whether record has same index
            if one_record[f.label_num] is tmp_index:
                dict_index_to_record[tmp_index][1].append(one_record)
                dict_index_to_record[tmp_index][0] += 1
            else:
                tmp_index = one_record[f.label_num]

                if tmp_index in dict_index_to_record.keys():    # has same index before
                    dict_index_to_record[tmp_index][0] += 1
                else:
                    dict_index_to_record[tmp_index] = [1, []]
                dict_index_to_record[tmp_index][1].append(one_record)

        self.dict_index_to_record = dict_index_to_record

    def file_save(self, file_dir):
        """save file to directory"""
        # if dir is not exit
        path = file_dir.strip().rstrip('\\')
        if not os.path.exists(path):
            os.mkdir(path)

        file_name = self._file.split(os.sep)[-1]    # get concrete name
        if isinstance(file_name, str):
            for index in self.dict_index_to_record.keys():
                with open(''.join([file_dir, os.sep, file_name,
                                   '_c{}_{}'.format(index, self.dict_index_to_record[index][0]), '.txt']),
                          'w+') as tmp_file:
                    tmp_str = []
                    for i in self.dict_index_to_record[index][1]:
                        tmp_str.append('\t'.join(i) + '\n')
                    tmp_file.writelines(tmp_str)


if __name__ == '__main__':
    # test
    file1 = FileSave('d:\\Documents\\PycharmProjects\\test1\\data\\batch1_labelAt3_missing_column.txt')
    for key in file1.dict_index_to_record.keys():
        print('key', key, 'value', file1.dict_index_to_record[key][0], '\n', file1.dict_index_to_record[key][1][0])
    file1.file_save('tmp')
