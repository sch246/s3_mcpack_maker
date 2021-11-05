# 创建的函数

函数列表可以用以下代码得到(然而包括类)

    import s3_mcpack as s3
    for obj in s3.__dict__:
        if hasattr(getattr(s3,obj),'__call__'):
            print(obj)


- mkfile: 创建对应路径的文件

- cutfirst: 删除字符串的第一个字符

- cuttab: 删除字符串开头缩进长度的内容

- re_empty: 删除列表内的空字符串

- cuthash: 对于列表内的所有字符串，删掉开头的#号并去除所有空格

- partstr: 清除所有空格，除了被()[]{}括住的内容单独作为一项外，按空格划分字符串并塞进列表

- partstrhead: 按首先碰到的n个空格把字符串分成n+1份并作为列表返回

- myeval: 输入字符串,将其中的\<a.b..\>形式的东西变成dic['a']['b']..后运行一次eval()然后返回

- evallist: 对列表的每一项尝试运行myeval()

- cutfuncs: 输入一段字符串列表，返回只包含customfunc和字符串的列表

- analyzefuncs: 输入一段字符串列表,返回解析后的字符串列表

- installpack: 对指定路径的mcfunction进行展开，不更改内容(改了后改回去了)

- mergelist: 将字符串列表转化为带换行的字符串

- partlines: 将带换行的字符串去掉换行并变成字符串列表

- dicUpdate: 合并字典,包括子字典

- listgetdic: 通过list获取字典下的字典下的字典...的值

- listsetdic: 通过list更改字典下的字典下的字典...的值

- getnbt: 把'a.b.c...'变成['a','b','c',...]运行listgetdic

- setnbt: 把'a.b.c...'变成['a','b','c',...]运行listsetdic

- mergenbt: 输入2个\<nbt\>,比较两个位置的值,若都是字典则合并,否则直接赋值

- removenbt: 输入1个\<nbt\>,移除该位置的值

- translatenbt: 输入'a.b[n].c...'返回'dic['a']['b'][n]['c']...'

- splitnbt: 输入'a.b[n].c...'返回['a','b',n,'c'...],其中n只能是数字

- log2_p: 输入一个数,得出用二分法需要的最少的层数(例如输入2输出1,输入3输出2,输入600输出10)

- mystr: 由于str()不能用所以用这个替代

- myint: 由于int()不能用所以用这个替代