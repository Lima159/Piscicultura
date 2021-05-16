from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

class CalibrateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calibrar dados")
        self.setWindowIcon(QtGui.QIcon('resources/adjust.png'))
        self.resize(270, 110)
        self.setFixedSize(270, 110)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        layout = QFormLayout()

        self.textFabricante = QLineEdit(self)
        layout.addRow("Fabricante:", self.textFabricante)

        self.textSubstancia = QLineEdit(self)
        layout.addRow("Substância:", self.textSubstancia)

        self.buttonArquivo = QPushButton('Abrir arquivo', self)
        self.buttonArquivo.clicked.connect(self.openFile)   
        layout.addRow("Documento:", self.buttonArquivo)

        self.button = QPushButton('Confirmar', enabled=False)
        self.button.clicked.connect(self.clickme)

        layout.addRow(self.button)

        self.textFabricante.textChanged.connect(self.disableButton)
        self.textSubstancia.textChanged.connect(self.disableButton)

        self.setLayout(layout)

    def openFile(self):   
        options = QFileDialog.Options()
        self.fileNameMeasurement, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif *.pdf)', options=options)
        print(self.fileNameMeasurement)

    def disableButton(self):
        self.button.setEnabled(bool(self.textFabricante.text()) and bool(self.textSubstancia.text()))

    def clickme(self):
        print("Fabricante:", self.textFabricante.text())
        print("Substancia:", self.textSubstancia.text())
        print("Arquivo:", self.fileName)