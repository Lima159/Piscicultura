from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PIL import Image  
import PIL  

class InputState:
    LOWER = 0
    CAPITAL = 1

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

    def clickme(self):
        fab = self.textFabricante.text()
        subs = self.textSubstancia.currentText()
        print("Fabricante:", fab)
        print("Substancia:", subs)
        print("Arquivo:", self.fileNameMeasurement)
        picture = Image.open(self.fileNameMeasurement)  
        picture = picture.save('C:\\Users\\Igor_\\OneDrive\\Área de Trabalho\\' + subs + '-' + fab + '.jpg')
        self.close()
"""
class Test(QWidget):
    def __init__(self):
        super(Test, self).__init__()

        self.b1 = KeyButton("1")
        self.b2 = KeyButton("2")
        self.b3 = KeyButton("3")
        self.b4 = KeyButton("4")

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.b1,0,0)
        self.layout.addWidget(self.b2,0,1)
        self.layout.addWidget(self.b3,1,0)
        self.layout.addWidget(self.b4,1,1)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    win = VirtualKeyboard()
    win.show()
    app.exec_()"""