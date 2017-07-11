# 数据类，来自input文件
class Data(object):
    name = ''

    ele_num = 0
    ele_name = []
    ele_ener = []

    cell_num = 0

    ene_num = 0
    ene_bin = []
    # cell_num*ene_num
    ene_map = []

    def __init__(self, name):
        self.name = name
        self.ele_num = 0
        self.ele_name = []
        self.ele_ener = []
        self.cell_num = 0
        self.ene_num = 0
        self.ene_bin = []
        self.ene_map = []

    def __str__(self):
        m = str(self.ele_num) + 'elements\n' + str(self.cell_num) + 'cells\n' + str(self.ene_num) + 'energy bins'
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
    # 物质信息，名称/密度
    matName = ''
    matD = ''
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


ele = ['', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
       'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr',
       'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La',
       'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os',
       'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am',
       'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl',
       'Mc', 'Lv', 'Ts', 'Og']
