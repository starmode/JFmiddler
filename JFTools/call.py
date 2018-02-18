# -*- coding: utf-8 -*-
from pathlib import Path
import shutil
from subprocess import Popen, PIPE
from time import sleep
from .model import defaultFILES


def copy(src: Path, dst: Path):
    shutil.copy(str(src), str(dst))


def jmct(info, jinput, gpath=''):
    _input = Path(jinput).resolve()
    # if gpath == '':
    #     _gpath = _input.parent
    # else:
    #     _gpath = gpath
    _gpath = _input.parent

    def _run():
        _p = Popen('jmct ' + str(_input), cwd=_gpath, stdout=PIPE, shell=True)
        while True:
            line = _p.stdout.readline()
            if line:
                info(line.strip().decode('utf-8'), 3)
                continue
            sleep(0.01)
            if _p.poll() is None:
                continue
            return _p.returncode

    def _check():
        _q = Popen('which jmct', shell=True)
        _q.wait()
        return _q.returncode

    if _check():
        try:
            _run()
        except Exception as a:
            info(repr(a), 3)
    else:
        info('无环境变量', 3)


def fisp(info, pid, env, group, indir: Path, _outdir=None):
    def show(text):
        info(text, 3)

    def clean():
        for file in ['input', 'output', 'FILES']:
            try:
                (indir / file).unlink()
            except FileNotFoundError:
                pass

    def _copy(_src, _dst):
        if indir != outdir:
            copy(_src, _dst)

    def _run():
        _p = Popen(str(fisppath), cwd=outdir, stdout=PIPE)
        pid[0] = _p.pid
        while True:
            line = _p.stdout.readline()
            if line:
                show(line.strip().decode('utf-8'))
                continue
            sleep(0.01)
            if _p.poll() is None:
                continue
            pid[0] = 0
            return _p.returncode

    # 传入参数处理
    fisppath = Path(env[0].strip()).resolve()
    if not fisppath.is_file():
        show('file not found: %s' % fisppath)
        return
    eaf = Path(env[1].strip()).resolve()
    # indir = Path(indir).resolve()

    # 可选功能：指定输出目录
    if _outdir is None:
        outdir = indir  # 默认为输入目录
    else:
        outdir = Path(_outdir).resolve()
        if not outdir.exists():
            outdir.mkdir()

    # 生成FILES文件
    files = defaultFILES
    files = files.replace(r'<case>', str(indir))
    files = files.replace(r'<eaf>', str(eaf))
    files = files.replace(r'<0>', group[0])
    files = files.replace(r'<1>', group[1])
    files = files.replace(r'<2>', group[2])
    # group[0]: 'n','p','d'
    # group[1]: '69', '100', '172', '175', '211', '315', '351'
    # group[2]: 'flt', 'fis', 'fus'
    with (outdir / 'FILES').open('w') as f:
        f.write(files)

    # 验证eaf地址
    eaf_gxs = r'eaf_%s_gxs_%s_%s_20070' % (group[0], group[1], group[2])
    if not Path(eaf / eaf_gxs).is_file():
        show(r'Cannot find: %s' % (eaf / eaf_gxs))
        return
    # 创建空文件
    if (indir / 'collapx').is_file():
        _copy(indir / 'collapx', outdir / 'collapx')
    else:
        (outdir / 'collapx').touch()
    if (indir / 'arrayx').is_file():
        _copy(indir / 'arrayx', outdir / 'arrayx')
    else:
        (outdir / 'arrayx').touch()
    # 预执行程序
    if (indir / 'summaryx').is_file():
        _copy(indir / 'summaryx', outdir / 'summaryx')
    if (indir / 'halfunc').is_file():
        _copy(indir / 'halfunc', outdir / 'halfunc')
    _copy(indir / 'fluxes', outdir / 'fluxes')

    if not (indir / 'collapx.i').is_file():
        show('无效目录: %s' % indir)
        return
    copy(indir / 'collapx.i', outdir / 'input')
    show('正在处理 collapx.i ...')
    if _run() != 0:
        # show('失败！')
        clean()
        return
    copy(indir / 'arrayx.i', outdir / 'input')
    show('正在处理 arrayx.i ...')
    if _run() != 0:
        # show('失败！')
        clean()
        return

    # 遍历.i文件，执行程序
    _list = list(indir.glob('*'))
    for i in range(0, len(_list)):
        _input = _list[i]
        if _input.suffix == '.i' and not (_input.name == 'collapx.i' or _input.name == 'arrayx.i'):
            name = _input.stem
            copy(indir / _input, outdir / 'input')
            show('正在处理 ' + str(_input) + ' ...')
            if _run() != 0:
                # show('失败！')
                clean()
                return
            copy(outdir / 'output', outdir.joinpath(name + '.o'))
            show('执行成功，输出：' + str(outdir.joinpath(name + '.o')))
    clean()
