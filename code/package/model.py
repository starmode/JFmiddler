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
    # 单位信息，角度/长度单位
    aUnit = ''
    lUnit = ''
    # 空间信息，位置/旋转，三元字符列表
    pos = []
    rot = []
    # 物质信息，名称/密度/体积/质量
    matName = ''
    matD = ''
    matV = ''
    matM = ''
    # 物质信息，成分[(元素名称，原子序数，原子质量，比例)，...]
    matGre = []

    def __init__(self, name):
        self.name = name
        self.aUnit = ''
        self.lUnit = ''
        self.pos = []
        self.rot = []
        self.matName = ''
        self.matD = ''
        self.matGre = []


# box栅元
class Box(Volume):
    x = ''
    y = ''
    z = ''

    def __init__(self, name):
        super().__init__(name)
        self.x = ''
        self.y = ''
        self.z = ''


# sphere栅元
class Sphere(Volume):
    deltaPhi = ''
    deltaTheta = ''
    # 外内半径
    rMax = ''
    rMin = ''
    startPhi = ''
    startTheta = ''

    def __init__(self, name):
        super().__init__(name)
        self.deltaPhi = ''
        self.deltaTheta = ''
        self.rMax = ''
        self.rMin = ''
        self.startPhi = ''
        self.startTheta = ''


# tube栅元
class Tube(Volume):
    rMax = ''
    rMin = ''
    startPhi = ''
    z = ''

    def __init__(self, name):
        super().__init__(name)
        self.rMax = ''
        self.rMin = ''
        self.startPhi = ''
        self.z = ''


class energyDis:
    def __init__(self):
        self.leftBound = 0.
        self.rightBound = 0.
        self.perc = 0.


ele = ['', 'H', 'HE', 'LI', 'BE', 'B', 'C', 'N', 'O', 'F', 'NE', 'NA', 'MG', 'AL', 'SI', 'P', 'S', 'CL', 'AR', 'K',
       'CA', 'SC', 'TI', 'V', 'CR', 'MN', 'FE', 'CO', 'NI', 'CU', 'ZN', 'GA', 'GE', 'AS', 'SE', 'BR', 'KR', 'RB', 'SR',
       'Y', 'ZR', 'NB', 'MO', 'TC', 'RU', 'RH', 'PD', 'AG', 'CD', 'IN', 'SN', 'SB', 'TE', 'I', 'XE', 'CS', 'BA', 'LA',
       'CE', 'PR', 'ND', 'PM', 'SM', 'EU', 'GD', 'TB', 'DY', 'HO', 'ER', 'TM', 'YB', 'LU', 'HF', 'TA', 'W', 'RE', 'OS',
       'IR', 'PT', 'AU', 'HG', 'TL', 'PB', 'BI', 'PO', 'AT', 'RN', 'FR', 'RA', 'AC', 'TH', 'PA', 'U', 'NP', 'PU', 'AM',
       'CM', 'BK', 'CF', 'ES', 'FM']
