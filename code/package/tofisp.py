# 利用neutron和allStructure生成fispact输入文件
# 输入：文件地址，neutron，allStructure
# 输出：无

import os, re
from .model import ele, Avogadro, defaultInput, defaultArrayx, defaultCollapx, defaultPrintlib

def _mkdir(path):
    #
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def _collapx(text, cell, path):
    _mkdir(path + '/' + cell)
    with open(path + '/' + cell + '/collapx.i', 'w') as f:
        mode = re.compile('{[ \t\n]*title[ \t\n]*}')
        text = mode.sub('Irradiation of ' + cell, text)
        f.write(text)

def _arrayx(text, cell, path):
    _mkdir(path + '/' + cell)
    with open(path + '/' + cell + '/arrayx.i', 'w') as f:
        mode = re.compile('{[ \t\n]*title[ \t\n]*}')
        text = mode.sub('Irradiation of ' + cell, text)
        f.write(text)

def _printlib(text, cell, path):
    _mkdir(path + '/' + cell)
    with open(path + '/' + cell + '/printlib.i', 'w') as f:
        mode = re.compile('{[ \t\n]*title[ \t\n]*}')
        text = mode.sub('Irradiation of ' + cell, text)
        f.write(text)

def _input(text, neutron, allStructure, cell, genRate, path):
    _mkdir(path + '/' + cell)
    with open(path + '/' + cell + '/input.i', 'w') as f:
        ## 此处修改
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
        tmp = float(allStructure[cell].matD) * float(neutron.cell_info[cell][1])
        # 字符串mass
        mass = '%E' % tmp
        elements = ['%d\n' % len(allStructure[cell].matGre)]
        # 这里修改下用原子序数查找元素简称，不要直接读取
        for element in allStructure[cell].matGre:
            elements.append(' %s %f\n' % (ele[element[2]], 100 * eleDensity[element[0]]/allDensity))
        # 字符串mass
        elements = ''.join(elements)[:-1]
        # 计算中子通量
        flux = 'FLUX %E' % (neutron.cell_info[cell][0] * genRate)

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
        f.write(text)


def writef(path, genRate, neutron, allStructure, _inputText = defaultInput, _collapxText = defaultCollapx, _arrayxText = defaultArrayx, _printlibText = defaultPrintlib):
    for cell in neutron.cell_info.keys():
        _input(_inputText, neutron, allStructure, cell, genRate, path)
        _collapx(_collapxText, cell, path)
        _arrayx(_arrayxText, cell, path)
        _printlib(_printlibText, cell, path)

