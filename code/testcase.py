from package.readjmct import readj
from package.readgdml import readg
from package.tofisp import writef
from package.readfisp import readf
from package.tojmct import writej

neutron = readj('./jmct/neutron.OUT')
structure = readg('./jmct/Model_test.gdml')
writef('./testcase', 7.8E+18, neutron, structure)
distributes = readf('./fisp')
writej('./testcase/photon.OUT', neutron, distributes, ' ' * 3)
