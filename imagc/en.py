import os
import webbrowser
from configparser import ConfigParser
from sys import exit
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from imageditor import ImagEditor, dimensaoImagem, tamanhoImagem

theme = open('themes/imagc.qss').read().strip()


class EN:
    """english-program"""

    def __init__(self):
        # ******* layout-principal *******
        layout_principal = QVBoxLayout()

        self.ferramentas = QDialog()
        self.ferramentas.setFixedSize(QSize(800, 550))
        self.ferramentas.setWindowTitle("ImaGC")
        self.ferramentas.setWindowIcon(QIcon("icons/favicon-192x192.png"))
        self.ferramentas.setStyleSheet(theme)

        # ******* background-image *******
        bg_image = QImage("icons/bg.jpg")
        set_bg_image = bg_image.scaled(QSize(800, 550))  # resize Image to widget's size
        palette = QPalette()
        palette.setBrush(palette.ColorGroup.All, palette.ColorRole.Window, QBrush(set_bg_image))
        self.ferramentas.setPalette(palette)

        # ******* global-vars *******
        self.nomeFicheiros = None

        # ******* menu *******
        menu = QMenuBar()
        layout_principal.setMenuBar(menu)

        hlp = menu.addMenu("Help")
        conf = hlp.addAction("Configurations")
        conf.triggered.connect(self._conf)
        hlp.addSeparator()

        instr = hlp.addAction("Instructions")
        instr.triggered.connect(self._instr)
        hlp.addSeparator()

        debug = hlp.addAction("Log errors")
        debug.triggered.connect(self._debug)
        hlp.addSeparator()

        _sair = lambda: exit(0)
        sair = hlp.addAction("Quit")
        sair.triggered.connect(_sair)

        menu.addSeparator()
        sobre = menu.addAction("About")
        sobre.triggered.connect(self._sobre)

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
    def _conf(self):
        def alterar():
            try:
                config = ConfigParser()
                if escolha_idioma.currentText() == 'Portugues':
                    config['MAIN'] = {'lang': escolha_idioma.currentText()}
                elif escolha_idioma.currentText() == 'English':
                    config['MAIN'] = {'lang': escolha_idioma.currentText()}
                with open('imagc.ini', 'w') as INIFILE:
                    config.write(INIFILE)
                QMessageBox.information(self.ferramentas, 'Successsful', 'The language set will be loaded after restart the program!')
                janela.close()
            except Exception as erro:
                QMessageBox.warning(self.ferramentas, 'Warning', f'While processing your request the following error was found:\n- {erro}')

        janela = QDialog(self.ferramentas)
        janela.setWindowTitle('ImaGC')
        janela.setFixedSize(QSize(300, 150))
        janela.setWindowIcon(QIcon('icons/favicon-192x192.png'))
        layout = QVBoxLayout()

        labelInfo = QLabel('<h3>Choose the language:</h3>')
        layout.addWidget(labelInfo)

        idiomas = ['Portugues', 'English']
        escolha_idioma = QComboBox()
        escolha_idioma.addItems(idiomas)
        layout.addWidget(escolha_idioma)

        btnSalvar = QPushButton('Save')
        btnSalvar.clicked.connect(alterar)
        layout.addWidget(btnSalvar)

        janela.setLayout(layout)
        janela.show()

    def _instr(self):
        janela = QDialog(self.ferramentas)
        janela.setWindowTitle("Instructions")
        layout = QVBoxLayout()

        instr_label = QLabel("""
Hello dear user!

It's with great pleasure and pride that I present the ImaGC to you
A simple and full of features program
Of which its main function is to edit images!

- To Add The Logo, It Must Have A Transparent Background Or A Transparent Mask;
- For The Conversion To (.Ico) The Program Edit The Binary Data Of The Image
And Redefines Its Dimensions;
- For The Conversion Of (.Gif) The Program Copies The Data From The Images
And Creates An Alternate Cycle Between Them With Duration Of 1 Second Per Frame;
- For The Conversion Of (.Pdf) The Program Also Copies The Image(s)
And Creates A Pdf File With Automatically Resized Images;
- For Image Resizing, The Program Optimizes The Original Size Of Images
And Resize According To The Dimension That The User Wishes To Reduce Or Increase;

Thank you very much for your support!
© 2021 Nurul GC
™ ArtesGC Inc""")
        instr_label.setStyleSheet("background-color: orange;"
                                  "padding: 10px;"
                                  "border-radius: 5px;")
        layout.addWidget(instr_label)

        _fechar = lambda: janela.close()
        fechar_btn = QPushButton('Ok')
        fechar_btn.clicked.connect(_fechar)
        layout.addWidget(fechar_btn)

        janela.setLayout(layout)
        janela.show()

    def _sobre(self):
        janela = QDialog(self.ferramentas)
        janela.setWindowTitle("About")
        layout = QVBoxLayout()

        sobre_label = QLabel("""
Name: <b>ImaGC</b><br>
Version: <b>0.7-102021</b><br>
Programmer & Designer: <b>Nurul-GC</b><br>
Company: <b>&trade;ArtesGC Inc.</b>""")
        sobre_label.setStyleSheet("background-color: orange;"
                                  "padding: 10px;"
                                  "border-radius: 5px;")
        layout.addWidget(sobre_label)

        _fechar = lambda: janela.close()
        fechar_btn = QPushButton('Ok')
        fechar_btn.clicked.connect(_fechar)
        layout.addWidget(fechar_btn)

        janela.setLayout(layout)
        janela.show()

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
        for log in os.listdir('./Debug'):
            lista_registo.addItem(log)
        layout_registo.addWidget(lista_registo)

        registo = QTextEdit()
        registo.setReadOnly(True)
        registo.setPlaceholderText("Choose one file to read its content..")
        layout_registo.addWidget(registo)

        layout_janela_debug.addRow(layout_registo)

        _fechar = lambda: janela_debug.close()
        botao_fechar = QPushButton("Close")
        botao_fechar.setDefault(True)
        botao_fechar.clicked.connect(_fechar)
        layout_janela_debug.addWidget(botao_fechar)

        janela_debug.setLayout(layout_janela_debug)
        janela_debug.show()

    # ******* windows *******
    def adicionar_logo(self):
        def procurar_imagem():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select the Image",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            nomeImagemAL.setText(nomeFicheiro)

        def procurar_logo():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select the Logo",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            nomeLogo.setText(nomeFicheiro)

        def add_logo_imagem():
            if nomeLogo.text() != "":
                QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select where to save the file")
                ImagEditor(_dir_salvar=dirSalvar).addLogo(_nome_logotipo=nomeLogo.text(),
                                                          _nome_imagem=nomeImagemAL.text())
                QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
            else:
                QMessageBox.critical(self.ferramentas, "Error", "Select the logo before to proceed and try again..")
                procurar_logo()

        def procurar_directorio():
            if nomeLogo.text() != "":
                nomeDirectorio = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select the Image")
                dirImagem.setText(nomeDirectorio)
                QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas, caption="Select where to save the file")
                ImagEditor(_dir_salvar=dirSalvar).addLogo(_nome_logotipo=nomeLogo.text(),
                                                          _dir_imagens=dirImagem.text())
                QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
            else:
                QMessageBox.critical(self.ferramentas, "Error", "Select the logo before to proceed and try again..")
                procurar_logo()

        def visualizar_logo():
            if nomeLogo.text() == "" or nomeLogo.text().isspace():
                QMessageBox.warning(self.ferramentas, "Failed to display the image",
                                    "Please select the image before to proceed..")
            else:
                janelaLogo = QDialog(self.ferramentas)
                janelaLogo.setWindowTitle("View Logo")
                janelaLogo.setPalette(QPalette(QColor("orange")))

                layoutJanelaLogo = QVBoxLayout()
                labelLogo = QLabel()
                labelLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelLogo.setToolTip("Logo presentation!")
                labelLogo.setPixmap(QPixmap(f"{nomeLogo.text()}").scaled(QSize(400, 400)))
                layoutJanelaLogo.addWidget(labelLogo)

                infoImage = QLabel(f"""<h3><i>Details</i></h3>
<b>Name</b>: {nomeLogo.text().split('/')[-1]}<br>
<b>Scale (original)</b>: {dimensaoImagem(_filename=nomeLogo.text())}pxs<br>
<b>Size</b>: {tamanhoImagem(nomeLogo.text())}""")
                layoutJanelaLogo.addWidget(infoImage)

                _fechar = lambda: janelaLogo.close()
                botaoFechar = QPushButton("Close")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaLogo.addWidget(botaoFechar)

                janelaLogo.setLayout(layoutJanelaLogo)
                janelaLogo.show()

        def visualizar_imagem():
            if nomeImagemAL.text() == "" or nomeImagemAL.text().isspace():
                QMessageBox.warning(self.ferramentas, "Failed to display the image",
                                    "Please select the image before to proceed..")
            else:
                janelaImagem = QDialog(self.ferramentas)
                janelaImagem.setWindowTitle("View Image")
                janelaImagem.setPalette(QPalette(QColor("orange")))

                layoutJanelaImagem = QVBoxLayout()
                labelImagem = QLabel()
                labelImagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelImagem.setToolTip("Image presentation!")
                labelImagem.setPixmap(QPixmap(f"{nomeImagemAL.text()}").scaled(QSize(400, 400)))
                layoutJanelaImagem.addWidget(labelImagem)

                infoImage = QLabel(f"""<h3><i>Details</i></h3>
<b>Name</b>: {nomeImagemAL.text().split('/')[-1]}<br>
<b>Scale (original)</b>: {dimensaoImagem(_filename=nomeImagemAL.text())}pxs<br>
<b>Size</b>: {tamanhoImagem(nomeImagemAL.text())}""")
                layoutJanelaImagem.addWidget(infoImage)

                _fechar = lambda: janelaImagem.close()
                botaoFechar = QPushButton("Close")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaImagem.addWidget(botaoFechar)

                janelaImagem.setLayout(layoutJanelaImagem)
                janelaImagem.show()

        layout = QFormLayout()
        layout.setSpacing(10)

        label_intro = QLabel("<h1><i>Add Logo</i></h1>")
        label_intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(label_intro)
        layout.addRow(QLabel("<hr>"))

        nomeLogo = QLineEdit()
        nomeLogo.setReadOnly(True)
        nomeLogo.setPlaceholderText("Search the logo to provide its name..")
        layout.addRow(nomeLogo)

        botao_logo = QPushButton("Search Logo")
        botao_logo.setDefault(True)
        botao_logo.clicked.connect(procurar_logo)

        botao_ver_logo = QPushButton("View Logo")
        botao_ver_logo.setDefault(True)
        botao_ver_logo.clicked.connect(visualizar_logo)
        layout.addRow(botao_logo, botao_ver_logo)
        layout.addRow(QLabel("<hr>"))

        nomeImagemAL = QLineEdit()
        nomeImagemAL.setReadOnly(True)
        nomeImagemAL.setPlaceholderText("Search the image to provide its name..")

        nomeImagemBotao = QPushButton("Search Image")
        nomeImagemBotao.clicked.connect(procurar_imagem)
        layout.addRow(nomeImagemBotao, nomeImagemAL)

        botao_ver_imagem = QPushButton("View Image")
        botao_ver_imagem.setDefault(True)
        botao_ver_imagem.clicked.connect(visualizar_imagem)

        botao_add_logo_imagem = QPushButton("Add Logo to Image")
        botao_add_logo_imagem.setDefault(True)
        botao_add_logo_imagem.clicked.connect(add_logo_imagem)
        layout.addRow(botao_ver_imagem, botao_add_logo_imagem)
        layout.addRow(QLabel("<hr>"))

        dirImagem = QLineEdit()
        dirImagem.setReadOnly(True)
        dirImagem.setPlaceholderText("Find the directory containing the images..")
        layout.addRow(dirImagem)

        dir_imagem_botao = QPushButton("Find Directory")
        dir_imagem_botao.setDefault(True)
        dir_imagem_botao.setToolTip("the logo will be added to the images automatically!")
        dir_imagem_botao.clicked.connect(procurar_directorio)
        layout.addRow(dir_imagem_botao)

        self.janela1.setLayout(layout)

    def converter_gif(self):
        def procurar_imagens():
            nomeImagensCG.clear()
            self.nomeFicheiros, filtroFicheiros = QFileDialog.getOpenFileNames(self.ferramentas,
                                                                               caption="Select the Image",
                                                                               filter="Image Files (*.png *.jpg *.jpeg)")
            if len(self.nomeFicheiros) < 2:
                QMessageBox.critical(self.ferramentas, "Error",
                                     "Select the images before to proceed and try again..")
            else:
                nomeImagensCG.addItems(self.nomeFicheiros)

        def previsualizar_img():
            dimensaoImagensCG = dimensaoImagem(nomeImagensCG.currentItem().text())
            tamanhoImagensCG = tamanhoImagem(nomeImagensCG.currentItem().text())
            imagem = QPixmap(nomeImagensCG.currentItem().text())
            imagem_label.setPixmap(imagem.scaled(QSize(150, 150)))
            imagem_label.setToolTip("This is not the original dimension of the image "
                                    "has just been adapted for a preview!")
            imagem_detail.setText(f"""
<b>Name</b>: {nomeImagensCG.currentItem().text().split('/')[-1]}<br>
<b>Size</b>: {tamanhoImagensCG}<br>
<b>Scale (original)</b>: {dimensaoImagensCG}
""")

        def converter_imagens():
            if self.nomeFicheiros is None:
                QMessageBox.critical(self.ferramentas, "Error", "Select the images before to proceed and try again..")
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

        layout = QFormLayout()
        layout.setSpacing(10)

        intro_label = QLabel("<h1><i>Convert to Gif</i></h1>")
        intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(intro_label)
        layout.addRow(QLabel("<hr>"))

        imagem_layout = QHBoxLayout()
        imagem_label = QLabel("Search the image\nto preview it..")
        imagem_label.setFixedSize(QSize(150, 150))
        imagem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagem_label.setStyleSheet("background-color: white; padding: 2px;")
        imagem_layout.addWidget(imagem_label)
        imagem_detail = QLabel("""
<b>Name</b>: None<br>
<b>Size</b>: None<br>
<b>Scale (original)</b>: None""")
        imagem_layout.addWidget(imagem_detail)
        layout.addRow(imagem_layout)

        labelConverter = QLabel("<b><i>Search the images to provide their names</i></b>")
        labelConverter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelConverter)

        nomeImagensCG = QListWidget()
        nomeImagensCG.setAlternatingRowColors(True)
        nomeImagensCG.setToolTip("Here will be shown the name of the images!")
        nomeImagensCG.itemClicked.connect(previsualizar_img)
        layout.addRow(nomeImagensCG)
        layout.addRow(QLabel("<hr>"))

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
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select the Image",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            nomeImagemCI.setText(nomeFicheiro)
            previsualizar_img()

        def previsualizar_img():
            dimensaoImagensCI = dimensaoImagem(nomeImagemCI.text())
            tamanhoImagensCI = tamanhoImagem(nomeImagemCI.text())
            imagem = QPixmap(nomeImagemCI.text())
            imagem_label.setPixmap(imagem.scaled(QSize(150, 150)))
            imagem_label.setToolTip("This is not the original dimension of the image "
                                    "has just been adapted for a preview!")
            imagem_detail.setText(f"""
<b>Name</b>: {nomeImagemCI.text().split('/')[-1]}<br>
<b>Size</b>: {tamanhoImagensCI}<br>
<b>Scale (original)</b>: {dimensaoImagensCI}pxs""")

        def converter():
            if nomeImagemCI.text() == "" or nomeImagemCI.text().isspace():
                QMessageBox.critical(self.ferramentas, "Error", "Select the image before to proceed and try again..")
                procurarImagem()
            else:
                try:
                    QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Select where to save the file")
                    ImagEditor(_dir_salvar=dirSalvar).convertendoIcone(_size=int(tamanhos.currentText()),
                                                                       _nome_imagem=nomeImagemCI.text())
                    QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Error", f"{erro}..")

        layout = QFormLayout()
        layout.setSpacing(10)

        labelIntro = QLabel("<h1><i>Convert to Ico</i></h1>")
        labelIntro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelIntro)
        layout.addRow(QLabel("<hr>"))

        imagem_layout = QHBoxLayout()
        imagem_label = QLabel("Search the image\nto preview it..")
        imagem_label.setFixedSize(QSize(150, 150))
        imagem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagem_label.setStyleSheet("background-color: white; padding: 2px;")
        imagem_layout.addWidget(imagem_label)
        imagem_detail = QLabel("""
<b>Name</b>: None<br>
<b>Size</b>: None<br>
<b>Scale (original)</b>: None""")
        imagem_layout.addWidget(imagem_detail)
        layout.addRow(imagem_layout)

        nomeImagemCI = QLineEdit()
        nomeImagemCI.setReadOnly(True)
        nomeImagemCI.setPlaceholderText('Search the image to provide its name..')

        botaoIco = QPushButton("Search Image")
        botaoIco.clicked.connect(procurarImagem)
        layout.addRow(botaoIco, nomeImagemCI)
        layout.addRow(QLabel("<hr>"))

        labelConverter = QLabel("<b><i>Convert to icon with different dimensions</i></b>")
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
                                                                               caption="Select the Image",
                                                                               filter="Image Files (*.png *.jpg *.jpeg)")
            if len(self.nomeFicheiros) < 1:
                QMessageBox.critical(self.ferramentas, "Error",
                                     "Select the images before to proceed and try again..")
            else:
                nomeImagensCP.addItems(self.nomeFicheiros)

        def previsualizarImg():
            dimensaoImagensCP = dimensaoImagem(nomeImagensCP.currentItem().text())
            tamanhoImagensCP = tamanhoImagem(nomeImagensCP.currentItem().text())
            imagem = QPixmap(nomeImagensCP.currentItem().text())
            imagemLabel.setPixmap(imagem.scaled(QSize(150, 150)))
            imagemLabel.setToolTip("This is not the original dimension of the image "
                                   "has just been adapted for a preview!")
            imagemDetail.setText(f"""
<b>Name</b>: {nomeImagensCP.currentItem().text().split('/')[-1]}<br>
<b>Size</b>: {tamanhoImagensCP}<br>
<b>Scale (original)</b>: {dimensaoImagensCP}pxs""")

        def converterImagens():
            if self.nomeFicheiros is None:
                QMessageBox.critical(self.ferramentas, "Error", "Select the images before to proceed and try again..")
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

        introLabel = QLabel("<h1><i>Convert to Pdf</i></h1>")
        introLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(introLabel)
        layout.addRow(QLabel("<hr>"))

        imagemLayout = QHBoxLayout()
        imagemLabel = QLabel("Search the image\nto preview it..")
        imagemLabel.setFixedSize(QSize(150, 150))
        imagemLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagemLabel.setStyleSheet('background-color: white; padding: 2px;')
        imagemLayout.addWidget(imagemLabel)
        imagemDetail = QLabel("""
<b>Name</b>: None<br>
<b>Size</b>: None<br>
<b>Scale (original)</b>: None""")
        imagemLayout.addWidget(imagemDetail)
        layout.addRow(imagemLayout)

        labelConverter = QLabel("<b><i>Search the images to provide their names</i></b>")
        labelConverter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelConverter)

        nomeImagensCP = QListWidget()
        nomeImagensCP.setAlternatingRowColors(True)
        nomeImagensCP.setToolTip("Here will be shown the name of the images!")
        nomeImagensCP.itemClicked.connect(previsualizarImg)
        layout.addRow(nomeImagensCP)
        layout.addRow(QLabel("<hr>"))

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
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Select the Image",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            nomeImagemRI.setText(nomeFicheiro)
            previsualizarImg()

        def previsualizarImg():
            dimensaoImagemRI = dimensaoImagem(nomeImagemRI.text())
            tamanhoImagemRI = tamanhoImagem(nomeImagemRI.text())
            imagem = QPixmap(nomeImagemRI.text())
            imagemLabel.setPixmap(imagem.scaled(QSize(150, 150)))
            imagemLabel.setToolTip("This is not the original dimension of the image "
                                   "has just been adapted for a preview!")
            imagemDetail.setText(f"""
<b>Name</b>: {nomeImagemRI.text().split('/')[-1]}<br>
<b>Size</b>: {tamanhoImagemRI}<br>
<b>Scale (original)</b>: {dimensaoImagemRI}pxs""")

        def redimensionar():
            if nomeImagemRI.text() == "" or nomeImagemRI.text().isspace():
                QMessageBox.critical(self.ferramentas, "Error", "Select the image before to proceed and try again..")
                procurarImagem()
            else:
                try:
                    QMessageBox.information(self.ferramentas, 'Warning', 'Select where to save the file..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Select where to save the file")
                    ImagEditor(_dir_salvar=dirSalvar).redimensionarImagem(_resizer=int(divisor.currentText()) / 100,
                                                                          _nome_imagem=nomeImagemRI.text())
                    QMessageBox.information(self.ferramentas, "Conclude", "Successful operation..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Error", f"{erro}..")

        layout = QFormLayout()
        layout.setSpacing(10)

        labelIntro = QLabel("<h1><i>Resize Image</i></h1>")
        labelIntro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelIntro)
        layout.addRow(QLabel("<hr>"))

        imagemLayout = QHBoxLayout()
        imagemLabel = QLabel("Search the image\nto preview it..")
        imagemLabel.setFixedSize(QSize(150, 150))
        imagemLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagemLabel.setStyleSheet('background-color: white; padding: 2px;')
        imagemLayout.addWidget(imagemLabel)
        imagemDetail = QLabel("""
<b>Name</b>: None<br>
<b>Size</b>: None<br>
<b>Scale (original)</b>: None""")
        imagemLayout.addWidget(imagemDetail)
        layout.addRow(imagemLayout)

        nomeImagemRI = QLineEdit()
        nomeImagemRI.setReadOnly(True)
        nomeImagemRI.setPlaceholderText('Search the image to provide its name..')

        botaoIco = QPushButton("Search Image")
        botaoIco.clicked.connect(procurarImagem)
        layout.addRow(botaoIco, nomeImagemRI)
        layout.addRow(QLabel("<hr>"))

        labelConverter = QLabel("<b><i>Set the percentage to resize the image</i></b>")
        labelConverter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelConverter)

        layoutDimensoes = QHBoxLayout()
        listaDivisor = [f'{n}' for n in range(10, 201, 30)]
        divisor = QComboBox()
        divisor.addItems(listaDivisor)
        divisor.setToolTip('Choose the percentage that would be aplied! (original_scale/percentage)')
        layoutDimensoes.addWidget(divisor)

        botaoConverter = QPushButton("Resize")
        botaoConverter.clicked.connect(redimensionar)
        layoutDimensoes.addWidget(botaoConverter)

        layout.addRow(layoutDimensoes)
        self.janela5.setLayout(layout)

    def alterar_janela(self, index):
        self.stack.setCurrentIndex(index)
