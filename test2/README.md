# 设计说明

​	（至少覆盖：类图、协作图、为达到封装性与性能的矛盾说明、复用了实验1中的哪些类、哪些代码、数据结构的选择, 等内容）。

1. 类图

   FileCsv与Record是聚合关系，FileTxt与Record是聚合关系

   FileCsv、FileTxt与FileFactory是依赖关系

   ![类图](https://github.com/bridgeQiao/Course_Object-Oriented/raw/master/test2/PIC/类图.png)

2. 协作图

   ![协作图](https://github.com/bridgeQiao/Course_Object-Oriented/raw/master/test2/PIC/协作图.png)

3. 为达到封装性与性能的矛盾说明

   有一些可以直接实现的过程式表达为了封装更好，放在了类里面，这样多了一次函数调用，增加了开销。

4. 复用说明

   复用了实验一中的FileFactory、FileTxt、Record类。（对于实验二来说没有使用FileTxt类）其中对FileFactory类，新增了对csv文件的处理方式；对FileTxt类进行了重构，将实验一的FileSave类的方法整合到FileTxt类中；对于Record类，增加了对数据的检查方法，和在实验二中需要用到的对日期的处理。对三个类，除了在FileTxt中增加index属性，没有修改其它的数据结构。

# 2. 可能的改进说明

​	可以实现File类接口，用FileScv和FileTxt来继承这个类。

​	简化主程序，优化算法，增加性能。

# 3. 实验总结

​	（此处可以陈述自己在完成该实验时遇到的困难和弯路，以及可能的进步方向等。）

​	重写了实验一的代码，增加了类的一些方法，将FileSave类合并到FileTxt类里面。

​	在编写FileCsv类时，参考了FileTxt的一些属性和方法，可以创建一个接口来对文件类进行抽象。

​	在得出最小日期时，总是有问题，然后对日期字符串进行了处理，对月和日是单数的，前面加了0，比如’1962/1/2’改成’1962/01/02’。

​	在写入csv文件时，要加入newline=’’参数，否则会多一行空格。

> 复用了实验一中的FileFactory、FileTxt、Record类。--- Actually it is not.﻿﻿﻿﻿
>
> 为什么不把文件中的每一行，一次性地转换为数值数组，以便后续直接处理？﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿