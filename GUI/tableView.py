def criarTableView(self):
        self.tableView = QTableView(self)
        self.tableView.setGeometry(QtCore.QRect(530, -10, 271, 571))
        self.tableView.setObjectName("tableView")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(570, 30, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("Bem Vindo ao aplicativo!")

        self.coletarAmostra = QtWidgets.QPushButton(self)
        self.coletarAmostra.setGeometry(QtCore.QRect(570, 110, 191, 23))
        self.coletarAmostra.setObjectName("coletarAmostra")
        self.coletarAmostra.setText("Coletar Amostra")
        self.coletarAmostra.clicked.connect(self.coletaAmostra)

        self.processarAmostra = QtWidgets.QPushButton(self)
        self.processarAmostra.setGeometry(QtCore.QRect(570, 140, 191, 23))
        self.processarAmostra.setObjectName("processarAmostra")
        self.processarAmostra.setText("Processar Amostra")
        self.processarAmostra.clicked.connect(self.filtroCinza)

        self.relatorioAnalise = QtWidgets.QGroupBox(self)
        self.relatorioAnalise.setGeometry(QtCore.QRect(580, 210, 181, 111))
        self.relatorioAnalise.setObjectName("relatorioAnalise")
        self.relatorioAnalise.setTitle("Relátorio de Análise")

        self.radioAmonia = QtWidgets.QRadioButton(self.relatorioAnalise)
        self.radioAmonia.setGeometry(QtCore.QRect(50, 20, 82, 17))
        self.radioAmonia.setObjectName("radioAmonia")
        self.radioAmonia.setText("Amônia")              

        self.radioNitrato = QtWidgets.QRadioButton(self.relatorioAnalise)
        self.radioNitrato.setGeometry(QtCore.QRect(50, 40, 82, 17))
        self.radioNitrato.setObjectName("radioNitrato")
        self.radioNitrato.setText("Nitrato")

        self.radioNitrito = QtWidgets.QRadioButton(self.relatorioAnalise)
        self.radioNitrito.setGeometry(QtCore.QRect(50, 60, 82, 17))
        self.radioNitrito.setObjectName("radioNitrito")
        self.radioNitrito.setText("Nitrito")

        self.avaliar = QtWidgets.QPushButton(self.relatorioAnalise)
        self.avaliar.setGeometry(QtCore.QRect(50, 80, 75, 23))
        self.avaliar.setObjectName("avaliar")
        self.avaliar.setText("Avaliar")

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(550, 370, 231, 80))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        
        self.visualizarRelatorio = QtWidgets.QRadioButton(self.groupBox)
        self.visualizarRelatorio.setGeometry(QtCore.QRect(10, 20, 101, 17))
        self.visualizarRelatorio.setObjectName("visualizarRelatorio")
        self.visualizarRelatorio.setText("Visualiar relatório")

        self.enviarSMS = QtWidgets.QRadioButton(self.groupBox)
        self.enviarSMS.setGeometry(QtCore.QRect(130, 20, 82, 17))
        self.enviarSMS.setObjectName("enviarSMS")
        self.enviarSMS.setText("Enviar SMS")

        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(70, 50, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("OK")                                

        self.armazenarColeta = QtWidgets.QPushButton(self)
        self.armazenarColeta.setGeometry(QtCore.QRect(590, 480, 131, 41))
        self.armazenarColeta.setObjectName("armazenarColeta")        
        self.armazenarColeta.setText("Armazenar coleta")