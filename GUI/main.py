from PyQt5 import QtCore, QtGui, QtWidgets
import coletarAmostra, cinza
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(530, -10, 271, 571))
        self.tableView.setObjectName("tableView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(570, 30, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(550, 370, 231, 80))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(130, 20, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 20, 101, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(70, 50, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(570, 110, 191, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(580, 210, 181, 111))
        self.groupBox_3.setObjectName("groupBox_3")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_3.setGeometry(QtCore.QRect(50, 20, 82, 17))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_4.setGeometry(QtCore.QRect(50, 40, 82, 17))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_5.setGeometry(QtCore.QRect(50, 60, 82, 17))
        self.radioButton_5.setObjectName("radioButton_5")
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_7.setGeometry(QtCore.QRect(50, 80, 75, 23))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(590, 480, 131, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(570, 140, 191, 23))
        self.pushButton_8.setObjectName("pushButton_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuArquivo = QtWidgets.QMenu(self.menubar)
        self.menuArquivo.setObjectName("menuArquivo")
        self.menuSair = QtWidgets.QMenu(self.menubar)
        self.menuSair.setObjectName("menuSair")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.menuArquivo.addAction(self.actionAbrir)
        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menubar.addAction(self.menuSair.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Bem Vindo ao aplicativo!"))
        self.radioButton.setText(_translate("MainWindow", "Enviar SMS"))
        self.radioButton_2.setText(_translate("MainWindow", "Visualiar relatório"))
        self.pushButton.setText(_translate("MainWindow", "OK"))
        self.pushButton_6.setText(_translate("MainWindow", "Coletar Amostra"))
        self.pushButton_6.clicked.connect(self.coletarAmostra)

        self.groupBox_3.setTitle(_translate("MainWindow", "Relátorio de Análise"))
        self.radioButton_3.setText(_translate("MainWindow", "Amônia"))
        self.radioButton_4.setText(_translate("MainWindow", "Nitrato"))
        self.radioButton_5.setText(_translate("MainWindow", "Nitrito"))
        self.pushButton_7.setText(_translate("MainWindow", "Avaliar"))
        self.pushButton_2.setText(_translate("MainWindow", "Armazenar coleta"))
        self.pushButton_8.setText(_translate("MainWindow", "Processar Amostra"))
        self.pushButton_8.clicked.connect(self.filtroCinza)

        self.menuArquivo.setTitle(_translate("MainWindow", "Arquivo"))
        self.menuSair.setTitle(_translate("MainWindow", "Sair"))
        self.menuSair = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close())

        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))


    def coletarAmostra(self):
        coletarAmostra.coleta(self)

    def filtroCinza(self):
        cinza.filtro(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
