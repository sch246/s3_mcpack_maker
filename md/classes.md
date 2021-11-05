# <a id="已创建的类">已创建的类</a>

可以用以下代码查看有什么类(好耶)

    import s3_mcpack as s3
    help(s3)

基本的类: file

建立在file上的类: mcjson, func

建立在mcjson上的类: advance, loot, predicate, recipe, dimension_type, dimension ,tag

建立在tag上的类: functag, entitytag, blocktag, fluidtag

使用方式是

## 创建

    <变量名> = <类名>(<MC中表示它用的路径名>)    例子: mcf = functag('#s3_def:triggers/world/load/init')

## save/load

从文件读取内容，以及保存内容到文件, 路径为可选参数，这里的路径指文件路径

    <变量名>.load([path])    例子: mcf.load()
    <变量名>.save([path])

## 设置值

改变值(内容)，除了file和mcjson外其它的value都是字符串列表的形式，不读取文件默认为空列表，需要保存到文件以使内容生效

    <变量名>.value = <值>    例子: mcf.value = ['s3_def:scb/load','s3_def:scb/load2']

## 增加项目

>注意，这是tag独有的方法，如果原来存在同名项目，则会被删去，新添加的项目会在列表的末尾

    <变量名>.add(<MC中的一个对应的标签>)        #单纯地增加一个项目
    <变量名>.add_s(<MC中的一个对应的标签>)      #增加一个required:false的项目

## 改变路径

改变路径会改变除了值以外的所有参数

    <变量名>.setname(<MC中表示的对应的路径名>)    例子: mcf.setname('#load')

## 输出信息

    <变量名>.print()

显示的样子

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
 
## 分析

递归对内容进行分析并运行对应函数,可以输入参数列表，目前只有func有此方法，将会调用customfuncs.py内的函数

    <变量名>.analyze([dic])