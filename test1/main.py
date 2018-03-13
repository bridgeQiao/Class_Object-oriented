import os
from tools.FileTxt import FileTxt
from tools.FileFactory import FileFactory
from tools.FileSave import FileSave

if __name__ == '__main__':
    files = FileFactory('data', 'txt').create()
    for file in files:
        f = FileTxt(file)
        print('{} 的维度是\t{}'.format(file.split(os.sep)[-1], f.count_dim()))
        file_save = FileSave(file)
        file_save.file_save('tmp')

        for i in file_save.dict_index_to_record.keys():
            print(i, file_save.dict_index_to_record[i][0], end=' ')
        print()

        f.check_raise()
