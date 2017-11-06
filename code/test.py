#TODO: 函数改名，调用方式调整，变量改名

import os
from package.read import jread
from package.readGdml import jreadGdml
from package.getGamma import getGamma
from package.write import writef
from package.writeF import writeff

neutron = jread('./jmct/result/JMCT.out')
#print(neutron)
allstructure = jreadGdml("./jmct/input/Model.gdml")
#print(allstructure)
writef("./fisp", neutron, allstructure)

#print(os.getcwd())

distributes = getGamma("./fisp/test70.o")

len(distributes)
i = 7
#print(distributes[i].leftBound)
#print(distributes[i].rightBound)
#print(distributes[i].perc)
newdata = writeff('./jmct/result/JMCT.out',distributes)
print(newdata)