# -*- coding: UTF-8 -*-
import os,json,re,math
import customfuncs
# 多少个空格算一次缩进
a_tab = '    '
the_dic = {'if': 0, 'json': {}, 'advance': {}, 'loot': {},
           'predicate': {}, 'recipe': {}, 'dimension_type': {}, 'dimension': {}, 'tag': {'func': {}, 'block': {}, 'entity': {}, 'fluid': {}}}




def mkfile(path):
    # print(path)
    filename = os.path.split(path)[0]
    if not os.path.exists(filename) and filename != '':
        os.makedirs(filename)
    if not os.path.exists(path):
        f = open(path, 'w', encoding='utf-8')
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
        match = re.match(
            r'([\#a-z0-9_\-][a-z0-9_\-\.]*):([a-z0-9_\-/\.]*)', self.name)
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
        f = open(path, 'w', encoding='utf-8')
        f.write(self.value)
        f.close()

    def load(self, path=''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, encoding='utf-8')
        self.value = f.read()
        f.close()


class mcjson(file):
    type = 'json'

    def save(self, path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, 'w', encoding='utf-8')
        f.write(json.dumps(self.value, indent=4))
        f.close()

    def load(self, path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, encoding='utf-8')
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
        for str0 in self.value:
            if str0 == name:
                self.value.remove(str0)
        self.value.append(name)
        
    def add_s(self, name):
        name = {"id": name, "required": False}
        self.add(name)
        
    def save(self, path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, 'w', encoding='utf-8')
        f.write(json.dumps({"replace": False, "values": self.value}, indent=4))
        f.close()
        
    def load(self, path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, encoding='utf-8')
        try:
            self.value = json.loads(f.read()).get('values')
        except:
            self.value =[]
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

def cuthash(list):
    list2 = []
    for str in list:
        if str[0] == '#':
            str = cutfirst(str)
        list2.append(str.replace(' ',''))
    return list2


def partstr(str):
    value = ['']
    hold_list = 0
    hold_dict = 0
    hold_bracket = 0
    hold_str = 0
    hold_str2 = 0
    for char in str:
        if char == '"':
            if hold_str == 0:
                hold_str = 1
            else:
                hold_str = 0
        if char == '\'':
            if hold_str2 == 0:
                hold_str2 = 1
            else:
                hold_str2 = 0
        if char == '[':
            hold_list += 1
        if char == ']':
            hold_list -= 1
        if char == '{':
            hold_dict += 1
        if char == '}':
            hold_dict -= 1
        if char == '(':
            hold_bracket += 1
        if char == ')':
            hold_bracket -= 1
        if char == ' ' and hold_list <= 0 and hold_bracket <= 0 and hold_dict <= 0 and hold_str == 0 and hold_str2 == 0:
            value.append('')
        else:
            if char != ' ':
                value[-1] += char
    return re_empty(value)


def partstrhead(str,count):
    value = ['']
    for char in str:
        if char == ' ' and len(value)<=count:
            value.append('')
        else:
            value[-1] += char
    return re_empty(value)


def myeval(str,dic):
    str2 = ''
    i = 0
    while i < len(str):
        if str[i] == '<':
            i += 1
            if str[i] != ' ' or '\t':
                str1 = ''
                while str[i] != '>':
                    str1 += str[i]
                    i += 1
                str2 += translatenbt(str1)
            else:
                str2 += '<' + str[i]
        else:
            str2 += str[i]
        i += 1
    try:
        return eval(str2)
    except:
        return str2
    
            


def evallist(list,dic):
    list2 = []
    for str in list:
        list2.append(myeval(str, dic))
    return list2


def evalstr(command, dic):
    a_str = ''
    pattern = re.compile(r"(<[^ ]+?>|f\{.+?\})")
    list = pattern.split(command)
    list2 = pattern.findall(command)
    for str2 in list:
        if str2 in list2:
            match = re.match(r'f\{(.+?)\}', str2)
            if match:
                str2 = match.group(1)
            a_str += str(myeval(str2, dic))
        else:
            a_str += str(str2)
    return a_str
    

class customfunc:
    def __init__(self,commandstr):
        commandstr = cutfirst(commandstr)
        command = partstrhead(commandstr,1)
        try:
            self.name = command[0]
        except:
            self.name = ''
        try:
            self.command = command[1]
        except:
            self.command = ''
        # print(self.name,'\n',self.command)
        self.value = []
        self.function = getattr(customfuncs, self.name, None)

    def execute(self, dic):
        return self.function(self.command, self.value, dic)


def cutfuncs(value):
    #切完后只有cusfunc和普通的字符串
    funcs = []
    for line in value:
        #如果全是空格
        if line.count(' ') == len(line):
            funcs.append(line)
        #如果是注释
        elif line[0] == '#':
            cusfunc = customfunc(line)
            if hasattr(cusfunc.function, '__call__'):
                funcs.append(cusfunc)
            else:
                funcs.append(line)
        #如果是缩进
        elif line[0:len(a_tab)] == a_tab:
            try:
                funcs[-1].value.append(cuttab(line))
            except:
                funcs.append(line)
        else:
            funcs.append(line)
    return funcs


def analyzefuncs(value,path,dic = the_dic):
    #输入字符串列表和函数路径名,返回解析完的字符串列表
    dic['path'] = path
    list0 = []
    for line in cutfuncs(value):
        #如果这一行是cusfunc
        if type(line) == customfunc:
            alist = line.execute(dic)  # 函数在这里运行
            # # 如果返回值是元组，取出dic
            # if type(alist) == type((1, 2)):
            #     dic = alist[1]
            #     print('是否相等:',dic.__eq__(alist[1]))
            #     alist = alist[0]
            # 如果返回值是字符串列表，递归
            if type(alist) == type([]):
                list0 = list0 + analyzefuncs(alist, path, dic)
        #如果是普通字符串
        else:
            list0.append(line)
    return list0


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
        f = open(path, 'w', encoding='utf-8')
        for line in self.value:
            f.write(line+'\n')
        f.close()

    def load(self,path = ''):
        if path == '':
            path = self.path
        mkfile(path)
        f = open(path, encoding='utf-8')
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

    def analyze(self, dic=the_dic):
        self.value = analyzefuncs(self.value,self.name,dic)
        self.save()

    
def installpack(path, keep=''):
    mcf = func('awa')
    mcf.path = path
    mcf.load()
    save = mcf.value
    mcf.analyze()
    if keep == '':
        mcf.value = save
        mcf.save()



def mergelist(list):
    # 将字符串列表转化为带换行的字符串
    str0 = ''
    for str1 in list:
        str0 += str1+'\n'
    return str0


def partlines(str0):
    # 将带换行的字符串去掉换行并变成字符串列表
    return str0.split('\n')


def dicUpdate(old_dic, new_dic):
    oldkeys = old_dic.keys()
    newkeys = new_dic.keys()
    for key in newkeys:
        if not ((key in oldkeys) and (type(old_dic[key]) == type({})) and (new_dic[key] == type({}))):
            old_dic[key] = new_dic[key]
        else:
            old_dic[key] = dicUpdate(old_dic[key], new_dic[key])
    return old_dic


def listgetdic(dic0, strlist):
    if len(strlist) == 0:
        return dic0
    if len(strlist)==1:
        return dic0[strlist[0]]
    elif len(strlist) > 1:
        return listgetdic(dic0[strlist[0]],strlist[1:len(strlist)])


def listsetdic(dic0, strlist, value):
    if len(strlist) == 0:
        dic0=value      #然而并没有什么用
    if len(strlist) == 1:
        dic0[strlist[0]] = value
    if len(strlist) > 1:
        if not strlist[0] in dic0.keys():
            dic0[strlist[0]] = {}
        listsetdic(dic0[strlist[0]], strlist[1:len(strlist)],value)


def getnbt(nbt, dic):
    #输入a.b.c等价于dic['a']['b']['c']
    return listgetdic(dic,splitnbt(nbt))
def setnbt(nbt, value, dic):
    #输入a.b.c等价于dic['a']['b']['c']
    #作用:若输入setnbt('a.b.c','d.e.f',dic)将a.b.c的值改为d.e.f的值,若a.b.c不存在将会创建,若类型不同将会覆盖
    return listsetdic(dic, splitnbt(nbt), value)
def mergenbt(nbt, value, dic):
    #输入a.b.c等价于dic['a']['b']['c']
    try:
        getnbt(nbt, dic)
    except:
        setnbt(nbt, {}, dic)
    old = splitnbt(nbt)
    olddic = listgetdic(dic, old[0:len(old)-1])
    if (type(olddic[old[-1]]) == type({})) and (type(value) == type({})):
        #如果它们都是字典
        dicUpdate(olddic[old[-1]], value)
    else:
        olddic[old[-1]] = value
def removenbt(nbt, dic):
    #输入a.b.c等价于dic['a']['b']['c']
    nbt = splitnbt(nbt)
    nbtdic = listgetdic(dic, nbt[0:len(nbt)-1])
    del(nbtdic[nbt[-1]])

def translatenbt(nbt):
    #输入a.b.c等价于dic['a']['b']['c']
    # 输入a[n].c呢==>dic['a'][n]['c']
    str0="dic"
    s = 0
    i = 0
    while i < len(nbt):
        if nbt[i]=='.':
            if s == 1:
                str0 += "']"
            s = 1
            i += 1
            str0 += "['"
        elif nbt[i] == '[':
            if s == 1:
                str0 += "']"
            s = 2
        if s==0:
            str0+="['"
            s=1
        str0 += nbt[i]
        i += 1
    if s == 1:
        str0 += "']"
    return str0


def splitnbt(nbt):
    #输入a.b.c等价于['a','b','c']
    # 输入a[n].c呢==>['a',n,'c']
    list0 = ['']
    i = 0
    while i < len(nbt):
        if nbt[i] == '.':
            list0.append('')
            i+=1
        elif nbt[i] == '[':
            if i==0:
                list0.pop()
            str0=''
            i += 1
            while nbt[i]!=']'and i<len(nbt):
                str0 += nbt[i]
                i += 1
            list0.append(int(str0))
        if nbt[i]!=']':
            list0[-1] += nbt[i]
        i += 1
    return list0


def log2_p(num):
    return math.ceil(math.log2(abs(num)))

def mystr(a):
    return str(a)


def myint(a):
    return int(a)
