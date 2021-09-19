import os
import webbrowser
from sys import exit
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from imageditor import ImagEditor

theme = open('themes/imagc.qss').read().strip()


# ******* portuguese-program *******
class PT:
    def __init__(self):
        # ******* layout-principal *******
        layout_principal = QVBoxLayout()

        self.ferramentas = QWidget()
        self.ferramentas.setFixedSize(QSize(800, 500))
        self.ferramentas.setWindowTitle("ImaGC")
        self.ferramentas.setWindowIcon(QIcon("icons/favicon-192x192.png"))
        self.ferramentas.setStyleSheet(theme)

        # ******* background-image *******
        bg_image = QImage("icons/bg.jpg")
        set_bg_image = bg_image.scaled(QSize(800, 500))  # resize Image to widget's size
        palette = QPalette()
        palette.setBrush(palette.ColorGroup.All, palette.ColorRole.Window, QBrush(set_bg_image))
        self.ferramentas.setPalette(palette)

        # ******* global-vars *******
        self.nomeImagemAL = None
        self.nomeImagemCI = None
        self.nomeImagemRI = None
        self.nomeImagensCG = None
        self.dimensaoImagensCG = None
        self.tamanhoImagensCG = None
        self.nomeImagensCP = None
        self.dimensaoImagensCP = None
        self.tamanhoImagensCP = None
        self.nomeFicheiros = None
        self.nomeLogo = None
        self.dirImagem = None
        self.botaoIco = None
        self.nomeImagemBotao = None

        # ******* menu *******
        menu = QMenuBar()
        layout_principal.setMenuBar(menu)
        instr = menu.addAction("Instruções")
        instr.triggered.connect(self._instr)

        debug = menu.addAction("Registo de erros")
        debug.triggered.connect(self._debug)

        sobre = menu.addAction("Sobre")
        sobre.triggered.connect(self._sobre)

        _sair = lambda: exit(0)
        sair = menu.addAction("Sair")
        sair.triggered.connect(_sair)

        # ******* list-options *******
        self.listaJanelas = QListWidget(self.ferramentas)
        self.listaJanelas.setAlternatingRowColors(True)
        self.listaJanelas.setFixedSize(QSize(200, 110))
        self.listaJanelas.addItem("Adicionar Logotipo")
        self.listaJanelas.addItem("Converter para Gif")
        self.listaJanelas.addItem("Converter para Ico")
        self.listaJanelas.addItem("Converter para Pdf")
        self.listaJanelas.addItem("Redimensionar Imagem")

        # ******* init-windows *******
        self.janela1 = QWidget()
        self.adicionar_logo()

        self.janela2 = QWidget()
        self.converter_gif()

        self.janela3 = QWidget()
        self.converter_ico()

        self.janela4 = QWidget()
        self.converter_pdf()

        self.janela5 = QWidget()
        self.redimensionar_imagem()

        # ******* stack *******
        self.stack = QStackedWidget(self.ferramentas)
        self.stack.addWidget(self.janela1)
        self.stack.addWidget(self.janela2)
        self.stack.addWidget(self.janela3)
        self.stack.addWidget(self.janela4)
        self.stack.addWidget(self.janela5)

        # ******* layout-janelas *******
        hbox = QHBoxLayout()
        hbox.addWidget(self.listaJanelas)
        hbox.addWidget(self.stack)
        layout_principal.addLayout(hbox)

        # ******* label-copyright *******
        browser = lambda: webbrowser.open('https://artesgc.home.blog')
        labelCopyright = QLabel("<hr><a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
        labelCopyright.setAlignment(Qt.AlignmentFlag.AlignRight)
        labelCopyright.setToolTip('Acesso a pagina oficial da ArtesGC!')
        labelCopyright.linkActivated.connect(browser)
        layout_principal.addWidget(labelCopyright)

        self.ferramentas.setLayout(layout_principal)
        self.listaJanelas.currentRowChanged.connect(self.alterar_janela)

    # ******* menu-functions *******
    def _instr(self):
        QMessageBox.information(self.ferramentas, "Instruções", """
Olaa caro usuário!

É com muito prazer e orgulho que apresento te o ImaGC
Um programa simples e cheio de funcionalidades
Das quais a sua principal função é de editar imagens!

- PARA O ADICIONAR O LOGOTIPO, ELE DEVE TER O FUNDO OU MASCARA TRANSPARENTE;
- PARA A CONVERSÃO DE (.ico) O PROGRAMA SUBESCREVE OS DADOS BINÁRIOS DA IMAGEM
E REDEFINE AS DIMENSÕES DA MESMA;
- PARA A CONVERSÃO DE (.gif) O PROGRAMA COPIA OS DADOS DAS IMAGENS
E CRIA UM CICLO ALTERNADO ENTRE ELAS COM DURAÇÃO DE 1 SEGUNDO POR QUADRO;
- PARA A CONVERSÃO DE (.pdf) O PROGRAMA COPIA IGUALMENTE A OU AS IMAGENS
E CRIA UM ARQUIVO PDF COM AS IMAGENS AUTOMATICAMENTE REDIMENSIONADAS;
- PARA O REDIMENSIONAMENTO DAS IMAGENS, O PROGRAMA OTIMIZA O TAMANHO ORIGINAL DAS IMAGENS
E REDIMENSIONA DE ACORDO A DIMENSÃO QUE O UTILIZADOR DESEJA REDUZIR OU AUMENTAR;

Muito Obrigado pelo apoio!
© 2021 Nurul GC
™ ArtesGC Inc""")

    def _sobre(self):
        janela = QDialog(self.ferramentas)
        janela.setWindowTitle("Sobre")
        layout = QVBoxLayout()

        sobre_label = QLabel("""
Nome: <b>ImaGC</b><br>
Versão: <b>0.6-092021</b><br>
Programador & Designer: <b>Nurul-GC</b><br>
Empresa: <b>&trade;ArtesGC Inc.</b>""")
        sobre_label.setStyleSheet("background-color: orange;"
                                  "padding: 5px;"
                                  "border-radius: 2px;")
        layout.addWidget(sobre_label)

        _fechar = lambda: janela.close()
        fechar_btn = QPushButton('Ok')
        fechar_btn.clicked.connect(_fechar)
        layout.addWidget(fechar_btn)

        janela.setLayout(layout)
        janela.exec()

    def _debug(self):
        def leitura_log():
            registo.clear()
            with open(f'./Debug/{lista_registo.currentItem().text()}', 'r') as log_file:
                registo.setText(log_file.read())

        janela_debug = QDialog(self.ferramentas)
        janela_debug.setFixedSize(QSize(700, 500))
        janela_debug.setWindowTitle("Registo de erros")
        layout_janela_debug = QFormLayout()

        layout_registo = QHBoxLayout()
        lista_registo = QListWidget()
        lista_registo.setSortingEnabled(True)
        lista_registo.setAlternatingRowColors(True)
        lista_registo.itemClicked.connect(leitura_log)
        layout_registo.addWidget(lista_registo)

        registo = QTextEdit()
        registo.setReadOnly(True)
        registo.setPlaceholderText("Selecione um dos arquivos para ler o seu conteudo..")
        layout_registo.addWidget(registo)

        for log in os.listdir('./Debug'):
            lista_registo.addItem(log)

        layout_janela_debug.addRow(layout_registo)

        _fechar = lambda: janela_debug.destroy(True)
        botao_fechar = QPushButton("Fechar")
        botao_fechar.setDefault(True)
        botao_fechar.clicked.connect(_fechar)
        layout_janela_debug.addWidget(botao_fechar)

        janela_debug.setLayout(layout_janela_debug)
        janela_debug.show()

    # ******* windows *******
    def adicionar_logo(self):
        def procurar_imagem():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione a Imagem",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeImagemAL.setText(nomeFicheiro)

        def procurar_logo():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas,
                                                                        caption="Selecione o Logotipo",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeLogo.setText(nomeFicheiro)

        def add_logo_imagem():
            if self.nomeLogo.text() != "":
                QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                             caption="Selecione onde salvar o arquivo")
                ImagEditor(_dir_salvar=dirSalvar, _nome_logotipo=self.nomeLogo.text(),
                           _nome_imagem=self.nomeImagemAL.text()).addLogo()
                QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
            else:
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione o logotipo antes de continuar e tente novamente..")
                self.procurarLogo()

        def procurar_directorio():
            if self.nomeLogo.text() != "":
                nomeDirectorio = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione a Imagem")
                self.dirImagem.setText(nomeDirectorio)
                QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                             caption="Selecione onde salvar o arquivo")
                ImagEditor(_dir_salvar=dirSalvar).addLogo(_nome_logotipo=self.nomeLogo.text(),
                                                          _dir_imagens=self.dirImagem.text())
                QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
            else:
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione o logotipo antes de continuar e tente novamente..")
                self.procurarLogo()

        def visualizar_logo():
            if self.nomeLogo.text() == "" or self.nomeLogo.text().isspace():
                QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem",
                                    "Por favor selecione a imagem antes de prosseguir..")
            else:
                janelaLogo = QDialog()
                janelaLogo.setWindowIcon(QIcon("icons/imagc.png"))
                janelaLogo.setWindowTitle("Visualizar Logo")
                janelaLogo.setPalette(QPalette(QColor("orange")))

                layoutJanelaLogo = QVBoxLayout()
                labelLogo = QLabel()
                labelLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelLogo.setToolTip("Apresentação do logotipo!")
                labelLogo.setPixmap(QPixmap(f"{self.nomeLogo.text()}").scaled(QSize(400, 400)))
                layoutJanelaLogo.addWidget(labelLogo)

                infoImage = QLabel(f"""<h3><i>Detalhes</i></h3>
<b>Nome</b>: {self.nomeLogo.text().split('/')[-1]}<br>
<b>Dimensão (original)</b>: {ImagEditor().dimensaoImagem(_filename=self.nomeLogo.text())} px<br>
<b>Tamanho</b>: {ImagEditor().tamanhoImagem(self.nomeLogo.text())}""")
                layoutJanelaLogo.addWidget(infoImage)

                _fechar = lambda: janelaLogo.destroy(True)
                botaoFechar = QPushButton("Fechar")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaLogo.addWidget(botaoFechar)

                janelaLogo.setLayout(layoutJanelaLogo)
                janelaLogo.show()

        def visualizar_imagem():
            if self.nomeImagemAL.text() == "" or self.nomeImagemAL.text().isspace():
                QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem",
                                    "Por favor selecione a imagem antes de prosseguir..")
            else:
                janelaImagem = QDialog()
                janelaImagem.setWindowIcon(QIcon("icons/imagc.png"))
                janelaImagem.setWindowTitle("Visualizar Imagem")
                janelaImagem.setPalette(QPalette(QColor("orange")))

                layoutJanelaImagem = QVBoxLayout()
                labelImagem = QLabel()
                labelImagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelImagem.setToolTip("Apresentação do logotipo!")
                labelImagem.setPixmap(QPixmap(f"{self.nomeImagemAL.text()}").scaled(QSize(400, 400)))
                layoutJanelaImagem.addWidget(labelImagem)

                infoImage = QLabel(f"""<h3><i>Detalhes</i></h3>
<b>Nome</b>: {self.nomeImagemAL.text().split('/')[-1]}<br>
<b>Dimensão (original)</b>: {ImagEditor().dimensaoImagem(_filename=self.nomeImagemAL.text())} px<br>
<b>Tamanho</b>: {ImagEditor().tamanhoImagem(self.nomeImagemAL.text())}""")
                layoutJanelaImagem.addWidget(infoImage)

                _fechar = lambda: janelaImagem.destroy(True)
                botaoFechar = QPushButton("Fechar")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaImagem.addWidget(botaoFechar)

                janelaImagem.setLayout(layoutJanelaImagem)
                janelaImagem.show()

        spacer = QLabel("<hr>")
        layout = QFormLayout()
        layout.setSpacing(10)

        label_intro = QLabel("<h1><i>Adicionar Logotipo</i></h1>")
        label_intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(label_intro)
        layout.addWidget(spacer)

        self.nomeLogo = QLineEdit()
        self.nomeLogo.setReadOnly(True)
        self.nomeLogo.setPlaceholderText("Procure pela imagem para obter o seu nome..")
        layout.addRow(self.nomeLogo)

        botao_logo = QPushButton("Procurar Logótipo")
        botao_logo.setDefault(True)
        botao_logo.clicked.connect(procurar_logo)

        botao_ver_logo = QPushButton("Visualizar Logótipo")
        botao_ver_logo.setDefault(True)
        botao_ver_logo.clicked.connect(visualizar_logo)
        layout.addRow(botao_logo, botao_ver_logo)
        layout.addWidget(spacer)

        self.nomeImagemAL = QLineEdit()
        self.nomeImagemAL.setReadOnly(True)
        self.nomeImagemAL.setPlaceholderText("Procure pela imagem para obter o seu nome..")

        self.nomeImagemBotao = QPushButton("Procurar Imagem")
        self.nomeImagemBotao.setDefault(True)
        self.nomeImagemBotao.clicked.connect(procurar_imagem)
        layout.addRow(self.nomeImagemBotao, self.nomeImagemAL)

        botao_ver_imagem = QPushButton("Visualizar Imagem")
        botao_ver_imagem.setDefault(True)
        botao_ver_imagem.clicked.connect(visualizar_imagem)

        botao_add_logo_imagem = QPushButton("Adicionar Logo a Imagem")
        botao_add_logo_imagem.setDefault(True)
        botao_add_logo_imagem.clicked.connect(add_logo_imagem)
        layout.addRow(botao_ver_imagem, botao_add_logo_imagem)
        layout.addWidget(spacer)

        self.dirImagem = QLineEdit()
        self.dirImagem.setReadOnly(True)
        self.dirImagem.setPlaceholderText("Localize o diretório contendo as imagens..")
        layout.addRow(self.dirImagem)

        dir_imagem_botao = QPushButton("Localizar Directório")
        dir_imagem_botao.setDefault(True)
        dir_imagem_botao.setToolTip("o logotipo sera adicionado as imagens automaticamente!")
        dir_imagem_botao.clicked.connect(procurar_directorio)
        layout.addRow(dir_imagem_botao)

        self.janela1.setLayout(layout)

    def converter_gif(self):
        def procurar_imagens():
            nome_imagens_cg.clear()
            self.nomeFicheiros, filtroFicheiros = QFileDialog.getOpenFileNames(self.ferramentas,
                                                                               caption="Selecione a Imagem",
                                                                               filter="Image Files (*.png *.jpg *.jpeg)")
            if len(self.nomeFicheiros) < 2:
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione 'as imagens' antes de continuar e tente novamente..")
            else:
                nome_imagens_cg.addItems(self.nomeFicheiros)

        def previsualizar_img():
            self.nomeImagensCG = nome_imagens_cg.currentItem().text()
            self.dimensaoImagensCG = ImagEditor().dimensaoImagem(self.nomeImagensCG)
            self.tamanhoImagensCG = ImagEditor().tamanhoImagem(self.nomeImagensCG)
            imagem = QPixmap(self.nomeImagensCG)
            imagem_label.setPixmap(imagem.scaled(QSize(150, 150)))
            imagem_label.setToolTip("Está não é a dimensão original da imagem "
                                    "apenas foi adaptada para uma pré-visualização!")
            imagem_detail.setText(f"""
<b>Nome</b>: {self.nomeImagensCG.split('/')[-1]}<br>
<b>Tamanho</b>: {self.tamanhoImagensCG}<br>
<b>Dimensões (original)</b>: {self.dimensaoImagensCG}
""")

        def converter_imagens():
            if self.nomeFicheiros is None:
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione as imagens antes de continuar e tente novamente..")
                procurar_imagens()
            else:
                try:
                    QMessageBox.warning(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Selecione onde salvar o arquivo")
                    ImagEditor(_dir_salvar=dirSalvar).convertendoGif(_images=self.nomeFicheiros)
                    QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"{erro}..")

        nome_imagens_cg = QListWidget()
        layout = QFormLayout()
        layout.setSpacing(10)
        spacer = QLabel("<hr>")

        intro_label = QLabel("<h1><i>Converter para Gif</i></h1>")
        intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(intro_label)
        layout.addRow(spacer)

        imagem_layout = QHBoxLayout()
        imagem_label = QLabel("Pesquise a imagem\npara pre-visualiza-la..")
        imagem_label.setFixedSize(QSize(150, 150))
        imagem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagem_label.setStyleSheet('background-color: white; padding: 2px;')
        imagem_layout.addWidget(imagem_label)
        imagem_detail = QLabel(f"""
<b>Nome</b>: {self.nomeImagensCG}<br>
<b>Tamanho</b>: {self.tamanhoImagensCG}<br>
<b>Dimensões (original)</b>: {self.dimensaoImagensCG}
""")
        imagem_layout.addWidget(imagem_detail)
        layout.addRow(imagem_layout)
        layout.addRow(spacer)

        nome_imagens_cg.setAlternatingRowColors(True)
        nome_imagens_cg.itemClicked.connect(previsualizar_img)
        layout.addRow(nome_imagens_cg)
        layout.addRow(spacer)

        layout_btns = QHBoxLayout()
        procurar_btn = QPushButton("Procurar Imagens")
        procurar_btn.clicked.connect(procurar_imagens)
        layout_btns.addWidget(procurar_btn)
        converter_btn = QPushButton("Converter Imagens")
        converter_btn.clicked.connect(converter_imagens)
        layout_btns.addWidget(converter_btn)

        layout.addRow(layout_btns)
        self.janela2.setLayout(layout)

    def converter_ico(self):
        def procurarImagem():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione a Imagem",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeImagemCI.setText(nomeFicheiro)

        def converter():
            if self.nomeImagemCI.text() == "" or self.nomeImagemCI.text().isspace():
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione a imagem antes de continuar e tente novamente..")
                self.procurarImagem()
            else:
                try:
                    QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Selecione onde salvar o arquivo")
                    ImagEditor(_dir_salvar=dirSalvar).convertendoIcone(_size=int(tamanhos.currentText()),
                                                                       _nome_imagem=self.nomeImagemCI.text())
                    QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"{erro}..")

        def visualizarImagem():
            if self.nomeImagemCI.text() == "" or self.nomeImagemCI.text().isspace():
                QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem",
                                    "Por favor selecione a imagem antes de prosseguir..")
            else:
                janelaImagem = QDialog()
                janelaImagem.setWindowIcon(QIcon("icons/imagc.png"))
                janelaImagem.setWindowTitle("Visualizar Imagem")
                janelaImagem.setPalette(QPalette(QColor("orange")))

                layoutJanelaImagem = QVBoxLayout()
                labelImagem = QLabel()
                labelImagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelImagem.setToolTip("Apresentação do logotipo!")
                labelImagem.setPixmap(QPixmap(f"{self.nomeImagemCI.text()}").scaled(QSize(400, 400)))
                layoutJanelaImagem.addWidget(labelImagem)

                infoImage = QLabel(f"""<h3><i>Detalhes</i></h3>
<b>Nome & Localização</b>: {self.nomeImagemCI.text()}<br>
<b>Dimensão (original)</b>: {ImagEditor().dimensaoImagem(_filename=self.nomeImagemCI.text())} px<br>
<b>Tamanho</b>: {ImagEditor().tamanhoImagem(self.nomeImagemCI.text())}""")
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

        labelIntro = QLabel("<h1><i>Converter para Ico</i></h1>")
        labelIntro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelIntro)
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

        labelConverter = QLabel("<b><i>Converta para ícone com dimensões diferentes:</i></b>")
        labelConverter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelConverter)

        layoutDimensoes = QHBoxLayout()
        listaTamanhos = ['16', '32', '128', '256']
        tamanhos = QComboBox()
        tamanhos.addItems(listaTamanhos)
        tamanhos.setToolTip('Escolha a dimensão!')
        layoutDimensoes.addWidget(tamanhos)

        botaoConverter = QPushButton("Converter")
        botaoConverter.clicked.connect(converter)
        layoutDimensoes.addWidget(botaoConverter)

        layout.addRow(layoutDimensoes)
        self.janela3.setLayout(layout)

    def converter_pdf(self):
        def procurarImagens():
            nomeImagensCP.clear()
            self.nomeFicheiros, filtroFicheiros = QFileDialog.getOpenFileNames(self.ferramentas,
                                                                               caption="Selecione a Imagem",
                                                                               filter="Image Files (*.png *.jpg *.jpeg)")
            if len(self.nomeFicheiros) < 1:
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione 'as imagens' antes de continuar e tente novamente..")
            else:
                nomeImagensCP.addItems(self.nomeFicheiros)

        def previsualizarImg():
            self.nomeImagensCP = nomeImagensCP.currentItem().text()
            self.dimensaoImagensCP = ImagEditor().dimensaoImagem(self.nomeImagensCP)
            self.tamanhoImagensCP = ImagEditor().tamanhoImagem(self.nomeImagensCP)
            imagem = QPixmap(self.nomeImagensCP)
            imagemLabel.setPixmap(imagem.scaled(QSize(150, 150)))
            imagemLabel.setToolTip("Está não é a dimensão original da imagem "
                                   "apenas foi adaptada para uma pré-visualização!")
            imagemDetail.setText(f"""
<b>Nome</b>: {self.nomeImagensCP.split('/')[-1]}<br>
<b>Tamanho</b>: {self.tamanhoImagensCP}<br>
<b>Dimensões (original)</b>: {self.dimensaoImagensCP}""")

        def converterImagens():
            if self.nomeFicheiros is None:
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione as imagens antes de continuar e tente novamente..")
                procurarImagens()
            else:
                try:
                    QMessageBox.warning(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Selecione onde salvar o arquivo")
                    ImagEditor(_dir_salvar=dirSalvar).convertendoPdf(_images=self.nomeFicheiros)
                    QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"{erro}..")

        layout = QFormLayout()
        layout.setSpacing(10)
        spacer = QLabel("<hr>")

        introLabel = QLabel("<h1><i>Converter para Pdf</i></h1>")
        introLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(introLabel)
        layout.addRow(spacer)

        imagemLayout = QHBoxLayout()
        imagemLabel = QLabel("Pesquise a imagem\npara pre-visualiza-la..")
        imagemLabel.setFixedSize(QSize(150, 150))
        imagemLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagemLabel.setStyleSheet('background-color: white; padding: 2px;')
        imagemLayout.addWidget(imagemLabel)
        imagemDetail = QLabel(f"""
<b>Nome</b>: {self.nomeImagensCP}<br>
<b>Tamanho</b>: {self.tamanhoImagensCP}<br>
<b>Dimensões (original)</b>: {self.dimensaoImagensCP}""")
        imagemLayout.addWidget(imagemDetail)
        layout.addRow(imagemLayout)
        layout.addRow(spacer)

        nomeImagensCP = QListWidget()
        nomeImagensCP.setAlternatingRowColors(True)
        nomeImagensCP.itemClicked.connect(previsualizarImg)
        layout.addRow(nomeImagensCP)
        layout.addRow(spacer)

        layoutBtns = QHBoxLayout()
        procurarBtn = QPushButton("Procurar Imagens")
        procurarBtn.clicked.connect(procurarImagens)
        layoutBtns.addWidget(procurarBtn)
        converterBtn = QPushButton("Converter Imagens")
        converterBtn.clicked.connect(converterImagens)
        layoutBtns.addWidget(converterBtn)

        layout.addRow(layoutBtns)
        self.janela4.setLayout(layout)

    def redimensionar_imagem(self):
        def procurarImagem():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione a Imagem",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeImagemRI.setText(nomeFicheiro)

        def redimensionar():
            if self.nomeImagemRI.text() == "" or self.nomeImagemRI.text().isspace():
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione a imagem antes de continuar e tente novamente..")
                self.procurarImagem()
            else:
                try:
                    QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Selecione onde salvar o arquivo")
                    ImagEditor(_dir_salvar=dirSalvar).redimensionarImagem(_resizer=int(divisor.currentText()) / 100,
                                                                          _nome_imagem=self.nomeImagemRI.text())
                    QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"{erro}..")

        def visualizarImagem():
            if self.nomeImagemRI.text() == "" or self.nomeImagemRI.text().isspace():
                QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem",
                                    "Por favor selecione a imagem antes de prosseguir..")
            else:
                janelaImagem = QDialog()
                janelaImagem.setWindowIcon(QIcon("icons/imagc.png"))
                janelaImagem.setWindowTitle("Visualizar Imagem")
                janelaImagem.setPalette(QPalette(QColor("orange")))

                layoutJanelaImagem = QVBoxLayout()
                labelImagem = QLabel()
                labelImagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelImagem.setToolTip("Apresentação do logotipo!")
                labelImagem.setPixmap(QPixmap(f"{self.nomeImagemRI.text()}").scaled(QSize(400, 400)))
                layoutJanelaImagem.addWidget(labelImagem)

                infoImage = QLabel(f"""<h3><i>Detalhes</i></h3>
<b>Nome</b>: {self.nomeImagemRI.text().split('/')[-1]}<br>
<b>Dimensão (original)</b>: {ImagEditor().dimensaoImagem(_filename=self.nomeImagemRI.text())} px<br>
<b>Tamanho</b>: {ImagEditor().tamanhoImagem(self.nomeImagemRI.text())}""")
                layoutJanelaImagem.addWidget(infoImage)

                _fechar = lambda: janelaImagem.destroy(True)
                botaoFechar = QPushButton("Fechar")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaImagem.addWidget(botaoFechar)

                janelaImagem.setLayout(layoutJanelaImagem)
                janelaImagem.show()

        spacer = QLabel("<hr>")
        layout = QFormLayout()
        layout.setSpacing(10)

        labelIntro = QLabel("<h1><i>Redimensionar Imagem</i></h1>")
        labelIntro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelIntro)
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

        labelConverter = QLabel("<b><i>Defina a percentagem que redimensionara a imagem:</i></b>")
        labelConverter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelConverter)

        layoutDimensoes = QHBoxLayout()
        listaDivisor = [f'{n}' for n in range(10, 201, 30)]
        divisor = QComboBox()
        divisor.addItems(listaDivisor)
        divisor.setToolTip('Escolha a percentagem a ser aplicada!')
        layoutDimensoes.addWidget(divisor)

        botaoConverter = QPushButton("Redimensionar")
        botaoConverter.clicked.connect(redimensionar)
        layoutDimensoes.addWidget(botaoConverter)

        layout.addRow(layoutDimensoes)
        self.janela5.setLayout(layout)

    def alterar_janela(self, index):
        self.stack.setCurrentIndex(index)
