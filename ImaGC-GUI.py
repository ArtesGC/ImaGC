# ***********************************************
#  (c) 2019-2021. Nurul GC                      *
#                                               *
#  Jovem Programador                            *
#  Estudante de Engenharia de Telecomunicações  *
#  Tecnologia de Informação e de Medicina.      *
#  Foco Fé Força Paciência                      *
#  Allah no Comando.                            *
# ***********************************************

from ImagcEditor import ImaGC
from PyQt5.Qt import *
from sys import argv, exit
from time import sleep
import webbrowser


class ImaGC_GUI:
    def __init__(self):
        self.janela = QWidget()
        self.janela.setWindowTitle("ImaGC")
        self.janela.setWindowIcon(QIcon("img/imagc-icon.png"))
        self.janela.setPalette(QPalette(QColor('orange')))
        self.janela.setStyleSheet('color: black;')

        layout = QVBoxLayout()

        label = QLabel()
        label.setPixmap(QPixmap("img/imagc.png").scaled(QSize(400, 400)))
        layout.addWidget(label)

        listaIdiomas = ['Set language - Defina o idioma', 'English', 'Português']
        self.idiomas = QComboBox()
        self.idiomas.addItems(listaIdiomas)
        layout.addWidget(self.idiomas)

        self.barraIniciar = QProgressBar()
        self.barraIniciar.setOrientation(Qt.Horizontal)
        layout.addWidget(self.barraIniciar)

        botaoIniciar = QPushButton('In..')
        botaoIniciar.clicked.connect(self.iniciar)
        layout.addWidget(botaoIniciar)

        self.janela.setLayout(layout)

    def iniciar(self):
        n = 0
        if self.idiomas.currentText() == 'English':
            while n < 101:
                self.barraIniciar.setValue(n)
                sleep(0.3)
                n += 2
            self.janela.destroy()
            app = ImaGC_GUI.EN()
            app.ferramentas.show()
        elif self.idiomas.currentText() == 'Português':
            while n < 101:
                self.barraIniciar.setValue(n)
                sleep(0.3)
                n += 2
            self.janela.destroy()
            app = ImaGC_GUI.PT()
            app.ferramentas.show()
        else:
            QMessageBox.information(self.janela, "Info", "- Please select a language!\n- Por favor selecione um idioma!")

    # ******* portuguese-program *******
    class PT:
        def __init__(self):
            self.ferramentas = QWidget()
            self.ferramentas.setFixedSize(QSize(800, 500))
            self.ferramentas.setWindowTitle("ImaGC")
            self.ferramentas.setWindowIcon(QIcon("img/imagc-icon.png"))
            # self.ferramentas.setPalette(QPalette(QColor("orange")))  # background-color

            # ******* background-image *******
            setBgImage = QImage("img/bg.jpg")
            sizeBgImage = setBgImage.scaled(QSize(800, 500))  # resize Image to widget's size
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(sizeBgImage))
            self.ferramentas.setPalette(palette)

            # ******* var *******
            self.nomeImagemAL = None
            self.nomeImagemCI = None
            self.nomeImagemRI = None
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
            self.listaJanelas.setFixedSize(QSize(200, 55))
            self.listaJanelas.addItem("Adicionar Logotipo")
            self.listaJanelas.addItem("Converter para Ico")
            self.listaJanelas.addItem("Redimensionar Imagem")

            # ******* init-windows *******
            self.janela1 = QWidget()
            self.adicionarLogo()
            self.janela2 = QWidget()
            self.converterIco()
            self.janela3 = QWidget()
            self.redimensionarImagem()

            # ******* stack *******
            self.stack = QStackedWidget(self.ferramentas)
            self.stack.addWidget(self.janela1)
            self.stack.addWidget(self.janela2)
            self.stack.addWidget(self.janela3)

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
Versão: 0.3-042021
Programador & Designer: Nurul-GC
Empresa: ArtesGC Inc.""")

        def _sair(self):
            exit(0)

        # ******* windows *******
        def adicionarLogo(self):
            def procurarImagem():
                nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione a Imagem", filter="Image Files (*.png *.jpg *.jpeg)")
                self.nomeImagemAL.setText(nomeFicheiro)

            def visualizarLogo():
                if self.nomeLogo.text() == "" or self.nomeLogo.text().isspace():
                    QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem", "Por favor selecione a imagem antes de prosseguir..")
                else:
                    janelaLogo = QDialog()
                    janelaLogo.setWindowIcon(QIcon("img/imagc.png"))
                    janelaLogo.setWindowTitle("Visualizar Logo")
                    janelaLogo.setPalette(QPalette(QColor("orange")))

                    layoutJanelaLogo = QVBoxLayout()
                    labelLogo = QLabel()
                    labelLogo.setAlignment(Qt.AlignCenter)
                    labelLogo.setToolTip("Apresentação do logotipo!")
                    labelLogo.setPixmap(QPixmap(f"{self.nomeLogo.text()}").scaled(QSize(400, 400)))
                    layoutJanelaLogo.addWidget(labelLogo)

                    infoImage = QLabel(f"""<b>Nome & Localização</b>: {self.nomeLogo.text()}<br>
<b>Dimensões (original)</b>: {ImaGC().dimensaoImagem(_filename=self.nomeLogo.text())} px<br>
<b>Tamanho</b>: {ImaGC().tamanhoImagem(self.nomeLogo.text())}""")
                    layoutJanelaLogo.addWidget(infoImage)

                    _fechar = lambda: janelaLogo.destroy(True)
                    botaoFechar = QPushButton("Fechar")
                    botaoFechar.setDefault(True)
                    botaoFechar.clicked.connect(_fechar)
                    layoutJanelaLogo.addWidget(botaoFechar)

                    janelaLogo.setLayout(layoutJanelaLogo)
                    janelaLogo.show()

            def visualizarImagem():
                if self.nomeImagemAL.text() == "" or self.nomeImagemAL.text().isspace():
                    QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem", "Por favor selecione a imagem antes de prosseguir..")
                else:
                    janelaImagem = QDialog()
                    janelaImagem.setWindowIcon(QIcon("img/imagc.png"))
                    janelaImagem.setWindowTitle("Visualizar Imagem")
                    janelaImagem.setPalette(QPalette(QColor("orange")))

                    layoutJanelaImagem = QVBoxLayout()
                    labelImagem = QLabel()
                    labelImagem.setAlignment(Qt.AlignCenter)
                    labelImagem.setToolTip("Apresentação do logotipo!")
                    labelImagem.setPixmap(QPixmap(f"{self.nomeImagemAL.text()}").scaled(QSize(400, 400)))
                    layoutJanelaImagem.addWidget(labelImagem)

                    infoImage = QLabel(f"""<b>Nome & Localização</b>: {self.nomeImagemAL.text()}<br>
<b>Dimensões (original)</b>: {ImaGC().dimensaoImagem(_filename=self.nomeImagemAL.text())} px<br>
<b>Tamanho</b>: {ImaGC().tamanhoImagem(self.nomeImagemAL.text())}""")
                    layoutJanelaImagem.addWidget(infoImage)

                    _fechar = lambda: janelaImagem.destroy(True)
                    botaoFechar = QPushButton("Fechar")
                    botaoFechar.setDefault(True)
                    botaoFechar.clicked.connect(_fechar)
                    layoutJanelaImagem.addWidget(botaoFechar)

                    janelaImagem.setLayout(layoutJanelaImagem)
                    janelaImagem.show()

            spacer = QLabel()
            layout = QFormLayout()
            layout.setSpacing(10)

            labelIntro = QLabel("<h2><i>Adicionar Logotipo</i></h2>")
            labelIntro.setAlignment(Qt.AlignCenter)
            labelIntro.setFont(QFont("times", 20))
            layout.addRow(labelIntro)
            layout.addWidget(spacer)

            self.nomeLogo = QLineEdit()
            self.nomeLogo.setReadOnly(True)
            self.nomeLogo.setPlaceholderText("Procure pela imagem para obter o seu nome..")
            layout.addRow(self.nomeLogo)

            botaoLogo = QPushButton("Procurar Logotipo")
            botaoLogo.setDefault(True)
            botaoLogo.clicked.connect(self.procurarLogo)

            botaoVerLogo = QPushButton("Visualizar Logotipo")
            botaoVerLogo.setDefault(True)
            botaoVerLogo.clicked.connect(visualizarLogo)
            layout.addRow(botaoLogo, botaoVerLogo)
            layout.addWidget(spacer)

            self.nomeImagemAL = QLineEdit()
            self.nomeImagemAL.setReadOnly(True)
            self.nomeImagemAL.setPlaceholderText("Procure pela imagem para obter o seu nome..")

            self.nomeImagemBotao = QPushButton("Procurar Imagem")
            self.nomeImagemBotao.setDefault(True)
            self.nomeImagemBotao.clicked.connect(procurarImagem)
            layout.addRow(self.nomeImagemBotao, self.nomeImagemAL)

            botaoVerImagem = QPushButton("Visualizar Imagem")
            botaoVerImagem.setDefault(True)
            botaoVerImagem.clicked.connect(visualizarImagem)

            botaoAddLogoImagem = QPushButton("Adicionar Logo a Imagem")
            botaoAddLogoImagem.setDefault(True)
            botaoAddLogoImagem.clicked.connect(self.addLogoImagem)
            layout.addRow(botaoVerImagem, botaoAddLogoImagem)
            layout.addWidget(spacer)

            self.dirImagem = QLineEdit()
            self.dirImagem.setReadOnly(True)
            self.dirImagem.setPlaceholderText("Localize o diretório contendo as imagens..")
            layout.addRow(self.dirImagem)

            dirImagemBotao = QPushButton("Localizar Directório")
            dirImagemBotao.setDefault(True)
            dirImagemBotao.setToolTip("o logotipo sera adicionado as imagens automaticamente!")
            dirImagemBotao.clicked.connect(self.procurarDirectorio)
            layout.addRow(dirImagemBotao)

            browser = lambda p: webbrowser.open('https://artesgc.home.blog')
            labeCopyright = QLabel("<a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
            labeCopyright.setAlignment(Qt.AlignRight)
            labeCopyright.setToolTip('Acesso a pagina oficial da ArtesGC!')
            labeCopyright.linkActivated.connect(browser)
            layout.addWidget(labeCopyright)

            self.janela1.setLayout(layout)

        def converterIco(self):
            def procurarImagem():
                nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione a Imagem", filter="Image Files (*.png *.jpg *.jpeg)")
                self.nomeImagemCI.setText(nomeFicheiro)

            def converter():
                if self.nomeImagemCI.text() == "" or self.nomeImagemCI.text().isspace():
                    QMessageBox.critical(self.ferramentas, "Erro", f"Selecione a imagem antes de continuar e tente novamente..")
                    self.procurarImagem()
                else:
                    try:
                        QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                        dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione onde salvar o arquivo")
                        ImaGC(_dir_salvar=dirSalvar, _nome_imagem=self.nomeImagemCI.text()).convertendoIcone(_size=int(tamanhos.currentText()))
                        QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
                    except Exception as erro:
                        QMessageBox.critical(self.ferramentas, "Erro", f"{erro}..")

            def visualizarImagem():
                if self.nomeImagemCI.text() == "" or self.nomeImagemCI.text().isspace():
                    QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem", "Por favor selecione a imagem antes de prosseguir..")
                else:
                    janelaImagem = QDialog()
                    janelaImagem.setWindowIcon(QIcon("img/imagc.png"))
                    janelaImagem.setWindowTitle("Visualizar Imagem")
                    janelaImagem.setPalette(QPalette(QColor("orange")))

                    layoutJanelaImagem = QVBoxLayout()
                    labelImagem = QLabel()
                    labelImagem.setAlignment(Qt.AlignCenter)
                    labelImagem.setToolTip("Apresentação do logotipo!")
                    labelImagem.setPixmap(QPixmap(f"{self.nomeImagemCI.text()}").scaled(QSize(400, 400)))
                    layoutJanelaImagem.addWidget(labelImagem)

                    infoImage = QLabel(f"""<b>Nome & Localização</b>: {self.nomeImagemCI.text()}<br>
<b>Dimensões (original)</b>: {ImaGC().dimensaoImagem(_filename=self.nomeImagemCI.text())} px<br>
<b>Tamanho</b>: {ImaGC().tamanhoImagem(self.nomeImagemCI.text())}""")
                    layoutJanelaImagem.addWidget(infoImage)

                    _fechar = lambda: janelaImagem.destroy(True)
                    botaoFechar = QPushButton("Fechar")
                    botaoFechar.setDefault(True)
                    botaoFechar.clicked.connect(_fechar)
                    layoutJanelaImagem.addWidget(botaoFechar)

                    janelaImagem.setLayout(layoutJanelaImagem)
                    janelaImagem.show()

            spacer = QLabel()
            layout = QFormLayout()
            layout.setSpacing(10)

            labelIntro = QLabel("<h2><i>Converter para Ico</i></h2>")
            labelIntro.setAlignment(Qt.AlignCenter)
            labelIntro.setFont(QFont("times", 20))
            layout.addRow(labelIntro)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            self.nomeImagemCI = QLineEdit()
            self.nomeImagemCI.setReadOnly(True)
            self.nomeImagemCI.setPlaceholderText("Procure pela imagem para obter o seu nome..")

            self.botaoIco = QPushButton("Procurar Imagem")
            self.botaoIco.clicked.connect(procurarImagem)
            layout.addRow(self.botaoIco, self.nomeImagemCI)

            botaoVerImagem = QPushButton("Visualizar Imagem")
            botaoVerImagem.clicked.connect(visualizarImagem)
            layout.addRow(botaoVerImagem)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            labelConverter = QLabel("<b><i>Converta para ícone com dimensões diferentes:</i></b>")
            labelConverter.setFont(QFont("times", 10))
            labelConverter.setAlignment(Qt.AlignCenter)
            layout.addRow(labelConverter)

            botaoConverter = QPushButton("Converter")
            botaoConverter.clicked.connect(converter)

            listaTamanhos = ['16', '32', '128', '256']
            tamanhos = QComboBox()
            tamanhos.addItems(listaTamanhos)
            tamanhos.setToolTip('Escolha a dimensão!')
            layout.addRow(tamanhos, botaoConverter)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            browser = lambda p: webbrowser.open('https://artesgc.home.blog')
            labelCopyright = QLabel("<a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
            labelCopyright.setAlignment(Qt.AlignRight)
            labelCopyright.setToolTip('Acesso a pagina oficial da ArtesGC!')
            labelCopyright.linkActivated.connect(browser)
            layout.addWidget(labelCopyright)

            self.janela2.setLayout(layout)

        def redimensionarImagem(self):
            def procurarImagem():
                nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione a Imagem", filter="Image Files (*.png *.jpg *.jpeg)")
                self.nomeImagemRI.setText(nomeFicheiro)

            def redimensionar():
                if self.nomeImagemRI.text() == "" or self.nomeImagemRI.text().isspace():
                    QMessageBox.critical(self.ferramentas, "Erro", f"Selecione a imagem antes de continuar e tente novamente..")
                    self.procurarImagem()
                else:
                    try:
                        QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                        dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione onde salvar o arquivo")
                        ImaGC(_dir_salvar=dirSalvar, _nome_imagem=self.nomeImagemRI.text()).redimensionarImagem(_size=int(tamanhos.currentText()))
                        QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
                    except Exception as erro:
                        QMessageBox.critical(self.ferramentas, "Erro", f"{erro}..")

            def visualizarImagem():
                from PIL import Image
                if self.nomeImagemRI.text() == "" or self.nomeImagemRI.text().isspace():
                    QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem", "Por favor selecione a imagem antes de prosseguir..")
                else:
                    janelaImagem = QDialog()
                    janelaImagem.setWindowIcon(QIcon("img/imagc.png"))
                    janelaImagem.setWindowTitle("Visualizar Imagem")
                    janelaImagem.setPalette(QPalette(QColor("orange")))

                    layoutJanelaImagem = QVBoxLayout()
                    labelImagem = QLabel()
                    labelImagem.setAlignment(Qt.AlignCenter)
                    labelImagem.setToolTip("Apresentação do logotipo!")
                    labelImagem.setPixmap(QPixmap(f"{self.nomeImagemRI.text()}").scaled(QSize(400, 400)))
                    layoutJanelaImagem.addWidget(labelImagem)

                    infoImage = QLabel(f"""<h3><i>Detalhes</i></h3>
<b>Nome & Localização</b>: {self.nomeImagemRI.text()}<br>
<b>Dimensões (original)</b>: {ImaGC().dimensaoImagem(_filename=self.nomeImagemRI.text())} px<br>
<b>Tamanho</b>: {ImaGC().tamanhoImagem(self.nomeImagemRI.text())}""")
                    layoutJanelaImagem.addWidget(infoImage)

                    _fechar = lambda: janelaImagem.destroy(True)
                    botaoFechar = QPushButton("Fechar")
                    botaoFechar.setDefault(True)
                    botaoFechar.clicked.connect(_fechar)
                    layoutJanelaImagem.addWidget(botaoFechar)

                    janelaImagem.setLayout(layoutJanelaImagem)
                    janelaImagem.show()

            spacer = QLabel()
            layout = QFormLayout()
            layout.setSpacing(10)

            labelIntro = QLabel("<h2><i>Redimensionar Imagem</i></h2>")
            labelIntro.setAlignment(Qt.AlignCenter)
            labelIntro.setFont(QFont("times", 20))
            layout.addRow(labelIntro)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            self.nomeImagemRI = QLineEdit()
            self.nomeImagemRI.setReadOnly(True)
            self.nomeImagemRI.setPlaceholderText("Procure pela imagem para obter o seu nome..")

            self.botaoIco = QPushButton("Procurar Imagem")
            self.botaoIco.clicked.connect(procurarImagem)
            layout.addRow(self.botaoIco, self.nomeImagemRI)

            botaoVerImagem = QPushButton("Visualizar Imagem")
            botaoVerImagem.clicked.connect(visualizarImagem)
            layout.addRow(botaoVerImagem)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            labelConverter = QLabel("<b><i>Redimensione a imagem para varios tamanhos:</i></b>")
            labelConverter.setFont(QFont("times", 10))
            labelConverter.setAlignment(Qt.AlignCenter)
            layout.addRow(labelConverter)

            botaoConverter = QPushButton("Redimensionar")
            botaoConverter.clicked.connect(redimensionar)

            listaTamanhos = ['200', '400', '600', '800', '1200']
            tamanhos = QComboBox()
            tamanhos.addItems(listaTamanhos)
            tamanhos.setToolTip('Escolha a dimensão!')
            layout.addRow(tamanhos, botaoConverter)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            browser = lambda p: webbrowser.open('https://artesgc.home.blog')
            labelCopyright = QLabel("<a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
            labelCopyright.setAlignment(Qt.AlignRight)
            labelCopyright.setToolTip('Acesso a pagina oficial da ArtesGC!')
            labelCopyright.linkActivated.connect(browser)
            layout.addWidget(labelCopyright)

            self.janela3.setLayout(layout)

        def alterarJanela(self, i):
            self.stack.setCurrentIndex(i)

        # ******* background-functions *******
        def procurarLogo(self):
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione o Logotipo", filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeLogo.setText(nomeFicheiro)

        def addLogoImagem(self):
            if self.nomeLogo.text() != "":
                QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione onde salvar o arquivo")
                ImaGC(_dir_salvar=dirSalvar, _nome_logotipo=self.nomeLogo.text(), _nome_imagem=self.nomeImagemAL.text()).addLogo()
                QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
            else:
                QMessageBox.critical(self.ferramentas, "Erro", f"Selecione o logotipo antes de continuar e tente novamente..")
                self.procurarLogo()

        def procurarDirectorio(self):
            if self.nomeLogo.text() != "":
                nomeDirectorio = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione a Imagem")
                self.dirImagem.setText(nomeDirectorio)
                QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione onde salvar o arquivo")
                ImaGC(_dir_salvar=dirSalvar, _nome_logotipo=self.nomeLogo.text(), _dir_imagem=self.dirImagem.text()).addLogo()
                QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
            else:
                QMessageBox.critical(self.ferramentas, "Erro", f"Selecione o logotipo antes de continuar e tente novamente..")
                self.procurarLogo()

    # ******* english-program *******
    class EN:
        def __init__(self):
            self.ferramentas = QWidget()
            self.ferramentas.setFixedSize(QSize(800, 500))
            self.ferramentas.setWindowTitle("ImaGC")
            self.ferramentas.setWindowIcon(QIcon("img/imagc-icon.png"))
            # self.ferramentas.setPalette(QPalette(QColor("orange")))  # background-color

            # ******* background-image *******
            setBgImage = QImage("img/bg.jpg")
            sizeBgImage = setBgImage.scaled(QSize(800, 500))  # resize Image to widget's size
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(sizeBgImage))
            self.ferramentas.setPalette(palette)

            # ******* var *******
            self.nomeImagemAL = None
            self.nomeImagemCI = None
            self.nomeImagemRI = None
            self.nomeLogo = None
            self.dirImagem = None
            self.botaoIco = None
            self.nomeImagemBotao = None

            # ******* menu *******
            menu = QToolBar(self.ferramentas)
            instr = menu.addAction("Instructions")
            instr.triggered.connect(self._instr)
            sobre = menu.addAction("About")
            sobre.triggered.connect(self._sobre)
            sair = menu.addAction("Quit")
            sair.triggered.connect(self._sair)

            # ******* list-options *******
            self.listaJanelas = QListWidget(self.ferramentas)
            self.listaJanelas.setFixedSize(QSize(200, 55))
            self.listaJanelas.addItem("Insert Logo")
            self.listaJanelas.addItem("Convert to Ico")
            self.listaJanelas.addItem("Resize Image")

            # ******* init-windows *******
            self.janela1 = QWidget()
            self.adicionarLogo()
            self.janela2 = QWidget()
            self.converterIco()
            self.janela3 = QWidget()
            self.redimensionarImagem()

            # ******* stack *******
            self.stack = QStackedWidget(self.ferramentas)
            self.stack.addWidget(self.janela1)
            self.stack.addWidget(self.janela2)
            self.stack.addWidget(self.janela3)

            # ******* layout-principal *******
            hbox = QHBoxLayout()
            hbox.addWidget(self.listaJanelas)
            hbox.addWidget(self.stack)

            self.ferramentas.setLayout(hbox)
            self.listaJanelas.currentRowChanged.connect(self.alterarJanela)

        # ******* menu-functions *******
        def _instr(self):
            QMessageBox.information(self.ferramentas, "Instructions", """
Hello dear user!

It is with great pleasure and pride that I present the ImaGC to you.
A simple and full of features program!
Of which its main function is to edit images.
Adding logos or converting to (.ico)..

- TO ADD THE LOGO IT MUST HAVE THE BACKGROUND OR TRANSPARENT MASCARA!
- FOR THE CONVERSION OF (.ico) THE PROGRAM SUBSCRIBES THE BINARY DATA OF THE IMAGE
AND REDEFINES THE DIMENSIONS OF THE SAME!

Thank you very much for your support!
© 2019-2021 Nurul Carvalho
™ ArtesGC Inc""")

        def _sobre(self):
            QMessageBox.information(self.ferramentas, "About", """
Name: ImaGC
Version: 0.3-042021
Programmer & Designer: Nurul-GC
Company: ArtesGC Inc.""")

        def _sair(self):
            exit(0)

        # ******* windows *******
        def adicionarLogo(self):
            def procurarImagem():
                nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select Image", filter="Image Files (*.png *.jpg *.jpeg)")
                self.nomeImagemAL.setText(nomeFicheiro)

            def visualizarLogo():
                if self.nomeLogo.text() == "" or self.nomeLogo.text().isspace():
                    QMessageBox.warning(self.ferramentas, "Failed to display the image", "Please select the image before proceeding..")
                else:
                    janelaLogo = QDialog()
                    janelaLogo.setWindowIcon(QIcon("img/imagc.png"))
                    janelaLogo.setWindowTitle("View Logo")
                    janelaLogo.setPalette(QPalette(QColor("orange")))

                    layoutJanelaLogo = QVBoxLayout()
                    labelLogo = QLabel()
                    labelLogo.setAlignment(Qt.AlignCenter)
                    labelLogo.setToolTip("Logo presentation!")
                    labelLogo.setPixmap(QPixmap(f"{self.nomeLogo.text()}").scaled(QSize(400, 400)))
                    layoutJanelaLogo.addWidget(labelLogo)

                    infoImage = QLabel(f"""<b>Name & Location</b>: {self.nomeLogo.text()}<br>
<b>Scale (original)</b>: {ImaGC().dimensaoImagem(_filename=self.nomeLogo.text())} px<br>
<b>Size</b>: {ImaGC().tamanhoImagem(self.nomeLogo.text())}""")
                    layoutJanelaLogo.addWidget(infoImage)

                    _fechar = lambda: janelaLogo.destroy(True)
                    botaoFechar = QPushButton("Close")
                    botaoFechar.setDefault(True)
                    botaoFechar.clicked.connect(_fechar)
                    layoutJanelaLogo.addWidget(botaoFechar)

                    janelaLogo.setLayout(layoutJanelaLogo)
                    janelaLogo.show()

            def visualizarImagem():
                if self.nomeImagemAL.text() == "" or self.nomeImagemAL.text().isspace():
                    QMessageBox.warning(self.ferramentas, "Failed to display the image", "Please select the image before proceeding..")
                else:
                    janelaImagem = QDialog()
                    janelaImagem.setWindowIcon(QIcon("img/imagc.png"))
                    janelaImagem.setWindowTitle("View Image")
                    janelaImagem.setPalette(QPalette(QColor("orange")))

                    layoutJanelaImagem = QVBoxLayout()
                    labelImagem = QLabel()
                    labelImagem.setAlignment(Qt.AlignCenter)
                    labelImagem.setToolTip("Image presentation!")
                    labelImagem.setPixmap(QPixmap(f"{self.nomeImagemAL.text()}").scaled(QSize(400, 400)))
                    layoutJanelaImagem.addWidget(labelImagem)

                    infoImage = QLabel(f"""<h3><i>Details</i></h3>
<b>Name & Location</b>: {self.nomeImagemAL.text()}<br>
<b>Scale (original)</b>: {ImaGC().dimensaoImagem(_filename=self.nomeImagemAL.text())} px<br>
<b>Size</b>: {ImaGC().tamanhoImagem(self.nomeImagemAL.text())}""")
                    layoutJanelaImagem.addWidget(infoImage)

                    _fechar = lambda: janelaImagem.destroy(True)
                    botaoFechar = QPushButton("Close")
                    botaoFechar.setDefault(True)
                    botaoFechar.clicked.connect(_fechar)
                    layoutJanelaImagem.addWidget(botaoFechar)

                    janelaImagem.setLayout(layoutJanelaImagem)
                    janelaImagem.show()

            spacer = QLabel()
            layout = QFormLayout()
            layout.setSpacing(10)

            labelIntro = QLabel("<h2><i>Add Logo</i></h2>")
            labelIntro.setAlignment(Qt.AlignCenter)
            labelIntro.setFont(QFont("times", 20))
            layout.addRow(labelIntro)
            layout.addWidget(spacer)

            self.nomeLogo = QLineEdit()
            self.nomeLogo.setReadOnly(True)
            self.nomeLogo.setPlaceholderText("Search the image to provide his name..")
            layout.addRow(self.nomeLogo)

            botaoLogo = QPushButton("Search Logo")
            botaoLogo.setDefault(True)
            botaoLogo.clicked.connect(self.procurarLogo)

            botaoVerLogo = QPushButton("View Logo")
            botaoVerLogo.setDefault(True)
            botaoVerLogo.clicked.connect(visualizarLogo)
            layout.addRow(botaoLogo, botaoVerLogo)
            layout.addWidget(spacer)

            self.nomeImagemAL = QLineEdit()
            self.nomeImagemAL.setReadOnly(True)
            self.nomeImagemAL.setPlaceholderText("Search the image to provide his name..")

            self.nomeImagemBotao = QPushButton("Search Image")
            self.nomeImagemBotao.clicked.connect(procurarImagem)
            layout.addRow(self.nomeImagemBotao, self.nomeImagemAL)

            botaoVerImagem = QPushButton("View Image")
            botaoVerImagem.setDefault(True)
            botaoVerImagem.clicked.connect(visualizarImagem)

            botaoAddLogoImagem = QPushButton("Add Logo to Image")
            botaoAddLogoImagem.setDefault(True)
            botaoAddLogoImagem.clicked.connect(self.addLogoImagem)
            layout.addRow(botaoVerImagem, botaoAddLogoImagem)
            layout.addWidget(spacer)

            self.dirImagem = QLineEdit()
            self.dirImagem.setReadOnly(True)
            self.dirImagem.setPlaceholderText("Find the directory containing the images..")
            layout.addRow(self.dirImagem)

            dirImagemBotao = QPushButton("Find Directory")
            dirImagemBotao.setDefault(True)
            dirImagemBotao.setToolTip("the logo will be added to the images automatically!")
            dirImagemBotao.clicked.connect(self.procurarDirectorio)
            layout.addRow(dirImagemBotao)

            browser = lambda p: webbrowser.open('https://artesgc.home.blog')
            labelCopyright = QLabel("<a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
            labelCopyright.setAlignment(Qt.AlignRight)
            labelCopyright.setToolTip('Access to the official website of ArtesGC!')
            labelCopyright.linkActivated.connect(browser)
            layout.addWidget(labelCopyright)

            self.janela1.setLayout(layout)

        def converterIco(self):
            def procurarImagem():
                nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select Image", filter="Image Files (*.png *.jpg *.jpeg)")
                self.nomeImagemCI.setText(nomeFicheiro)

            def converter():
                if self.nomeImagemCI.text() == "" or self.nomeImagemCI.text().isspace():
                    QMessageBox.critical(self.ferramentas, "Error", f"Select the image before continuing and try again..")
                    self.procurarImagem()
                else:
                    try:
                        QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                        dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select where to save the file")
                        ImaGC(_dir_salvar=dirSalvar, _nome_imagem=self.nomeImagemCI.text()).convertendoIcone(_size=int(tamanhos.currentText()))
                        QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
                    except Exception as erro:
                        QMessageBox.critical(self.ferramentas, "Error", f"{erro}..")

            def visualizarImagem():
                if self.nomeImagemCI.text() == "" or self.nomeImagemCI.text().isspace():
                    QMessageBox.warning(self.ferramentas, "Failed to display the image", "Please select the image before proceeding..")
                else:
                    janelaImagem = QDialog()
                    janelaImagem.setWindowIcon(QIcon("img/imagc.png"))
                    janelaImagem.setWindowTitle("View Image")
                    janelaImagem.setPalette(QPalette(QColor("orange")))

                    layoutJanelaImagem = QVBoxLayout()
                    labelImagem = QLabel()
                    labelImagem.setAlignment(Qt.AlignCenter)
                    labelImagem.setToolTip("Image presentation!")
                    labelImagem.setPixmap(QPixmap(f"{self.nomeImagemCI.text()}").scaled(QSize(400, 400)))
                    layoutJanelaImagem.addWidget(labelImagem)

                    infoImage = QLabel(f"""<h3><i>Details</i></h3>
<b>Name & Location</b>: {self.nomeImagemCI.text()}<br>
<b>Scale (original)</b>: {ImaGC().dimensaoImagem(_filename=self.nomeImagemCI.text())} px<br>
<b>Size</b>: {ImaGC().tamanhoImagem(self.nomeImagemCI.text())}""")
                    layoutJanelaImagem.addWidget(infoImage)

                    _fechar = lambda: janelaImagem.destroy(True)
                    botaoFechar = QPushButton("Close")
                    botaoFechar.setDefault(True)
                    botaoFechar.clicked.connect(_fechar)
                    layoutJanelaImagem.addWidget(botaoFechar)

                    janelaImagem.setLayout(layoutJanelaImagem)
                    janelaImagem.show()

            spacer = QLabel()
            layout = QFormLayout()
            layout.setSpacing(10)

            labelIntro = QLabel("<h2><i>Convert to Ico</i></h2>")
            labelIntro.setAlignment(Qt.AlignCenter)
            labelIntro.setFont(QFont("times", 20))
            layout.addRow(labelIntro)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            self.nomeImagemCI = QLineEdit()
            self.nomeImagemCI.setReadOnly(True)
            self.nomeImagemCI.setPlaceholderText('Search the image to provide his name..')

            self.botaoIco = QPushButton("Search Image")
            self.botaoIco.clicked.connect(procurarImagem)
            layout.addRow(self.botaoIco, self.nomeImagemCI)

            botaoVerImagem = QPushButton("View Image")
            botaoVerImagem.clicked.connect(visualizarImagem)
            layout.addRow(botaoVerImagem)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            labelConverter = QLabel("<b><i>Convert to icon with different dimensions:</i></b>")
            labelConverter.setFont(QFont("times", 10))
            labelConverter.setAlignment(Qt.AlignCenter)
            layout.addRow(labelConverter)

            botaoConverter = QPushButton("Convert")
            botaoConverter.clicked.connect(converter)

            listaTamanhos = ['16', '32', '128', '256']
            tamanhos = QComboBox()
            tamanhos.addItems(listaTamanhos)
            tamanhos.setToolTip('Choose the size!')
            layout.addRow(tamanhos, botaoConverter)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            browser = lambda p: webbrowser.open('https://artesgc.home.blog')
            labelCopyright = QLabel("<a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
            labelCopyright.setAlignment(Qt.AlignRight)
            labelCopyright.setToolTip('Access to the official website of ArtesGC!')
            labelCopyright.linkActivated.connect(browser)
            layout.addWidget(labelCopyright)

            self.janela2.setLayout(layout)

        def redimensionarImagem(self):
            def procurarImagem():
                nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select Image", filter="Image Files (*.png *.jpg *.jpeg)")
                self.nomeImagemRI.setText(nomeFicheiro)

            def redimensionar():
                if self.nomeImagemRI.text() == "" or self.nomeImagemRI.text().isspace():
                    QMessageBox.critical(self.ferramentas, "Error", f"Select the image before continuing and try again..")
                    self.procurarImagem()
                else:
                    try:
                        QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                        dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select where to save the file")
                        ImaGC(_dir_salvar=dirSalvar, _nome_imagem=self.nomeImagemRI.text()).redimensionarImagem(_size=int(tamanhos.currentText()))
                        QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
                    except Exception as erro:
                        QMessageBox.critical(self.ferramentas, "Error", f"{erro}..")

            def visualizarImagem():
                if self.nomeImagemRI.text() == "" or self.nomeImagemRI.text().isspace():
                    QMessageBox.warning(self.ferramentas, "Failed to display the image", "Please select the image before proceeding..")
                else:
                    janelaImagem = QDialog()
                    janelaImagem.setWindowIcon(QIcon("img/imagc.png"))
                    janelaImagem.setWindowTitle("View Image")
                    janelaImagem.setPalette(QPalette(QColor("orange")))

                    layoutJanelaImagem = QVBoxLayout()
                    labelImagem = QLabel()
                    labelImagem.setAlignment(Qt.AlignCenter)
                    labelImagem.setToolTip("Image presentation!")
                    labelImagem.setPixmap(QPixmap(f"{self.nomeImagem.text()}").scaled(QSize(400, 400)))
                    layoutJanelaImagem.addWidget(labelImagem)

                    infoImage = QLabel(f"""<h3><i>Details</i></h3>
<b>Name & Location</b>: {self.nomeImagemRI.text()}<br>
<b>Scale (original)</b>: {ImaGC().dimensaoImagem(_filename=self.nomeImagemRI.text())} px<br>
<b>Size</b>: {ImaGC().tamanhoImagem(self.nomeImagemRI.text())}""")
                    layoutJanelaImagem.addWidget(infoImage)

                    _fechar = lambda: janelaImagem.destroy(True)
                    botaoFechar = QPushButton("Close")
                    botaoFechar.setDefault(True)
                    botaoFechar.clicked.connect(_fechar)
                    layoutJanelaImagem.addWidget(botaoFechar)

                    janelaImagem.setLayout(layoutJanelaImagem)
                    janelaImagem.show()

            spacer = QLabel()
            layout = QFormLayout()
            layout.setSpacing(10)

            labelIntro = QLabel("<h2><i>Resize Image</i></h2>")
            labelIntro.setAlignment(Qt.AlignCenter)
            labelIntro.setFont(QFont("times", 20))
            layout.addRow(labelIntro)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            self.nomeImagemRI = QLineEdit()
            self.nomeImagemRI.setReadOnly(True)
            self.nomeImagemRI.setPlaceholderText('Search the image to provide his name..')

            self.botaoIco = QPushButton("Search Image")
            self.botaoIco.clicked.connect(procurarImagem)
            layout.addRow(self.botaoIco, self.nomeImagemRI)

            botaoVerImagem = QPushButton("View Image")
            botaoVerImagem.clicked.connect(visualizarImagem)
            layout.addRow(botaoVerImagem)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            labelConverter = QLabel("<b><i>Resize the image to different dimensions:</i></b>")
            labelConverter.setFont(QFont("times", 10))
            labelConverter.setAlignment(Qt.AlignCenter)
            layout.addRow(labelConverter)

            botaoConverter = QPushButton("Resize")
            botaoConverter.clicked.connect(redimensionar)

            listaTamanhos = ['200', '400', '600', '800', '1200']
            tamanhos = QComboBox()
            tamanhos.addItems(listaTamanhos)
            tamanhos.setToolTip('Choose the scale!')
            layout.addRow(tamanhos, botaoConverter)
            layout.addWidget(spacer)
            layout.addWidget(spacer)

            browser = lambda p: webbrowser.open('https://artesgc.home.blog')
            labelCopyright = QLabel("<a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
            labelCopyright.setAlignment(Qt.AlignRight)
            labelCopyright.setToolTip('Access to the official website of ArtesGC!')
            labelCopyright.linkActivated.connect(browser)
            layout.addWidget(labelCopyright)

            self.janela3.setLayout(layout)

        def alterarJanela(self, i):
            self.stack.setCurrentIndex(i)

        # ******* background-functions *******
        def procurarLogo(self):
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select the Logo", filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeLogo.setText(nomeFicheiro)

        def addLogoImagem(self):
            if self.nomeLogo.text() != "":
                QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select where to save the file")
                ImaGC(_dir_salvar=dirSalvar, _nome_logotipo=self.nomeLogo.text(), _nome_imagem=self.nomeImagemAL.text()).addLogo()
                QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
            else:
                QMessageBox.critical(self.ferramentas, "Error", f"Select the logo before continuing and try again..")
                self.procurarLogo()

        def procurarDirectorio(self):
            if self.nomeLogo.text() != "":
                nomeDirectorio = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select the Image")
                self.dirImagem.setText(nomeDirectorio)
                QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select where to save the file")
                ImaGC(_dir_salvar=dirSalvar, _nome_logotipo=self.nomeLogo.text(), _dir_imagem=self.dirImagem.text()).addLogo()
                QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
            else:
                QMessageBox.critical(self.ferramentas, "Error", f"Select the logo before continuing and try again..")
                self.procurarLogo()


if __name__ == '__main__':
    gc = QApplication(argv)
    gcApp = ImaGC_GUI()
    gcApp.janela.show()
    gc.exec_()
