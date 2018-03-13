import os
from tools.file_txt import FileTxt
from tools.file_csv import FileCsv


# 得到目录下的所有相关格式的文件，并返回列表
class FileFactory(object):
    """get all TXT file in the directory

    Attributes:
        filePath : directory
        flag : determine format of the file
    """

    def __init__(self, file_path, flag='txt'):
        self.filePath = file_path
        self.flag = flag
        self.search()

    def search(self):
        """get all txt file"""
        files = os.listdir(self.filePath)
        txt_file = []
        for f in files:
            f_ext = f.split('.')[-1]
            if f_ext == self.flag:
                if self.flag == 'txt':
                    txt_file.append(FileTxt(os.sep.join([self.filePath, f])))

                if self.flag == 'csv':
                    txt_file.append(FileCsv(os.sep.join([self.filePath, f])))

        return txt_file


if __name__ == '__main__':
    # test the function
    file = FileFactory('d:\\Documents\\PycharmProjects\\test2\\data')
