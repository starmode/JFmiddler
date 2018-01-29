from package.readjmct import readj
from package.readgdml import readg
from package.tofisp import writef
from package.readfisp import readf
from package.tojmct import writej
# MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())

def one():
    with open('./testcase/photon.OUT') as f:
        text = f.read()
    neutron = readj('./jmct/neutron.OUT')
    structure = readg('./jmct/Model_test.gdml')
    writef('./testcase', 7.8E+18, neutron, structure)
    distributes = readf('./fisp')
    writej('./testcase/photon_new.OUT', text, neutron, distributes, ' ' * 3, './testcase/photon_new.OUT')

def all(n):
    for i in range(n):
        one()

# profile.run('all(1000)')
one()