# -*- coding: utf-8 -*-
import os
import traceback
import pathlib
from PyQt5.QtCore import QThread, pyqtSignal
from JFlink.read import readj, readg, readf
from JFlink.write import writef, writej
from JFlink.call import CallJm, CallFis


class Fis(QThread, CallFis):
    siginfo = pyqtSignal(str, int)
    sigend = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.case = ''
        self.pid = 0
        self.workalone = False

    def run(self):
        count = 0
        self.siginfo.emit('调用Fispact中...', 0)
        try:
            p = pathlib.Path(self.case.strip())
            _dirs = [_ for _ in p.iterdir() if _.is_dir()]
            for _dir in _dirs:
                _path = p.resolve() / _dir
                if not self.isInterruptionRequested():
                    count += 1
                    self.siginfo.emit('[%d/%d]%s' % (count, len(_dirs), str(_path)), 0)
                    self.fisp(_path, info=self.siginfo.emit)
                    # 清理工作目录
                    self.clean2(_path)
        except Exception as e:
            self.siginfo.emit(traceback.format_exc(), 0)
        finally:
            self.siginfo.emit('调用结束', 0)
            self.sigend.emit()

    def kill(self):
        if self.pid != 0:
            os.kill(self.pid, 9)

    def clean2(self, path, flag=0):
        for file in path.iterdir():
            if file.name in ['arrayx', 'collapx', 'graph', 'halfunc', 'summaryx'] or (flag and file.suffix == '.o'):
                (path / file).unlink()

    # def cleanall(self, path):
    #     self.clean2(path, 1)


class Jm(QThread, CallJm):
    siginfo = pyqtSignal(str, int)
    sigend = pyqtSignal()

    def __init__(self):
        super(Jm, self).__init__()
        self.JInPath = ''

    def run(self):
        self.siginfo.emit('调用Jmct中...', 0)
        try:
            self.jmct(self.JInPath, info=self.siginfo.emit)
        except Exception as e:
            self.siginfo.emit(traceback.format_exc(), 0)
        self.siginfo.emit('调用结束', 0)
        self.sigend.emit()

    def kill(self):
        if self.pid != 0:
            os.kill(self.pid, 9)


class JtoF(QThread):
    signal1 = pyqtSignal(bool)  # updateBar
    signal2 = pyqtSignal(int, int)  # getOneProgress
    siginfo = pyqtSignal(str, int)  # info
    sigend = pyqtSignal()

    def __init__(self):
        super(JtoF, self).__init__()
        self.JPathU = ''
        self.GPath = ''
        self.FPath = ''
        self.CText = ''
        self.AText = ''
        self.IText = ''
        self.PText = ''
        self.GenRate = ''

    def run(self):
        self.siginfo.emit('执行JMCT --> FISPACT', 0)
        try:
            _GenRate = float(self.GenRate)
        except ValueError:
            self.siginfo.emit('错误：光子单位时间产额不是有效数据', 0)
            self.sigend.emit()
            return
        except Exception as e:
            self.siginfo.emit(traceback.format_exc(), 0)
            self.sigend.emit()
            return
        self.siginfo.emit('读取JMCT输出文件 %s' % self.JPathU, 0)
        try:
            _neutron = readj(self.JPathU, self.signal1.emit, self.signal2.emit)
        except FileNotFoundError as e:
            self.siginfo.emit('错误：JMCT输出文件位置无效 -> ' + repr(e), 0)
            self.sigend.emit()
            return
        except AttributeError as e:
            self.siginfo.emit('错误：JMCT输出文件不合法 -> ' + repr(e), 0)
            self.sigend.emit()
            return
        except Exception as e:
            self.siginfo.emit(traceback.format_exc(), 0)
            self.sigend.emit()
            return
        self.siginfo.emit('读取GDML结构文件 %s' % self.GPath, 0)
        try:
            _structure = readg(self.GPath, self.signal1.emit, self.signal2.emit)
        except FileNotFoundError:
            self.siginfo.emit('错误：GDML结构文件位置无效', 0)
            self.sigend.emit()
            return
        except Exception as e:
            self.siginfo.emit(traceback.format_exc(), 0)
            self.sigend.emit()
            return

        self.siginfo.emit('将FISPACT输入文件写入 %s' % self.FPath, 0)
        try:
            writef(self.FPath, _GenRate, _neutron, _structure, self.IText, self.CText, self.AText, self.PText,
                   self.signal1.emit, self.signal2.emit)
        except Exception as e:
            self.siginfo.emit(traceback.format_exc(), 0)
            self.sigend.emit()
            return
        self.siginfo.emit('文件转换完成', 0)
        self.sigend.emit()


class FtoJ(QThread):
    signal1 = pyqtSignal(bool)  # updateBar
    signal2 = pyqtSignal(int, int)  # getOneProgress
    siginfo = pyqtSignal(str, int)  # info
    sigend = pyqtSignal()

    def __init__(self):
        super(FtoJ, self).__init__()
        self.FPath = ''
        self.JPathD = ''
        self.JModel = ''
        self.JText = ''
        self.Max = ''
        self.Remain = True

    def run(self):
        self.siginfo.emit('执行FISPACT --> JMCT', 0)

        try:
            maxFlag = float(self.Max)
        except Exception as e:
            self.siginfo.emit(traceback.format_exc(), 0)
            self.sigend.emit()
            return
        self.siginfo.emit('读取JMCT输出文件 %s' % self.JPathD, 0)
        try:
            neutron = readj(self.JPathD, self.signal1.emit, self.signal2.emit)
        except FileNotFoundError:
            self.siginfo.emit('错误：JMCT输出文件位置无效', 0)
            self.sigend.emit()
            return
        except AttributeError as e:
            self.siginfo.emit('错误：JMCT输出文件不合法 -> ' + repr(e), 0)
            self.sigend.emit()
            return
        except Exception as e:
            self.siginfo.emit(traceback.format_exc(), 0)
            self.sigend.emit()
            return
        self.siginfo.emit('读取FISPACT输出文件 %s' % self.FPath, 0)
        try:
            distributes = readf(self.FPath, maxFlag, self.signal1.emit, self.signal2.emit)
        except FileNotFoundError as e:
            self.siginfo.emit('错误：FISPACT输出文件位置无效 ->' + repr(e), 0)
            self.sigend.emit()
            return
        except Exception as e:
            self.siginfo.emit(traceback.format_exc(), 0)
            self.sigend.emit()
            return
        tmp = pathlib.Path(self.JModel)
        if self.Remain:
            newPath = tmp.with_name(tmp.stem + '_new.input')
        else:
            newPath = tmp.with_name(tmp.stem + '.input')
        self.siginfo.emit('将新的JMCT输入文件写入 %s' % newPath, 0)
        try:
            writej(newPath, self.JText, neutron, distributes, self.signal1.emit, self.signal2.emit)
        except AttributeError as e:
            self.siginfo.emit('错误：JMCT模板文件不含有{source}关键字 -> ' + repr(e), 0)
            self.sigend.emit()
            return
        except Exception:
            self.siginfo.emit(traceback.format_exc(), 0)
            self.sigend.emit()
            return
        self.siginfo.emit('文件转换完成', 0)
        self.sigend.emit()
