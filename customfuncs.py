# -*- coding: UTF-8 -*-
import os
import s3_mcpack as s3


def setfunc(command, value, flag=''):
    mcf = s3.func(command[1])
    mcf.value = value
    mcf.save()
    mcf.analyze()


def mcfor(command, value, flag=''):
    list = []
    obj = command[1]
    if command[2] == 'in':
        for range0 in command[3]:
            for line in value:
                list.append(line.replace(str(obj), str(range0)))
        return list


def analyze(command, value=[], flag=''):
    mcf = s3.func(command[1],)
    mcf.load()
    mcf.analyze()


def let(command, value, flag=''):
    list = []
    obj = command[1]
    if command[2] == '=':
        for line in value:
            list.append(line.replace(str(obj),str(command[3])))
        return list


def mcif(command, value, flag=''):
    if command[1]:
        return value, ''
    else:
        return [], 'if_false'
def mcelif(command, value, flag):
    if flag == 'if_false':
        if command[1]:
            return value, ''
        else:
            return [], 'if_false'
def mcelse(command, value, flag):
    if flag == 'if_false':
        return value, ''


def mc(command, value=[], flag=''):
    a_str = str(command[1])
    for obj in command[2:len(command)]:
        a_str += ' ' + str(obj)
    return [a_str]


def setblocktag(command, value, flag=''):
    mcf = s3.blocktag(command[1])
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


def setfunctag(command, value, flag=''):
    mcf = s3.functag(command[1])
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


def setentitytag(command, value, flag=''):
    mcf = s3.entitytag(command[1])
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


def setfluidtag(command, value, flag=''):
    mcf = s3.fluidtag(command[1])
    mcf.print()
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
