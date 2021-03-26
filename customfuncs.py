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
