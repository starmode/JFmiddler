# 从jmct输出文件读取栅元信息
# 输入：文件地址
# 输出：model.Data实例neutron

import re

from .model import Data


def _m2ev(raw, flag):
    # 仅内部调用
    # 将MeV转换为eV
    # raw--input--list，原始数据集合
    # flag--input--str，'e'或'E'，科学记数法的表示方式
    # result--output--list，处理后的数据集合
    assert type(raw) == list
    assert type(flag) == str
    result = []
    for i in range(len(raw)):
        tmp = raw[i].split(flag)
        if len(tmp) == 1:
            raw[i] = float(tmp[0]) * 1000000
        else:
            raw[i] = float(tmp[0]) * (10 ** (6 + int(tmp[1])))
        tmp = '%E' % raw[i]
        tmp = tmp.replace('+', '')
        mode = re.compile(r'E0+$')
        tmp = mode.sub('', tmp)
        mode = re.compile(r'E0+')
        tmp = mode.sub('E', tmp)
        mode = re.compile(r'E-0+')
        tmp = mode.sub('E-', tmp)
        result.append(tmp)
    return result

def readj(path):
    # 读取JMCT输出文件并解析出各材料物质信息
    # path--input--JMCT输出文件位置
    # neutron--output--所有材料物质信息
    assert type(path) == str
    neutron = Data('Transporting')
    with open(path, 'r') as f:
        allItem = f.read()
        mode = re.compile(r'energy_bin[ \de\-,=.]+')
        mid = mode.search(allItem).group(0)
        mid = mid.replace(' ', '')
        mid = mid.strip('energy_bin=')
        mode = re.compile(r'^/c+$')
        mid = mode.sub('', mid)
        mid = mid.split(',')
        neutron.eneBin = _m2ev(mid, 'e')
        neutron.eneNum = len(neutron.eneBin)

        # 几何体相关信息储存
        mode = re.compile('Tally4_0,(.+?)---', re.S)
        mid = mode.findall(allItem)
        name = []
        energy = []
        volume = []
        # 储存关心的几何体数量
        neutron.cellNum = len(mid)
        for i in range(neutron.cellNum):
            mode = re.compile(r'cell: (.+?),', re.S)
            if mode.search(mid[i]).group(0)[6:-1] != 'World':
                name.append(mode.search(mid[i]).group(0)[6:-1])
                # 储存每个几何体的中子通量
                mode = re.compile(r'total +\d.\d+e[+-]\d{2,3}')
                temp = mode.findall(mid[i])
                energy.append(float(temp[0][16:]))
                # 储存每个几何体的体积
                mode = re.compile(r'volume\(cm\^3\): \d+.\d+e?[+-]?\d{0,2}')
                temp = mode.search(mid[i]).group(0)
                volume.append(float(temp[14:]))
            neutron.cellInfo = dict(zip(name, zip(energy, volume)))
    return neutron
