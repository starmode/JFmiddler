import os
from shutil import copy
from subprocess import call


# 未测试
def jmct(_input, _useEnv=True, _path=''):
    _input = os.path.realpath(_input)
    if _useEnv:
        os.system('jmct ' + _input)
    else:
        os.system(_path + _input)


def fisp(_env, _group, _indir, _outdir=''):
    _fisppath = os.path.realpath(_env[0])
    _eaf = os.path.realpath(_env[1])
    _indir = os.path.realpath(_indir)
    if _outdir == '':
        _outdir = os.path.join(_indir, 'output')
    # 可选功能：指定输出目录
    with open(os.path.dirname(__file__) + '/FILES_prototype', 'r') as f:
        files = f.read()
    files = files.replace(r'<case>', _indir)
    files = files.replace(r'<eaf>', _eaf)
    files = files.replace(r'<0>', _group[0])
    files = files.replace(r'<1>', _group[1])
    files = files.replace(r'<2>', _group[2])
    # group[0]: 'n','p','d'
    # group[1]: '69', '100', '172', '175', '211', '315', '351'
    # group[2]: 'FLA', 'FIS', 'FUS'
    _eaf_gxs = os.path.join(_eaf, 'eaf_' + _group[0] + '_gxs_' + _group[1] + '_' + _group[2] + '_20070')
    if not os.path.isfile(_eaf_gxs):
        print('Cannot find ' + _eaf_gxs)
        # raise FileNotFoundError
        return
    # 验证eaf地址
    if not os.path.exists(_outdir):
        os.mkdir(_outdir)
    with open(_outdir + '/FILES', 'w') as f:
        f.write(files)
    # 生成FILES文件

    if os.path.isfile(_indir + '/collapx'):
        copy(_indir + '/collapx', _outdir + '/collapx')
    else:
        open(_outdir + '/collapx', 'w').close()
    if os.path.isfile(_indir + '/arrayx'):
        copy(_indir + '/arrayx', _outdir + '/arrayx')
    else:
        open(_outdir + '/arrayx', 'w').close()
    # 创建空文件
    if os.path.isfile(_indir + '/summaryx'):
        copy(_indir + '/summaryx', _outdir + '/summaryx')
    if os.path.isfile(_indir + '/halfunc'):
        copy(_indir + '/halfunc', _outdir + '/halfunc')
    copy(_indir + '/fluxes', _outdir + '/fluxes')
    copy(_indir + '/collapx.i', _outdir + '/input')
    call(['cmd', '/c', 'cd /d ' + _outdir + ' && ' + _fisppath])
    copy(_indir + '/arrayx.i', _outdir + '/input')
    call(['cmd', '/c', 'cd /d ' + _outdir + ' && ' + _fisppath])
    if os.path.isfile(_indir + '/printlib.i'):
        copy(_indir+'/printlib.i', _outdir + '/input')
        call(['cmd', '/c', 'cd /d ' + _outdir + ' && ' + _fisppath])
        copy(_outdir + '/output', _outdir + '/printlib.o')
    _list = os.listdir(_indir)
    for i in range(0, len(_list)):
        _input = _list[i]
        if _input[-2:] == '.i' and not (_input == 'collapx.i' or _input == 'arrayx.i' or _input == 'printlib.i'):
            name = _input[:-2]
            copy(_indir + '/' + _input, _outdir + '/input')
            call(['cmd', '/c', 'cd /d ' + _outdir + ' && ' + _fisppath])
            copy(_outdir + '/output', _outdir + '/' + name + '.o')
    os.remove(_outdir + '/input')
    os.remove(_outdir + '/output')


# 调用举例：
# fisppath = r'G:\大创资料\FISPACT-07\fispact\fisp20070.exe'
# eaf = r'G:\大创资料\FISPACT-07\eaf_data'
# case = r'G:\git\JFmiddler\testcase\compare\fisp\AL6061'
#
# env = ['', '']
# env[0] = fisppath
# env[1] = eaf
# group = ['', '', '']
# group[0] = 'n'
# group[1] = '175'
# group[2] = 'fus'
#
# fisp(env, group, case)
