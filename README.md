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

举例

以下是一个mcfunction文件,绝对路径记为mcpath
    
    #set func s3_tp:load
        #for_ treetype in ['oak','birch','spruce','dark_oak','acacia','jungle']
            #mc setblock ~ ~ ~ treetype_log

因为刚做好大概的就发上来了所以要使用得用python的命令行或新建脚本来运行,注意运行路径要选在datapack的根目录,和pack.mcmeta并列

    import s3_mcpack as s3
    mcpath = 对应mcfunction的路径
    s3.installpack(mcpath)
    
类似这样就行

运行后会生成这样的东东

在执行路径下的data/s3_tp/functions/load.mcfunction

    setblock ~ ~ ~ oak_log
    setblock ~ ~ ~ birch_log
    setblock ~ ~ ~ spruce_log
    setblock ~ ~ ~ dark_oak_log
    setblock ~ ~ ~ acacia_log
    setblock ~ ~ ~ jungle_log



#关于这样的注释命令可以怎么写

同一级可以有多个相同的命令

命令之间可以相互嵌套，也就是说在mcfor下面放一些setfunc可以循环生成文件

有什么命令以及有什么作用可以查看并修改customfuncs.py

所有#后的内容根据空格划分后都运行了一次eval()，所以可能会出现一些奇怪的东西，但同时所有的表达式也变得可以运算，注意表达式之间不要有空格



#创建新的注释命令

编辑customfuncs.py

每个自定义命令需要有3个允许的输入值，分别表示

当前行（去掉了#，并且根据空格划分进了list，并且全部运行了一次eval()，注意函数名和#间不能有空格），

当前对应的缩进下的全部内容（如果有，每一行去掉一级缩进后放进了list），

以及前面留下的flag（如果有）
    
其中return的第一项得是一项字符串组成的列表，每个字符串将作为一行放进在原来文件中的位置，第二项是flag



#使用创建的类

基本的类: file

建立在file上的类: mcjson, func

建立在mcjson上的类: advance, loot, predicate, recipe, dimension_type, dimension ,tag

建立在tag上的类: functag, entitytag, blocktag, fluidtag

使用方式是

#创建

    <变量名> = <类名>(<MC中表示它用的路径名>)    例子: mcf = functag('#s3_def:triggers/world/load/init')

#从文件读取内容，以及保存内容到文件, 路径为可选参数，这里的路径指文件路径

    <变量名>.load([path])    例子: mcf.load()
    <变量名>.save([path])

#改变值(内容)，除了file和mcjson外其它的value都是字符串列表的形式，不读取文件默认为空列表，需要保存到文件以使内容生效

    <变量名>.value = <值>    例子: mcf.value = ['s3_def:scb/load','s3_def:scb/load2']

#增加项目，注意，这是tag独有的方法，如果原来存在同名项目，则会被删去，新添加的项目会在列表的末尾

    <变量名>.add(<MC中的一个对应的标签>)        #单纯地增加一个项目
    <变量名>.add_s(<MC中的一个对应的标签>)      #增加一个required:false的项目

#改变路径，改变路径会改变除了值以外的所有参数

    <变量名>.setname(<MC中表示的对应的路径名>)    例子: mcf.setname('#load')

#输出信息

    <变量名>.print()

#显示的样子

    ========================
    name: #load
    type_path: tags/functions
    path: data/minecraft/tags/functions/load.json
    space: minecraft
    space_path: load
    value:
    [
        {
            "required": false,
            "id": "s3_def:scb/load"
        },
        {
            "required": false,
            "id": "s3_def:scb/load2"
        }
    ]
 
#递归对内容进行分析并运行对应函数，目前只有func有此方法，将会调用customfuncs.py内的函数

    <变量名>.analyze()



创建的函数:

mkfile: 创建对应路径的文件

cutfirst: 删除字符串的第一个字符

cuttab: 删除字符串开头缩进长度的内容

re_empty: 删除列表内的空字符串

cuthash: 对于列表内的所有字符串，删掉开头的#号并去除所有空格

partstr: 清除所有空格，除了被()[]{}括住的内容单独作为一项外，按空格划分字符串并塞进列表

evallist: 对列表的每一项尝试运行eval()

installpack: 对指定路径的mcfunction进行展开，不更改内容(改了后改回去了)



#目前可以运行的命令，，
自己去customfuncs.py里面找吧，，应该都挺易懂的



#作者

就我一个人，目前来说

mcJE_ID=sch233

bilibili=https://space.bilibili.com/172818145

mcbbs=https://www.mcbbs.net/home.php?mod=space&uid=740479
