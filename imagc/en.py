import os
import webbrowser
from sys import exit
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from imageditor import ImagEditor

theme = open('themes/imagc.qss').read().strip()


# ******* english-program *******
class EN:
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
        instr = menu.addAction("Instructions")
        instr.triggered.connect(self._instr)

        debug = menu.addAction("Log errors")
        debug.triggered.connect(self._debug)

        sobre = menu.addAction("About")
        sobre.triggered.connect(self._sobre)

        _sair = lambda: exit(0)
        sair = menu.addAction("Quit")
        sair.triggered.connect(_sair)

        # ******* list-options *******
        self.listaJanelas = QListWidget(self.ferramentas)
        self.listaJanelas.setAlternatingRowColors(True)
        self.listaJanelas.setFixedSize(QSize(200, 110))
        self.listaJanelas.addItem("Add Logo")
        self.listaJanelas.addItem("Convert to Gif")
        self.listaJanelas.addItem("Convert to Ico")
        self.listaJanelas.addItem("Convert to Pdf")
        self.listaJanelas.addItem("Resize Image")

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
        labelCopyright.setToolTip('Access to the official website of ArtesGC!')
        labelCopyright.linkActivated.connect(browser)
        layout_principal.addWidget(labelCopyright)

        self.ferramentas.setLayout(layout_principal)
        self.listaJanelas.currentRowChanged.connect(self.alterar_janela)

    # ******* menu-functions *******
    def _instr(self):
        QMessageBox.information(self.ferramentas, "Instructions", """
Hello dear user!

It's with great pleasure and pride that I present the ImaGC to you
A simple and full of features program
Of which its main function is to edit images!

- TO ADD THE LOGO, IT MUST HAVE A TRANSPARENT BACKGROUND OR A TRANSPARENT MASK;
- FOR THE CONVERSION TO (.ico) THE PROGRAM EDIT THE BINARY DATA OF THE IMAGE
AND REDEFINES ITS DIMENSIONS;
- FOR THE CONVERSION OF (.gif) THE PROGRAM COPIES THE DATA FROM THE IMAGES
AND CREATES AN ALTERNATE CYCLE BETWEEN THEM WITH DURATION OF 1 SECOND PER FRAME;
- FOR THE CONVERSION OF (.pdf) THE PROGRAM ALSO COPIES THE IMAGE(S)
AND CREATES A PDF FILE WITH AUTOMATICALLY RESIZED IMAGES;
- FOR IMAGE RESIZING, THE PROGRAM OPTIMIZES THE ORIGINAL SIZE OF IMAGES
AND RESIZE ACCORDING TO THE DIMENSION THAT THE USER WISHES TO REDUCE OR INCREASE;

Thank you very much for your support!
© 2021 Nurul GC
™ ArtesGC Inc""")

    def _sobre(self):
        janela = QDialog(self.ferramentas)
        janela.setWindowTitle("About")
        layout = QVBoxLayout()

        sobre_label = QLabel("""
Name: <b>ImaGC</b><br>
Version: <b>0.6-092021</b><br>
Programmer & Designer: <b>Nurul-GC</b><br>
Company: <b>&trade;ArtesGC Inc.</b>""")
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
        janela_debug.setWindowTitle("Log errors")
        layout_janela_debug = QFormLayout()

        layout_registo = QHBoxLayout()
        lista_registo = QListWidget()
        lista_registo.setSortingEnabled(True)
        lista_registo.setAlternatingRowColors(True)
        lista_registo.itemClicked.connect(leitura_log)
        layout_registo.addWidget(lista_registo)

        registo = QTextEdit()
        registo.setReadOnly(True)
        registo.setPlaceholderText("Choose one file to read its content..")
        layout_registo.addWidget(registo)

        for log in os.listdir('./Debug'):
            lista_registo.addItem(log)

        layout_janela_debug.addRow(layout_registo)

        _fechar = lambda: janela_debug.destroy(True)
        botao_fechar = QPushButton("Close")
        botao_fechar.setDefault(True)
        botao_fechar.clicked.connect(_fechar)
        layout_janela_debug.addWidget(botao_fechar)

        janela_debug.setLayout(layout_janela_debug)
        janela_debug.show()

    # ******* windows *******
    def adicionar_logo(self):
        def procurar_imagem():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select Image",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeImagemAL.setText(nomeFicheiro)

        def procurar_logo():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select the Logo",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeLogo.setText(nomeFicheiro)

        def add_logo_imagem():
            if self.nomeLogo.text() != "":
                QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select where to save the file")
                ImagEditor(_dir_salvar=dirSalvar).addLogo(_nome_logotipo=self.nomeLogo.text(),
                                                          _nome_imagem=self.nomeImagemAL.text())
                QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
            else:
                QMessageBox.critical(self.ferramentas, "Error", f"Select the logo before to proceed and try again..")
                self.procurarLogo()

        def procurar_directorio():
            if self.nomeLogo.text() != "":
                nomeDirectorio = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select the Image")
                self.dirImagem.setText(nomeDirectorio)
                QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select where to save the file")
                ImagEditor(_dir_salvar=dirSalvar).addLogo(_nome_logotipo=self.nomeLogo.text(),
                                                          _dir_imagens=self.dirImagem.text())
                QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
            else:
                QMessageBox.critical(self.ferramentas, "Error", f"Select the logo before to proceed and try again..")
                self.procurarLogo()

        def visualizar_logo():
            if self.nomeLogo.text() == "" or self.nomeLogo.text().isspace():
                QMessageBox.warning(self.ferramentas, "Failed to display the image",
                                    "Please select the image before to proceed..")
            else:
                janelaLogo = QDialog()
                janelaLogo.setWindowIcon(QIcon("icons/imagc.png"))
                janelaLogo.setWindowTitle("View Logo")
                janelaLogo.setPalette(QPalette(QColor("orange")))

                layoutJanelaLogo = QVBoxLayout()
                labelLogo = QLabel()
                labelLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelLogo.setToolTip("Logo presentation!")
                labelLogo.setPixmap(QPixmap(f"{self.nomeLogo.text()}").scaled(QSize(400, 400)))
                layoutJanelaLogo.addWidget(labelLogo)

                infoImage = QLabel(f"""<h3><i>Details</i></h3>
<b>Name</b>: {self.nomeLogo.text().split('/')[-1]}<br>
<b>Scale (original)</b>: {ImagEditor().dimensaoImagem(_filename=self.nomeLogo.text())} px<br>
<b>Size</b>: {ImagEditor().tamanhoImagem(self.nomeLogo.text())}""")
                layoutJanelaLogo.addWidget(infoImage)

                _fechar = lambda: janelaLogo.destroy(True)
                botaoFechar = QPushButton("Close")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaLogo.addWidget(botaoFechar)

                janelaLogo.setLayout(layoutJanelaLogo)
                janelaLogo.show()

        def visualizar_imagem():
            if self.nomeImagemAL.text() == "" or self.nomeImagemAL.text().isspace():
                QMessageBox.warning(self.ferramentas, "Failed to display the image",
                                    "Please select the image before proceeding..")
            else:
                janelaImagem = QDialog()
                janelaImagem.setWindowIcon(QIcon("icons/imagc.png"))
                janelaImagem.setWindowTitle("View Image")
                janelaImagem.setPalette(QPalette(QColor("orange")))

                layoutJanelaImagem = QVBoxLayout()
                labelImagem = QLabel()
                labelImagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelImagem.setToolTip("Image presentation!")
                labelImagem.setPixmap(QPixmap(f"{self.nomeImagemAL.text()}").scaled(QSize(400, 400)))
                layoutJanelaImagem.addWidget(labelImagem)

                infoImage = QLabel(f"""<h3><i>Details</i></h3>
<b>Name</b>: {self.nomeImagemAL.text().split('/')[-1]}<br>
<b>Scale (original)</b>: {ImagEditor().dimensaoImagem(_filename=self.nomeImagemAL.text())} px<br>
<b>Size</b>: {ImagEditor().tamanhoImagem(self.nomeImagemAL.text())}""")
                layoutJanelaImagem.addWidget(infoImage)

                _fechar = lambda: janelaImagem.destroy(True)
                botaoFechar = QPushButton("Close")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaImagem.addWidget(botaoFechar)

                janelaImagem.setLayout(layoutJanelaImagem)
                janelaImagem.show()

        spacer = QLabel("<hr>")
        layout = QFormLayout()
        layout.setSpacing(10)

        label_intro = QLabel("<h1><i>Add Logo</i></h1>")
        label_intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(label_intro)
        layout.addWidget(spacer)

        self.nomeLogo = QLineEdit()
        self.nomeLogo.setReadOnly(True)
        self.nomeLogo.setPlaceholderText("Search the image to provide his name..")
        layout.addRow(self.nomeLogo)

        botao_logo = QPushButton("Search Logo")
        botao_logo.setDefault(True)
        botao_logo.clicked.connect(procurar_logo)

        botao_ver_logo = QPushButton("View Logo")
        botao_ver_logo.setDefault(True)
        botao_ver_logo.clicked.connect(visualizar_logo)
        layout.addRow(botao_logo, botao_ver_logo)
        layout.addWidget(spacer)

        self.nomeImagemAL = QLineEdit()
        self.nomeImagemAL.setReadOnly(True)
        self.nomeImagemAL.setPlaceholderText("Search the image to provide its name..")

        self.nomeImagemBotao = QPushButton("Search Image")
        self.nomeImagemBotao.clicked.connect(procurar_imagem)
        layout.addRow(self.nomeImagemBotao, self.nomeImagemAL)

        botao_ver_imagem = QPushButton("View Image")
        botao_ver_imagem.setDefault(True)
        botao_ver_imagem.clicked.connect(visualizar_imagem)

        botao_add_logo_imagem = QPushButton("Add Logo to Image")
        botao_add_logo_imagem.setDefault(True)
        botao_add_logo_imagem.clicked.connect(add_logo_imagem)
        layout.addRow(botao_ver_imagem, botao_add_logo_imagem)
        layout.addWidget(spacer)

        self.dirImagem = QLineEdit()
        self.dirImagem.setReadOnly(True)
        self.dirImagem.setPlaceholderText("Find the directory containing the images..")
        layout.addRow(self.dirImagem)

        dir_imagem_botao = QPushButton("Find Directory")
        dir_imagem_botao.setDefault(True)
        dir_imagem_botao.setToolTip("the logo will be added to the images automatically!")
        dir_imagem_botao.clicked.connect(procurar_directorio)
        layout.addRow(dir_imagem_botao)

        self.janela1.setLayout(layout)

    def converter_gif(self):
        def procurar_imagens():
            nome_imagens_cg.clear()
            self.nomeFicheiros, filtroFicheiros = QFileDialog.getOpenFileNames(self.ferramentas,
                                                                               caption="Select the Image",
                                                                               filter="Image Files (*.png *.jpg *.jpeg)")
            if len(self.nomeFicheiros) < 2:
                QMessageBox.critical(self.ferramentas, "Error",
                                     f"Select 'the images' before to proceed and try again..")
            else:
                nome_imagens_cg.addItems(self.nomeFicheiros)

        def previsualizar_img():
            self.nomeImagensCG = nome_imagens_cg.currentItem().text()
            self.dimensaoImagensCG = ImagEditor().dimensaoImagem(self.nomeImagensCG)
            self.tamanhoImagensCG = ImagEditor().tamanhoImagem(self.nomeImagensCG)
            imagem = QPixmap(self.nomeImagensCG)
            imagem_label.setPixmap(imagem.scaled(QSize(150, 150)))
            imagem_label.setToolTip("This is not the original dimension of the image "
                                    "has just been adapted for a preview!")
            imagem_detail.setText(f"""
<b>Name</b>: {self.nomeImagensCG.split('/')[-1]}<br>
<b>Size</b>: {self.tamanhoImagensCG}<br>
<b>Scale (original)</b>: {self.dimensaoImagensCG}
""")

        def converter_imagens():
            if self.nomeFicheiros is None:
                QMessageBox.critical(self.ferramentas, "Error", f"Select the images before to proceed and try again..")
                procurar_imagens()
            else:
                try:
                    QMessageBox.warning(self.ferramentas, 'Warning', 'Select where to save the file..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Select where to save the file")
                    ImagEditor(_dir_salvar=dirSalvar).convertendoGif(_images=self.nomeFicheiros)
                    QMessageBox.information(self.ferramentas, "Conclude", "Successful Operation..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Error", f"{erro}..")

        nome_imagens_cg = QListWidget()
        layout = QFormLayout()
        layout.setSpacing(10)
        spacer = QLabel("<hr>")

        intro_label = QLabel("<h1><i>Convert to Gif</i></h1>")
        intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(intro_label)
        layout.addRow(spacer)

        imagem_layout = QHBoxLayout()
        imagem_label = QLabel("Search the image\nto preview it..")
        imagem_label.setFixedSize(QSize(150, 150))
        imagem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagem_label.setStyleSheet('background-color: white; padding: 2px;')
        imagem_layout.addWidget(imagem_label)
        imagem_detail = QLabel(f"""
<b>Name</b>: {self.nomeImagensCG}<br>
<b>Size</b>: {self.tamanhoImagensCG}<br>
<b>Scale (original)</b>: {self.dimensaoImagensCG}
""")
        imagem_layout.addWidget(imagem_detail)
        layout.addRow(imagem_layout)
        layout.addRow(spacer)

        nome_imagens_cg.setAlternatingRowColors(True)
        nome_imagens_cg.itemClicked.connect(previsualizar_img)
        layout.addRow(nome_imagens_cg)
        layout.addRow(spacer)

        layout_btns = QHBoxLayout()
        procurar_btn = QPushButton("Search Images")
        procurar_btn.clicked.connect(procurar_imagens)
        layout_btns.addWidget(procurar_btn)
        converter_btn = QPushButton("Convert Images")
        converter_btn.clicked.connect(converter_imagens)
        layout_btns.addWidget(converter_btn)

        layout.addRow(layout_btns)
        self.janela2.setLayout(layout)

    def converter_ico(self):
        def procurarImagem():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select Image",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeImagemCI.setText(nomeFicheiro)

        def converter():
            if self.nomeImagemCI.text() == "" or self.nomeImagemCI.text().isspace():
                QMessageBox.critical(self.ferramentas, "Error", f"Select the image before continuing and try again..")
                self.procurarImagem()
            else:
                try:
                    QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Select where to save the file")
                    ImagEditor(_dir_salvar=dirSalvar).convertendoIcone(_size=int(tamanhos.currentText()),
                                                                       _nome_imagem=self.nomeImagemCI.text())
                    QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Error", f"{erro}..")

        def visualizarImagem():
            if self.nomeImagemCI.text() == "" or self.nomeImagemCI.text().isspace():
                QMessageBox.warning(self.ferramentas, "Failed to display the image",
                                    "Please select the image before proceeding..")
            else:
                janelaImagem = QDialog()
                janelaImagem.setWindowIcon(QIcon("icons/imagc.png"))
                janelaImagem.setWindowTitle("View Image")
                janelaImagem.setPalette(QPalette(QColor("orange")))

                layoutJanelaImagem = QVBoxLayout()
                labelImagem = QLabel()
                labelImagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelImagem.setToolTip("Image presentation!")
                labelImagem.setPixmap(QPixmap(f"{self.nomeImagemCI.text()}").scaled(QSize(400, 400)))
                layoutJanelaImagem.addWidget(labelImagem)

                infoImage = QLabel(f"""<h3><i>Details</i></h3>
<b>Name & Location</b>: {self.nomeImagemCI.text()}<br>
<b>Scale (original)</b>: {ImagEditor().dimensaoImagem(_filename=self.nomeImagemCI.text())} px<br>
<b>Size</b>: {ImagEditor().tamanhoImagem(self.nomeImagemCI.text())}""")
                layoutJanelaImagem.addWidget(infoImage)

                _fechar = lambda: janelaImagem.destroy(True)
                botaoFechar = QPushButton("Close")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaImagem.addWidget(botaoFechar)

                janelaImagem.setLayout(layoutJanelaImagem)
                janelaImagem.show()

        spacer = QLabel("<hr>")
        layout = QFormLayout()
        layout.setSpacing(10)

        labelIntro = QLabel("<h1><i>Convert to Ico</i></h1>")
        labelIntro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelIntro)
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

        labelConverter = QLabel("<b><i>Convert to icon with different dimensions:</i></b>")
        labelConverter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelConverter)

        layoutDimensoes = QHBoxLayout()
        listaTamanhos = ['16', '32', '128', '256']
        tamanhos = QComboBox()
        tamanhos.addItems(listaTamanhos)
        tamanhos.setToolTip('Choose the size!')
        layoutDimensoes.addWidget(tamanhos)

        botaoConverter = QPushButton("Convert")
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
                QMessageBox.critical(self.ferramentas, "Error",
                                     f"Select the images before to proceed and try again..")
            else:
                nomeImagensCP.addItems(self.nomeFicheiros)

        def previsualizarImg():
            self.nomeImagensCP = nomeImagensCP.currentItem().text()
            self.dimensaoImagensCP = ImagEditor().dimensaoImagem(self.nomeImagensCP)
            self.tamanhoImagensCP = ImagEditor().tamanhoImagem(self.nomeImagensCP)
            imagem = QPixmap(self.nomeImagensCP)
            imagemLabel.setPixmap(imagem.scaled(QSize(150, 150)))
            imagemLabel.setToolTip("This is not the original dimension of the image "
                                   "has just been adapted for a preview!")
            imagemDetail.setText(f"""
<b>Name</b>: {self.nomeImagensCP.split('/')[-1]}<br>
<b>Size</b>: {self.tamanhoImagensCP}<br>
<b>Scale (original)</b>: {self.dimensaoImagensCP}""")

        def converterImagens():
            if self.nomeFicheiros is None:
                QMessageBox.critical(self.ferramentas, "Error", f"Select the images before to proceed and try again..")
                procurarImagens()
            else:
                try:
                    QMessageBox.warning(self.ferramentas, 'Warning', 'Select where to save the file..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Select where to save the file")
                    ImagEditor(_dir_salvar=dirSalvar).convertendoPdf(_images=self.nomeFicheiros)
                    QMessageBox.information(self.ferramentas, "Conclude", "Successful Operation..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Error", f"{erro}..")

        layout = QFormLayout()
        layout.setSpacing(10)
        spacer = QLabel("<hr>")

        introLabel = QLabel("<h1><i>Convert to Pdf</i></h1>")
        introLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(introLabel)
        layout.addRow(spacer)

        imagemLayout = QHBoxLayout()
        imagemLabel = QLabel("Search the image\nto preview it..")
        imagemLabel.setFixedSize(QSize(150, 150))
        imagemLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagemLabel.setStyleSheet('background-color: white; padding: 2px;')
        imagemLayout.addWidget(imagemLabel)
        imagemDetail = QLabel(f"""
<b>Name</b>: {self.nomeImagensCP}<br>
<b>Size</b>: {self.tamanhoImagensCP}<br>
<b>Scale (original)</b>: {self.dimensaoImagensCP}""")
        imagemLayout.addWidget(imagemDetail)
        layout.addRow(imagemLayout)
        layout.addRow(spacer)

        nomeImagensCP = QListWidget()
        nomeImagensCP.setAlternatingRowColors(True)
        nomeImagensCP.itemClicked.connect(previsualizarImg)
        layout.addRow(nomeImagensCP)
        layout.addRow(spacer)

        layoutBtns = QHBoxLayout()
        procurarBtn = QPushButton("Search Images")
        procurarBtn.clicked.connect(procurarImagens)
        layoutBtns.addWidget(procurarBtn)
        converterBtn = QPushButton("Convert Images")
        converterBtn.clicked.connect(converterImagens)
        layoutBtns.addWidget(converterBtn)

        layout.addRow(layoutBtns)
        self.janela4.setLayout(layout)

    def redimensionar_imagem(self):
        def procurarImagem():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select Image",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            self.nomeImagemRI.setText(nomeFicheiro)

        def redimensionar():
            if self.nomeImagemRI.text() == "" or self.nomeImagemRI.text().isspace():
                QMessageBox.critical(self.ferramentas, "Error", f"Select the image before to proceed and try again..")
                self.procurarImagem()
            else:
                try:
                    QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Select where to save the file")
                    ImagEditor(_dir_salvar=dirSalvar).redimensionarImagem(_resizer=int(divisor.currentText()) / 100,
                                                                          _nome_imagem=self.nomeImagemRI.text())
                    QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Error", f"{erro}..")

        def visualizarImagem():
            if self.nomeImagemRI.text() == "" or self.nomeImagemRI.text().isspace():
                QMessageBox.warning(self.ferramentas, "Failed to display the image",
                                    "Please select the image before to proceed..")
            else:
                janelaImagem = QDialog()
                janelaImagem.setWindowIcon(QIcon("icons/imagc.png"))
                janelaImagem.setWindowTitle("View Image")
                janelaImagem.setPalette(QPalette(QColor("orange")))

                layoutJanelaImagem = QVBoxLayout()
                labelImagem = QLabel()
                labelImagem.setAlignment(Qt.AlignCenter)
                labelImagem.setToolTip("Image presentation!")
                labelImagem.setPixmap(QPixmap(f"{self.nomeImagemRI.text()}").scaled(QSize(400, 400)))
                layoutJanelaImagem.addWidget(labelImagem)

                infoImage = QLabel(f"""<h3><i>Details</i></h3>
<b>Name</b>: {self.nomeImagemRI.text().split('/')[-1]}<br>
<b>Scale (original)</b>: {ImagEditor().dimensaoImagem(_filename=self.nomeImagemRI.text())} px<br>
<b>Size</b>: {ImagEditor().tamanhoImagem(self.nomeImagemRI.text())}""")
                layoutJanelaImagem.addWidget(infoImage)

                _fechar = lambda: janelaImagem.destroy(True)
                botaoFechar = QPushButton("Close")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaImagem.addWidget(botaoFechar)

                janelaImagem.setLayout(layoutJanelaImagem)
                janelaImagem.show()

        spacer = QLabel("<hr>")
        layout = QFormLayout()
        layout.setSpacing(10)

        labelIntro = QLabel("<h1><i>Resize Image</i></h1>")
        labelIntro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelIntro)
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

        labelConverter = QLabel("<b><i>Set the percentage to resize the image:</i></b>")
        labelConverter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelConverter)

        layoutDimensoes = QHBoxLayout()
        listaDivisor = [f'{n}' for n in range(10, 201, 30)]
        divisor = QComboBox()
        divisor.addItems(listaDivisor)
        divisor.setToolTip('Choose the percentage to be aplied!')
        layoutDimensoes.addWidget(divisor)

        botaoConverter = QPushButton("Resize")
        botaoConverter.clicked.connect(redimensionar)
        layoutDimensoes.addWidget(botaoConverter)

        layout.addRow(layoutDimensoes)
        self.janela5.setLayout(layout)

    def alterar_janela(self, index):
        self.stack.setCurrentIndex(index)
