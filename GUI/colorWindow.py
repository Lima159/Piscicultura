from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from googletrans import Translator
from PyQt5.QtGui import QFont

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
        
        #print(r1, g1, b1, r2, g2, b2)

        self.setWindowIcon(QtGui.QIcon('resources/color.png'))
        self.setFixedSize(300, 350)
        self.requested_colour = (r1, g1, b1)        
        #self.getNameColor()

        #translator = Translator()
        #tl = translator.translate(nameColor, dest='pt')
        #print(tl)
        textColorAprox = QLabel(parent=self, text="Cor aproximada" ) #+ self.nameColor
        textColorAprox.setGeometry(20,20, 100, 100)
        textColorAprox.setAlignment(Qt.AlignLeft) 
        textColorAprox.setFont(QFont('Arial', 9))
        buttonColorAprox = QPushButton(parent=self, text='')
        buttonColorAprox.setEnabled(False)
        buttonColorAprox.setStyleSheet("background-color:rgb(" + str(r1) + "," + str(g1) + "," + str(b1) + ")");
        buttonColorAprox.setGeometry(170,20, 100, 100)

        self.requested_colour = (r2, g2, b2)        
        #self.getNameColor()
        textColorPred = QLabel(parent=self, text="Cor predominante" )#+ self.nameColor
        textColorPred.setGeometry(20,150, 100, 100)
        textColorPred.setAlignment(Qt.AlignLeft) 
        textColorPred.setFont(QFont('Arial', 9))
        buttonColorPred = QPushButton(parent=self, text='')
        buttonColorPred.setEnabled(False)
        buttonColorPred.setStyleSheet("background-color:rgb(" + str(r2) + "," + str(g2) + "," + str(b2) + ")");
        buttonColorPred.setGeometry(170,150, 100, 100)

        self.frame = QGroupBox(self)    
        self.frame.setFont(QFont('Arial', 9))
        self.frame.setTitle("Selecionar análise")   
        self.frame.setGeometry(20, 270, 250, 60)     

        buttonParseAmonia = QPushButton(parent=self, text='Amônia')
        buttonParseAmonia.setGeometry(30, 290, 70, 30)

        buttonParseNitrato = QPushButton(parent=self, text='Nitrato')
        buttonParseNitrato.setGeometry(110, 290, 70, 30)

        buttonParseNitrito = QPushButton(parent=self, text='Nitrito')
        buttonParseNitrito.setGeometry(190, 290, 70, 30)