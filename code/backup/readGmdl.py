# 从gdml文件中读取栅元信息
# 输入：文件地址
# 输出：字典allStructure
## 有修改
from lxml import etree
import pickle
from model import Volume


def getVal(root, path):
    return root.xpath(path)[0]

try:
    root = etree.parse('../jmct/input/Model_test.gdml')
except:
    pass
# 获取常数定义
conTree = root.xpath('./define/constant')
conNames = [con.xpath('@name')[0] for con in conTree]
conVal = [con.xpath('@value')[0] for con in conTree]

# 获取位置定义
posTree = root.xpath('./define/position')
posName = [pos.xpath('@name')[0] for pos in posTree]
posVal = [(pos.xpath('@unit')[0], float(pos.xpath('@x')[0]), float(pos.xpath('@y')[0]), float(pos.xpath('@z')[0])) for pos in posTree]

# 获取角度定义
rotTree = root.xpath('./define/rotation')
rotName = [rot.xpath('@name')[0] for rot in rotTree]
rotVal = [(rot.xpath('@unit')[0], float(rot.xpath('@x')[0]), float(rot.xpath('@y')[0]), float(rot.xpath('@z')[0])) for rot in rotTree]

constants = dict(zip(conNames, conVal))
position = dict(zip(posName, posVal))
rotation = dict(zip(rotName, rotVal))

# 获取元素定义
eleTree = root.xpath('./materials/element')
eleName = [ele.xpath('@name')[0] for ele in eleTree]
# 序号0-3为int原子序数，double原子质量，string 原子简称
# eleInf = [(ele.xpath('@Z')[0],ele.xpath('atom/@value')[0],ele.xpath('@formula')[0]) for ele in eleTree ]
# 暂定不需要formula
# 此处修改1行
eleInf = [(int(ele.xpath('@Z')[0]), float(ele.xpath('atom/@value')[0])) for ele in eleTree]
elements = dict(zip(eleName, eleInf))
# 此处修改2行
tmp = [e[0] for e in eleInf]
zElements = dict(zip(tmp, eleName))


# 获取材料定义
# 对于纯净物材料，用z在元素字典中查找相应元素
matTree = root.xpath('./materials/material')
matName = [mat.xpath('@name')[0] for mat in matTree]
matD = [mat.xpath('D/@value')[0] for mat in matTree]
## 此处修改1行
matEles = [
    [(fac.xpath('@ref')[0], float(fac.xpath('@n')[0])) for fac in mat.xpath('fraction')] if len(mat.xpath('@Z')) == 0 else [(
        zElements[int(mat.xpath('@Z')[0])], 1.0)] for mat in matTree]
materials = dict(zip(matName, zip(matD, matEles)))

# 此处删除多行

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

for key in allStructure.keys():
    print(
        key+'\t'+allStructure[key].property + '\t' + allStructure[key].name + '\t' + allStructure[key].matName + '\t' +
        allStructure[key].matD)
    print(allStructure[key].matGre)
    print('\n')

with open('structure', 'wb') as out:
    pickle.dump(allStructure, out)