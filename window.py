import os
import re
import platform
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime
from static import Ui_MainWindow
from JFTools.model import defaultInput, defaultArrayx, defaultCollapx, defaultPrintlib
from JFTools.read import readj, readg, readf
from JFTools.write import writef, writej
from JFTools.call import jmct, fisp

SavedNeutron = None


class Dynamics(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Dynamics, self).__init__()
        self.setupUi(self)
        # 内部变量
        self._Zoom = 0
        self._LastRoute = 'C:/'
        self._FISPWork = ''
        self._InfoText = ''
        # False--JtoF True--FtoJ
        self._ToDoL = False
        # False--callF True--callJ
        self._ToDoR = False
        self._ProgressOne = 0
        self._ProgressAll = 0
        self._Num = 0
        self._OneStep = 0
        self._AllStep = 0
        # 动作信号
        self.JOutFilePickU.clicked.connect(self.openJFileUp)
        self.JOutFilePickD.clicked.connect(self.openJFileDown)
        self.GFilePick.clicked.connect(self.openGFile)
        self.FWorkPickU.clicked.connect(self.openFDirUp)
        self.FWorkPickD.clicked.connect(self.openFDirDown)
        self.LoadFile.clicked.connect(self.loadFiles)
        self.ResetL.clicked.connect(self.resetL)
        self.QuitL.clicked.connect(QCoreApplication.instance().quit)
        self.JtoFChose.clicked.connect(self.jtoF)
        self.FtoJChose.clicked.connect(self.ftoJ)
        self.StartL.clicked.connect(self.start)
        self.JModelPick.clicked.connect(self.openJModel)

        self.FPick.clicked.connect(self.openFInstall)
        self.EPick.clicked.connect(self.openEAFDir)
        self.FWorkPick.clicked.connect(self.openFDirRight)
        self.JInPick.clicked.connect(self.openJIn)
        self.ResetR.clicked.connect(self.resetR)
        self.QuitR.clicked.connect(QCoreApplication.instance().quit)
        self.StartR.clicked.connect(self.call)

        self.CallFISP.clicked.connect(self.callF)
        self.CallJMCT.clicked.connect(self.callJ)
        self.allEnableL(True)
        self.allEnableR(True)
        self.pickPath()

        self.fis = Fis()
        self.fis.signal.connect(self.info)

        self.jmct = Jm()
        self.jmct.signal.connect(self.info)

        self.j2f = JtoF()
        self.j2f.signal1.connect(self.updateBar)
        self.j2f.signal2.connect(self.getOneProgress)
        self.j2f.siginfo.connect(self.info)

        self.f2j = FtoJ()
        self.f2j.signal1.connect(self.updateBar)
        self.f2j.signal2.connect(self.getOneProgress)
        self.f2j.siginfo.connect(self.info)

        self.__desktop = QApplication.desktop()
        self.reSize()

    def closeEvent(self, event):
        self.savePath()
        event.accept()

    def pickPath(self):
        if 'wiz.ini' in os.listdir('.'):
            try:
                with open('./wiz.ini') as f:
                    lines = f.readlines()
                for line in lines:
                    tmp = line.split('=')
                    if len(tmp) != 2:
                        continue
                    if tmp[0] == 'FISPACT':
                        self.FPath.setText(tmp[1])
                    elif tmp[0] == 'EAF':
                        self.EPath.setText(tmp[1])
            except:
                pass

    def savePath(self):
        if self.FPath.text() != '' or self.EPath.text() != '':
            with open('./wiz.ini', 'w') as f:
                f.write('FISPACT=%s\n' % self.FPath.text())
                f.write('EAF=%s' % self.EPath.text())

    def reSize(self):
        screenRect = self.__desktop.screenGeometry()
        height = screenRect.height() * 9 // 10
        weight = round(37 * height / 52)
        self.resize(weight, height)
        self.setFixedSize(self.width(), self.height())

    def allEnableL(self, flag):
        self.JOutFilePathU.setEnabled(flag)
        self.GFilePath.setEnabled(flag)
        self.FWorkPathU.setEnabled(flag)
        self.JOutFilePickU.setEnabled(flag)
        self.GFilePick.setEnabled(flag)
        self.FWorkPickU.setEnabled(flag)
        self.GenRate.setEnabled(flag)
        self.Collapx.setEnabled(flag)
        self.Arrayx.setEnabled(flag)
        self.Input.setEnabled(flag)
        self.Printlib.setEnabled(flag)

        self._ToDoL = flag
        self.RetractLen.setEnabled(not flag)
        self.MaxFlag.setEnabled(not flag)
        self.JOutFilePathD.setEnabled(not flag)
        self.FWorkPathD.setEnabled(not flag)
        self.JModelPath.setEnabled(not flag)
        self.JOutFilePickD.setEnabled(not flag)
        self.FWorkPickD.setEnabled(not flag)
        self.JModelPick.setEnabled(not flag)
        self.JMCT.setEnabled(not flag)
        self.RemainJOut.setEnabled(not flag)

        self.FileEdit.setCurrentIndex(0 if flag else 4)

    def allEnableR(self, flag):
        self._ToDoR = flag
        self.Group.setEnabled(flag)
        self.Weight.setEnabled(flag)
        self.Particle.setEnabled(flag)
        self.FWorkPathR.setEnabled(flag)
        self.FWorkPick.setEnabled(flag)
        self.FPath.setEnabled(flag)
        self.EPath.setEnabled(flag)
        self.FPick.setEnabled(flag)
        self.EPick.setEnabled(flag)

        self.JInPath.setEnabled(not flag)
        self.JInPick.setEnabled(not flag)

    def jtoF(self):
        self.allEnableL(True)

    def ftoJ(self):
        self.allEnableL(False)

    def callF(self):
        self.allEnableR(True)

    def callJ(self):
        self.allEnableR(False)

    def getOneProgress(self, t, n):
        if self._ToDoL == True:
            self._Zoom = 1 / 8
        else:
            self._Zoom = 1 / 7
        self._Num = n
        self._OneStep = 100 / t
        self._AllStep = 100 * self._Zoom / t

    def updateBar(self, clear):
        if clear:
            self._ProgressOne = 0
            self._ProgressOne += self._OneStep
            self._ProgressAll += self._AllStep
            self.info('1/%d' % self._Num, 1)
        else:
            self._ProgressOne += self._OneStep
            self._ProgressAll += self._AllStep
            self.info(round((self._ProgressOne * self._Num) // 100), 2)
        self.Bar.setValue(round(self._ProgressAll))
        print(self._ProgressAll, self._Zoom, self._AllStep)

    def openJFileUp(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "JMCT Output File (*.out);;All Files (*)")
        self.JOutFilePathU.setText(self._LastRoute)
        if self.Sync.isChecked():
            self.JOutFilePathD.setText(self._LastRoute)

    def openJFileDown(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "JMCT Output File (*.out);;All Files (*)")
        self.JOutFilePathD.setText(self._LastRoute)
        if self.Sync.isChecked():
            self.JOutFilePathU.setText(self._LastRoute)

    def openJModel(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "JMCT Input File (*.input);;All Files (*)")
        self.JModelPath.setText(self._LastRoute)

    def openGFile(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "GDML Structure File (*.gdml);;All Files (*)")
        self.GFilePath.setText(self._LastRoute)

    def openFDirUp(self):
        self._LastRoute = QFileDialog.getExistingDirectory(self, "选择文件夹", self._LastRoute)
        self._FISPWork = self._LastRoute
        self.FWorkPathU.setText(self._LastRoute)
        if self.Sync.isChecked():
            self.FWorkPathD.setText(self._LastRoute)
        if self.GenCall.isChecked():
            self.FWorkPathR.setText(self._LastRoute)

    def openFDirDown(self):
        self._LastRoute = QFileDialog.getExistingDirectory(self, "选择文件夹", self._LastRoute)
        self._FISPWork = self._LastRoute
        self.FWorkPathD.setText(self._LastRoute)
        if self.Sync.isChecked():
            self.FWorkPathU.setText(self._LastRoute)
        if self.GenCall.isChecked():
            self.FWorkPathR.setText(self._LastRoute)

    def openFInstall(self):
        if 'Windows' in platform.system():
            self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                              "FISPACT Binary File (*.exe);;All Files (*)")
        else:
            self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                              "FISPACT Binary File (*.bin);;All Files (*)")
        self.FPath.setText(self._LastRoute)

    def openEAFDir(self):
        self._LastRoute = QFileDialog.getExistingDirectory(self, "选择文件夹", self._LastRoute)
        self.EPath.setText(self._LastRoute)

    def openFDirRight(self):
        self._LastRoute = QFileDialog.getExistingDirectory(self, "选择文件夹", self._LastRoute)
        self.FWorkPathR.setText(self._LastRoute)

    def openJIn(self):
        self._LastRoute, ok = QFileDialog.getOpenFileName(self, "选择文件", self._LastRoute,
                                                          "JMCT Input File (*.in);;All Files (*)")
        self.JInPath.setText(self._LastRoute)

    def info(self, text, mode=0):
        # mode=0 -- newline
        # mode=1 -- sameline
        # mode=2 -- revise
        # mode=3 -- newline without empty line
        time = QTime.currentTime()
        if mode == 0:
            if len(self._InfoText) > 0 and self._InfoText[-1] != '\n':
                self._InfoText += '\n\n'
            self._InfoText += '[%s] %s' % (time.toString(Qt.DefaultLocaleLongDate), text)
        elif mode == 1:
            self._InfoText += '...%s' % text
        elif mode == 2:
            self._InfoText = re.sub('\d+(/\d+)$', r'%d\1' % text, self._InfoText)
        elif mode == 3:
            if len(self._InfoText) > 0 and self._InfoText[-1] != '\n':
                self._InfoText += '\n'
            self._InfoText += '[%s] %s' % (time.toString(Qt.DefaultLocaleLongDate), text)
        self.StatusL.setText(self._InfoText)
        self.StatusR.setText(self._InfoText)
        self.StatusL.moveCursor(QTextCursor.End)
        self.StatusR.moveCursor(QTextCursor.End)

    def loadFiles(self):
        if self._ToDoL == True:
            if self._FISPWork == '':
                self.info('错误：未指定FISPACT工作目录', 0)
            else:
                self.info('从 %s 读取FISPACT输入文件' % self._FISPWork, 0)
                dirs = os.listdir(self._FISPWork)
                tmp = list(filter(lambda name: name[-2:] == '.i', dirs))
                # 是否找到至少一个文件
                found = False
                if 'collapx.i' in tmp:
                    self.info('更新collapx.i', 1)
                    with open(self._FISPWork + '/collapx.i') as f:
                        text = f.read()
                    self.CFileEdit.setText(text)
                    found = True
                else:
                    self.info('未找到collapx.i', 1)
                if 'arrayx.i' in tmp:
                    self.info('更新arrayx.i', 1)
                    with open(self._FISPWork + '/arrayx.i') as f:
                        text = f.read()
                    self.AFileEdit.setText(text)
                    found = True
                else:
                    self.info('未找到arrayx.i', 1)
                if 'printlib.i' in tmp:
                    self.info('更新printlib.i', 1)
                    with open(self._FISPWork + '/arrayx.i') as f:
                        text = f.read()
                    self.PFileEdit.setText(text)
                    found = True
                else:
                    self.info('未找到printlib.i', 1)
                if 'input.i' in tmp:
                    self.info('更新input.i', 1)
                    with open(self._FISPWork + '/input.i') as f:
                        text = f.read()
                    self.IFileEdit.setText(text)
                    found = True
                else:
                    self.info('未找到input.i', 1)
                if not found:
                    self.info('错误：工作目录下没有发现任何有效文件', 0)
        elif self._ToDoL == False:
            path = self.JModelPath.text()
            if path == '':
                self.info('错误：未指定JMCT模板文件', 0)
            else:
                try:
                    self.info('从 %s 读取JMCT模板文件' % path, 0)
                    with open(path) as f:
                        text = f.read()
                    self.JFileEdit.setText(text)
                except FileNotFoundError as e:
                    self.info('错误：JMCT模板文件位置无效 -> ' + repr(e), 0)
                    return
                except Exception as e:
                    self.info(repr(e))
                    return

    def resetL(self):
        self.info('左页面重置信息', 0)
        self.CFileEdit.setText(defaultCollapx)
        self.AFileEdit.setText(defaultArrayx)
        self.PFileEdit.setText(defaultPrintlib)
        self.IFileEdit.setText(defaultInput)
        self.JOutFilePathU.setText('')
        self.JOutFilePathD.setText('')
        self.GFilePath.setText('')
        self.FWorkPathU.setText('')
        self.FWorkPathD.setText('')
        self.JtoFChose.setChecked(True)
        self.RetractLen.setCurrentIndex(0)
        self.allEnableL(True)
        self._FISPWork = ''

    def resetR(self):
        self.info('右页面重置信息', 0)
        # self.Group.setCurrentIndex(3)
        # self.Weight.setCurrentIndex(0)
        # self.Particle.setCurrentIndex(0)
        # self.FPath.setText('')
        # self.EPath.setText('')
        # self.FWorkPathR.setText('')
        # self.JPath.setText('')
        # self.JInPath.setText('')
        # self.CallFISP.setChecked(True)
        # self.allEnableR(True)
        # self.envEnable()

    def start(self):
        self._ProgressAll = 0
        if self._ToDoL == True:
            try:
                self.info('执行JMCT --> FISPACT', 0)
                self.j2f.JPathU = self.JOutFilePathU.text()
                self.j2f.GPath = self.GFilePath.text()
                self.j2f.FPathU = self.FWorkPathU.text()
                self.j2f.CText = self.CFileEdit.toPlainText()
                self.j2f.AText = self.AFileEdit.toPlainText()
                self.j2f.IText = self.IFileEdit.toPlainText()
                self.j2f.PText = self.PFileEdit.toPlainText()
                self.j2f.GenRate = self.GenRate.text()
                self.j2f.SaveNeu_isChecked = self.SaveNeu.isChecked()

                self.j2f.start()

            except Exception as e:
                self.info(str(e), 0)

        elif self._ToDoL == False:
            try:
                self.info('执行FISPACT --> JMCT', 0)
                self.f2j.FPathD = self.FWorkPathD.text()
                self.f2j.JPathD = self.JOutFilePathD.text()
                self.f2j.JModel = self.JModelPath.text()
                self.f2j.JText = self.JFileEdit.toPlainText()
                self.f2j.maxFlag = float(self.MaxFlag.text())
                self.f2j.SaveNeu_isChecked = self.SaveNeu.isChecked()
                self.f2j.RemainJOut_isChecked = self.RemainJOut.isChecked()
                self.f2j.index = self.RetractLen.currentIndex()

                if self.f2j.JText == '':
                    self.info('自动导入JMCT模板文件', 0)
                    self.loadFiles()
                    self.f2j.JText = self.JFileEdit.toPlainText()

                self.f2j.start()
            except Exception as e:
                self.info(repr(e), 0)

    def call(self):
        if self._ToDoR == True:
            # callFISP
            FPath = self.FPath.text()
            EPath = self.EPath.text()
            Case = self.FWorkPathR.text()

            tmp = ['69', '100', '172', '175', '211', '315', '351']
            g = tmp[self.Group.currentIndex()]
            tmp = ['flt', 'fis', 'fus']
            w = tmp[self.Weight.currentIndex()]
            tmp = ['n', 'p', 'd']
            p = tmp[self.Particle.currentIndex()]

            if FPath == '':
                self.info('错误：未指定FISPACT主程序位置', 0)
                return
            if EPath == '':
                self.info('错误：未指定EAF数据库安装目录', 0)
                return
            if Case == '':
                self.info('错误：未指定FISPACT工作目录', 0)
                return
            group = [p, g, w]
            env = [FPath, EPath]
            self.fis.env = env
            self.fis.group = group
            self.fis.case = Case
            self.fis.start()
        else:
            # callJMCT
            JInPath = self.JInPath.text()
            if JInPath == '':
                self.info('错误：未指定JMCT输入文件', 0)
                return
            self.jmct.JInPath = JInPath
            self.jmct.start()


class Fis(QThread):
    signal = pyqtSignal(str, int)
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

    def __init__(self):
        super(JtoF, self).__init__()
        self.JPathU = ''
        self.GPath = ''
        self.FPathU = ''
        self.CText = ''
        self.AText = ''
        self.IText = ''
        self.PText = ''
        self.GenRate = ''

    def run(self):
        global SavedNeutron
        try:
            _GenRate = float(self.GenRate)
        except ValueError:
            self.siginfo.emit('错误：光子单位时间产额不是有效数据', 0)
            return
        except Exception as e:
            self.siginfo.emit(repr(e))
            return

        if self.SaveNeu_isChecked and SavedNeutron:
            self.siginfo.emit('读取暂存的物质信息', 0)
            _neutron = SavedNeutron
        elif self.SaveNeu_isChecked and not SavedNeutron:
            self.siginfo.emit('没有暂存的物质信息', 0)

        self.siginfo.emit('读取JMCT输出文件 %s' % self.JPathU, 0)
        if not (self.SaveNeu_isChecked and SavedNeutron):
            try:
                _neutron = readj(self.JPathU, self.signal1.emit, self.signal2.emit)
            except FileNotFoundError as e:
                self.siginfo.emit('错误：JMCT输出文件位置无效 -> ' + repr(e), 0)
                return
            except AttributeError as e:
                self.siginfo.emit('错误：JMCT输出文件不合法 -> ' + repr(e), 0)
                return
            except Exception as e:
                self.siginfo.emit(repr(e), 0)
                return
        if self.SaveNeu_isChecked and not SavedNeutron:
            self.siginfo.emit('储存物质信息', 0)
            SavedNeutron = _neutron
        self.siginfo.emit('读取GDML结构文件 %s' % self.GPath, 0)
        try:
            _structure = readg(self.GPath, self.signal1.emit, self.signal2.emit)
        except FileNotFoundError:
            self.siginfo.emit('错误：GDML结构文件位置无效', 0)
            return
        except Exception as e:
            self.siginfo.emit(repr(e), 0)
            return

        self.siginfo.emit('将FISPACT输入文件写入 %s' % self.FPathU, 0)
        try:
            writef(self.FPathU, _GenRate, _neutron, _structure, self.IText, self.CText, self.AText, self.PText,
                   self.signal1.emit, self.signal2.emit)
        except Exception as e:
            self.siginfo.emit(repr(e), 0)
            return
        self.siginfo.emit('文件转换完成', 0)


class FtoJ(QThread):
    signal1 = pyqtSignal(bool)  # updateBar
    signal2 = pyqtSignal(int, int)  # getOneProgress
    siginfo = pyqtSignal(str, int)  # info

    def __init__(self):
        super(FtoJ, self).__init__()
        self.FPathD = ''
        self.JPathD = ''
        self.JModel = ''
        self.JText = ''
        self.maxFlag = ''

    def run(self):
        global SavedNeutron
        tmp = [' ' * 3, ' ' * 2, ' ' * 4, '\t']
        split = tmp[self.index]

        if self.SaveNeu_isChecked and SavedNeutron:
            self.siginfo.emit('读取暂存的物质信息', 0)
            neutron = SavedNeutron
        elif self.SaveNeu_isChecked and not SavedNeutron:
            self.siginfo.emit('没有暂存的物质信息', 0)
        self.siginfo.emit('读取JMCT输出文件 %s' % self.JPathD, 0)
        if not (self.SaveNeu_isChecked and SavedNeutron):
            try:
                neutron = readj(self.JPathD, self.signal1.emit, self.signal2.emit)
            except FileNotFoundError:
                self.siginfo.emit('错误：JMCT输出文件位置无效', 0)
                return
            except AttributeError as e:
                self.siginfo.emit('错误：JMCT输出文件不合法 -> ' + repr(e), 0)
                return
            except Exception as e:
                self.siginfo.emit(repr(e), 0)
                return
        if self.SaveNeu_isChecked and not SavedNeutron:
            self.siginfo.emit('储存物质信息', 0)
            SavedNeutron = neutron
        self.siginfo.emit('读取FISPACT输出文件 %s' % self.FPathD, 0)
        try:
            distributes = readf(self.FPathD, self.maxFlag, self.signal1.emit, self.signal2.emit)
        except FileNotFoundError as e:
            self.siginfo.emit('错误：FISPACT输出文件位置无效 ->' + repr(e), 0)
            return
        except Exception as e:
            self.siginfo.emit(repr(e), 0)
            return
        pos = self.JPathD.rindex('.')
        if self.RemainJOut_isChecked:
            newPath = self.JPathD[:pos] + '_new' + '.in'
        else:
            newPath = self.JPathD[:pos] + '.in'
        self.siginfo.emit('将新的JMCT输入文件写入 %s' % newPath, 0)
        try:
            writej(self.JModel, self.JText, neutron, distributes, split, newPath, self.signal1.emit, self.signal2.emit)
        except AttributeError as e:
            self.siginfo.emit('错误：JMCT模板文件不含有{source}关键字 -> ' + repr(e), 0)
            return
        except Exception as e:
            self.siginfo.emit(repr(e), 0)
            return
        self.siginfo.emit('文件转换完成', 0)
