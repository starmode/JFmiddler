from JFlink.read import *
from JFlink.write import *
from JFlink.call import CallFis
import os

if __name__ == '__main__':
    # 1: j2f
    jin = r'./mix/jmct/neutron.OUT'
    neutron = readj(jin)
    allStructure = readg(r'./mix/jmct/Model_test.gdml')
    fpath = r'./mix/fisp'
    writef(fpath, 7.8E18, neutron, allStructure)
    # 2: callF
    callf = CallFis()
    callf.env = [r'G:\大创资料\FISPACT-07\fispact\fisp20070.exe',
                 r'G:\大创资料\FISPACT-07\eaf_data']
    callf.group = ['n', '175', 'fus']
    # for _dir in os.listdir(fpath):
    #     p = os.path.join(fpath, _dir)
    #     if os.path.isdir(p):
    #         callf.fisp(p)
    [callf.fisp(os.path.join(fpath, _dir)) for _dir in os.listdir(fpath) if os.path.isdir(os.path.join(fpath, _dir))]
