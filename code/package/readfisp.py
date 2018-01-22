# 从fispact输出文件中读取光谱信息
# 输入：文件地址
# 输出：list[model.energyDis *24]

import re, os
from .model import energyDis


def readf(path, maxFlag = 20.):
    # 读取FISPACT输出文件并解析出所有材料的光谱分布
    # path--input--FISPACT输出文件顶层目录
    # maxFlag--input--光子分布无穷大等效值
    # allDistributes--output--提取出的所有材料的光谱类
    if type(maxFlag) == int:
        maxFlag = float(maxFlag)

    assert type(path) == str
    assert type(maxFlag) == float or int

    folders = os.listdir(path)
    allDistributes = {}
    for folder in folders:
        files = os.listdir(path + '/' +folder)
        for file in files:
            if file[-2:] == '.o':
                with open(path + '/' + folder + '/' + file) as f:
                    allItem = f.read()
                    distributes, gamma = _extractPrec(allItem, maxFlag)
                    allDistributes[folder] = [gamma, distributes]
    return allDistributes

def _extractPrec(allItem, maxFlag = 20.):
    # 仅内部调用
    # 从FISPACT输出文件特定的文本中解析出光谱
    # allItem--input--某FISPACT文件内容
    # maxFlag--input--光子分布无穷大等效值
    # gamma--output--光子产额总量
    # distributes--output--提取出的一种材料的光谱类
    assert type(allItem) == str
    assert type(maxFlag) == float

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
        distribute.rightBound = float(result[1]) if len(result) == 2 else maxFlag
        patten = re.compile(r'\d.\d{5}E[+-]\d{2}')
        distribute.perc = float(item)
        distributes.append(distribute)
    return gamma, distributes
