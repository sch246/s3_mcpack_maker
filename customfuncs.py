# -*- coding: UTF-8 -*-
import os,re
import s3_mcpack as s3


def setfunc(command, value, dic={}):
    mcf = s3.func(command)
    mcf.value = value
    mcf.save()
    mcf.analyze()
    

def set(command, value, dic={}):
    command = s3.partstr(command)
    if command[0] == 'func':
        mcf = s3.func(command[1])
        mcf.value = value
        mcf.save()
        mcf.analyze()
    if command[0] == 'tag':
        if command[1] == 'block':
            mcf = s3.blocktag(command[2])
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
                    mcf.value.append(str2)
            mcf.save()
        if command[1] == 'func':
            mcf = s3.functag(command[2])
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
                    mcf.value.append(str2)
            mcf.save()
        if command[1] == 'entity':
            mcf = s3.entitytag(command[2])
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
                    mcf.value.append(str2)
            mcf.save()
        if command[1] == 'fluid':
            mcf = s3.fluidtag(command[2])
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
                    mcf.value.append(str2)
            mcf.save()




def for_(command, value, dic={}):
    command = s3.evallist(s3.partstr(command))
    list = []
    obj = command[0]
    if command[1] == 'in':
        for range0 in command[2]:
            for line in value:
                list.append(line.replace(str(obj), str(range0)))
        return list
def if_(command, value, dic={}):
    if eval(command):
        dic['if'] = True
        return value, dic
    else:
        dic['if'] = False
        return [], dic
def elif_(command, value, dic):
    if dic['if'] == False:
        if eval(command):
            dic['if'] = True
            return value, dic
        else:
            return []
def else_(command, value, dic):
    if dic['if'] == False:
        dic['if'] = True
        return value, dic


def analyze(command, value=[], dic={}):
    command = s3.partstr(command)
    if command[0] == 'func':
        mcf = s3.func(command[1])
        mcf.load()
        mcf.analyze()


def let(command, value=[], dic={}):
    command = s3.partstrhead(command,2)
    list = []
    obj = command[0]
    if command[1] == '=':
        dic[obj] = eval(command[2])
        for line in value:
            list.append(line.replace(obj,str(eval(command[2]))))
        return list, dic


def mc(command, value=[], dic={}):
    a_str = ''
    for str2 in re.split(r'(dic\[.+\])', command):
        if re.match(r'dic\[.+\]', str2):
            a_str += str(eval(str2))
        else:
            a_str += str2
    return [a_str]


def print_(command, value, dic={}):
    print(eval(command))
    return 0
