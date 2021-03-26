# s3_mcpack_maker

创建if时不需要跳转文件夹了，顺便解决了文件内和文件外的穷举问题，从头创建和继续使用都行


#为啥创建这个东东

因为在写我的世界(minecraft)数据包(datapack)的时候每写一个if就得跳转一个文件所以很烦

所以写了这个

#安装

并没有考虑过

因为是.py所以安装了python的话可以直接运行

并且记事本也可以编辑

因为是给写数据包的玩家用的所以应该都会安装这种东西吧

注意这两个文件是相互调用的所以改了名字的话里面也得一起改

#使用

在编辑一个mcfunction文件的时候可以添加一些特别的注释

使用脚本对这个mcfunction进行解读实现对应的效果

比如

#以下是一个mcfunction文件,绝对路径记为mcpath
    
    #setfunc s3_tp:load

        #mcfor treetype in ['oak','birch','spruce','dark_oak','acacia','jungle']

            #mc setblock ~ ~ ~ treetype_log

因为刚做好大概的就发上来了所以要使用得用python的命令行或新建脚本来运行,注意运行路径要选在datapack的根目录,和pack.mcmeta并列

    import s3_mcpack as s3
    
    mcpath = 对应mcfunction的路径

    s3.installpack(mcpath)
    
类似这样就行

随后会在执行路径的data/s3_tp/functions/下新建load.mcfunction

    setblock ~ ~ ~ oak_log

    setblock ~ ~ ~ birch_log

    setblock ~ ~ ~ spruce_log

    setblock ~ ~ ~ dark_oak_log

    setblock ~ ~ ~ acacia_log

    setblock ~ ~ ~ jungle_log

同一级可以有多个相同的命令

命令之间可以相互嵌套，也就是说在mcfor下面放一些setfunc可以循环生成文件

有什么命令以及有什么作用可以查看并修改customfuncs.py

所有#后的内容根据空格划分后都运行了一次eval()，所以可能会出现一些奇怪的东西，但同时所有的表达式也变得可以运算，注意表达式之间不要有空格

每个自定义命令需要有3个允许的输入值，分别表示


当前行（去掉了#，并且根据空格划分进了list，并且全部运行了一次eval()，注意函数名和#间不能有空格），

当前对应的缩进下的全部内容（如果有，每一行去掉一级缩进后放进了list），

以及前面留下的flag（如果有）
    
其中return的第一项得是一项字符串组成的列表，每个字符串将作为一行放进在原来文件中的位置，第二项是flag


目前可以运行的命令，，自己去customfuncs.py里面找吧，，应该都挺易懂的


#作者

就我一个人，目前来说

mcJE_ID=sch233

bilibili=https://space.bilibili.com/172818145

mcbbs=https://www.mcbbs.net/home.php?mod=space&uid=740479
