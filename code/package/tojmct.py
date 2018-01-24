import re
def _genSource(cell, i, neutron, allDistributions, pre, split):
    # 仅内部调用
    tmp = []
    segments = []
    samProb = []
    distributions = allDistributions[cell][0]
    possibility = allDistributions[cell][1] * neutron.cellInfo[cell][1]
    for distribution in distributions:
        segments.append('%.1f, %.1f, ' % (distribution.leftBound, distribution.rightBound))
        samProb.append('%e, ' % distribution.perc)
    segments = ''.join(segments)
    samProb = ''.join(samProb)
    segments = segments[:-2]
    samProb = samProb[:-2]
    tmp.append('%sSource_%d {\n' % (pre, i))
    tmp.append('%s%sprobability                        = %e\n' % (pre, split, possibility))
    tmp.append('%s%scell_name                          = \"%s\"\n' % (pre, split, cell))
    tmp.append('%s%sprobability_of_energy_distribution = 1\n' % (pre, split))
    tmp.append('%s%senergy_distribution                = \"dist_%d\" \n' % (pre, split,  i))
    tmp.append('%s%sdist_%d {\n' % (pre, split, i))
    tmp.append('%s%sdistribution_type  = \"piecewise_uniform_spectrum\"\n' % (pre, split * 2))
    tmp.append('%s%ssegments           = %s\n' % (pre, split * 2, segments))
    tmp.append('%s%ssample_probability = %s\n' % (pre, split * 2, samProb))
    tmp.append('%s%s}\n%s}\n' % (pre, split, pre))
    return ''.join(tmp)


def writej(path, neutron, allDistributions, split):
    # 生成JMCT输入文件
    # path--input--JMCT输入文件位置
    # neutron--input--由JMCT输出文件读取的所有材料物质信息
    # allStructure--input--由GDML文件读取的所有材料物质信息
    # split--input--括号缩进
    with open(path, 'r') as f:
        text = f.read()
    mode = re.compile('{[ \t\n]*source[ \t\n]*}')

    try:
        pos = mode.search(text).start()
    except AttributeError:
        pass
    offset = pos - text.rfind('\n', 0, pos) - 1
    pre = offset * ' '
    numOfStus = len(neutron.cellInfo.keys())
    tmp = ['number_of_source = %d\n' % numOfStus]
    tmp.append('%sparticle_type    = 2\n' % pre)
    # 此处for循环用apply优化
    length = len(neutron.cellInfo)
    numList = [i for i in range(length)]
    neutronList = [neutron] * length
    allDisList = [allDistributions] * length
    preList = [pre] * length
    splitList = [split] * length

    tmp.extend(list(map(_genSource, neutron.cellInfo.keys(), numList, neutronList, allDisList, preList, splitList)))

    tmp = ''.join(tmp)
    pointPos = path.rfind('.')
    text = mode.sub(tmp, text)

    with open(path[:pointPos] + '_new' + path[pointPos:], 'w') as f:
        f.write(text)

