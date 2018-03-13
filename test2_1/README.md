# 1. 设计说明

（请给出**本实验代码**与**实验2**的设计图（包括类图、顺序图）的差异性（包括：增删改了哪些类、哪些方法），并给出说明是什么原因导致本实验的代码与实验2的设计图的不同？）。

- 在Record类中，去掉了length属性，添加label属性。为了降低耦合，将读取一行和添加到列表的计算放到Record里，将多个判断异常的方法合并成一个；
- 将之前的FileCsv和FileTxt合并成File类，Record集合改为含有文件指针，不再直接保存。为了实现读一行处理一行的功能，实现了读一行和判断是否存在下一行的方法；
- 将FileFactory类改为Folder类，为了降低主函数的控制，增加新建文件方法，将主要的逻辑部分放到这个方法里。由于第一行和后面的数据是分开的，增加写入第一行的方法，也起到清空之前的文件内容的功能；
- 在实现保存一个日期的五个记录中，为了增加可理解性和单一职责，添加了二维字符串数组StrMatrix类，有行和列的数量以及数据属性，添加保存一个字符串和保存一列数据的方法，为了降低Folder类的控制，将保存到文件的计算放到这个类里。

# 2. 可能的改进说明

​	其中判断标签所在列的方法采用的是：如果文件名没有指明，则默认是0，可以实现更**智能**一点；

​	大部分的逻辑控制在Folder类的file_new方法里。

# 3. 实验总结

（此处可以陈述自己在完成该实验时遇到的困难和弯路，以及可能的进步方向等。）

- 在实现代码的过程中，之前以为txt和csv文件需要用不同的方法去实现读取和保存的方法，于是分成了两个类，在实验二中发现可以用相同的方式读取和保存。


- 之前习惯直接保存所有的数据，然后进行处理，发现很占用内存，而且处理起来会慢一点，分开处理会好很多。


- 之前习惯将控制放到上层去处理，类与类之间的耦合度很高，发现将逻辑和具体实现分开后，会使可理解性和重用性提高。
- 需要对面向对象有更深入的认识，能够更好的去分离一个问题中的有意义的类和关于这个类的属性，在代码实现过程中，需要更好的去考虑重用的问题。

> StrMatrix类，有行和列的数量以及数据属性，添加保存一个字符串和保存一列数据的方法，为了降低Folder类的控制，将保存到文件的计算放到这个类里。
>
> --- Why keep strings and rows at the same time?﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿