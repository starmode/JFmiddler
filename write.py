import pickle
from model import Data

neutron = Data()
with open('out', 'rb') as out:
    neutron = pickle.load(out)
