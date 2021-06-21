# -*- coding: UTF-8 -*-
import os,re,json
from typing import Pattern
import s3_mcpack as s3


def setfunc(command, value, dic):
    #创建mcfunction, 只需要像在mc里填function一样, 缩进后填内容
    #setfunc <evalstr>
    #   <analyze>
    mcf = s3.func(s3.evalstr(command, dic))
    mcf.value = value
    mcf.save()
    mcf.analyze()

def addtag(command, value, dic):
    #添加tag,若无文件则会创建,functag添加时会加上required:false, 缩进后需要按照格式填(为了更好地使用自动补全)
    #addtag block/func/entity/fluid <evalstr>
    #   execute if block ~ ~ ~ <evalstr>
    #   function <evalstr>
    #   execute if entity @e[type=<evalstr>]
    #   #<evalstr>
    command = s3.partstr(command)
    c1 = s3.evalstr(command[1], dic)
    if command[0] == 'block':
        mcf = s3.blocktag(c1)
        mcf.load()
        # mcf.print()
        for str in value:
            str2 = ''
            checkstr = 'execute if block ~ ~ ~ '
            checklen = len(checkstr)
            if len(str) > checklen and str[0:checklen] == checkstr:
                for char in str[checklen:len(str)]:
                    if char == ' ':
                        break
                    else:
                        str2 += char
                mcf.add(s3.evalstr(str2,dic))
        mcf.save()
    if command[0] == 'func':
        mcf = s3.functag(c1)
        mcf.load()
        # mcf.print()
        for str in value:
            str2 = ''
            checkstr = 'function '
            checklen = len(checkstr)
            if len(str) > checklen and str[0:checklen] == checkstr:
                for char in str[checklen:len(str)]:
                    if char == ' ':
                        break
                    else:
                        str2 += char
                mcf.add_s(s3.evalstr(str2, dic))
        # mcf.print()
        mcf.save()
    if command[0] == 'entity':
        mcf = s3.entitytag(c1)
        mcf.load()
        # mcf.print()
        for str in value:
            str2 = ''
            checkstr = 'execute if entity @e[type='
            checklen = len(checkstr)
            if len(str) > checklen and str[0:checklen] == checkstr:
                for char in str[checklen:len(str)]:
                    if char == ']':
                        break
                    else:
                        str2 += char
                mcf.add(s3.evalstr(str2, dic))
        mcf.save()
    if command[0] == 'fluid':
        mcf = s3.fluidtag(c1)
        mcf.load()
        # mcf.print()
        for str in value:
            str2 = ''
            checkstr = '#'
            checklen = len(checkstr)
            if len(str) > checklen and str[0:checklen] == checkstr:
                for char in str[checklen:len(str)]:
                    if char == ' ':
                        if str2 == '':
                            continue
                        else:
                            break
                    else:
                        str2 += char
                mcf.add(s3.evalstr(str2, dic))
        mcf.save()


def set(command, value, dic):
    #用来创建文件的命令,然而现在并没有什么用了
    #set func <evalstr>
    #   <analyze>
    command = s3.partstr(command)
    if command[0] == 'func':
        c1 = s3.evalstr(command[1],dic)
        mcf = s3.func(c1)
        mcf.value = value
        mcf.save()
        mcf.analyze()


def for_(command, value, dic):
    #for循环,和python一模一样(可不是嘛)
    #for_ <nbt> in <eval>
    #   <analyze>
    command = s3.partstrhead(command, 2)
    c2 = s3.myeval(command[2], dic)
    list = []
    if command[1] == 'in':
        for range0 in c2:
            list.append(f'#let {command[0]} = {range0}')
            list += value
        return list
def if_(command, value, dic):
    #这一块也和python一模一样
    #if_ <eval>
    #   <analyze>
    if s3.myeval(command, dic):
        dic['if'] = True
        return value
    else:
        dic['if'] = False
        return []
def elif_(command, value, dic):
    #同上
    #elif_ <eval>
    #   <analyze>
    if dic['if'] == False:
        if s3.myeval(command, dic):
            dic['if'] = True
            return value
        else:
            return []
def else_(command, value, dic):
    #同上
    #else_
    #   <analyze>
    if dic['if'] == False:
        dic['if'] = True
        return value


def analyze(command, value, dic):
    #分析指定位置的mcf,并没有什么用
    #analyze func <evalstr>
    command = s3.partstr(command)
    if command[0] == 'func':
        mcf = s3.func(s3.evalstr(command[1],dic))
        mcf.load()
        mcf.analyze()


def let(command, value, dic):
    #可以用于赋值,接受后面或者缩进的内容
    #你可以用这个和puts制作函数
    #let <nbt> = <eval>
    command = s3.partstrhead(command, 2)
    if len(command) == 1:
        s3.setnbt(command[0], s3.mergelist(value), dic)
    else:
        if len(command)==2:
            command.append('')
        list = []
        if command[1] == '=':
            s3.setnbt(command[0], s3.myeval(command[2], dic),dic)


def mc(command, value, dic):
    #你可以在后面放上含有变量的mc命令
    #mc <evalstr>
    return [s3.evalstr(command,dic)]


def print_(command, value, dic):
    #解析一下后面的内容并print
    #print_ <eval>
    print(s3.myeval(command, dic))
    return 0


def run(command, value, dic):
    #在这里填写#run print(xx)也能实现上面的功能,而且你能在这里方便地使用s3_mcpack内的对象,注意这里不支持赋值或for或if之类的语句
    #run <eval>
    s3.myeval(command, dic)
    return 0


def put(command, value, dic):
    #把后面的内容以及缩进后的内容作为字符串放下来,不作任何操作(但是可能会再次被解析)
    #put <str>
    return [command] + value


def dic(command, value, dic):
    #操作文件以及dic下的变量
    #dic load json/predicate/... <evalstr>[ to <nbt>]   #默认从(json/predicate/...).<evalstr>中提取
    #dic load tag func/... <evalstr>[ to <nbt>]   #默认从tag.(func/...).<evalstr>中提取
    #dic save json/predicate/... <evalstr>[ from <nbt>]   #默认保存到(json/predicate/...).<evalstr>
    #dic save json/predicate/... <evalstr>[ value <eval>] #默认保存到(json/predicate/...).<evalstr>
    #dic save tag func/... <evalstr>[ from <nbt>]   #默认保存到tag.(func/...).<evalstr>
    #dic save tag func/... <evalstr>[ value <eval>] #默认保存到tag.(func/...).<evalstr>
    #dic set <nbt> from <nbt>    #等价于 #let <nbt> = getnbt('<nbt>',dic)
    #dic set <nbt> value <eval>  #等价于 #let <nbt> = <eval>
    #dic merge <nbt> from <nbt>
    #dic merge <nbt> value <eval>
    #dic remove <nbt>
    #列表操作其实可以用#run直接搞的
    #比如 #run setnbt('c',<a.b>[0:len(<a.b>)-1],dic)就是去掉列表a.b的最后一位再把剩下的赋给c
    #这个除了load和save外都能用#run直接搞的
    command = s3.partstr(command)
    c0 = command[0]
    c1 = command[1]
    if c0 == 'load':
        c2 = s3.evalstr(command[2], dic)
        if c1 == 'json':
            mcf = s3.mcjson('awa')
            mcf.path = c2+'.json'
            mcf.load()
            if len(command) > 3 and command[3] == 'to':
                s3.setnbt(command[4], mcf.value,dic)
            s3.setnbt('json.'+c2, mcf.value, dic)
            return 0
        jsons = ('predicate', 'advance', 'loot',
                 'recipe', 'dimension_type', 'dimension')
        if c1 in jsons:
            mcf = getattr(s3, c1)(c2)
            mcf.load()
            if len(command) > 3 and command[3] == 'to':
                s3.setnbt(command[4], mcf.value, dic)
            s3.setnbt(c1+'.'+c2, mcf.value, dic)
            return 0
        if c1 == 'tag':
            tags = ('func', 'block', 'entity','fluid')
            c3 = command[3]
            if c2 in tags:
                mcf = getattr(s3, c2)(c3)
                mcf.load()
                if len(command) > 4 and command[4] == 'to':
                    s3.setnbt(command[5], mcf.value, dic)
                s3.setnbt('tag.'+c2+'.'+c3, mcf.value, dic)
                return 0
            
    if c0 == 'save':
        c2 = s3.evalstr(command[2], dic)
        if c1 == 'json':
            mcf = s3.mcjson('awa')
            mcf.path = c2+'.json'
            if len(command) > 3 and command[3] == 'from':
                mcf.value = s3.getnbt(command[4], dic)
            elif len(command) > 3 and command[3] == 'value':
                mcf.value = s3.myeval(command[4], dic)
            else:
                mcf.value = s3.getnbt('json.'+c2, dic)
            mcf.save()
            return 0
        jsons = ('predicate', 'advance', 'loot',
                 'recipe', 'dimension_type', 'dimension')
        if c1 in jsons:
            mcf = getattr(s3, c1)(c2)
            if len(command) > 3 and command[3] == 'from':
                mcf.value = s3.getnbt(command[4], dic)
            elif len(command) > 3 and command[3] == 'value':
                mcf.value = s3.myeval(command[4], dic)
            else:
                mcf.value = s3.getnbt(c1+'.'+c2, dic)
            mcf.save()
            return 0
        if c1 == 'tag':
            tags = ('func', 'block', 'entity', 'fluid')
            c3 = command[3]
            if c2 in tags:
                mcf = getattr(s3, c2)(c3)
                if len(command) > 4 and command[4] == 'from':
                    mcf.value = s3.getnbt(command[5], dic)
                elif len(command) > 4 and command[4] == 'value':
                    mcf.value = s3.myeval(command[5], dic)
                else:
                    mcf.value = s3.getnbt('tag.'+c2+'.'+c3, dic)
                mcf.save()
                return 0
            
    if c0 == 'set':
        if command[2] == 'from':
            s3.setnbt(c1, s3.getnbt(command[3], dic), dic)
        if command[2] == 'value':
            s3.setnbt(c1, s3.myeval(command[3], dic), dic)
    if c0 == 'merge':
        if command[2] == 'from':
            s3.mergenbt(c1, s3.getnbt(command[3], dic), dic)
        if command[2] == 'value':
            s3.mergenbt(c1, s3.myeval(command[3], dic), dic)
    if c0 == 'remove':
        s3.removenbt(c1,dic)


def mcprint(command, value, dic):
    #简单的tellraw
    #mcprint <eval>
    #使用方法 mcprint [(<text>,<color>),..]
    list = s3.myeval(command, dic)
    if type(list)!=type([]):
        list = [list]
    jsonlist = []
    for Text in list:
        jsonlist.append({'text':Text[0],'color':Text[1]})
    str = 'tellraw @a '+ json.dumps(jsonlist)
    return [str]


def scb(command, value, dic):
    #没什么用的scb简写..
    #scb <0> <1> = <3>
    #scb <0> <1> = <3> <4>
    command = s3.partstr(s3.evalstr(command), dic)
    if command[2] == '=':
        if len(command) == 5:
            return [f'scoreboard players operation {command[0]} {command[1]} = {command[3]} {command[4]}']
        if len(command) == 4:
            #scb <0> <1> = (<a>+<b>)
            if '+' in command[3] or '-' in command[3] or '*' in command[3] or '/' in command[3] or '%' in command[3]:
                pass
            else:
                return [f'scoreboard players set {command[0]} {command[1]} {command[3]}']
    if command[2] in ['+=', '-=', '*=', '/=', '%=']:
        if len(command) == 5:
            return [f'scoreboard players operation {command[0]} {command[1]} {command[2]} {command[3]} {command[4]}']
        if len(command) == 4:
            return [f'scoreboard players set # tmp {command[3]}', f'scoreboard players operation {command[0]} {command[1]} {command[2]} # tmp']


def puts(command, value, dic):
    #把后面的内容解析后放下来,内容必须是字符串(可能会再次被解析)
    #你可以用这个和let制作函数
    #return_ <eval>
    return s3.partlines(s3.myeval(command,dic))
