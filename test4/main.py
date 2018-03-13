from tools.folder import Folder

if __name__ == '__main__':
    # 实验一，产生文件保存到out文件夹
    folder = Folder('data1')
    folder.save_all('out')
    print("实验一的数据已经处理完成")
    # 实验二，产生test4.csv文件
    folder = Folder('data2')
    folder.file_new("test4.csv")
    print("实验二的数据已经处理完成")
