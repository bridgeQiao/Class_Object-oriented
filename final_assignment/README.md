# 数据处理综合应用

​	注意：请确保提交的论文没有抄袭，否则以零分处理。

1. 给定如下数据文件格式：

除第一行外，每行均为记录型数据格式，每行表示一条记录。每条记录形如：<label> <field1><field2>….<fieldn>，其中标签label字段的值可以是整数、日期；field*i*字段的值为整数或浮点数，即数值型数据。每个记录的维度=该记录的字段数（即列数）-1（除去标签字段）。试以面向对象的程序设计方法开发一个数据处理综合应用程序，达到下述功能需求和质量度量工作。

​	1.1 功能需求：

| 功能项目        | 描述                                       |
| ----------- | ---------------------------------------- |
| A. 数据装载     | 对指定目录下的每一个文件，实现下述功能：1）得到该文件的维度d，所有记录的维度取值中，频率最大对应的维度。2）将label字段值相同的记录输出到一个文件x。文件x的内容格式满足1.1的定义3）对于文件中的某行是\r\n或空格的情况，应忽略并仍能够处理后续行。 4）过滤非法记录，非法记录指这样的记录：它的维度不等于该文件的维度d；除了标签字段，它包含非数值型数据。将过滤完所有非法记录后的其余合法记录，按这些合法记录在原文件中出现的顺序，输出到文件y，文件y的内容 格式满足1.1的定义。 |
| B. 数据合并     | 利用已经实现的功能A，即数据装载和校验能力，装载指定目录下的任意n个文件，设计迭代算法，每次读取来自n个文件的n个记录，组成label值相同的合法记录组（若没有读取到由n个记录组成的合法记录组，则跳过当前标签小于最大标签的记录，读取下一条再进行匹配）。将上述的所有合法记录组，按label值由小到大的顺序输出到文件y，文件y的格式仍然满足1.1的定义。 |
| e C. 数据规范化  | 对指定目录下的每一个文件或每一组文件，利用功能A或B获得合法文件z，对文件z除去标签字段外的其余字段随机执行下列规范化算法中的任意一个：a) Z-score scaling:variables recalculated as (Vi - mean of {Vi})/s, where "s" is thestandard deviation of {Vi}.As a result, all variables in the data set haveequal means (0) and standard deviations (1) but different ranges. b) Dividingstandard deviation: Dividing each value Vi by the standard deviation of {Vi}. Thismethod produces a set of transformed variables with variances of 1, butdifferent means and ranges. c) 0 - 1 scaling: for each variable Vi: (Vi - min {Vi})/ (max {Vi} – min{Vi}) |
| D. Kmeans聚类 | Kmeans算法设计：在对任意输入文件进行规范化之后，对结果数据集执行1次Kmeans算法，对数据集中的所有记录进行划分，需要划分的子集（簇）的个数k可从数据集的类标签中获得。输出划分后的各个簇的成员到文件中（利用功能A已经实现的类）。[Kmeans算法](https://en.wikipedia.org/wiki/K-means_clustering)的描述。 算法结果分析：将每次运行的结果与真的簇进行比较，输出如下confusion matrix矩阵（见下表），输出计算得到簇i与真簇j之间的对应关系（见下表描述） |

Confusion matrix

![confuse_matrix](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/confuse_matrix.png)

从上述矩阵中可得到每个计算得到的簇i与真簇j之间的对应关系，即满足以下两个条件：

- 交集个数的总和最大。


-  每个计算得到的簇i对应不同的真簇j （一个例子如上述矩阵中的阴影所示）

1.2 **质量度量：**

![质量度量](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/质量度量.png)

#### 设计描述

类图如下所示：

![类图](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/类图.png)

功能A:

![序列图_A](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/序列图_A.png)

功能B：

![序列图_B](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/序列图_B.png)

功能C：

![序列图_C](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/序列图_C.png)

功能D：

![序列图_D](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/序列图_D.png)

#### 调用描述

调用树

![调用图](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/调用图.png)

#### 主控代码

##### 数据加载

```python
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
```

##### 数据合并

```python
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
    print('随机选择了类别为{}的{}个文件，分别是{}'.format(
      					category, n, list(map(lambda x: x.file_name, random_files))))
    # 对文件初始化后，新建Folder对象
    for x in random_files:
        x.resume_file_handle()
    folder2 = Folder(out_dir, random_files)
    # 保存
    file_name = 'combination.txt'
    folder2.save_combine(file_name)
    print('数据已合并')
```

##### 数据标准化

```python
def data_standardization(in_dir, out_dir):
    # 选0对A产生的out_load目录下的文件处理，选1对B产生的combination文件处理
    method = {0: data_load, 1: data_merge}
    method_rand = random.randint(0, 1)
    method[method_rand](in_dir, out_dir)
    if method_rand is 0:
        folder = Folder(out_dir)
        for file in folder.files:
            file.normalization()
        return method_rand, folder
    if method_rand is 1:
        file = File('combination.txt')
        file.normalization()
        return method_rand, file
```

##### K-means算法

```python
def k_means(in_dir, out_dir):
    key, data_standardized = data_standardization(in_dir, out_dir)
    if key is 0:
        for file in data_standardized.files:
            cluster_list, labels = file.k_means(100)
            file.confuse_matrix(cluster_list, labels)
    if key is 1:
        cluster_list, labels = data_standardized.k_means(1)
        data_standardized.confuse_matrix(cluster_list, labels)
```

#### 可复用类

Record类：依赖系统库`re`, `random`，非系统库`numpy`，使用时传入文件句柄和标签所在列数

Cluster类：依赖非系统库`numpy`, `Record`类，初始化需要传入一维数值列表，在使用时，需要传入Record对象

#### 常量定义

```python
in_dir='data'
out_dir='out_load'
```

------

### 实验结果

当在规范化时随机运行A时，一部分结果如下：

![结果_A_1](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/结果_A_1.png)

数据装载结果如下，这里默认选择标签是类标的那组：

![结果_A_2](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/结果_A_2.png)

![结果_A_3](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/结果_A_3.png)

规范化运行完成后，直接进行k-means聚类，其中标颜色的是数量最多的类。

当在规范化时随机运行B时，结果如下：

![结果_B_1](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/结果_B_1.png)

数据装载结果和上图相同

随机选择了n个文件，这里默认时选择标签是日期的那组，合并结果如下：

![结果_B_2](http://github.com/bridgeQiao/Course_Object-Oriented/raw/master/final_assignment/PIC/结果_B_2.png)

由于进行k-means算法的数据是实验B的结果，所以类标超过1000，运行时间很慢，这里没有显示结果