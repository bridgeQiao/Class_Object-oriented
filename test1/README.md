# 实验一

## 实验要求

读入给定目录下所有文本文件

对每一个文件，实现下述功能：

1. 输出该文件的数据维度（即不包括类标签所在列的列数）。
2. 将属于同一类标签的记录输出到一个文件，文件编号如`batch1_labelAt0_c1_5.txt`（存放属于类标签1的所有记录，该类共有5条记录），`batch1_ batch1_labelAt0_c2_15.txt`（存放属于类标签2的所有记录，共15条记录）。注意有些数据集文件的类标签不一定是数字，可能是字母（如a,b,c等）
3. 对于文件中的某行是`\r\n`或空格的情况，应忽略并仍能够处理后续行。
4. 能够处理非法情况：包括列数不等（如：某一行的列数少于或多于其它行）、某一行包括非数值数据，程序应输出哪一行记录存在非法情况，以便数据准备人员查看。

## 设计说明

### 1. 数据结构设计

1. **FileFactory**类：文件工厂类，方便处理文件夹的多个文件类型；

   - 属性

     filePath: 文件目录

     flag: 标记文件类型，默认是txt格式

   - 方法

     create: 创建txt文件对象

2. **FileTxt**类：文件工厂类，方便处理文件夹的多个文件类型；

   - 属性

     file_name: 文件名

     label_num：标签在第几列

     data：记录数据，用Record类保存

   - 方法

     create_txt：将文件名中提示了标签列数的提取出来，保存到label_num里，没有提示的，默认为0

     get_data: 将文件里的每一行数据保存到data里

     count_dim: 计算列数，取众数

     check_raise：将列数不等和除标签列的数据存在字母

3. **Record**类：记录类，对记录进行处理；

   - 属性

     record: 一行记录，用数组保存

     length：记录的数据个数，包含标签

   - 方法

4. **FileSave**类：将同一标签的数据保存。

   - 属性

     _file: 文件名

     dict_index_to_record: 数据，用字典保存，·key·:标签,·value·:[总和，记录]，列表表示

   - 方法

     get_dict_index_to_record: 默认使用，对文件进行处理，得到字典

     file_save：保存文件

### 2. 执行流程设计

- 创建FileFactory类，读入所有的文本文件；

- 用FileTxt类对每个文件进行处理，得到文件的维度并输出，将记录保存在Record类里；

- 对所有的记录进行处理，使用FileSave类进行保存。

- 打印出所有非法情况

### 3. 程序框图

![程序框图](https://github.com/bridgeQiao/Course_Object-Oriented/raw/master/test1/PIC/程序框图.png)

### 4. 各种非法情况的正确处理结果

存在数据异常的情况：

![结果_1](https://github.com/bridgeQiao/Course_Object-Oriented/raw/master/test1/PIC/结果_1.png)

存在列数不同的情况：

![结果_2](https://github.com/bridgeQiao/Course_Object-Oriented/raw/master/test1/PIC/结果_2.png)
