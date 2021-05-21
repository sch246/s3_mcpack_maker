# s3_mcpack_maker

创建if时不需要跳转文件夹了，顺便解决了文件内和文件外的穷举问题，从头创建和继续使用都行


mcf = mcfunction

#为啥创建这个东东

因为在写我的世界(minecraft)数据包(datapack)的时候每写一个if就得跳转一个文件所以很烦

所以写了这个

#安装

这是用来解析mcf内特定注释并实现相应功能的东东，所以要使用得先有一个写了特定注释的mcf,你可以使用示例来测试一下

最好所有文件都放在目标数据包目录下

因为是.py所以安装了python的话可以直接运行installmcf来展开,默认展开的文件是同目录下的load.mcfunction

注意这两个文件是相互调用的所以改了名字的话里面也得一起改

#使用

在编辑一个mcfunction文件的时候可以添加一些特别的注释

使用脚本对这个mcfunction进行解读实现对应的效果

运行installmcf.py,输入目标数据包所在的文件夹和要展开的mcf,如果直接按2下enter的话就是默认工作目录为目标数据包且工作目录下有load.mcfunction

你可以运行一下,当目录中出现load.mcfunction后进行编辑,随后再运行一下()

例如test1里面是这样
    
    #set func s3_tp:load
        #for_ treetype in ['oak','birch','spruce','dark_oak','acacia','jungle']
            #mc setblock ~ ~ ~ treetype_log

运行后会生成这样的东东

在执行路径下的data/s3_tp/functions/load.mcfunction

    setblock ~ ~ ~ oak_log
    setblock ~ ~ ~ birch_log
    setblock ~ ~ ~ spruce_log
    setblock ~ ~ ~ dark_oak_log
    setblock ~ ~ ~ acacia_log
    setblock ~ ~ ~ jungle_log

当一个命令后有缩进内容时,会递归运行直到所有缩进都消失

文件中有更多的test...



#关于这样的注释命令可以怎么写

同一级可以有多个相同的命令

命令之间可以相互嵌套，也就是说在mcfor下面放一些setfunc可以循环生成文件

有什么命令以及有什么作用可以查看并修改customfuncs.py



#创建新的注释命令

编辑customfuncs.py

每个自定义命令需要有3个允许的输入值，分别表示

当前行（去掉了#，并且根据空格划分进了list，并且全部运行了一次eval()，注意函数名和#间不能有空格），

当前对应的缩进下的全部内容（如果有，每一行去掉一级缩进后放进了list），

以及dic

(dic是一个字典,存储之前留下的数据,注意解析的顺序并不是严格的从上至下,而是一层一层地解析的,所以在for里面放变量运算需要绕一点弯)

其中return的第一项得是一项字符串组成的列表，每个字符串将作为一行放进在原来文件中的位置,如果什么都不放的话可以填[]或者其它的什么东西(比如0)，第二项是dic,可以不填



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

partstrhead: 按首先碰到的n个空格把字符串分成n+1份并作为列表返回

evallist: 对列表的每一项尝试运行eval()

installpack: 对指定路径的mcfunction进行展开，不更改内容(改了后改回去了)



#目前可以运行的命令，，

自己去customfuncs.py里面找吧，，应该都挺易懂的(划掉)

    #引号内填的是缩进下的每一行对应的内容

    #创建mcfunction,只需要像在mc里填function一样,缩进后填内容
    setfunc <func name>             'command'

    #一般的文件创建(里面包含了setfunc,,)
    set func <func name>            'command'
        tag block <blocktag name>   'execute if block ~ ~ ~ <block name>'
            func <functag name>     'function <func name>'
            entity <entitytag name> 'execute if entity @e[type=<entity type>]'
            fluid <fluidtag name>   '#<fluid type>'

    #简单的for循环,<target>和<range>和python一模一样,但原理是对command进行简单的字符串替换,对注释的内容也有效
    for_ <target> in <range>        'command'
    
    #if这一块,这个应该不需要解释,,
    if_ <condition>                 'command'
    elif_ <condition>               'command'
    else_                           'command'

    #展开对应路径的mcf,也许并没有什么用
    analyze <func name>

    #对变量进行赋值或运算(不建议的功能: 可以替换缩进下的内容)
    let <variable> = <...>          ['command']

    #将后面的命令作为mc命令放到原位,如果有变量则会被解析
    mc <command>

    #输出解析后的命令到命令行窗口
    print_ <command>

#变量的使用

统一使用dict['<variable>']来指代变量

使用let <variable> = <...>来创建变量和给变量赋值

<...>可以是任意能被eval()解析的表达式

例如

    #let a = 1
    #let b = dic['a'] + 1
    #print_ dic['b']
    #mc say dic['b']

会得到2

并且文件内会变成say 2

#作者

就我一个人，目前来说

mcJE_ID=sch233

bilibili=https://space.bilibili.com/172818145

mcbbs=https://www.mcbbs.net/home.php?mod=space&uid=740479
