import pickle
from model import Data

neutron = Data('Transporting')
with open('save', 'rb') as out:
    neutron = pickle.load(out)

with open('enbins.i', 'w') as f:
    f.write('\'' + neutron.name + '\'\n')
    f.write(str(neutron.ene_num) + '\n')
    ele_inf = list(','.join(neutron.ene_bin))
    print(ele_inf)
    index = [i for i, a in enumerate(ele_inf) if a == ',']
    print(index)
    for i in range(1, len(index) // 7 + 1):
        ele_inf.insert(index[7 * i - 1] + i, '\n')
    f.write(''.join(ele_inf))

with open('transport.i', 'w') as f:
    f.write('ATDISPEN %d\n' % (neutron.ele_num))
    # 从元素代号获取元素名称
    f.write('FISPACT\n')
    f.write('* ' + neutron.name + '\n')
    f.write('GETDECAY 0\n')
    f.write('GETXS 1 1')
