# 从jmct输出文件读取栅元信息
# 输入：文件地址
# 输出：model.Data实例neutron

import pickle
import re

from .model import Data, ele


def m2ev(mid0, flag):
    # to format from MeV to eV FISPACT-TYPE
    # mid=[]
    # flag='e' or 'E'
    result = []
    for i0 in range(len(mid0)):
        temp0 = mid0[i0].split(flag)
        if len(temp0) == 1:
            mid0[i0] = float(temp0[0]) * 1000000
        else:
            mid0[i0] = float(temp0[0]) * (10 ** (6 + int(temp0[1])))
        temp0 = '%E' % mid0[i0]
        temp0 = temp0.replace('+', '')
        mode0 = re.compile(r'E0+$')
        temp0 = mode0.sub('', temp0)
        mode0 = re.compile(r'E0+')
        temp0 = mode0.sub('E', temp0)
        mode0 = re.compile(r'E-0+')
        temp0 = mode0.sub('E-', temp0)
        result.append(temp0)
    return result


def find_ele(ids):
    ans = []
    for eid in ids:
        ans.append(ele[int(eid[0:-7])])
    return ans

neutron = Data('Transporting')
with open('JMCT.out', 'r') as f:
    all_item = f.read()

    # # element name提取元素代号
    # mode = re.compile(r'\d+.\d{2}[cep]')
    # mid = mode.findall(all_item)
    # neutron.ele_name = find_ele(mid)
    # print(len(neutron.ele_name))
    # # print(neutron.ele_name)
    #
    # # element energy提取元素能量（eV）
    # mode = re.compile(r'\d.\d{5}E-\d{2}')
    # mid = mode.findall(all_item)
    # neutron.ele_ener = m2ev(mid, 'E')
    # # print(neutron.ele_ener)

    # element number提取元素总数
    # neutron.ele_num = len(neutron.ele_name)
    #
    # # 去重
    # neutron.leaveout()

    # energy bin/energy number提取能量箱和数量
    mode = re.compile(r'energy_bin[ \de\-,=.]+')
    mid = mode.findall(all_item)[0]
    mid = mid.replace(' ', '')
    mid = mid.strip('energy_bin=')
    mode = re.compile(r'^/c+$')
    mid = mode.sub('', mid)
    mid = mid.split(',')
    neutron.ene_bin = m2ev(mid, 'e')
    neutron.ene_num = len(neutron.ene_bin)
    # print(neutron.ene_bin)

    # 几何体相关信息储存
    mode = re.compile('Tally4_0,(.+?)---', re.S)
    mid = mode.findall(all_item)
    name = []
    energy=[]
    volume = []
    # 储存关心的几何体数量
    neutron.cell_num = len(mid)
    for i in range(neutron.cell_num):
        mode = re.compile(r'cell: (.+?),', re.S)
        name.append(mode.findall(mid[i])[0])
        # 储存每个几何体的中子通量
        # total           2.35844e-08
        mode = re.compile(r'total +\d.\d+e[+-]\d{2,3}')
        temp = mode.findall(mid[i])
        energy.append(temp[0][16:])
        # 储存每个几何体的体积
        # volume = 9.08924e+06
        print(mid[i])
        # \d.\d+(e[+-]\d{2,3})?
        mode = re.compile(r'volume\(cm\^3\): \d+.\d+e?[+-]?\d{0,2}')
        temp = mode.findall(mid[i])
        volume.append(temp[0][14:])
        neutron.cell_info = dict(zip(name,zip(energy,volume)))
    print(neutron.cell_info)
# print(neutron)
with open('neutron', 'wb') as out:
    pickle.dump(neutron, out)
