# 从fispact输出文件中读取光谱信息
# 输入：文件地址
# 输出：list[model.energyDis *24]

import re, os
from .model import energyDis

def readFisp(path):
    folders = os.listdir(path)
    allDistributes = {}
    for folder in folders:
        files = os.listdir(path + '/' +folder)
        for file in files:
            if file[-2:] == '.o':
                with open(path + '/' +folder + '/' + file) as f:
                    allItem = f.read()
                    distributes, gamma = extractPrec(allItem)
                    allDistributes[folder] = [gamma, distributes]
    return distributes

def extractPrec(allItem):
    distributes = []
    patten = re.compile(r'\(0.0 -0.01 {2}MeV\).+?DOSE',re.S)
    targetPart = patten.findall(allItem)[-1]

    patten = re.compile(r'Total gammas \(per cc per second\) {6}\d\.\d{5}E[+-]\d{2}')
    tmp = patten.findall(allItem)[-1]
    patten = re.compile(r'\d.\d+E[+-]\d*')
    gamma = float(patten.findall(tmp)[0])

    patten = re.compile(r'\d.\d+E[+-]\d*')
    items = patten.findall(targetPart)
    items = [items[i] for i in range(len(items)) if i%2 == 1]

    patten = re.compile(r'\(\d+.\d+ *-+>?\d*.*\d* *MeV\)')
    bound = patten.findall(targetPart)

    for i, item in enumerate(items):
        distribute = energyDis()
        patten = re.compile(r'\d{1,2}\.\d{1,2}')
        result = patten.findall(bound[i])
        distribute.leftBound = float(result[0])
        # 这里用max替代20
        distribute.rightBound = float(result[1]) if len(result) == 2 else 20.
        patten = re.compile(r'\d.\d{5}E[+-]\d{2}')
        distribute.perc = float(item)
        distributes.append(distribute)
        return gamma, distributes
