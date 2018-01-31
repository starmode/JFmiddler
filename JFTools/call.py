import os
from shutil import copy
from subprocess import call, Popen, PIPE
from time import sleep
from .model import defaultFILES


# 未测试
def jmct(_input, _useEnv=True, _path=''):
    _input = os.path.realpath(_input)
    call(['jmct', _input])


def fisp(info, env, group, indir, outdir=''):
    def show(text):
        info(text, 3)

    def _copy(_src, _dst):
        if indir != outdir:
            copy(_src, _dst)

    def _run():
        _p = Popen(fisppath, cwd=outdir, stdout=PIPE)
        while True:
            line = _p.stdout.readline()
            if line:
                show(line.strip().decode('utf-8'))
                continue
            sleep(0.01)
            if _p.poll() is None:
                continue
            return _p.returncode

    # 传入参数处理
    fisppath = os.path.realpath(env[0].strip())
    if not os.path.isfile(fisppath):
        show('file not found: %s' % fisppath)
        return
    eaf = os.path.realpath(env[1].strip())
    indir = os.path.realpath(indir.strip())

    # 可选功能：指定输出目录
    if outdir == '':
        outdir = indir  # 默认为输入目录
    else:
        outdir = os.path.realpath(outdir)
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # 生成FILES文件
    files = defaultFILES
    files = files.replace(r'<case>', indir)
    files = files.replace(r'<eaf>', eaf)
    files = files.replace(r'<0>', group[0])
    files = files.replace(r'<1>', group[1])
    files = files.replace(r'<2>', group[2])
    # group[0]: 'n','p','d'
    # group[1]: '69', '100', '172', '175', '211', '315', '351'
    # group[2]: 'flt', 'fis', 'fus'
    with open(os.path.join(outdir, 'FILES'), 'w') as f:
        f.write(files)

    # 验证eaf地址
    eaf_gxs = r'%s\eaf_%s_gxs_%s_%s_20070' % (eaf, group[0], group[1], group[2])
    if not os.path.isfile(eaf_gxs):
        show(r'Cannot find: %s\eaf_%s_gxs_%s_%s_20070' % (eaf, group[0], group[1], group[2]))
        return

    # 创建空文件
    if os.path.isfile(indir + '/collapx'):
        _copy(indir + '/collapx', outdir + '/collapx')
    else:
        open(outdir + '/collapx', 'w').close()
    if os.path.isfile(indir + '/arrayx'):
        _copy(indir + '/arrayx', outdir + '/arrayx')
    else:
        open(outdir + '/arrayx', 'w').close()
    # 预执行程序
    if os.path.isfile(indir + '/summaryx'):
        _copy(indir + '/summaryx', outdir + '/summaryx')
    if os.path.isfile(indir + '/halfunc'):
        _copy(indir + '/halfunc', outdir + '/halfunc')
    _copy(indir + '/fluxes', outdir + '/fluxes')

    if not os.path.isfile(indir + '/collapx.i'):
        show('无效目录: %s' % indir)
        return
    copy(indir + '/collapx.i', outdir + '/input')
    show('正在处理 collapx.i ...')
    if _run() != 0:
        show('失败！')
        return
    copy(indir + '/arrayx.i', outdir + '/input')
    show('正在处理 arrayx.i ...')
    if _run() != 0:
        show('失败！')
        return

    # 遍历.i文件，执行程序
    _list = os.listdir(indir)
    for i in range(0, len(_list)):
        _input = _list[i]
        if _input[-2:] == '.i' and not (_input == 'collapx.i' or _input == 'arrayx.i'):
            name = _input[:-2]
            copy(indir + '/' + _input, outdir + '/input')
            show('正在处理 ' + _input + ' ...')
            if _run() != 0:
                show('失败！')
                return
            copy(outdir + '/output', outdir + '/' + name + '.o')
            show('执行成功，输出：' + os.path.join(outdir, name + '.o'))

    os.remove(outdir + '/input')
    os.remove(outdir + '/output')
