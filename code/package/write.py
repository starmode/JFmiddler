# 利用neutron和allStructure生成fispact输入文件
# 输入：文件地址，neutron，allStructure
# 输出：无

import os
from .model import ele

def collapx(title, bins, debug=False):
    with open('collapx.i', 'w') as f:
        if not debug:
            f.write('NOHEAD\n')
        else:
            f.write('MONITOR 1\n')
        f.write('COLLAPSE %d\n' % bins)
        f.write('FISPACT\n')
        f.write('* %s\n' % title)
        f.write('END\n')
        f.write('* END OF RUN')
        
def arrayx(title, isFirstTime, debug=False):
    with open('arrayx.i', 'w') as f:
        if not debug:
            f.write('NOHEAD\n')
        else:
            f.write('MONITOR 1\n')
        f.write('SPEK\n')
        f.write('ENFA\n')
        # 标题有待后期修改，适应不同能群
        f.write('* EAF_2007,315-Group,zone 13\n')
        if isFirstTime:
            f.write('TAPA\n')
        else:
            f.write('ARRAY\n')
        f.write('FISPACT\n')
        f.write('* %s\n' % title)
        f.write('END\n')
        f.write('* END OF RUN')
def printlib(title, debug=False):
    with open('printlib.i', 'w') as f:
        if not debug:
            f.write('NOHEAD\n')
        else:
            f.write('MONITOR 1\n')
        f.write('AINP\n')
        f.write('FISPACT\n')
        f.write('* %s\n' % title)
        # 默认输出所有内容，后期修改可能是2
        f.write('PRINTLIB 0\n')
        f.write('END\n')
        f.write('* END OF RUN')
        
        
def test(file_path, title, cell, neutron, allStructure, debug=False):
    with open(file_path , 'w') as f:
        if not debug:
            f.write('NOHEAD\n')
        else:
            f.write('MONITOR 1\n')
        f.write('AINP\n')
        f.write('FISPACT\n')
        f.write('* %s\n' % title)
        # 写入DENSITY
        # 单位g/cm^3
        f.write('DENSITY %.5E\n' % float(allStructure[cell].matD))
        # 写入MASS
        mass = float(allStructure[cell].matD) * float(neutron.cell_info[cell][1])
        f.write('MASS %.5E %d\n' % (mass, len(allStructure[cell].matGre)))
        # 这里修改下用原子序数查找元素简称，不要直接读取
        for element in allStructure[cell].matGre:
            f.write('%s %.1f\n' % (ele[int(element[2])], float(element[1]*100)))
        # MIND参数，可能要调整
        f.write('MIND 1.E5\n')
        f.write('HAZA\n')
        f.write('ATWO\n')
        f.write('FLUX %.5E\n' % float(neutron.cell_info[cell][0]))
        # 这里插入
        f.write('LEVEL 100 1\n')
        f.write('ZERO\n')
        f.write('TIME 1 DAYS ATOMS\n')
        f.write('END\n')
        f.write('* %s\n' % title)
        
        
def writef(dir_path,neutron,allStructure):

    # with open('spectra', 'w') as f:
    #     f.write('\'%s\'\n' % neutron.name)
    #     f.write('%d\n' % neutron.ene_num)
    #     ele_inf = list(','.join(neutron.ene_bin))
    #     index = [i for i, a in enumerate(ele_inf) if a == ',']
    #     mid = ''.join(ele_inf)
    #     mid = mid.split(',')
    #     for i, t in enumerate(mid):
    #         if i < len(mid) - 1:
    #             f.write('%+12s ' % t)
    #         else:
    #             f.write('%+12s' % t)
    #         if i % 7 == 6 and i > 0:
    #             f.write('\n')
    
    os.chdir(dir_path)
    #此处会改变整个程序的工作目录，不妥
    
    collapx('COLLAPSE EAF_315_FUS_990', 315)
    title = 'transporting'
    arrayx(title, True)
    printlib(title)
    i=1
    for cell in neutron.cell_info.keys():
        test('test'+str(i)+'.i','ok',cell,neutron,allStructure)
        i=i+1
