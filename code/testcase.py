from package.readjmct import readj
from package.readgdml import readg
from package.tofisp import writef
from package.readfisp import readf
from package.tojmct import writej
from package.runfisp import fisp
import cProfile as profile
def one():
    neutron = readj('./jmct/neutron.OUT')
    structure = readg('./jmct/Model_test.gdml')
    writef('./testcase', 7.8E+18, neutron, structure)
    distributes = readf('./fisp')
    writej('./testcase/photon.OUT', neutron, distributes, ' ' * 3)

def all(n):
    for i in range(n):
        one()

# profile.run('all(500)')
# one()

fisp(r'G:\大创资料\FISPACT-07\fispact\fisp20070.exe',r'G:\大创资料\FISPACT-07\eaf_data','./fisp/SS316')