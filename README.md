# s3_mcpack_maker

解析mcf内特定注释并实现相应功能，从头创建和继续使用都行


mcf = mcfunction

#为啥创建这个东东

开始是因为在写我的世界(minecraft)数据包(datapack)的时候每写一个if就得跳转一个文件很烦

所以写了这个

不过现在对于写mcfunc挺完善了

#安装

这是用来解析mcf内特定注释并实现相应功能的东东，所以要使用得先有一个写了特定注释的mcf,你可以使用示例来测试一下

最好所有文件都放在目标数据包目录下，否则需要手动指定路径

.py文件是相互调用的

因为是.py所以安装了python的话可以直接运行installmcf来展开,默认展开的文件是同目录下的load.mcfunction

#使用

在编辑一个mcfunction文件的时候可以添加一些特别的注释

用installmcf.py对这个mcfunction进行解读实现对应的效果

运行installmcf.py,

连续Enter4下会直接展开工作目录下的load.mcfunction到工作目录

输入目标数据包所在的文件夹,Enter,直接enter会选择工作目录为目标数据包

输入要展开的mcf,Enter,直接enter会选择当前工作目录下的load.mcfunction,即使前一个Enter选择了其它路径,工作目录暂且不变

选择这次展开是否改变原文件的内容,Enter,直接enter默认不改变,如果想改变原文件内容，请随便输入什么后按Enter

会显示出路径，再按一下Enter就是运行了

你可以运行一下,当目录中出现load.mcfunction后进行编辑,随后再运行一下()

例如test1里面是这样
    
    #set func s3_tp:load
        #for_ treetype in ['oak','birch','spruce','dark_oak','acacia','jungle']
            #mc setblock ~ ~ ~ <treetype>_log

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


#字段环境

注释命令由字段构成,一般情况下用空格分开,除了固定内容的字段外,字段内能填什么,该怎么填取决于字段环境

命令的字段环境会在customfuncs里标出

以下是字段环境的解释

\<str\>: 作为字符串处理

\<eval\>: 先查找形如\<a.b.c...\>的内容并转换为dic['a']['b']['c']...,随后对新的字符串运行eval(),所有在s3_mcpack中定义的函数都可以直接使用

\<evalstr\>: 查找形如f{(..)}和(\<..\>)的内容,将括号内的内容用\<eval\>并转换为字符串后合并回原位置,处理新字符串

\<nbt\>: 输入a.b.c..代表dic['a']['b']['c']...

\<analyze\>: 仅在注释命令后的缩进中出现,表示会将其作为注释命令解析

#变量的使用

所有的变量存储在一个名为dic的字典中，使用变量的方式取决于字段环境,例如对变量a.b.c和变量a

\<eval\>里: '\<a\>'和'\<a.b.c\>'

\<evalstr\>里: '\<a\>'和'\<a.b.c\>',或者'f{\<a\>}'和'f{\<a.b.c\>}'

\<nbt\>里: 'a' 和 'a.b.c'

可以使用#let \<nbt\> = \<eval\>来创建变量和给变量赋值

也可以用#dic set \<nbt\> value \<eval\>

或者#run setnbt('\<nbt\>',\<eval\>,dic)

变量是从上到下解析，全局通用的

例如

    #let a = 1
    #put
        #let b = <a> + 1
    #print_ <b>
    #mc say <b>

会得到2

并且文件内会变成say 2

#已有变量

customfuncs已经使用了一些变量,更改它们时可能会出现一些预料之外的错误

\<if\>: 用于控制if_,elif_,else_命令

\<json\>\<predicate\>等: 用于dic load/save的默认赋值,将会保存/读取到json/predicate.<evalstr>



#目前可以运行的命令，，

所有注释命令都在customfuncs.py内创建,并且写了如何使用的注释



#创建新的注释命令

编辑customfuncs.py

每个自定义命令有3个输入值，(command, value, dic)

command 是当前行的命令的字符串（就是#<命令名> command 中的command，注意函数名和#间不能有空格）

value 是字符串列表, 存储当前对应的缩进下的全部内容（每一行去掉一级缩进）

dic 是一个字典,用于存储变量

return [list] 有1个允许的值

第一项 是一项字符串列表，每个字符串将作为一行放进在原来文件中的位置,如果什么都不放的话可以填[]或者其它的什么东西(比如0),返回的字符串列表会在下一条命令解析之前被再次解析



#使用创建的类

可以用以下代码查看有什么类(好耶)

    import s3_mcpack as s3
    help(s3)

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
 
#递归对内容进行分析并运行对应函数,可以输入参数列表，目前只有func有此方法，将会调用customfuncs.py内的函数

    <变量名>.analyze([dic])



#创建的函数:

函数列表可以用以下代码得到(然而包括类)

    import s3_mcpack as s3
    for obj in s3.__dict__:
        if hasattr(getattr(s3,obj),'__call__'):
            print(obj)


mkfile: 创建对应路径的文件

cutfirst: 删除字符串的第一个字符

cuttab: 删除字符串开头缩进长度的内容

re_empty: 删除列表内的空字符串

cuthash: 对于列表内的所有字符串，删掉开头的#号并去除所有空格

partstr: 清除所有空格，除了被()[]{}括住的内容单独作为一项外，按空格划分字符串并塞进列表

partstrhead: 按首先碰到的n个空格把字符串分成n+1份并作为列表返回

myeval: 输入字符串,将其中的\<a.b..\>形式的东西变成dic['a']['b']..后运行一次eval()然后返回

evallist: 对列表的每一项尝试运行myeval()

cutfuncs: 输入一段字符串列表，返回只包含customfunc和字符串的列表

analyzefuncs: 输入一段字符串列表,返回解析后的字符串列表

installpack: 对指定路径的mcfunction进行展开，不更改内容(改了后改回去了)

mergelist: 将字符串列表转化为带换行的字符串

partlines: 将带换行的字符串去掉换行并变成字符串列表

dicUpdate: 合并字典,包括子字典

listgetdic: 通过list获取字典下的字典下的字典...的值

listsetdic: 通过list更改字典下的字典下的字典...的值

getnbt: 把'a.b.c...'变成['a','b','c',...]运行listgetdic

setnbt: 把'a.b.c...'变成['a','b','c',...]运行listsetdic

mergenbt: 输入2个\<nbt\>,比较两个位置的值,若都是字典则合并,否则直接赋值

removenbt: 输入1个\<nbt\>,移除该位置的值

translatenbt: 输入'a.b.c...'返回'dic['a']['b']['c']...'


#作者

就我一个人，目前来说

mcJE_ID=sch233

bilibili=https://space.bilibili.com/172818145

mcbbs=https://www.mcbbs.net/home.php?mod=space&uid=740479
