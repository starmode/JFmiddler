import re


def Source(distributions, n, args={}):
    space = ' ' * 3
    # particle_type = 2
    # energy_distribution = “uniform"
    # y_distri_name{
    #    distribution_type = “piecewise_uniform_spectrum”    
    #      segments = left_end_1, right_end_1, … , left_end_n2, right_end_n2
    #     sample_probability = p_1, … , p_n2
    # }
    tips = ['probability', 'particle_type', 'energy_distribution', 'probability_of_energy_distribution']
    if args:
        tips.extend(args.keys())
    src = '%sSource_%d {\n' % (space * 2, n)
    prob = '%s%-40s= %f\n' % (space * 3, tips[0], 1.0)
    type = '%s%-40s= %d\n' % (space * 3, tips[1], 2)
    tagEneDist = '%s%-40s= "%s"\n' % (space * 3, tips[2], 'uniform')
    tagProbDist = '%s%-40s= %d\n' % (space * 3, tips[3], 1.0)

    segments = ''
    samProb = ''
    for distribution in distributions:
        segments += '%f, %f, ' % (distribution.leftBound, distribution.rightBound)
        samProb += '%f, ' % distribution.perc
    segments = segments[:-1]
    samProb = samProb[:-1]

    dist = '%suniform {\n%sdistribution_type = "piecewise_uniform_spectrum"' \
           '\n%ssegments = %s\n%ssample_probability = %s\n%s}\n' % (
           space * 3, space * 4, space * 4, segments, space * 4, samProb, space * 3)
    end = '%s}\n' % (space * 2)
    # print(src+prob+type+tagEneDist+tagProbDist+dist+end)
    return src + prob + type + tagEneDist + tagProbDist + dist + end


def writeff(jout_path, distributes):
    with open(jout_path, 'r') as f:
        all = f.read()
        m = re.search(r'number_of_source = (\d)', all)
        n = int(m.group(1))
        # n为放置的源序数

        start = all.find('Source ')
        i = start
        num = 0
        flag = 0
        while (True):
            if all[i] == '{':
                num = num + 1
            elif all[i] == '}':
                num = num - 1
                flag = 1
            if num == 1 and flag == 1:
                break
            i = i + 1

            # i 确定新数据插入位置
        # print(all[start:i])
        newData = all[:i + 2] + Source(distributes, n) + all[i + 2:]
        # print(newData)
    return newData
