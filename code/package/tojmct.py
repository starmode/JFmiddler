import re

def writej(path, neutron, allDistributions, split = ' ' * 3):
    # split 分隔符，str
    # pre 前缀空格数
    with open(path, 'r') as f:
        mode = re.compile('{[ \t\n]*source[ \t\n]*}')
        text = f.read()
        try:
            pos = mode.search(text).start()
        except AttributeError:
            raise
        offset = 0
        while text[pos - offset] != '\n':
            offset += 1
        pre = offset * ' '
    numOfStus = len(neutron.cell_info.keys())
    tmp = ['number_of_source = %d\n' % numOfStus]
    tmp.append('%sparticle_type    = 2\n' % pre)
    for i, cell in enumerate(neutron.cell_info.keys()):
        segments = []
        samProb = []
        distributions = allDistributions[cell][0]
        possibility = allDistributions[cell][1] * neutron.cell_info[cell][1]
        for distribution in distributions:
            segments.append('%f, %f, ' % (distribution.leftBound, distribution.rightBound))
            samProb.append('%e, ' % distribution.perc)
        segments = ''.join(segments)
        samProb = ''.join(samProb)
        segments = segments[:-1]
        samProb = samProb[:-1]
        tmp.append('%sSource_%d {\n' % (pre, i))
        tmp.append('%sprobability                        = %e\n' % (pre, possibility))
        tmp.append('%scell_name                          = \"%s\"\n' % (pre, cell))
        tmp.append('%sprobability_of_energy_distribution = 1\n' % pre)
        tmp.append('%senergy_distribution                = \"dist_%d\" \n' % (pre, i))
        tmp.append('%sdist_%d {\n' % (pre, i))
        tmp.append('%s%sdistribution_type  = \"piecewise_uniform_spectrum\"\n' % (pre * 2, split))
        tmp.append('%s%ssegments           = %s\n' % (pre * 2, split, segments))
        tmp.append('%s%ssample_probability = %s\n' % (pre * 2, split, samProb))
        tmp.append('%s%s}\n%s}\n' % (pre * 2, split, pre))
    tmp = ''.join(tmp)

    pointPos = path.rfind('.')

    with open(path[:pointPos] + '_new' + path[pointPos:], 'w') as f:
        text = mode.sub(tmp, text)
        f.write(text)

