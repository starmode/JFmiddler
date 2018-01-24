# 利用neutron和allStructure生成fispact输入文件
# 输入：文件地址，neutron，allStructure
# 输出：无

import os, re
from .model import ele, Avogadro, defaultInput, defaultArrayx, defaultCollapx, defaultPrintlib

def _genElements(element, eleDensity, allDensity):
    return ' %s %f\n' % (ele[element[2]], 100 * eleDensity[element[0]] / allDensity)

def _mkdir(path):
    # 仅内部调用
    # 在完整路径处新建文件夹
    # path--input--建立文件夹位置
    # *--output--bool,是否成功建立文件夹
    assert type(path) == str
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False

def _collapx(text, cell, path):
    # 仅内部调用
    # 生成FISPACT输入文件collapx.i
    # text--input--初始化文件内容
    # cell--input--材料名称
    # path--input--FISPACT输入文件顶层路径
    assert type(text) == str
    assert type(cell) == str
    assert type(path) == str
    _mkdir(path + '/' + cell)
    mode = re.compile('{[ \t\n]*title[ \t\n]*}')
    text = mode.sub('Irradiation of ' + cell, text)
    with open(path + '/' + cell + '/collapx.i', 'w') as f:
        f.write(text)

def _arrayx(text, cell, path):
    # 仅内部调用
    # 生成FISPACT输入文件arrayx.i
    # text--input--初始化文件内容
    # cell--input--材料名称
    # path--input--FISPACT输入文件顶层路径
    _mkdir(path + '/' + cell)
    mode = re.compile('{[ \t\n]*title[ \t\n]*}')
    text = mode.sub('Irradiation of ' + cell, text)
    with open(path + '/' + cell + '/arrayx.i', 'w') as f:
        f.write(text)

def _printlib(text, cell, path):
    # 仅内部调用
    # 生成FISPACT输入文件printlib.i
    # text--input--初始化文件内容
    # cell--input--材料名称
    # path--input--FISPACT输入文件顶层路径
    _mkdir(path + '/' + cell)
    mode = re.compile('{[ \t\n]*title[ \t\n]*}')
    text = mode.sub('Irradiation of ' + cell, text)
    with open(path + '/' + cell + '/printlib.i', 'w') as f:
        f.write(text)

def _input(text, neutron, allStructure, cell, genRate, path):
    # 仅内部调用
    # 生成FISPACT输入文件input.i
    # text--input--初始化文件内容
    # neutron--input--由JMCT输出文件读取的所有材料物质信息
    # allStructure--input--由GDML文件读取的所有材料物质信息
    # cell--input--材料名称
    # genRate--input--光子产生速度
    # path--input--FISPACT输入文件顶层路径
    _mkdir(path + '/' + cell)
    eleDensity = {}
    allDensity = 0.
    for element in allStructure[cell].matGre:
        tmp = element[1] * element[3] / Avogadro
        allDensity += tmp
        eleDensity[element[0]] = tmp
    # 计算DENSITY
    # 单位g/cm^3
    density = '%E' % allDensity
    # 写入MASS
    tmp = float(allStructure[cell].matD) * float(neutron.cellInfo[cell][1])
    # 字符串mass
    mass = '%E' % tmp
    elements = ['%d\n' % len(allStructure[cell].matGre)]
    # 此处需要map优化
    matLen = len(allStructure[cell].matGre)
    eleDensityList = [eleDensity] * matLen
    allDensityList = [allDensity] * matLen

    elements = list(map(_genElements, allStructure[cell].matGre, eleDensityList, allDensityList))
    tmp = ['%d\n' % len(allStructure[cell].matGre)]
    tmp.extend(elements)
    elements = tmp
    # for element in allStructure[cell].matGre:
    #     elements.append(' %s %f\n' % (ele[element[2]], 100 * eleDensity[element[0]]/allDensity))
    # 字符串elements
    elements = ''.join(elements)[:-1]
    # 计算中子通量
    flux = 'FLUX %E' % (neutron.cellInfo[cell][0] * genRate)

    # 替换
    mode = re.compile('{[ \t\n]*title[ \t\n]*}')
    text = mode.sub('Irradiation of ' + cell, text)
    mode = re.compile('{[ \t\n]*mass[ \t\n]*}')
    text = mode.sub(mass, text)
    mode = re.compile('{[ \t\n]*density[ \t\n]*}')
    text = mode.sub(density, text)
    mode = re.compile('{[ \t\n]*flux[ \t\n]*}')
    text = mode.sub(flux, text)
    mode = re.compile('{[ \t\n]*elements[ \t\n]*}')
    text = mode.sub(elements, text)

    with open(path + '/' + cell + '/input.i', 'w') as f:
        f.write(text)


def writef(path, genRate, neutron, allStructure, _inputText = defaultInput, _collapxText = defaultCollapx, _arrayxText = defaultArrayx, _printlibText = defaultPrintlib):
    # 生成FISPACT输入文件
    # ?text--input--初始化文件内容
    # neutron--input--由JMCT输出文件读取的所有材料物质信息
    # allStructure--input--由GDML文件读取的所有材料物质信息
    # genRate--input--光子产生速度
    # path--input--FISPACT输入文件顶层路径
    for cell in neutron.cellInfo.keys():
        _input(_inputText, neutron, allStructure, cell, genRate, path)
        _collapx(_collapxText, cell, path)
        _arrayx(_arrayxText, cell, path)
        _printlib(_printlibText, cell, path)

