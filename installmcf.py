# -*- coding: UTF-8 -*-
import s3_mcpack as s3
import os
packpath = ''
mcfpath = ''


while not os.path.exists(packpath):
    packpath = input('输入数据包文件夹路径(无输入则会在当前文件夹创建)')
    try:
        if packpath == '':
            packpath = os.getcwd()
        s3.mkfile(packpath)
    except:
        input('请输入一个正常点的路径...')


while not os.path.exists(mcfpath):
    mcfpath = input('输入要展开的mcfunction路径(无输入则会在当前文件夹创建load.mcfunction)')
    try:
        if mcfpath == '':
            mcfpath = os.path.join(os.getcwd(),'load.mcfunction')
        s3.mkfile(mcfpath)
    except:
        input('请输入一个正常点的路径...')

keep = input('原mcf的内容是否不变,不变则直接enter,否则输入任意符号后enter')

os.chdir(packpath)
input('数据包路径为: '+packpath+'\n待展开的mcf路径为: '+mcfpath+'\n按enter继续...')
s3.installpack(mcfpath,keep)
