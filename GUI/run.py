import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
#from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
#    qApp, QFileDialog, QTableView, QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtWidgets import *
import coletarAmostra, cinza, cantizacao, readFiles
import os, sys
from PIL import Image
import webcolors
from googletrans import Translator
from colorthief import ColorThief

class ColorWindow(QMainWindow):
    def getNameColor(self):
        try:
            self.nameColor = webcolors.rgb_to_name(self.requested_colour)
        except ValueError:
            min_colours = {}
            for key, name in webcolors.css3_hex_to_names.items():
                r_c, g_c, b_c = webcolors.hex_to_rgb(key)
                rd = (r_c - self.requested_colour[0]) ** 2
                gd = (g_c - self.requested_colour[1]) ** 2
                bd = (b_c - self.requested_colour[2]) ** 2
                min_colours[(rd + gd + bd)] = name
            self.nameColor = min_colours[min(min_colours.keys())]

    def __init__(self, r1, g1, b1, r2, g2, b2):
        super().__init__()
        
        self.height = 300
        self.width = 300
        self.requested_colour = (r1, g1, b1)        
        self.getNameColor()

        translator = Translator()
        #tl = translator.translate(nameColor, dest='pt')
        #print(tl)
        textColorAprox = QLabel(parent=self, text="Cor aprox: " + self.nameColor)
        textColorAprox.setGeometry(20,20, 100, 100)
        textColorAprox.setAlignment(Qt.AlignLeft) 
        buttonColorAprox = QPushButton(parent=self, text='')
        buttonColorAprox.setEnabled(False)
        buttonColorAprox.setStyleSheet("background-color:rgb(" + str(r1) + "," + str(g1) + "," + str(b1) + ")");
        buttonColorAprox.setGeometry(170,20, 100, 100)

        self.requested_colour = (r2, g2, b2)        
        self.getNameColor()
        textColorPred = QLabel(parent=self, text="Cor pred: " + self.nameColor)
        textColorPred.setGeometry(20,150, 100, 100)
        textColorPred.setAlignment(Qt.AlignLeft) 
        buttonColorPred = QPushButton(parent=self, text='')
        buttonColorPred.setEnabled(False)
        buttonColorPred.setStyleSheet("background-color:rgb(" + str(r2) + "," + str(g2) + "," + str(b2) + ")");
        buttonColorPred.setGeometry(170,150, 100, 100)
        
        buttonParse = QPushButton(parent=self, text='Análisar Substâncias')
        buttonParse.setGeometry(120,290, 120, 30)

        self.resize(350, 350)

    

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.printer = QPrinter()
        self.scaleFactor = 0.0
        self.fileName = "image.jpg"
        self.check = True

        self.imageLabel = QLabel()
        self.imageLabel.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))
       
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()       

        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)         

    #REALIZA CLICK PARA OBTER COORDENADA
    def getCoordenada(self):
        color_thief = ColorThief(self.fileName)
        dominant_color = color_thief.get_color(quality=1)
        print("Dominante:", dominant_color)
        #self.colorView = ColorWindow(dominant_color[0], dominant_color[1], dominant_color[2])
        #self.colorView.show()
        closest_color = readFiles.get_closet_color(list(dominant_color))
        self.colorView = ColorWindow(closest_color[0][0], closest_color[0][1], closest_color[0][2], dominant_color[0], dominant_color[1], dominant_color[2])
        self.colorView.setWindowTitle("Análise de cores");
        self.colorView.show()
        #im = Image.open(self.fileName)
        """self.image=QtGui.QImage(self.fileName)
        self.pixmap=QtGui.QPixmap.fromImage(self.image)
        self.imageLabel.setPixmap(self.pixmap)
        self.check = True
        self.imageLabel.mousePressEvent=self.getPixel"""

    #OBTEM COR A PARTIR DA COORDENADA
    def getPixel(self, event):
        if self.check:
            x = event.pos().x()
            y = event.pos().y()
            print("X=",x," y= ",y)
            im = Image.open(self.fileName)
            #pix = im.load()
            #print(pix[x, y]) 
            pix = im.convert('RGB')  
            r, g, b = pix.getpixel((x, y))
            
            self.colorView = ColorWindow(r, g, b)
            self.colorView.show()  
        

        #self.check = False
        #print("X=",x," y= ",y)        

    def coletarAmostra(self):
        coletarAmostra.coleta(self) 

    def filtroCinza(self):
        imagemEmTonsDeCinza = cinza.filtro(self)

        imagemEmTonsDeCinza = cv2.resize(imagemEmTonsDeCinza, (500,500))
        self.data = np.array(imagemEmTonsDeCinza).reshape(500,500).astype(np.int32)
        qimage = QtGui.QImage(self.data, self.data.shape[0], self.data.shape[1], QtGui.QImage.Format_RGB32)

        self.imageLabel.setPixmap(QPixmap.fromImage(qimage))
        self.scaleFactor = 1.0 

        self.scrollArea.setVisible(True)

    def filtroCantizacao(self):
        imagemCantizada = cantizacao.filtro(self)
        imagemCantizada = cv2.resize(imagemCantizada, (500,500))
        self.data = np.array(imagemCantizada).reshape(500,500).astype(np.int32)
        qimage = QtGui.QImage(self.data, self.data.shape[0], self.data.shape[1], QtGui.QImage.Format_RGB32)

        self.imageLabel.setPixmap(QPixmap.fromImage(qimage))
        #self.scaleFactor = 1.0 

        self.scrollArea.setVisible(True)

    def open(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        print (self.fileName)
        if self.fileName:
            image = QImage(self.fileName)
            #print(type(image))
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()
            self.resize(image.width() + 130, image.height() + 40)
            
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
        self.filtroCinza = QAction("&Cinza", self, triggered=self.filtroCinza)
        self.filtroCantizacao = QAction("&Cantizacao", self, triggered=self.filtroCantizacao)
        self.coletarAmostra = QAction("&Coletar Amostra", self, triggered=self.coletarAmostra)
        self.getCoordenada = QAction("&RGB", self, triggered=self.getCoordenada)
        
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
        self.processMenu.addAction(self.coletarAmostra)
        self.processMenu.addAction(self.filtroCinza)
        self.processMenu.addAction(self.filtroCantizacao)

        self.analiseMenu = QMenu("&Analise", self)
        self.analiseMenu.addAction(self.getCoordenada)
        
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
    sys.exit(app.exec_())
