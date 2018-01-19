import pickle
import re
with open('neutron', 'rb') as f:
    neutron = pickle.load(f)

def Source(path, neutron, allDistributions, pre, split = ' ' * 3):
    # split 分隔符，str
    # pre 前缀空格数
    numOfStus = len(neutron.cell_info.keys())
    tmp = ['number_of_source = %d\n' % numOfStus]
    tmp.append('particle_type    = 2\n')
    for i, cell in enumerate(neutron.cell_info.keys()):
        segments = []
        samProb = []
        distributions = allDistributions[cell][1]
        possibility = allDistributions[cell][0] * neutron.cell_info[cell][1]
        for distribution in distributions:
            segments.append('%f, %f, ' % (distribution.leftBound, distribution.rightBound))
            samProb += '%f, ' % distribution.perc
        ''.join(segments)
        ''.join(samProb)
        segments = segments[:-1]
        samProb = samProb[:-1]

        tmp.append('%sSource_%d {\n' % (pre, i))
        tmp.append('%sprobability                        = %e\n' % (pre, possibility))
        tmp.append('%scell_name                          = \"%s\"\n' % (pre, cell))
        tmp.append('%sprobability_of_energy_distribution = 1\n' % pre)
        tmp.append('%senergy_distribution                = \"dist_%d\" {\n' % (pre, i))
        tmp.append('%sdist_%d {\n' % (pre, i))
        tmp.append('%s%sdistribution_type  = \"piecewise_uniform_spectrum\"\n' % (pre * 2, split))
        tmp.append('%s%ssegments           = %s\n' % (pre * 2, split, segments))
        tmp.append('%s%ssample_probability = %s\n' % (pre * 2, split, samProb))
        tmp.append('%s%s}\n%s}' % (pre * 2, split, pre))
        tmp = ''.join(tmp)

        with open(path) as f:
            text = f.read()
            mode = re.compile('{[ \t\n]*source[ \t\n]*}')
            text = mode.sub(tmp, text)
            f.write(text)



with open('JMCT.out', 'r') as f:
    all = f.read()
    m = re.search(r'number_of_source = (\d)', all)
    n = int(m.group(1))
    #n为放置的源序数

    start = all.find('Source ')
    i = start
    num = 0
    flag = 0
    while(True):
        if all[i] == '{':
            num=num+1
        elif all[i] == '}':
            num = num -1
            flag = 1
        if num == 1 and flag == 1:
            break
        i = i + 1

        #i 确定新数据插入位置
    #print(all[start:i])
    newData = all[:i+2]+Source(distributions, n)+all[i+2:]
    print(newData)

