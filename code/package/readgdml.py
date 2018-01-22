# 从gdml文件中读取栅元信息
# 输入：文件地址
# 输出：字典allStructure

from lxml import etree
from .model import Volume

def readg(path):
    # 读取GDML文件并解析出各材料物质信息
    # path--input--GDML文件位置
    # allStructure--output--所有材料填充物质信息
    assert type(path) == str
    try:
        root = etree.parse(path)
    except:
        raise FileNotFoundError
    # 获取常数定义
    conTree = root.xpath('./define/constant')
    conNames = [con.xpath('@name')[0] for con in conTree]
    conVal = [con.xpath('@value')[0] for con in conTree]

    # 获取位置定义
    posTree = root.xpath('./define/position')
    posName = [pos.xpath('@name')[0] for pos in posTree]
    posVal = [(pos.xpath('@unit')[0], float(pos.xpath('@x')[0]), float(pos.xpath('@y')[0]), float(pos.xpath('@z')[0]))
              for pos in posTree]

    # 获取角度定义
    rotTree = root.xpath('./define/rotation')
    rotName = [rot.xpath('@name')[0] for rot in rotTree]
    rotVal = [(rot.xpath('@unit')[0], float(rot.xpath('@x')[0]), float(rot.xpath('@y')[0]), float(rot.xpath('@z')[0]))
              for rot in rotTree]

    constants = dict(zip(conNames, conVal))
    position = dict(zip(posName, posVal))
    rotation = dict(zip(rotName, rotVal))

    # 获取元素定义
    eleTree = root.xpath('./materials/element')
    eleName = [ele.xpath('@name')[0] for ele in eleTree]
    # 序号0-3为int原子序数，double原子质量，string 原子简称
    # eleInf = [(ele.xpath('@Z')[0],ele.xpath('atom/@value')[0],ele.xpath('@formula')[0]) for ele in eleTree ]
    # 暂定不需要formula
    eleInf = [(int(ele.xpath('@Z')[0]), float(ele.xpath('atom/@value')[0])) for ele in eleTree]
    elements = dict(zip(eleName, eleInf))

    # 定义原子数-元素名字典
    tmp = [e[0] for e in eleInf]
    zElements = dict(zip(tmp, eleName))
    # 获取材料定义
    # 对于无引用的材料，定义同名新元素，假装引用
    matTree = root.xpath('./materials/material')
    matName = [mat.xpath('@name')[0] for mat in matTree]
    matD = [mat.xpath('D/@value')[0] for mat in matTree]
    matEles = [
        [(fac.xpath('@ref')[0], float(fac.xpath('@n')[0])) for fac in mat.xpath('fraction')] if len(
            mat.xpath('@Z')) == 0 else [(
            zElements[int(mat.xpath('@Z')[0])], 1.0)] for mat in matTree]

    materials = dict(zip(matName, zip(matD, matEles)))


    # 获取栅元定义
    solids = {}
    solid = root.xpath('./solids')[0]

    for volume in solid:
        # 设置通用属性
        name = volume.xpath('@name')[0]
        newVol = Volume(name)
        newVol.property = volume.tag
        solids[name] = newVol

    # 补充栅元的物质信息和空间信息
    allStructure = {}
    structures = root.xpath('./structure/volume')
    for structure in structures:
        name = structure.xpath('@name')[0]
        # 物质信息
        if name != 'World':
            solidRef = structure.xpath('solidref/@ref')[0]
            materialRef = structure.xpath('materialref/@ref')[0]
            if solids.__contains__(solidRef):
                volume = solids[solidRef]
            else:
                volume = Volume(solidRef)
            items = materials[materialRef]
            volume.matName = materialRef
            volume.matD = items[0]
            volume.matGre = [item + elements[item[0]] for item in items[1]]
            allStructure[name[6:]] = volume
    return allStructure
