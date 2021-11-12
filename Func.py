# -*- coding: utf-8 -*-
"""
[Mathematica]の代用品
"""


import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import sympy
from sympy import *


class Function(QtWidgets.QMainWindow):
    def __init__(self):
        super(Function, self).__init__()
        self.findIndex = -1
        self.resize(1000, 500)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle('Functions')
        self.textEdit = QtWidgets.QTextEdit(self)
        self.setCentralWidget(self.textEdit)
        
        self.fileMenu = self.menuBar().addMenu('ファイル')
        self.openAction = self.fileMenu.addAction('開く')
        self.saveAction = self.fileMenu.addAction('保存')
        self.endAction = self.fileMenu.addAction('終了')
        
        self.execMenu = self.menuBar().addMenu('実行')
        self.execAction = self.execMenu.addAction('コードを実行')
        
        self.editMenu = self.menuBar().addMenu('編集')
        self.findAction = self.editMenu.addAction('検索')
        self.replaceAction = self.editMenu.addAction('置換')
        
        self.formatMenu = self.menuBar().addMenu('書式')
        self.fontAction = self.formatMenu.addAction('フォント')
        
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.execAction.triggered.connect(self._exec)
        self.endAction.triggered.connect(lambda : Ender(self).show())
        self.findAction.triggered.connect(lambda : FindDialog(self).show())
        self.replaceAction.triggered.connect(lambda : ReplaceDialog(self).show())
        self.fontAction.triggered.connect(self.changeFont)
        
    
    
    def end_ (self):
        self.close()
        
        
    def openFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, '開く', '', 'Text file(*.txt)')
        if fileName == '':
            return
        with open(fileName, mode='r') as f:
            self.textEdit.setPlainText(f.read())
    
    
    def saveFile(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, '保存', '', 'Text file(*.txt)')
        if fileName == '':
            return
        with open(fileName, mode='w') as f:
            f.write(self.textEdit.toPlainText())
    
    
    def saveFile_2(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, '保存', '', 'Text file(*.txt)')
        if fileName == '':
            return
        with open(fileName, mode='w') as f:
            f.write(self.textEdit.toPlainText())
            Function.end_(functions)
    
    
    def findText(self, findText, reverse=False):
        if findText == '':
            return
        text = self.textEdit.toPlainText()
        if reverse:
            self.findIndex = text.rfind(findText, 0, self.findIndex )
        else:
            self.findIndex = text.find(findText, self.findIndex + 1 )
        if self.findIndex == -1:
            return
        textCursor = self.textEdit.textCursor()
        textCursor.setPosition(self.findIndex)
        textCursor.setPosition(self.findIndex + len(findText), QtGui.QTextCursor.KeepAnchor)
        self.textEdit.setTextCursor(textCursor)
        self.activateWindow()
    
    
    def replace(self, findText, replaceText):
        text = self.textEdit.toPlainText()
        if findText == self.textEdit.textCursor().selectedText():
            index = self.textEdit.textCursor().selectionStart()
            replaced = text[ : index ] + replaceText + text[index + len(findText) : ]
            self.textEdit.setPlainText(replaced)
        self.findText(findText)
    
    
    def replaceAll(self, findText, replaceText):
        self.textEdit.setPlainText(self.textEdit.toPlainText().replace(findText, replaceText))
    
    
    def changeFont(self):
        font, ok = QtWidgets.QFontDialog.getFont(self.textEdit.currentFont(), self)
        if not ok:
            return
        self.textEdit.setFont(font)
    
    
    def _exec(self):
        text = self.textEdit.toPlainText()
        _text = text.splitlines()
        for text_1 in range(len(_text) - 1):
            exec(_text[text_1])
        dfgh = sympy.sympify(_text[-1])
        print(dfgh)
        sympy.pprint(dfgh)



class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.label_0 = QtWidgets.QLabel('検索する文字列:')
        self.label_1 = QtWidgets.QLabel('置換後の文字列:')
        self.label_2 = QtWidgets.QLabel('保存しますか？')
        self.lineEdit_0 = QtWidgets.QLineEdit()
        self.lineEdit_1 = QtWidgets.QLineEdit()
        self.button_0 = QtWidgets.QPushButton('次のを検索')
        self.button_1 = QtWidgets.QPushButton('前のを検索')
        self.button_2 = QtWidgets.QPushButton('置換')
        self.button_3 = QtWidgets.QPushButton('全て置換')
        self.button_4 = QtWidgets.QPushButton('キャンセル')
        self.button_5 = QtWidgets.QPushButton('保存する')
        self.button_6 = QtWidgets.QPushButton('保存しない')
        
        self.setLayout( QtWidgets.QGridLayout() )
        self.layout().addWidget(self.label_0,    0, 0, 1, 1 )
        self.layout().addWidget(self.label_1,    1, 0, 1, 1 )
        self.layout().addWidget(self.label_2,    0, 0, 1, 1 )
        self.layout().addWidget(self.lineEdit_0, 0, 1, 1, 1 )
        self.layout().addWidget(self.lineEdit_1, 1, 1, 1, 1 )
        self.layout().addWidget(self.button_0,   0, 2, 1, 1 )
        self.layout().addWidget(self.button_1,   1, 2, 1, 1 )
        self.layout().addWidget(self.button_2,   2, 2, 1, 1 )
        self.layout().addWidget(self.button_3,   3, 2, 1, 1 )
        self.layout().addWidget(self.button_4,   4, 2, 1, 1 )
        self.layout().addWidget(self.button_5,   0, 2, 1, 1 )
        self.layout().addWidget(self.button_6,   0, 3, 1, 1 )
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        
        self.button_0.clicked.connect(lambda : self.parent().findText(self.lineEdit_0.text()))
        self.button_1.clicked.connect(lambda : self.parent().findText(self.lineEdit_0.text(), True))
        self.button_2.clicked.connect(lambda : self.parent().replace(self.lineEdit_0.text(), self.lineEdit_1.text() ))
        self.button_3.clicked.connect(lambda : self.parent().textEdit.replaceAll( self.lineEdit_0.text(), self.lineEdit_1.text() ))
        self.button_4.clicked.connect(lambda : self.reject())
        self.button_5.clicked.connect(self.ends)
        self.button_6.clicked.connect(self.endg)
    
    
    def endg (self):
        self.close()
        self.parent().end_()
        
    def ends(self):
        self.close()
        self.parent().saveFile_2()


class FindDialog(Dialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)
        self.setWindowTitle('検索')
        self.label_1.hide()
        self.lineEdit_1.hide()
        self.button_2.hide()
        self.button_3.hide()
        self.button_5.hide()
        self.button_6.hide()
        self.label_2.hide()


class ReplaceDialog(Dialog):
    def __init__(self, parent=None):
        super(ReplaceDialog, self).__init__(parent)
        self.setWindowTitle('置換')
        self.button_1.hide()
        self.button_5.hide()
        self.button_6.hide()
        self.label_2.hide()

class Ender(Dialog):
    def __init__(self, parent=None):
        super(Ender, self).__init__(parent)
        self.setWindowTitle('Functions')
        self.button_0.hide()
        self.button_1.hide()
        self.button_2.hide()
        self.button_3.hide()
        self.label_0.hide()
        self.label_1.hide()
        self.lineEdit_0.hide()
        self.lineEdit_1.hide()
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    functions = Function()
    functions.show()
    app.exec()
   
