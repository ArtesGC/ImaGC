# ******************************************************************************
#  (c) 2019-2021. Nurul GC                                                     *
#                                                                              *
#  Jovem Programador                                                           *
#  Estudante de Engenharia de Telecomunicações                                 *
#  Tecnologia de Informação e de Medicina.                                     *
#  Foco Fé Força Paciência                                                     *
#  Allah no Comando.                                                           *
# ******************************************************************************

from ImagcEditor import ImaGC
from PyQt5.Qt import *
from sys import argv
import webbrowser


class ImaGC_GUI:
    def __init__(self):
        self.gc = QApplication(argv)
        self.ferramentas = QWidget()
        self.ferramentas.setFixedSize(800, 400)
        self.ferramentas.setWindowTitle("ImaGC")
        self.ferramentas.setWindowIcon(QIcon("img/imagc.png"))
        # self.ferramentas.setPalette(QPalette(QColor("orange")))  # background-color

        # ******* background-image *******
        setBgImage = QImage("img/bg.jpg")
        sizeBgImage = setBgImage.scaled(QSize(800, 400))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sizeBgImage))
        self.ferramentas.setPalette(palette)

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
        QMessageBox.information(self.ferramentas, "Instruções", """
Olaa caro usuário!

É com muito prazer e orgulho que apresento te o ImaGC..
Um programa simples e cheio de funcionalidades!
Das quais a sua principal função é de editar imagens,
adicionando logotipos ou convertendo para (.ico)..

- PARA O ADICIONAMENTO DO LOGOTIPO ELE DEVE TER O FUNDO OU MASCARA TRANSPARENTE!
- PARA A CONVERSÃO DE (.ico) O PROGRAMA SUBESCREVE OS DADOS BINÁRIOS DA IMAGEM E REDEFINE AS DIMENSÕES DA MESMA!

Muito Obrigado pelo apoio!
© 2019-2021 Nurul Carvalho
™ ArtesGC Inc""")

    def _sobre(self):
        QMessageBox.information(self.ferramentas, "Sobre", """
Nome: ImaGC
Versão: 0.2-022021
Programador & Designer: Nurul-GC
Empresa: ArtesGC Inc.""")

    def _sair(self):
        self.gc.exit(0)

    # ******* windows-functions *******
    def adicionarLogo(self):
        def visualizarLogo():
            if self.nomeLogo.text() == "":
                QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem", "Por favor selecione ou localize a imagem antes de prosseguir..")
            else:
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
            if self.nomeImagem.text() == "":
                QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem", "Por favor selecione ou localize a imagem antes de prosseguir..")
            else:
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

        labelIntro = QLabel("<h2><i>Adicionar Logotipo</i></h2>")
        labelIntro.setAlignment(Qt.AlignCenter)
        labelIntro.setFont(QFont("", 20))
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
        self.nomeImagemBotao.clicked.connect(self.procurarImagem)
        botaoAddLogoImagem = QPushButton("Adicionar Logo a Imagem")
        botaoAddLogoImagem.setDefault(True)
        botaoAddLogoImagem.clicked.connect(self.addLogoImagem)
        botaoVerImagem = QPushButton("Visualizar Imagem")
        botaoVerImagem.setDefault(True)
        botaoVerImagem.clicked.connect(visualizarImagem)
        layoutImagem.addRow("<b>Adicionar logotipo a uma unica imagem: *</b>", self.nomeImagem)
        layoutImagem.addWidget(self.nomeImagemBotao)
        layoutImagem.addWidget(botaoAddLogoImagem)
        layoutImagem.addWidget(botaoVerImagem)
        layout.addLayout(layoutImagem)

        layoutDirImagem = QFormLayout()
        self.dirImagem = QLineEdit()
        self.dirImagem.setReadOnly(True)
        dirImagemBotao = QPushButton("Localizar Directório")
        dirImagemBotao.setDefault(True)
        dirImagemBotao.setToolTip("o logotipo sera adicionado as imagens automaticamente!")
        dirImagemBotao.clicked.connect(self.procurarDirectorio)
        layoutDirImagem.addRow("<b>Adicionar logotipo a várias imagens: *</b>", self.dirImagem)
        layoutDirImagem.addWidget(dirImagemBotao)
        layout.addLayout(layoutDirImagem)

        browser = lambda p: webbrowser.open('https://artesgc.home.blog')
        labeCopyright = QLabel("<a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
        labeCopyright.setAlignment(Qt.AlignRight)
        labeCopyright.setToolTip('Acesso a pagina oficial da ArtesGC!')
        labeCopyright.linkActivated.connect(browser)
        layout.addWidget(labeCopyright)

        self.janela1.setLayout(layout)

    def converterIco(self):
        def converter():
            if self.nomeImagem.text() == "":
                QMessageBox.critical(self.ferramentas, "Erro", f"Selecione a imagem antes de continuar e tente novamente..")
                self.procurarImagem()
            else:
                try:
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione onde salvar o arquivo")
                    ImaGC(dir_salvar=dirSalvar, nome_imagem=self.nomeImagem.text()).convertendoIcone()
                    QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"{erro}..")

        def visualizarImagem():
            if self.nomeImagem.text() == "":
                QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem", "Por favor selecione ou localize a imagem antes de prosseguir..")
            else:
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

        labelIntro = QLabel("<h2><i>Converter para Ico</i></h2>")
        labelIntro.setAlignment(Qt.AlignCenter)
        labelIntro.setFont(QFont("", 20))
        layout.addWidget(labelIntro, 5)

        self.nomeImagem = QLineEdit()
        self.nomeImagem.setReadOnly(True)
        layout.addWidget(self.nomeImagem)

        self.botaoIco = QPushButton("Procurar Imagem")
        self.botaoIco.setDefault(True)
        self.botaoIco.clicked.connect(self.procurarImagem)
        layout.addWidget(self.botaoIco)

        botaoVerImagem = QPushButton("Visualizar Imagem")
        botaoVerImagem.setDefault(True)
        botaoVerImagem.clicked.connect(visualizarImagem)
        layout.addWidget(botaoVerImagem)

        layoutConverter = QHBoxLayout()
        labeCopyright = QLabel("<b><i>Converta para icone com dimensões diferentes:</i></b>")
        labeCopyright.setFont(QFont("", 10))
        labeCopyright.setAlignment(Qt.AlignCenter)
        layoutConverter.addWidget(labeCopyright)

        botao256 = QPushButton("Converter (16x32x64x128x256)")
        botao256.setDefault(True)
        botao256.clicked.connect(converter)
        layoutConverter.addWidget(botao256)
        layout.addLayout(layoutConverter)

        browser = lambda p: webbrowser.open('https://artesgc.home.blog')
        labeCopyright = QLabel("<a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
        labeCopyright.setAlignment(Qt.AlignRight)
        labeCopyright.setToolTip('Acesso a pagina oficial da ArtesGC!')
        labeCopyright.linkActivated.connect(browser)
        layout.addWidget(labeCopyright)

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

    def addLogoImagem(self):
        if self.nomeLogo.text() != "":
            dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione onde salvar o arquivo")
            ImaGC(dir_salvar=dirSalvar, nome_logotipo=self.nomeLogo.text(), nome_imagem=self.nomeImagem.text()).addLogo()
            QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
        else:
            QMessageBox.critical(self.ferramentas, "Erro", f"Selecione o logotipo antes de continuar e tente novamente..")
            self.procurarLogo()

    def procurarDirectorio(self):
        nomeDirectorio = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione a Imagem", directory="")
        if self.nomeLogo.text() != "":
            self.dirImagem.setText(nomeDirectorio)
            dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione onde salvar o arquivo")
            ImaGC(dir_salvar=dirSalvar, nome_logotipo=self.nomeLogo.text(), dir_imagem=self.dirImagem.text()).addLogo()
            QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
        else:
            QMessageBox.critical(self.ferramentas, "Erro", f"Selecione o logotipo antes de continuar e tente novamente..")
            self.procurarLogo()


if __name__ == '__main__':
    app = ImaGC_GUI()
    app.ferramentas.show()
    app.gc.exec_()
