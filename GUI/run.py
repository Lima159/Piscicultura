import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtCore import QTimer,QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
import coletarAmostra, readFiles
from colorWindow import ColorWindow
from keyboard import VirtualKeyboard
import os, sys
from PIL import Image
import webcolors
from colorthief import ColorThief

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.printer = QPrinter()
        self.scaleFactor = 0.0
        self.fileName = "image.jpg"
        self.check = True

        self.imageLabel = QLabel()
        self.imageLabel.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))
        self.imageLabel.setAlignment(Qt.AlignCenter)
       
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)

        self.createActions()
        #self.createMenus()    
        self.createToolBars()   

        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)         

    def createToolBars(self):
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

        self.menuBar = QtWidgets.QToolBar("Ações")
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.menuBar)

        self.menuBar.addAction(QIcon("resources/file.png"), "&Abrir Arquivo", self.open)
        self.menuBar.addSeparator()
        self.menuBar.addAction(QIcon("resources/camera.png"), "&Coletar Amostra", self.coletarAmostra)
        self.menuBar.addSeparator()
        self.menuBar.addAction(QIcon("resources/adjust.png"), "&Calibrar", self.calibrar)
        self.menuBar.addSeparator()
        self.menuBar.addAction(QIcon("resources/analyze.png"), "&Analisar Amostra", self.getCoordenada)
        self.menuBar.addSeparator()
        self.menuBar.addAction(QIcon("resources/help.png"), "&Ajuda")
        self.menuBar.addSeparator()
        self.menuBar.addAction(QIcon("resources/exit.png"), "&Sair", self.close)

    #REALIZA CLICK PARA OBTER COORDENADA
    def getCoordenada(self):
        mensuracao = self.getMensuracao()
        color_thief = ColorThief(self.fileName)
        dominant_color = color_thief.get_color(quality=1)
        #print("Dominante:", dominant_color)
        closest_color = readFiles.get_closet_color(list(dominant_color), mensuracao)
        resultado_analise = readFiles.get_resultado(closest_color, mensuracao)
        print("Resultado: " + str(resultado_analise))
        self.colorView = ColorWindow(closest_color[0][0], closest_color[0][1], closest_color[0][2], 
            dominant_color[0], dominant_color[1], dominant_color[2], resultado_analise)
        self.colorView.setWindowTitle("Análise de cores");
        self.colorView.show()

    def getMensuracao(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'Selecione a mensuração que deseja utilizar na análise', '',
                                                  'Mensuração (*.txt *.csv)', options=options)
        return fileName

    #OBTEM COR A PARTIR DA COORDENADA
    def getPixel(self, event):
        if self.check:
            x = event.pos().x()
            y = event.pos().y()
            print("X=",x," y= ",y)
            im = Image.open(self.fileName)
            pix = im.convert('RGB')  
            r, g, b = pix.getpixel((x, y))
            
            self.colorView = ColorWindow(r, g, b)
            self.colorView.show()

    def calibrar(self):
        self.calibrarView = VirtualKeyboard()
        self.calibrarView.show()

    def coletarAmostra(self):
        coletarAmostra.coleta(self) 

    def open(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, 'Selecione a imagem da amostra', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        print (self.fileName)
        if self.fileName:
            image = QImage(self.fileName)
            #print(type(image))
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % self.fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()
            #self.resize(image.width() + 130, image.height() + 40)
            
            #if not self.fitToWindowAct.isChecked():
            #    self.imageLabel.adjustSize()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()
    
    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)
        self.coletarAmostras = QAction("&Coletar Amostra", self, triggered=self.coletarAmostra)
        self.getCoordenad = QAction("&RGB", self, triggered=self.getCoordenada)
        self.Calibrar = QAction("&Calibrar", self, triggered=self.calibrar)
        
    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.processMenu = QMenu("&Amostra", self)
        self.processMenu.addAction(self.coletarAmostras)

        self.analiseMenu = QMenu("&Analise", self)
        self.analiseMenu.addAction(self.Calibrar)
        self.analiseMenu.addAction(self.getCoordenad)
        
        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.processMenu)
        self.menuBar().addMenu(self.analiseMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    imageViewer.setWindowTitle("AquaSys")
    imageViewer.setWindowIcon(QtGui.QIcon('resources/fish.png'))

    splash = QSplashScreen(QPixmap('resources/ifba.jpg'))
    splash.show()
    QTimer.singleShot(2000, splash.close)

    sys.exit(app.exec_())
