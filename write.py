import pickle

with open('save', 'rb') as out:
    neutron = pickle.load(out)

with open('enbins.i', 'w') as f:
    f.write('\'%s\'\n' % neutron.name)
    f.write('%d\n' % neutron.ene_num)
    ele_inf = list(','.join(neutron.ene_bin))
    index = [i for i, a in enumerate(ele_inf) if a == ',']
    # for i in range(1, len(index) // 7 + 1):
    #     ele_inf.insert(index[7 * i - 1] + i, '\n')
    mid = ''.join(ele_inf)
    mid = mid.split(',')
    for i, t in enumerate(mid):
        if i < len(mid) - 1:
            f.write('%+12s,' % t)
        else:
            f.write('%+12s' % t)
        if i % 7 == 6 and i > 0:
            f.write('\n')

with open('transport.i', 'w') as f:
    f.write('ATDISPEN %d\n' % neutron.ele_num)
    for i, ele in enumerate(neutron.ele_name):
        f.write('   %-2s%+12s\n' % (ele, neutron.ele_ener[i]))
    f.write('FISPACT\n')
    f.write('* ' + neutron.name + '\n')
    f.write('GETDECAY 0\n')
    f.write('GETXS 1 1')
