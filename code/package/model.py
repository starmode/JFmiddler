# 定义所使用的数据结构

# 数据类，来自input文件
class Data(object):
    name = ''

    ele_num = 0
    ele_name = []
    ele_ener = []

    cell_num = 0
    cell_info = {}

    ene_num = 0
    ene_bin = []

    # cell_num*ene_num

    def __init__(self, name):
        self.name = name
        self.ele_num = 0
        self.ele_name = []
        self.ele_ener = []
        self.cell_num = 0
        self.cell_info = {}
        self.ene_num = 0
        self.ene_bin = []

    def __str__(self):
        m = str(self.ele_num) + ' elements\n' + str(self.cell_num) + ' cells\n' + str(self.ene_num) + ' energy bins'
        return m

    def leaveout(self):
        # 对元素集合进行去重

        ele_name_new = [self.ele_name[i] for i in range(1, self.ele_num) if
                        self.ele_name[i] != self.ele_name[i - 1] or self.ele_ener[i] != self.ele_ener[i - 1]]
        ele_name_new.insert(0, self.ele_name[0])
        ele_ener_new = [self.ele_ener[i] for i in range(1, self.ele_num) if
                        self.ele_name[i] != self.ele_name[i - 1] or self.ele_ener[i] != self.ele_ener[i - 1]]
        ele_ener_new.insert(0, self.ele_ener[0])
        ele_num_new = len(ele_ener_new)
        self.ele_num = ele_num_new
        self.ele_name = ele_name_new
        self.ele_ener = ele_ener_new


# 栅元类，来自gmdl文件
class Volume(object):
    name = ''
    property = ''
    # 物质信息，名称/密度/体积/质量
    matName = ''
    matD = ''
    matV = ''
    matM = ''
    # 物质信息，成分[(元素名称，原子序数，原子质量，比例)，...]
    matGre = []

    def __init__(self, name):
        self.name = name
        self.matName = ''
        self.matD = ''
        self.matGre = []

# 光子分布类
class energyDis:
    def __init__(self):
        self.leftBound = 0.
        self.rightBound = 0.
        self.perc = 0.

# 阿伏伽德罗常数
Avogadro = 0.602

# 元素原子量对应表
ele = ['', 'H', 'HE', 'LI', 'BE', 'B', 'C', 'N', 'O', 'F', 'NE', 'NA', 'MG', 'AL', 'SI', 'P', 'S', 'CL', 'AR', 'K',
       'CA', 'SC', 'TI', 'V', 'CR', 'MN', 'FE', 'CO', 'NI', 'CU', 'ZN', 'GA', 'GE', 'AS', 'SE', 'BR', 'KR', 'RB', 'SR',
       'Y', 'ZR', 'NB', 'MO', 'TC', 'RU', 'RH', 'PD', 'AG', 'CD', 'IN', 'SN', 'SB', 'TE', 'I', 'XE', 'CS', 'BA', 'LA',
       'CE', 'PR', 'ND', 'PM', 'SM', 'EU', 'GD', 'TB', 'DY', 'HO', 'ER', 'TM', 'YB', 'LU', 'HF', 'TA', 'W', 'RE', 'OS',
       'IR', 'PT', 'AU', 'HG', 'TL', 'PB', 'BI', 'PO', 'AT', 'RN', 'FR', 'RA', 'AC', 'TH', 'PA', 'U', 'NP', 'PU', 'AM',
       'CM', 'BK', 'CF', 'ES', 'FM']
defaultInput = 'NOHEAD\nMONITOR 1\nAINP\nFISPACT\n* {title}\nDENSITY {density}\nMASS {mass} {elements}\nMIND ' \
               '1.0\nHALF\nGRAPH 2 0 0 1 2\n{flux}ATOMS\nLEVEL 100 1\nTIME 1.0\nHALF\nDOSE 1\nATOMS\nNOSTABLE\nLEVEL ' \
               '20 1\nFLUX 0.\nZERO\nTIME 1.0 HOURS ATOMSEND\n* END\n/*\n '
defaultCollapx = 'MONITOR 1\nCOLLAPSE 175\nFISPACT\n* {title}\nEND\n* END ' \
                 'OF RUN\n/*\n '
defaultArrayx = 'MONITOR 1\nSPEK\nENFA\n* {title}\nTAPA\nFISPACT\n* WRITE DATA TO ARRAY FILE.\nEND\n* END OF ' \
                'RUN\n/*\n '
defaultPrintlib = ''
