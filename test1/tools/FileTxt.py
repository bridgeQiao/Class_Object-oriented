import re
from scipy.stats import mode
from tools.Record import Record


class FileTxt(object):
    """process txt file

    Attributes:
        file_name : file name
        label_num : the label's position of one record
        data : all record of txt file
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.label_num = None
        self.data = []

        self.create_txt()
        self.get_data()

    def create_txt(self):
        """find the label_num from the file's name"""
        self.label_num = re.search(r'labelAt\d+', self.file_name)
        if self.label_num is None:  # if file's name has not 'labelAt'
            self.label_num = 0
        else:  # has 'labelAt'
            self.label_num = int(re.findall(r'\d+', self.label_num[0])[0])

    def get_data(self):
        """save record to data"""
        with open(self.file_name) as txt_tmp:
            f = txt_tmp.readlines()
            for one_line_data in f:
                one_line_data = one_line_data.split()
                if len(one_line_data) is 1:
                    one_line_data = one_line_data[0].split(',')

                str1 = Record(one_line_data)
                self.data.append(str1)

    def count_dim(self):
        """count number of columns in a file"""
        count_num = []
        for i in self.data:
            count_num.append(i.length)
        # get mode of number, exclude index
        return mode(count_num)[0][0] - 1

    def check_raise(self):
        """check abnormalities"""
        count = 0
        dim_include_index = self.count_dim() + 1
        not_match = []
        has_data_anomalies = []

        for record in self.data:  # determine whether there are column numbers and data anomalies
            count += 1
            # match dim
            if record.length != dim_include_index:
                not_match.append(count)

            record.record.pop(self.label_num)  # exclude label
            if len(re.findall(r'[a-zA-Z]', ''.join(record.record))) is not 0:
                has_data_anomalies.append(count)

        if len(not_match) != 0:
            print('存在列数不等的情况，如下：')
            for i in not_match:
                print(i, end=' ')
            print()

        if len(has_data_anomalies) != 0:
            print('存在数据异常，如下：')
            for i in has_data_anomalies:
                print(i, end=' ')
            print()


if __name__ == '__main__':
    # test
    # file1 = FileTxt('d:\\Documents\\PycharmProjects\\test1\\data\\batch1_labelAt3_missing_column.txt')
    file1 = FileTxt('d:\\Documents\\PycharmProjects\\test1\\data\\batch1_labelAt0_nonNumeric.txt')
    print(file1.file_name, file1.label_num)
    print(file1.count_dim())
    print(file1.check_raise())
