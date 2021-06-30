from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QImage
import PIL  
from PIL import Image
import cv2
import numpy as np
import csv

class InputState:
    LOWER = 0
    CAPITAL = 1

sheet = """
        QWidget {
            border: 3px solid black;
            border-radius: 3px;
            background-color: rgb(76, 133, 224);
            }
        """;

class KeyButton(QPushButton):
    sigKeyButtonClicked = pyqtSignal(object)

    def __init__(self, key):
        super(KeyButton, self).__init__()

        self._key = key
        self._activeSize = QSize(50,50)
        self.clicked.connect(self.emitKey)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

    def emitKey(self):
        self.sigKeyButtonClicked.emit(self._key)

    def enterEvent(self, event):
        self.setFixedSize(self._activeSize)

    def leaveEvent(self, event):
        self.setFixedSize(self.sizeHint())

    def sizeHint(self):
        return QSize(40, 40)

class VirtualKeyboard(QWidget):
    sigInputString = pyqtSignal(object)
    sigKeyButtonClicked = pyqtSignal(object)

    def __init__(self):
        super(VirtualKeyboard, self).__init__()

        self.setWindowTitle("Calibrar dados")
        self.setWindowIcon(QtGui.QIcon('resources/adjust.png'))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.globalLayout = QVBoxLayout(self)
        self.keysLayout = QGridLayout()
        self.buttonLayout = QHBoxLayout()
        self.horizontalLayoutSubstancia = QHBoxLayout()
        self.horizontalLayoutFabricante = QHBoxLayout()
        self.horizontalLayoutArquivo = QHBoxLayout()
        self.horizontalLayoutConfirmar = QHBoxLayout()

        self.keyListByLines = [
                    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ç'],
                    ['z', 'x', 'c', 'v', 'b', 'n', 'm', '.', '_', ' '],
                ]
        self.inputString = ""
        self.state = InputState.LOWER

        self.stateButton = QPushButton()
        self.stateButton.setText('Maiúsculo')
        self.backButton = QPushButton()
        self.backButton.setText('Apagar')

        self.okButton = QPushButton()
        self.okButton.setText('Confirmar')
        self.okButton.setStyleSheet(sheet)

        self.clearButton = QPushButton()
        self.clearButton.setText("Limpar")

        self.textFabricante = QLineEdit()
        self.labelFabricante = QLabel("Fabricante:")

        self.textSubstancia = QComboBox()
        self.textSubstancia.addItem("Amônia")
        self.textSubstancia.addItem("Nitrato")
        self.textSubstancia.addItem("Nitrito")
        self.labelSubstancia = QLabel("Substância:")

        self.buttonArquivo = QPushButton('Abrir arquivo')
        self.buttonArquivo.clicked.connect(self.openFile)
        self.labelArquivo = QLabel("Documento:")

        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(self.addInputByKey)
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.stateButton.clicked.connect(self.switchState)
        self.backButton.clicked.connect(self.backspace)

        self.okButton.clicked.connect(self.clickme) 

        self.clearButton.clicked.connect(self.emitCancel)

        self.buttonLayout.addWidget(self.clearButton)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.stateButton)
        #self.buttonLayout.addWidget(self.okButton)

        self.horizontalLayoutSubstancia.addWidget(self.labelSubstancia)
        self.horizontalLayoutSubstancia.addWidget(self.textSubstancia, 1)
        self.globalLayout.addLayout(self.horizontalLayoutSubstancia);

        self.horizontalLayoutFabricante.addWidget(self.labelFabricante)
        self.horizontalLayoutFabricante.addWidget(self.textFabricante)
        self.globalLayout.addLayout(self.horizontalLayoutFabricante);

        #self.globalLayout.addWidget(self.textFabricante)
        self.globalLayout.addLayout(self.keysLayout)

        self.globalLayout.addLayout(self.buttonLayout)

        self.horizontalLayoutArquivo.addWidget(self.labelArquivo)
        self.horizontalLayoutArquivo.addWidget(self.buttonArquivo, 1)
        self.globalLayout.addLayout(self.horizontalLayoutArquivo); 

        self.horizontalLayoutConfirmar.addWidget(self.okButton)
        self.globalLayout.addLayout(self.horizontalLayoutConfirmar);

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def switchState(self):
        self.state = not self.state

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.textFabricante.setText(self.inputString)
        print(self.inputString)

    def backspace(self):
        self.textFabricante.backspace()
        self.inputString = self.inputString[:-1]

    def emitInputString(self):
        self.sigInputString.emit(self.inputString)

    def emitCancel(self):
        self.sigInputString.emit("")
        self.inputString = ""
        self.textFabricante.setText(self.inputString)

    def sizeHint(self):
        return QSize(480,272)

    def openFile(self):
        options = QFileDialog.Options()
        self.fileNameMeasurement, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                                          'Images (*.png *.jpeg *.jpg *.bmp *.gif *.pdf)', options=options)
        print(self.fileNameMeasurement)

        calibrarWindow = CalibramentoWindow(self.fileNameMeasurement)
        calibrarWindow.resize(550, 600)
        calibrarWindow.setWindowTitle("Arquivo a ser calibrado")
        calibrarWindow.setWindowIcon(QtGui.QIcon('resources/fish.png'))
        calibrarWindow.exec_()
        self.value = calibrarWindow.getTabela()
        #print("Pegou valor:", self.value)
        #return value
        
    def clickme(self):
        fab = self.textFabricante.text()
        subs = self.textSubstancia.currentText()
        print("Fabricante:", fab)
        print("Substancia:", subs)
        print("Arquivo:", self.fileNameMeasurement)
        #picture = Image.open(self.fileNameMeasurement)  
        #picture = picture.save('C:\\Users\\Igor_\\OneDrive\\Área de Trabalho\\' + subs + '-' + fab + '.jpg')
        self.criarArquivo(fab, subs, self.value);
        self.close()

    def criarArquivo(self, fab, subs, value):
        path = "measurements/"
        name = subs + '.' + fab
        print("Nome do arquivo:", name)
        print("Array:", self.value)
        with open(path + name + '.csv', 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Red', 'Green', 'Blue', 'Value'])
            filewriter.writerows(self.value)


class CalibramentoWindow(QDialog):
    def __init__(self, image):
        super().__init__()

        self.arquivo = []
        #self.setFixedSize(300, 350)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.fileName = QImage(image)        
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.fileName))

        self.clickButton = QPushButton('Clique aqui e no ponto, depois informe o nível da substância')
        self.clickButton.clicked.connect(self.getCoordenada)

        self.closeWindow = QPushButton("Finalizar calibração")
        self.closeWindow.clicked.connect(self.close)
        self.closeWindow.setStyleSheet(sheet)

        wid = QWidget(self)
        #self.setCentralWidget(wid)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.clickButton)
        self.layout.addWidget(self.imageLabel)
        self.layout.addWidget(self.closeWindow)
        wid.setLayout(self.layout)


    def getCoordenada(self):
        self.image=QtGui.QImage(self.fileName)
        self.pixmap=QtGui.QPixmap.fromImage(self.image)
        self.imageLabel.setPixmap(self.pixmap)
        self.check = True
        self.imageLabel.mousePressEvent=self.getPixel

    def getPixel(self, event):
        if self.check:
            x = event.pos().x()
            y = event.pos().y()
            #print("X=",x," y= ",y)
            #print(self.fileName)
            im = self.convertQImageToMat(self.fileName)
            im = Image.fromarray(im)
            pix = im.load()
            #print(pix[x, y]) 
            pix = im.convert('RGB')  
            r, g, b = pix.getpixel((x, y))
            #print("X=",x," y= ",y)

            value = self.buildPopup()
            self.adicionarValorALista(r, g, b, value)

        self.check = False

    def adicionarValorALista(self, r, g, b, value):
        #print("NOVA LINHA")
        self.tabela = []
        self.tabela.append(r)
        self.tabela.append(g)
        self.tabela.append(b)
        self.tabela.append(value)
        self.arquivo.append(self.tabela)
        print("+ Linha", self.arquivo)
        #self.close()

    def getTabela(self):
        return self.arquivo

    def convertQImageToMat(self, incomingImage):
        incomingImage = incomingImage.convertToFormat(4)

        width = incomingImage.width()
        height = incomingImage.height()

        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
        return arr

    def buildPopup(self):
        #name = item.text()
        exPopup = popupValor()
        exPopup.resize(265, 340)
        exPopup.setWindowTitle("Valores do ponto")
        exPopup.setWindowIcon(QtGui.QIcon('resources/fish.png'))
        #self.exPopup.show()
        exPopup.exec_()
        value = exPopup.getValor()
        #print("Pegou valor:", value)
        return value

class popupValor(QDialog):
    def __init__(self):
        super(popupValor, self).__init__()
        sigKeyButtonClicked = pyqtSignal(object)
        #self.center()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        wid = QWidget(self)
        #self.setCentralWidget(wid)
        self.layout = QVBoxLayout(self)

        self.valorLabel = QLabel("Valor (válido ppm, outra unidade ou característica):")
        self.valorSubstancia = QLineEdit(self)
        self.confirmarButton = QPushButton('Confirmar', enabled=True)
        self.confirmarButton.clicked.connect(self.confirmarValor)
        self.confirmarButton.setStyleSheet(sheet)

        self.keysLayout = QGridLayout()
        self.keyListByLines = [
                    ['7', '8', '9'],
                    ['4', '5', '6'],
                    ['1', '2', '3'],
                    [',', '2', '.'],
                ]
        self.inputString = ""
        self.state = InputState.LOWER
        for lineIndex, line in enumerate(self.keyListByLines):
            for keyIndex, key in enumerate(line):
                buttonName = "keyButton" + key.capitalize()
                self.__setattr__(buttonName, KeyButton(key))
                self.keysLayout.addWidget(self.getButtonByKey(key), self.keyListByLines.index(line), line.index(key))
                self.getButtonByKey(key).setText(key)
                self.getButtonByKey(key).sigKeyButtonClicked.connect(self.addInputByKey)
                self.keysLayout.setColumnMinimumWidth(keyIndex, 50)
            self.keysLayout.setRowMinimumHeight(lineIndex, 50)

        self.backButton = QPushButton()
        self.backButton.setText('Apagar')

        self.backButton.clicked.connect(self.backspace)

        self.layout.addWidget(self.valorLabel)
        self.layout.addWidget(self.valorSubstancia)
        self.layout.addLayout(self.keysLayout)
        self.layout.addWidget(self.backButton)
        self.layout.addWidget(self.confirmarButton)

        wid.setLayout(self.layout)

    def getLineForButtonByKey(self, key):
        return [key in keyList for keyList in self.keyListByLines].index(True)

    def getButtonByKey(self, key):
        return getattr(self, "keyButton" + key.capitalize())

    def addInputByKey(self, key):
        self.inputString += (key.lower(), key.capitalize())[self.state]
        self.valorSubstancia.setText(self.inputString)
        print(self.inputString)

    def backspace(self):
        self.valorSubstancia.backspace()
        self.inputString = self.inputString[:-1]

    def confirmarValor(self):
        self.close()

    def getValor(self):
        return self.valorSubstancia.text()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())