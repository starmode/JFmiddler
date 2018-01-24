# 定义所使用的数据结构

# 数据类，来自input文件
class Data(object):
    name = ''


    def __init__(self, name):
        self.name = name
        self.eleNum = 0
        self.eleName = []
        self.eleEner = []
        self.cellNum = 0
        self.cellInfo = {}
        self.eneNum = 0
        self.eneBin = []

    def __str__(self):
        m = str(self.eleNum) + ' elements\n' + str(self.cellNum) + ' cells\n' + str(self.eneNum) + ' energy bins'
        return m

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
