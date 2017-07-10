from lxml import etree

# 遇到的问题
# 1.哪些标签是可选的或者有多种不同格式？(目前已知material的Z标签有两种格式)
# 2.位置和角度的单位只能是mm和radian吗？
# 3.元素的简称formula是否无用？(暂定为无用)
# 4.类似M00000001_Z013027的name标签在生成时是否有规律？
# 5.solids里的栅元块是否都为同一种类别？
try:
    root = etree.parse('bmodel.gdml')
except:
    pass
# 获取常数定义
conTree = root.xpath('./define/constant')
conNames = [con.xpath('@name')[0] for con in conTree]
conVal = [con.xpath('@value')[0] for con in conTree]

# 获取位置定义
posTree = root.xpath('./define/position')
posName = [pos.xpath('@name')[0] for pos in posTree]
# posUnit = root.xpath('./define/position/@unit')
posVal = [(pos.xpath('@x')[0], pos.xpath('@y')[0], pos.xpath('@z')[0]) for pos in posTree]

# 获取角度定义
rotTree = root.xpath('./define/rotation')
rotName = [rot.xpath('@name')[0] for rot in rotTree]
# rotUnit = root.xpath('./define/rotation/@unit')
rotVal = [(rot.xpath('@x')[0], rot.xpath('@y')[0], rot.xpath('@z')[0]) for rot in rotTree]

constants = dict(zip(conNames, conVal))
position = dict(zip(posName, posVal))
rotation = dict(zip(rotName, rotVal))

# 获取元素定义
eleTree = root.xpath('./materials/element')
eleName = [ele.xpath('@name')[0] for ele in eleTree]
# 序号0-3为int原子序数，double原子质量，string 原子简称
# eleInf = [(ele.xpath('@Z')[0],ele.xpath('atom/@value')[0],ele.xpath('@formula')[0]) for ele in eleTree ]
# 暂定不需要formula
eleInf = [(ele.xpath('@Z')[0], ele.xpath('atom/@value')[0]) for ele in eleTree]
elements = dict(zip(eleName, eleInf))

# 获取材料定义
# 对于无引用的材料，定义同名新元素，假装引用
matTree = root.xpath('./materials/material')
matName = [mat.xpath('@name')[0] for mat in matTree]
matD = [mat.xpath('D/@value')[0] for mat in matTree]
matEles = [
    [(fac.xpath('@ref')[0], fac.xpath('@n')[0]) for fac in mat.xpath('fraction')] if len(mat.xpath('@Z')) == 0 else (
    mat.xpath('@name')[0], '1') for mat in matTree]

materials = dict(zip(matName, zip(matD, matEles)))

# 更新新定义的元素
newTree = [mat for mat in matTree if len(mat.xpath('@Z')) != 0]
newName = [new.xpath('@name')[0] for new in newTree]
newInf = [(new.xpath('@Z')[0], new.xpath('atom/@value')[0]) for new in newTree]
newEles = dict(zip(newName, newInf))
print(newEles)
elements.update(newEles)

print(constants)
print(position)
print(rotation)
print(elements)
print(materials)
