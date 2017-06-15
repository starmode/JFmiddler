class Data(object):
    ele_num = 0
    ele_name = []
    ele_ener = []

    cell_num = 0

    ene_num = 0
    ene_bin = []
    # cell_num*ene_num
    ene_map = []

    def __init__(self):
        pass

    def __str__(self):
        m = str(self.ele_num) + 'elements\n' + str(self.cell_num) + 'cells\n' + str(self.ene_num) + 'energy bins'
        return m
