import os


# 未测试
def jmct(_input):
    _input = os.path.realpath(_input)
    os.system('jmct ' + _input)
