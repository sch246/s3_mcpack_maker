# -*- coding: UTF-8 -*-
import os
import s3_mcpack as s3


def setfunc(command, value, dic={}):
    mcf = s3.func(command[1])
    mcf.value = value
    mcf.save()
    mcf.analyze()
    

def set(command, value, dic={}):
    if command[1] == 'func':
        mcf = s3.func(command[2])
        mcf.value = value
        mcf.save()
        mcf.analyze()
    if command[1] == 'tag':
        if command[2] == 'block':
            mcf = s3.blocktag(command[3])
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
        if command[2] == 'func':
            mcf = s3.functag(command[3])
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
        if command[2] == 'entity':
            mcf = s3.entitytag(command[3])
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
        if command[2] == 'fluid':
            mcf = s3.fluidtag(command[3])
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
    command = s3.evallist(command)
    list = []
    obj = command[1]
    if command[2] == 'in':
        for range0 in command[3]:
            for line in value:
                list.append(line.replace(str(obj), str(range0)))
        return list
def if_(command, value, dic={}):
    command = s3.evallist(command)
    if command[1]:
        return value, ''
    else:
        return [], 'if_false'
def elif_(command, value, flag):
    command = s3.evallist(command)
    if flag == 'if_false':
        if command[1]:
            return value, ''
        else:
            return [], 'if_false'
def else_(command, value, flag):
    command = s3.evallist(command)
    if flag == 'if_false':
        return value, ''


def analyze(command, value=[], dic={}):
    if command[1] == 'func':
        mcf = s3.func(command[2],)
        mcf.load()
        mcf.analyze()


def let(command, value, dic={}):
    list = []
    obj = command[1]
    if command[2] == '=':
        for line in value:
            list.append(line.replace(obj,str(eval(command[3]))))
        return list


 
def mc(command, value=[], dic={}):
    a_str = command[1]
    for obj in command[2:len(command)]:
        a_str += ' ' + obj
    return [a_str]
