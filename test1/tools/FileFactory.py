import os


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

    def create(self):
        """get all txt file"""
        files = os.listdir(self.filePath)
        txt_file = []
        for f in files:
            if f.split('.')[-1] == self.flag:
                txt_file.append(os.sep.join([self.filePath, f]))

        return txt_file


if __name__ == '__main__':
    # test the function
    file = FileFactory('data')
