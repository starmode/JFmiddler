# 从fispact输出文件中读取光谱信息
# 输入：文件地址
# 输出：list[model.energyDis *24]

import re
from model import energyDis

with open('../src/test1.o') as f:
    allItem = f.read()

distributes = []
patten = re.compile(r'\(0.0 -0.01 {2}MeV\).+?DOSE',re.S)
targetPart = patten.findall(allItem)[0]

#print(allItem)
patten = re.compile(r'ACTIVATION {2}\(MeV per Second\) {19}\d\.\d{5}E[+-]\d{2}')
gamma = float(patten.findall(allItem)[0][-11:])

patten = re.compile(r'\(.+?MeV.+?[+-]\d{2}')
items = patten.findall(targetPart)
for item in items:
    distribute = energyDis()
    patten = re.compile(r'\d{1,2}\.\d{1,2}')
    result = patten.findall(item)
    distribute.leftBound = float(result[0])
    distribute.rightBound = float(result[1]) if len(result) == 3 else 999.
    patten = re.compile(r'\d.\d{5}E[+-]\d{2}')
    distribute.perc = float(patten.findall(item)[0]) / gamma
    distributes.append(distribute)