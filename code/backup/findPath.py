
# 测试用途，不计入package
from os import walk
from os.path import join
import re
from model import ele

# 这个改为需要调研的文件名
name = 'test'
# 这里改为查找的根目录
path = '/home/starkind/桌面/大创/testcases/testcases'
enum = {}
para = {}
num = 0
for root, dirs, files in walk(path):
    for file in files:
        if name==file[0:4]:
            with open(join(root, file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.rstrip('\n')
                    line = line.rstrip(' ')
                    line = line.strip(' ')
                    if len(line) != 0 and line[0] != '*' and line[0] != '/' and line[0] != '<':
                        words = line.split(' ')
                        if enum.__contains__(words[0]):
                            enum[words[0]] = enum[words[0]] + 1
                        else:
                            enum[words[0]] = 1
                        if len(words) != 1 or para.__contains__(words[0]):
                            if para.__contains__(words[0]) and len(words) != 1:
                                para[words[0]].append(words[1:])
                            elif para.__contains__(words[0]):
                                para[words[0]].append([''])
                            else:
                                para[words[0]] = [words[1:]]
            num = num + 1

moveitem=[]

sci=re.compile('^\d.\d{5}E[-,+]\d{2}$')
element=re.compile('^\w{1,2}\d{2,3}m?n?\*?$')
# enum['科学计数法如4.21006E-14']=0
# enum['元素如Cu']=0
# enum['元素如Lu176m*']=0
# # 清洗数据，合并同类型
# for key in enum.keys():
#     if len(re.findall(sci,key))!=0:
#         moveitem.append(key)
#         enum['科学计数法如4.21006E-14']+=1
#     if key in ele:
#         moveitem.append(key)
#         enum['元素如Cu'] += 1
#     if len(re.findall(element,key))!=0:
#         moveitem.append(key)
#         enum['元素如Lu176m*']+=1
#
# for key in moveitem:
#     enum.pop(key)
yes = re.compile('^\w+$')
purnum = re.compile('^\d+$')
for key in enum.keys():
    if len(re.findall(yes,key))==0:
        moveitem.append(key)
    elif key in ele:
        moveitem.append(key)
    elif len(re.findall(element,key))!=0:
        moveitem.append(key)
    elif len(re.findall(purnum,key))!=0:
        moveitem.append(key)


for key in moveitem:
    enum.pop(key)
for key in enum.keys():
    enum[key] = (enum[key], enum[key] / num)


enlist=list(enum.items())
enlist=sorted(enlist,key=lambda e:e[1][0], reverse=True)
enum=dict(enlist)
print(enum)
for key in para.keys():
    print(key)
    print(para[key])

with open('test.txt','w') as f:
    for key in enum:
        f.write(key+' : ')
        f.write(str(enum[key]))
        f.write('\n')

