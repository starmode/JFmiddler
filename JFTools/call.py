import os
from shutil import copy
from subprocess import call

# 未测试
def jmct(_input, _useEnv = True, _path = ''):
    _input = os.path.realpath(_input)
    if _useEnv:
        os.system('jmct ' + _input)
    else:
        os.system(_path + _input)

def fisp(_fisppath, _eaf, _case):
    _fisppath = os.path.realpath(_fisppath)
    _eaf = os.path.realpath(_eaf)
    _case = os.path.realpath(_case)
    _workdir = _case + '/output'
    with open(os.path.dirname(__file__) + '/FILES_prototype', 'r') as f:
        files = f.read()
    files = files.replace(r'<eaf>', _eaf)
    files = files.replace(r'<eaf_fis>', _eaf + '/eaf_n_fis_20070')
    files = files.replace(r'<eaf_asscfy>', _eaf + '/eaf_n_asscfy_20070')
    files = files.replace(r'<eaf_gxs>', _eaf + '/eaf_n_gxs_175_fus_20070')
    # 以上3个需要变量代替
    files = files.replace(r'<case>', _case)
    if not os.path.exists(_workdir):
        os.mkdir(_workdir)
    os.chdir(_workdir)
    with open('FILES', 'w') as f:
        f.write(files)
    # 生成FILES文件

    if os.path.isfile(_case + '/collapx'):
        copy(_case + '/collapx', 'collapx')
    else:
        open('collapx', 'w').close()
    if os.path.isfile(_case + '/arrayx'):
        copy(_case + '/arrayx', 'arrayx')
    else:
        open('arrayx', 'w').close()
    if os.path.isfile(_case + '/summaryx'):
        copy(_case + '/summaryx', 'summaryx')
    if os.path.isfile(_case + '/halfunc'):
        copy(_case + '/halfunc', 'halfunc')
    copy(_case + '/fluxes', 'fluxes')

    copy(_case + '/collapx.i', 'input')
    call(_fisppath)
    copy(_case + '/arrayx.i', 'input')
    call(_fisppath)
    if os.path.isfile(_case + '/printlib.i'):
        copy(_case+'/printlib.i', 'input')
        call(_fisppath)
        copy('output', 'printlib.o')
    _list = os.listdir(_case)
    for i in range(0, len(_list)):
        _input = _list[i]
        if _input[-2:] == '.i' and not (_input == 'collapx.i' or _input == 'arrayx.i' or _input == 'printlib.i'):
            name = _input[:-2]
            copy(_case + '/' + _input, 'input')
            call(_fisppath)
            copy('output', _workdir + '/' + name + '.o')
    os.remove(_workdir + '/input')
    os.remove(_workdir + '/output')
