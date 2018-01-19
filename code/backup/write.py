# 利用neutron和allStructure生成fispact输入文件
# 输入：文件地址，neutron，allStructure
# 输出：无
## 大修改
import pickle
import re
from model import ele, Avogadro
import os


with open('neutron', 'rb') as f:
    neutron = pickle.load(f)

with open('structure', 'rb') as f:
    allStructure = pickle.load(f)


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def collapx(text, cell, path):
    mkdir(path + '/' +cell)
    with open('collapx.i', 'w') as f:
        mode = re.compile('{[ \t\n]*title[ \t\n]*}')
        text = mode.sub('* Irradiation of ' + cell, text)
        f.write(text)

def arrayx(text, cell, path):
    mkdir(path + '/' + cell)
    with open(path + '/' + cell + '/arrayx.i', 'w') as f:
        mode = re.compile('{[ \t\n]*title[ \t\n]*}')
        text = mode.sub('* Irradiation of ' + cell, text)
        f.write(text)

def printlib(text, cell, path):
    mkdir(path + '/' + cell)
    with open(path + '/' + cell + '/printlib.i', 'w') as f:
        mode = re.compile('{[ \t\n]*title[ \t\n]*}')
        text = mode.sub('* Irradiation of ' + cell, text)
        f.write(text)

def input(text, cell, genRate, path):
    mkdir(path + '/' + cell)
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
        text = mode.sub('* Irradiation of ' + cell, text)
        mode = re.compile('{[ \t\n]*mass[ \t\n]*}')
        text = mode.sub(mass, text)
        mode = re.compile('{[ \t\n]*density[ \t\n]*}')
        text = mode.sub(density, text)
        mode = re.compile('{[ \t\n]*flux[ \t\n]*}')
        text = mode.sub(flux, text)
        mode = re.compile('{[ \t\n]*elements[ \t\n]*}')
        text = mode.sub(elements, text)
        f.write(text)

text = '''NOHEAD\nMONITOR 1\nAINP\nFISPACT\n{title}\nDENSITY {density}\nMASS {mass} {elements}\nMIND 1.0\nHALF\nGRAPH 2 0 0 1 2\n{flux}
ATOMS\nLEVEL 100 1\nTIME 1.0\nHALF\nDOSE 1\nATOMS\nNOSTABLE\nLEVEL 20 1\nFLUX 0.\nZERO\nTIME 1.0 HOURS ATOMS
END\n* END\n/*\n'''

for cell in neutron.cell_info.keys():
    input(text, cell, 7.8E18, '.')
