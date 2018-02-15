import os
from PyQt5.QtCore import QThread, pyqtSignal
from JFTools.read import readj, readg, readf
from JFTools.write import writef, writej
from JFTools.call import jmct, fisp
from JFTools.model import Data

class Fis(QThread):
    signal = pyqtSignal(str, int)
    sigend = pyqtSignal()
    case = ''
    env = ['', '']
    group = ['', '', '']

    def run(self):
        self.signal.emit('调用Fispact中...', 0)
        try:
            for _dir in os.listdir(self.case):
                _path = os.path.join(self.case, _dir)
                self.signal.emit(_path, 0)
                if os.path.isdir(_path):
                    fisp(self.signal.emit, self.env, self.group, _path)
        except Exception as a:
            self.signal.emit(str(a), 0)
        self.signal.emit('调用结束', 0)


class Jm(QThread):
    signal = pyqtSignal(str, int)
    sigend = pyqtSignal()
    JInPath = ''

    def run(self):
        self.signal.emit('调用Jmct中...', 0)
        try:
            jmct(self.signal.emit, self.JInPath)
        except Exception as a:
            self.signal.emit(str(a), 0)
        self.signal.emit('调用结束', 0)


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
        self._SavedNeutron = None

    def run(self):
        self.siginfo.emit('执行JMCT --> FISPACT', 0)
        try:
            _GenRate = float(self.GenRate)
        except ValueError:
            self.siginfo.emit('错误：光子单位时间产额不是有效数据', 0)
            self.sigend.emit()
            return
        except Exception as e:
            self.siginfo.emit(repr(e))
            self.sigend.emit()
            return

        if self.SaveNeu_isChecked and self._SavedNeutron:
            self.siginfo.emit('读取暂存的物质信息', 0)
            _neutron = self._SavedNeutron
        elif self.SaveNeu_isChecked and not self._SavedNeutron:
            self.siginfo.emit('没有暂存的物质信息', 0)

        self.siginfo.emit('读取JMCT输出文件 %s' % self.JPathU, 0)
        if not (self.SaveNeu_isChecked and self._SavedNeutron):
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
                self.siginfo.emit(repr(e), 0)
                self.sigend.emit()
                return
        if self.SaveNeu_isChecked and not self._SavedNeutron:
            self.siginfo.emit('储存物质信息', 0)
            self._SavedNeutron = _neutron
        self.siginfo.emit('读取GDML结构文件 %s' % self.GPath, 0)
        try:
            _structure = readg(self.GPath, self.signal1.emit, self.signal2.emit)
        except FileNotFoundError:
            self.siginfo.emit('错误：GDML结构文件位置无效', 0)
            self.sigend.emit()
            return
        except Exception as e:
            self.siginfo.emit(repr(e), 0)
            self.sigend.emit()
            return

        self.siginfo.emit('将FISPACT输入文件写入 %s' % self.FPath, 0)
        try:
            writef(self.FPath, _GenRate, _neutron, _structure, self.IText, self.CText, self.AText, self.PText,
                   self.signal1.emit, self.signal2.emit)
        except Exception as e:
            self.siginfo.emit(repr(e), 0)
            self.sigend.emit()
            return
        self.siginfo.emit('文件转换完成', 0)
        self.sigend.emit()

class FtoJ(QThread):

    signal1 = pyqtSignal(bool)  # updateBar
    signal2 = pyqtSignal(int, int)  # getOneProgress
    siginfo = pyqtSignal(str, int)  # info
    sigend = pyqtSignal(Data)

    def __init__(self):
        super(FtoJ, self).__init__()
        self.FPath = ''
        self.JPathD = ''
        self.JModel = ''
        self.JText = ''
        self.Max = ''
        self.Retract = 0
        self.WheSaveNeu = False
        self.Remain = True
        self.SavedNeutron = None

    def run(self):
        self.siginfo.emit('执行FISPACT --> JMCT', 0)

        tmp = [' ' * 3, ' ' * 2, ' ' * 4, '\t']
        split = tmp[self.Retract]

        try:
            maxFlag = float(self.Max)
        except Exception as e:
            self.siginfo.emit(repr(e), 0)
            self.sigend.emit(self.SavedNeutron)
            return
        if self.WheSaveNeu and self.SavedNeutron:
            self.siginfo.emit('读取暂存的物质信息', 0)
            neutron = self.SavedNeutron
        elif self.WheSaveNeu and not self.SavedNeutron:
            self.siginfo.emit('没有暂存的物质信息', 0)
        self.siginfo.emit('读取JMCT输出文件 %s' % self.JPathD, 0)
        if not (self.WheSaveNeu and self.SavedNeutron):
            try:
                neutron = readj(self.JPathD, self.signal1.emit, self.signal2.emit)
            except FileNotFoundError:
                self.siginfo.emit('错误：JMCT输出文件位置无效', 0)
                self.sigend.emit(self.SavedNeutron)
                return
            except AttributeError as e:
                self.siginfo.emit('错误：JMCT输出文件不合法 -> ' + repr(e), 0)
                self.sigend.emit(self.SavedNeutron)
                return
            except Exception as e:
                self.siginfo.emit(repr(e), 0)
                self.sigend.emit(self.SavedNeutron)
                return
        if self.WheSaveNeu and not self.SavedNeutron:
            self.siginfo.emit('储存物质信息', 0)
            self.SavedNeutron = neutron
        self.siginfo.emit('读取FISPACT输出文件 %s' % self.FPath, 0)
        try:
            distributes = readf(self.FPath, maxFlag, self.signal1.emit, self.signal2.emit)
        except FileNotFoundError as e:
            self.siginfo.emit('错误：FISPACT输出文件位置无效 ->' + repr(e), 0)
            self.sigend.emit(self.SavedNeutron)
            return
        except Exception as e:
            self.siginfo.emit(repr(e), 0)
            self.sigend.emit(self.SavedNeutron)
            return
        pos = self.JPathD.rindex('.')
        if self.Remain:
            newPath = self.JPathD[:pos] + '_new' + '.in'
        else:
            newPath = self.JPathD[:pos] + '.in'
        self.siginfo.emit('将新的JMCT输入文件写入 %s' % newPath, 0)
        try:
            writej(self.JModel, self.JText, neutron, distributes, split, newPath, self.signal1.emit, self.signal2.emit)
        except AttributeError as e:
            self.siginfo.emit('错误：JMCT模板文件不含有{source}关键字 -> ' + repr(e), 0)
            self.sigend.emit(self.SavedNeutron)
            return
        except Exception as e:
            self.siginfo.emit(repr(e), 0)
            self.sigend.emit(self.SavedNeutron)
            return
        self.siginfo.emit('文件转换完成', 0)
        self.sigend.emit(self.SavedNeutron)