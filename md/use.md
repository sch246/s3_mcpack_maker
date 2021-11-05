# 使用说明

稍微更详细的说明

## 内容列表

- [使用](#使用)
- [命令](#命令)
- [参数类型](#参数类型)
- [变量](#变量)
- [递归](#递归)
- [创建新的命令](#创建新的命令)
- [已创建的类](./classes.md)
- [创建的函数](./funcs.md)

## 使用

### 要使用本模块,你需要做以下几步

在某个需要解析的mcfunction文件内输入[命令](#命令)

运行本模块的py并指定路径

等待完成即可。(

### 更详细的步骤

把3个py文件放进数据包内和data文件夹并列

运行 installmcf.py,

连续Enter4下会直接展开工作目录下的load.mcfunction到工作目录


- 输入目标数据包所在的文件夹,Enter,直接enter会选择工作目录为目标数据包

- 输入要展开的mcf,Enter,直接enter会选择当前工作目录下的load.mcfunction,即使前一个Enter选择了其它路径,工作目录暂且不变

- 选择这次展开是否改变原文件的内容,Enter,直接enter默认不改变,如果想改变原文件内容，请随便输入什么后按Enter

- 会显示出路径，再按一下Enter就是运行了


>你可以运行一下,当目录中出现load.mcfunction后进行编辑,随后再运行一下()

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

>当一个命令后有缩进内容时,会递归运行直到所有缩进都消失

## 命令

**命令**是本模块的核心，一般是说定义的注释后面的命令，而不是mc命令，由**命令名**和**参数**组成

**命令**均在mcfunction内编写，之所以采用注释只是不想看到报错

查看[格式](./command_format.md)

命令均在[命令列表](../customfuncs.py)内定义，里面定义的命令名就是注释命令的命令名

>命令使用[dic](#dic)传参)

## 参数类型

注释命令由命令名和参数构成,一般情况下用空格分开,参数填什么,该怎么填取决于参数类型

以下是解释

- \<str\>: 作为字符串处理

- \<eval\>: 先查找形如\<a.b.c...\>的内容并转换为dic['a']['b']['c']...,随后对新的字符串运行eval(),所有在s3_mcpack中定义的函数都可以直接使用

- \<evalstr\>: 查找形如f{(..)}和(\<..\>)的内容,将括号内的内容用\<eval\>并转换为字符串后合并回原位置,处理新字符串

- \<nbt\>: 输入a.b.c..代表dic['a']['b']['c']...

- \<analyze\>: 仅在注释命令后的缩进中出现,表示会将其作为注释命令解析

## 变量

### <a id="dic">变量的使用</a>

所有的变量存储在一个名为dic的字典中，表示变量的方式取决于参数类型,例如对变量a和变量a.b.c

- \<eval\>里: '\<a\>'和'\<a.b.c\>'

- \<evalstr\>里: '\<a\>'和'\<a.b.c\>'，或者'f{\<a\>}'和'f{\<a.b.c\>}'

- \<nbt\>里: 'a' 和 'a.b.c'

### 变量的赋值

可以使用以下几条来创建变量和给变量赋值
- #let \<nbt\> = \<eval\>

- #dic set \<nbt\> value \<eval\>

- #run setnbt('\<nbt\>',\<eval\>,dic)

### 变量的通用性

变量是从上到下解析，全局通用的

例如

    #let a = 1
    #put
        #let b = <a> + 1
    #print_ <b>
    #mc say <b>

会得到2

并且文件内会变成say 2

### 已有变量

customfuncs已经使用了一些变量,更改它们时可以会出现一些预料之外的错误

- \<if\>: 用于控制if_,elif_,else_命令

- \<json\>\<predicate\>等: 用于dic load/save的默认赋值,将会保存/读取到json/predicate.<evalstr>


## 递归

利用customfuncs下的功能可以做到创建函数并使用递归,以下是一个简单例子

    #let f
        #if_ <n> > 0
            #mc say <n>
            #let n = <n>-1
            #puts <f>
    #let n = 5
    #setfunc test
        #puts <f>

将在minecraft:test的mcf中创建以下内容

    say 5
    say 4
    say 3
    say 2
    say 1

>但是更一般的函数不能这样创建,因为所有变量都是全局变量

以下是一个更一般的函数的例子,这个mcf的作用是建立一个scb和storage之间的容量为1024的映射,,这样就可以给1024个玩家每人分配一个nbt存储空间(因为懒得造例子就复制自己的数据包)

    #let eff.func
        #let n = <eff.input>[-1][0]
        #let s = <eff.input>[-1][1]
        #let x = <eff.input>[-1][2]
        #let li = <eff.input>[-1][3]
        #setfunc <s>
            #if_ <n> == -1
                #puts <f>
            #if_ <n> > -1
                #for_ c in [0,1]
                    #let n = <eff.input>[-1][0]
                    #let s = <eff.input>[-1][1]
                    #let x = <eff.input>[-1][2]
                    #let li = <eff.input>[-1][3]
                    #if_ <n> > 0
                        #mc execute unless data storage memory personf{<li>+'['+mystr(<c>)+']'} run data modify storage memory person<li> append value []
                    #elif_ <n> == 0
                        #mc execute unless data storage memory personf{<li>+'['+mystr(<c>)+']'} run data modify storage memory person<li> append value {}
                    #let li = <li>+'['+mystr(<c>)+']'
                    #let s = f"{<s>}_{<c>}/{<n>-1}"
                    #mc execute if score memory slot matches f{<x>+<c>*2**<n>}..f{<x>+(2**(<n>+<c>))-1} run function <s>
                    #run <eff.input>.append((<n>-1,<s>,<x>+<c>*2**<n>,<li>))
                    #puts <eff>
        #run <eff.input>.pop()

    #let f
        #mc execute if score # tmp matches 0 run data modify storage memory person<li> set from storage memoryinput person
        #mc execute if score # tmp matches 1 run data modify storage memoryoutput person set from storage memory person<li>


    #let eff.input = []
    #let n = 9
    #let s = 's3.math:memory/person/eff/'+mystr(<n>)
    #let x = 0
    #let li = ''
    #run <eff.input>.append((<n>,<s>,<x>,<li>))
    #puts <eff.func>


这里使用了list来模拟栈,list.pop()和list.append()来控制内容的进出,使用元组来存储输入参数

>函数在最后一定要运行pop()来清除变量

可以注意到for内重新赋值了一次变量,那是因为在for内改变了变量的值,,

## 创建新的命令

编辑[customfuncs.py](../customfuncs.py)

每个自定义命令有3个输入值
- command
- value
- dic

command 是当前行的命令的字符串（就是#<命令名> command 中的command，注意函数名和#间不能有空格），也就是**参数**

value 是字符串列表, 存储当前对应的缩进下的全部内容（每一行去掉一级缩进），也就是**缩进**

dic 是一个字典,用于存储变量

return [list] 是一项字符串列表，每个字符串将作为一行放进在原来文件中的位置,如果什么都不放的话可以填[]或者其它的什么东西(比如0),返回的字符串列表会在下一条命令解析之前被再次解析

## [已创建的类](./classes.md)

## [创建的函数](./funcs.md)
