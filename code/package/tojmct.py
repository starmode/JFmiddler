import re

def Source(path, text, neutron, allDistributions, pre, split = ' ' * 3):
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

        with open(path, 'w') as f:
            mode = re.compile('{[ \t\n]*source[ \t\n]*}')
            text = mode.sub(tmp, text)
            f.write(text)

