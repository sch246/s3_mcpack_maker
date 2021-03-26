# -*- coding: UTF-8 -*-
import os,json,re
import customfuncs
# 多少个空格算一次缩进
a_tab = '    '


def mkfile(path):
    filename = os.path.split(path)[0]
    if not os.path.exists(filename):
        os.makedirs(filename)
    if not os.path.exists(path):
        f = open(path, 'w')
        f.close()
    

class file:
    type = 'txt'
    type_path = 'file'
    name = None
    path = None
    space = None
    space_path = None
    value = None
    def __init__(self, str):
        self.setname(str)

    def setname(self, str):
        self.name = str
        self.__getpath()
        self.__setpath()

    def __getpath(self):
        match = re.match(r'([a-z0-9_\-]*):([a-z0-9_\-/\.]*)', self.name)
        if match != None:
            self.space = match.group(1).replace('#', '')
            self.space_path = match.group(2)
        else:
            match = re.match(r'(.*)', self.name)
            if match != None:
                self.space = 'minecraft'
                self.space_path = match.group(1).replace('#','')
  
    def __setpath(self):
        self.path = f'data/{self.space}/{self.type_path}/{self.space_path}.{self.type}'

    def save(self, path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, 'w')
        f.write(self.value)
        f.close()

    def load(self, path=''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path)
        self.value = f.read()
        f.close()


class mcjson(file):
    type = 'json'

    def save(self, path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, 'w')
        f.write(json.dumps(self.value, indent=4))
        f.close()

    def load(self, path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path)
        self.value = json.loads(f.read())
        f.close()

    def print(self):
        print('\n========================')
        print('name: ' + self.name)
        print('type_path: ' + self.type_path)
        print('path: ' + self.path)
        print('space: ' + self.space)
        print('space_path: ' + self.space_path)
        print('value: \n' + json.dumps(self.value, indent=4))


class advance(mcjson):
    type_path = 'advancements'
class loot(mcjson):
    type_path = 'loot_tables'
class predicate(mcjson):
    type_path = 'predicates'
class recipe(mcjson):
    type_path = 'recipes'
class dimension_type(mcjson):
    type_path = 'dimension_type'
class dimension(mcjson):
    type_path = 'dimension'

class tag(mcjson):
    type_path = 'tags'

    def __init__(self, str):
        self.setname(str)
        self.value = []

    def add(self, name):
        for str in self.value:
            if str == name:
                list.remove(str)
        self.value.append(name)
        
    def add_s(self, name):
        name = {"id": name, "required": False}
        self.add(name)
        
    def save(self, path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, 'w')
        f.write(json.dumps({"replace": False, "values": self.value}, indent=4))
        f.close()
        
    def load(self, path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path)
        self.value = json.loads(f.read()).get('values')
        f.close()


class functag(tag):
    type_path = 'tags/functions'
class entitytag(tag):
    type_path = 'tags/entity_types'
class blocktag(tag):
    type_path = 'tags/blocks'
class fluidtag(tag):
    type_path = 'tags/fluids'
        



def cutfirst(str):
    return str[1: len(str)]

def cuttab(str):
    return str[len(a_tab): len(str)]

def re_empty(list):
    list2 = []
    for str in list:
        if str != '':
            list2.append(str)
    return list2


def partstr(str):
    value = ['']
    hold_list = False
    hold_dict = False
    hold_bracket = False
    for char in str:
        if char == '[':
            hold_list == True
        if char == ']':
            hold_list == False
        if char == '{':
            hold_dict == True
        if char == '}':
            hold_dict == False
        if char == '(':
            hold_bracket == True
        if char == ')':
            hold_bracket == False
        if char == ' ' and hold_list == False and hold_bracket == False and hold_dict == False:
            value.append('')
        else:
            if char != ' ':
                value[-1] += char
        value2 = []
        for str in re_empty(value):
            try:
                value2.append(eval(str))
            except:
                value2.append(str)
    return value2



class customfunc:
    def __init__(self,commandstr):
        self.command = partstr(commandstr)
        self.name = self.command[0]
        # print(self.name,type(self.name))
        self.value = []
        self.function = getattr(customfuncs, self.name, None)

    def execute(self):
        self.function(self.command, self.value)



class func(file):
    type = 'mcfunction'
    type_path = 'functions'

    def __init__(self, str):
        self.setname(str)
        self.value = []

    def save(self, path=''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, 'w')
        for line in self.value:
            f.write(line+'\n')
        f.close()

    def load(self,path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path)
        self.value = []
        for line in f.readlines():
            self.value.append(line.replace('\n', ''))
        f.close()
            


    def print(self):
        print('\n========================')
        print('name: '+self.name)
        print('type_path: ' + self.type_path)
        print('path: '+self.path)
        print('space: '+self.space)
        print('space_path: '+self.space_path)
        print('value: {')
        for line in self.value:
            print(line)
        print('}')

    def analyze(self):
        again = 0
        funcs = []
        for line in self.value:
            if line.count(' ') == len(line):
                funcs.append(line)
            elif line[0] == '#':
                line = cutfirst(line)
                cusfunc = customfunc(line)
                if hasattr(cusfunc.function, '__call__'):
                    funcs.append(cusfunc)
                else:
                    funcs.append(line)
            elif line[0:len(a_tab)] == a_tab:
                try:
                    funcs[-1].value.append(cuttab(line))
                except:
                    print('out')
            else:
                funcs.append(line)
        # print(json.dumps(self.value, indent=4))
        # print(json.dumps(mcf.value, indent=4))
        self.value = []
        flag = ''
        for mcfunc in funcs:
            if type(mcfunc) == customfunc:
                #通过返回值决定是否重复运行
                alist = mcfunc.function(mcfunc.command, mcfunc.value, flag)
                if type(alist) == type((1,2)):
                    flag = alist[1]
                    alist = alist[0]
                if type(alist)==type([]):
                    for str in alist:
                        if type(str)==type(' '):
                            self.value.append(str)
                            again += 1
            else:
                self.value.append(mcfunc)
        self.save()
        if again >= 1:
            self.analyze()
        

def installpack(path):
    mcf = func('awa')
    mcf.path = path
    mcf.load()
    save = mcf.value
    mcf.analyze()
    mcf.value = save
    mcf.save()