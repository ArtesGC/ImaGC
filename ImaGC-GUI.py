# ******************************************************************************
#  (c) 2019-2021. Nurul GC                                                     *
#                                                                              *
#  Jovem Programador                                                           *
#  Estudante de Engenharia de Telecomunicações                                 *
#  Tecnologia de Informação e de Medicina.                                     *
#  Foco Fé Força Paciência                                                     *
#  Allah no Comando.                                                           *
# ******************************************************************************

from ImagcEditor.imagcEditor import Image, ImaGC
from PyQt5.Qt import *
from sys import argv


class ImaGC_GUI:
    def __init__(self):
        self.gc = QApplication(argv)
        self.ferramentas = QWidget()
        self.ferramentas.setFixedSize(1000, 500)
        self.ferramentas.setWindowTitle("ImaGC")
        self.ferramentas.setWindowIcon(QIcon("img/imagc.png"))
        self.ferramentas.setPalette(QPalette(QColor("orange")))

        # ******* var *******
        self.nomeImagem = None
        self.nomeLogo = None
        self.dirImagem = None
        self.botaoIco = None
        self.nomeImagemBotao = None

        # ******* menu *******
        menu = QToolBar(self.ferramentas)
        instr = menu.addAction("Instruções")
        instr.triggered.connect(self._instr)
        sobre = menu.addAction("Sobre")
        sobre.triggered.connect(self._sobre)
        sair = menu.addAction("Sair")
        sair.triggered.connect(self._sair)

        # ******* list-options *******
        self.listaJanelas = QListWidget(self.ferramentas)
        self.listaJanelas.setFixedSize(150, 36)
        self.listaJanelas.addItem("Adicionar Logotipo")
        self.listaJanelas.addItem("Converter para Ico")

        # ******* init-windows *******
        self.janela1 = QWidget()
        self.adicionarLogo()
        self.janela2 = QWidget()
        self.converterIco()

        # ******* stack *******
        self.stack = QStackedWidget(self.ferramentas)
        self.stack.addWidget(self.janela1)
        self.stack.addWidget(self.janela2)

        # ******* layout-principal *******
        hbox = QHBoxLayout()
        hbox.addWidget(self.listaJanelas)
        hbox.addWidget(self.stack)

        self.ferramentas.setLayout(hbox)
        self.listaJanelas.currentRowChanged.connect(self.alterarJanela)

    # ******* menu-functions *******
    def _instr(self):
        QMessageBox.information(self.ferramentas, "Instruções", """...""")

    def _sobre(self):
        QMessageBox.information(self.ferramentas, "Sobre", """...""")

    def _sair(self):
        self.gc.exit(0)

    # ******* windows-functions *******
    def adicionarLogo(self):
        def visualizarLogo():
            janelaLogo = QDialog()
            janelaLogo.setWindowIcon(QIcon("img/imagc.png"))
            janelaLogo.setWindowTitle("Visualizar Logo")
            janelaLogo.setPalette(QPalette(QColor("orange")))

            layoutJanelaLogo = QVBoxLayout()
            labelLogo = QLabel()
            labelLogo.setToolTip("Apresentação do logotipo!")
            labelLogo.setPixmap(QPixmap(f"{self.nomeLogo.text()}"))
            layoutJanelaLogo.addWidget(labelLogo)

            _fechar = lambda: janelaLogo.destroy(True)
            botaoFechar = QPushButton("Fechar")
            botaoFechar.setDefault(True)
            botaoFechar.clicked.connect(_fechar)
            layoutJanelaLogo.addWidget(botaoFechar)

            janelaLogo.setLayout(layoutJanelaLogo)
            janelaLogo.show()

        def visualizarImagem():
            janelaImagem = QDialog()
            janelaImagem.setWindowIcon(QIcon("img/imagc.png"))
            janelaImagem.setWindowTitle("Visualizar Imagem")
            janelaImagem.setPalette(QPalette(QColor("orange")))

            layoutJanelaImagem = QVBoxLayout()
            labelImagem = QLabel()
            labelImagem.setToolTip("Apresentação do logotipo!")
            labelImagem.setPixmap(QPixmap(f"{self.nomeImagem.text()}"))
            layoutJanelaImagem.addWidget(labelImagem)

            _fechar = lambda: janelaImagem.destroy(True)
            botaoFechar = QPushButton("Fechar")
            botaoFechar.setDefault(True)
            botaoFechar.clicked.connect(_fechar)
            layoutJanelaImagem.addWidget(botaoFechar)

            janelaImagem.setLayout(layoutJanelaImagem)
            janelaImagem.show()

        layout = QVBoxLayout()

        labelIntro = QLabel("<b>Add Logos</b>")
        labelIntro.setAlignment(Qt.AlignCenter)
        layout.addWidget(labelIntro)

        layoutLogo = QFormLayout()
        self.nomeLogo = QLineEdit()
        self.nomeLogo.setReadOnly(True)
        botaoLogo = QPushButton("Procurar Logotipo")
        botaoLogo.setDefault(True)
        botaoLogo.clicked.connect(self.procurarLogo)
        botaoVerLogo = QPushButton("Visualizar Logotipo")
        botaoVerLogo.setDefault(True)
        botaoVerLogo.clicked.connect(visualizarLogo)
        layoutLogo.addRow("<b>Selecione a localização do logotipo: *</b>", self.nomeLogo)
        layoutLogo.addWidget(botaoLogo)
        layoutLogo.addWidget(botaoVerLogo)
        layout.addLayout(layoutLogo)

        layoutImagem = QFormLayout()
        self.nomeImagem = QLineEdit()
        self.nomeImagem.setReadOnly(True)
        self.nomeImagemBotao = QPushButton("Procurar Imagem")
        self.nomeImagemBotao.setDefault(True)
        self.nomeImagemBotao.setCheckable(True)
        self.nomeImagemBotao.clicked.connect(self.procurarImagem)
        botaoVerImagem = QPushButton("Visualizar Imagem")
        botaoVerImagem.setDefault(True)
        botaoVerImagem.clicked.connect(visualizarImagem)
        layoutImagem.addRow("<b>Adicionar logotipo a uma unica imagem: *</b>", self.nomeImagem)
        layoutImagem.addWidget(self.nomeImagemBotao)
        layoutImagem.addWidget(botaoVerImagem)
        layout.addLayout(layoutImagem)

        layoutDirImagem = QFormLayout()
        self.dirImagem = QLineEdit()
        self.dirImagem.setReadOnly(True)
        dirImagemBotao = QPushButton("Localizar Directório")
        dirImagemBotao.setDefault(True)
        dirImagemBotao.clicked.connect(self.procurarDirectorio)
        layoutDirImagem.addRow("<b>Adicionar logotipo a várias imagens: *</b>", self.dirImagem)
        layoutDirImagem.addWidget(dirImagemBotao)
        layout.addLayout(layoutDirImagem)

        self.janela1.setLayout(layout)

    def converterIco(self):
        def converter():
            if botao16.isChecked():
                size = (16, 16)
            elif botao32.isChecked():
                size = (32, 32)
            elif botao64.isChecked():
                size = (64, 64)
            elif botao128.isChecked():
                size = (128, 128)
            elif botao256.isChecked():
                size = (256, 256)

            ImaGC(nome_imagem=self.nomeImagem.text(), dimensao_ico=size).convertendoIcone()
            QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")

        def visualizarImagem():
            janelaImagem = QDialog()
            janelaImagem.setWindowIcon(QIcon("img/imagc.png"))
            janelaImagem.setWindowTitle("Visualizar Imagem")
            janelaImagem.setPalette(QPalette(QColor("orange")))

            layoutJanelaImagem = QVBoxLayout()
            labelImagem = QLabel()
            labelImagem.setToolTip("Apresentação do logotipo!")
            labelImagem.setPixmap(QPixmap(f"{self.nomeImagem.text()}"))
            layoutJanelaImagem.addWidget(labelImagem)

            _fechar = lambda: janelaImagem.destroy(True)
            botaoFechar = QPushButton("Fechar")
            botaoFechar.setDefault(True)
            botaoFechar.clicked.connect(_fechar)
            layoutJanelaImagem.addWidget(botaoFechar)

            janelaImagem.setLayout(layoutJanelaImagem)
            janelaImagem.show()

        layout = QVBoxLayout()

        labelIntro = QLabel("<b>Converter para Ico</b>")
        labelIntro.setAlignment(Qt.AlignCenter)
        layout.addWidget(labelIntro)

        self.nomeImagem = QLineEdit()
        self.nomeImagem.setReadOnly(True)
        layout.addWidget(self.nomeImagem)

        self.botaoIco = QPushButton("Procurar Imagem")
        self.botaoIco.setDefault(True)
        self.botaoIco.setCheckable(True)
        self.botaoIco.clicked.connect(self.procurarImagem)
        layout.addWidget(self.botaoIco)

        botaoVerImagem = QPushButton("Visualizar Imagem")
        botaoVerImagem.setDefault(True)
        botaoVerImagem.clicked.connect(visualizarImagem)
        layout.addWidget(botaoVerImagem)

        layoutConverter = QHBoxLayout()
        labelInfo = QLabel("<i>Selecione a dimensão do icone:</i>")
        labelInfo.setAlignment(Qt.AlignCenter)
        layoutConverter.addWidget(labelInfo)

        botao16 = QPushButton("16x16")
        botao16.setDefault(True)
        botao16.setCheckable(True)
        botao16.clicked.connect(converter)
        layoutConverter.addWidget(botao16)

        botao32 = QPushButton("32x32")
        botao32.setDefault(True)
        botao32.setCheckable(True)
        botao32.clicked.connect(converter)
        layoutConverter.addWidget(botao32)

        botao64 = QPushButton("64x64")
        botao64.setDefault(True)
        botao64.setCheckable(True)
        botao64.clicked.connect(converter)
        layoutConverter.addWidget(botao64)

        botao128 = QPushButton("128x128")
        botao128.setDefault(True)
        botao128.setCheckable(True)
        botao128.clicked.connect(converter)
        layoutConverter.addWidget(botao128)

        botao256 = QPushButton("256x256")
        botao256.setDefault(True)
        botao256.setCheckable(True)
        botao256.clicked.connect(converter)
        layoutConverter.addWidget(botao256)
        layout.addLayout(layoutConverter)

        self.janela2.setLayout(layout)

    def alterarJanela(self, i):
        self.stack.setCurrentIndex(i)

    # ******* imagc-functions *******
    def procurarLogo(self):
        nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione o Logotipo", directory="", filter="Image Files (*.png *.jpg *.jpeg)", initialFilter="")
        self.nomeLogo.setText(nomeFicheiro)

    def procurarImagem(self):
        nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione a Imagem", directory="", filter="Image Files (*.png *.jpg *.jpeg)", initialFilter="")
        self.nomeImagem.setText(nomeFicheiro)
        if self.nomeImagemBotao.isChecked():
            if self.nomeLogo.text() != "":
                ImaGC(nome_logotipo=self.nomeLogo.text(), nome_imagem=self.nomeImagem.text()).addLogo()
            else:
                QMessageBox.critical(self.ferramentas, "Erro", f"[x_x] - Selecione o logotipo antes de continuar..")
                self.procurarLogo()

    def procurarDirectorio(self):
        nomeDirectorio = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione a Imagem", directory="")
        self.dirImagem.setText(nomeDirectorio)
        if self.nomeLogo.text() != "":
            ImaGC(nome_logotipo=self.nomeLogo.text(), dir_imagem=self.dirImagem.text()).addLogo()
        else:
            QMessageBox.critical(self.ferramentas, "Erro", f"[x_x] - Selecione o logotipo antes de continuar..")
            self.procurarLogo()


if __name__ == '__main__':
    app = ImaGC_GUI()
    app.ferramentas.show()
    app.gc.exec_()
