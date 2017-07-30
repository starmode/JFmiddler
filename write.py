import pickle

title = 'transporting'

with open('neutron', 'rb') as f:
    neutron = pickle.load(f)

with open('structure', 'wb') as f:
    pickle.dump(allStructure, f)


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


collapx('COLLAPSE EAF_315_FUS_990', 315)


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


arrayx(title, True)


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


printlib(title)


def test(num, title, debug=False):
    with open('test%d.i' % num, 'w') as f:
        if not debug:
            f.write('NOHEAD\n')
        else:
            f.write('MONITOR 1\n')
        f.write('AINP\n')
        f.write('FISPACT\n')
        f.write('* %s\n' % title)
        # 写入DENSITY
        # 写入MASS
        # MIND参数，可能要调整
        f.write('MIND 1.E5\n')

