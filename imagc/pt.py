import os
import webbrowser
from sys import exit
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from imageditor import ImagEditor, dimensaoImagem, tamanhoImagem

theme = open('themes/imagc.qss').read().strip()


# ******* portuguese-program *******
class PT:
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
        janela = QDialog(self.ferramentas)
        janela.setWindowTitle("Instruções")
        layout = QVBoxLayout()

        instr_label = QLabel("""
Olaa caro usuário!

É com muito prazer e orgulho que apresento te o ImaGC
Um programa simples e cheio de funcionalidades
Das quais a sua principal função é de editar imagens!

- Para O Adicionar O Logotipo, Ele Deve Ter O Fundo Ou Mascara Transparente;
- Para A Conversão De (.Ico) O Programa Subescreve Os Dados Binários Da Imagem
E Redefine As Dimensões Da Mesma;
- Para A Conversão De (.Gif) O Programa Copia Os Dados Das Imagens
E Cria Um Ciclo Alternado Entre Elas Com Duração De 1 Segundo Por Quadro;
- Para A Conversão De (.Pdf) O Programa Copia Igualmente A Ou As Imagens
E Cria Um Arquivo Pdf Com As Imagens Automaticamente Redimensionadas;
- Para O Redimensionamento Das Imagens, O Programa Otimiza O Tamanho Original Das Imagens
E Redimensiona De Acordo A Dimensão Que O Utilizador Deseja Reduzir Ou Aumentar;

Muito Obrigado pelo apoio!
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
        janela.setWindowTitle("Sobre")
        layout = QVBoxLayout()

        sobre_label = QLabel("""
Nome: <b>ImaGC</b><br>
Versão: <b>0.6-092021</b><br>
Programador & Designer: <b>Nurul-GC</b><br>
Empresa: <b>&trade;ArtesGC Inc.</b>""")
        sobre_label.setStyleSheet("background-color: orange;"
                                  "padding: 10px;"
                                  "border-radius: 5px;")
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
        for log in os.listdir('./Debug'):
            lista_registo.addItem(log)
        layout_registo.addWidget(lista_registo)

        registo = QTextEdit()
        registo.setReadOnly(True)
        registo.setPlaceholderText("Selecione um dos arquivos para ler o seu conteudo..")
        layout_registo.addWidget(registo)

        layout_janela_debug.addRow(layout_registo)

        _fechar = lambda: janela_debug.close()
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
            nomeImagemAL.setText(nomeFicheiro)

        def procurar_logo():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(self.ferramentas, caption="Selecione o Logotipo",
                                                                        filter="Image Files (*.png *.jpg *.jpeg)")
            nomeLogo.setText(nomeFicheiro)

        def add_logo_imagem():
            if nomeLogo.text() != "":
                QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                             caption="Selecione onde salvar o arquivo")
                ImagEditor(_dir_salvar=dirSalvar, _nome_logotipo=nomeLogo.text(),
                           _nome_imagem=nomeImagemAL.text()).addLogo()
                QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
            else:
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione o logotipo antes de continuar e tente novamente..")
                procurar_logo()

        def procurar_directorio():
            if nomeLogo.text() != "":
                nomeDirectorio = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione a Imagem")
                self.dirImagem.setText(nomeDirectorio)
                QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                             caption="Selecione onde salvar o arquivo")
                ImagEditor(_dir_salvar=dirSalvar).addLogo(_nome_logotipo=nomeLogo.text(),
                                                          _dir_imagens=dirImagem.text())
                QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
            else:
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione o logotipo antes de continuar e tente novamente..")
                procurar_logo()

        def visualizar_logo():
            if nomeLogo.text() == "" or nomeLogo.text().isspace():
                QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem",
                                    "Por favor selecione a imagem antes de prosseguir..")
            else:
                janelaLogo = QDialog()
                janelaLogo.setWindowIcon(QIcon("icons/imagc.png"))
                janelaLogo.setWindowTitle("Visualizar Logotipo")
                janelaLogo.setPalette(QPalette(QColor("orange")))

                layoutJanelaLogo = QVBoxLayout()
                labelLogo = QLabel()
                labelLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelLogo.setToolTip("Apresentação do logotipo!")
                labelLogo.setPixmap(QPixmap(f"{nomeLogo.text()}").scaled(QSize(400, 400)))
                layoutJanelaLogo.addWidget(labelLogo)

                infoImage = QLabel(f"""<h3><i>Detalhes</i></h3>
<b>Nome</b>: {nomeLogo.text().split('/')[-1]}<br>
<b>Dimensões (original)</b>: {dimensaoImagem(_filename=nomeLogo.text())} px<br>
<b>Tamanho</b>: {tamanhoImagem(nomeLogo.text())}""")
                layoutJanelaLogo.addWidget(infoImage)

                _fechar = lambda: janelaLogo.close()
                botaoFechar = QPushButton("Fechar")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaLogo.addWidget(botaoFechar)

                janelaLogo.setLayout(layoutJanelaLogo)
                janelaLogo.show()

        def visualizar_imagem():
            if nomeImagemAL.text() == "" or nomeImagemAL.text().isspace():
                QMessageBox.warning(self.ferramentas, "Falha ao apresentar a imagem",
                                    "Por favor selecione a imagem antes de prosseguir..")
            else:
                janelaImagem = QDialog(self.ferramentas)
                janelaImagem.setWindowIcon(QIcon("icons/imagc.png"))
                janelaImagem.setWindowTitle("Visualizar Imagem")
                janelaImagem.setPalette(QPalette(QColor("orange")))

                layoutJanelaImagem = QVBoxLayout()
                labelImagem = QLabel()
                labelImagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelImagem.setToolTip("Apresentação da Imagem!")
                labelImagem.setPixmap(QPixmap(f"{nomeImagemAL.text()}").scaled(QSize(400, 400)))
                layoutJanelaImagem.addWidget(labelImagem)

                infoImage = QLabel(f"""<h3><i>Detalhes</i></h3>
<b>Nome</b>: {nomeImagemAL.text().split('/')[-1]}<br>
<b>Dimensões (original)</b>: {dimensaoImagem(_filename=nomeImagemAL.text())} px<br>
<b>Tamanho</b>: {tamanhoImagem(nomeImagemAL.text())}""")
                layoutJanelaImagem.addWidget(infoImage)

                _fechar = lambda: janelaImagem.close()
                botaoFechar = QPushButton("Fechar")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaImagem.addWidget(botaoFechar)

                janelaImagem.setLayout(layoutJanelaImagem)
                janelaImagem.show()

        layout = QFormLayout()
        layout.setSpacing(10)

        label_intro = QLabel("<h1><i>Adicionar Logotipo</i></h1>")
        label_intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(label_intro)
        layout.addRow(QLabel("<hr>"))

        nomeLogo = QLineEdit()
        nomeLogo.setReadOnly(True)
        nomeLogo.setPlaceholderText("Procure pelo logotipo para obter o seu nome..")
        layout.addRow(nomeLogo)

        botao_logo = QPushButton("Procurar Logotipo")
        botao_logo.setDefault(True)
        botao_logo.clicked.connect(procurar_logo)

        botao_ver_logo = QPushButton("Visualizar Logotipo")
        botao_ver_logo.setDefault(True)
        botao_ver_logo.clicked.connect(visualizar_logo)
        layout.addRow(botao_logo, botao_ver_logo)
        layout.addRow(QLabel("<hr>"))

        nomeImagemAL = QLineEdit()
        nomeImagemAL.setReadOnly(True)
        nomeImagemAL.setPlaceholderText("Procure pela imagem para obter o seu nome..")

        nomeImagemBotao = QPushButton("Procurar Imagem")
        nomeImagemBotao.setDefault(True)
        nomeImagemBotao.clicked.connect(procurar_imagem)
        layout.addRow(nomeImagemBotao, nomeImagemAL)

        botao_ver_imagem = QPushButton("Visualizar Imagem")
        botao_ver_imagem.setDefault(True)
        botao_ver_imagem.clicked.connect(visualizar_imagem)

        botao_add_logo_imagem = QPushButton("Adicionar Logotipo a Imagem")
        botao_add_logo_imagem.setDefault(True)
        botao_add_logo_imagem.clicked.connect(add_logo_imagem)
        layout.addRow(botao_ver_imagem, botao_add_logo_imagem)
        layout.addRow(QLabel("<hr>"))

        dirImagem = QLineEdit()
        dirImagem.setReadOnly(True)
        dirImagem.setPlaceholderText("Localize o diretório contendo as imagens..")
        layout.addRow(dirImagem)

        dir_imagem_botao = QPushButton("Localizar Directório")
        dir_imagem_botao.setDefault(True)
        dir_imagem_botao.setToolTip("o logotipo sera adicionado as imagens automaticamente!")
        dir_imagem_botao.clicked.connect(procurar_directorio)
        layout.addRow(dir_imagem_botao)

        self.janela1.setLayout(layout)

    def converter_gif(self):
        def procurar_imagens():
            nomeImagensCG.clear()
            self.nomeFicheiros, filtroFicheiros = QFileDialog.getOpenFileNames(self.ferramentas,
                                                                               caption="Selecione a Imagem",
                                                                               filter="Image Files (*.png *.jpg *.jpeg)")
            if len(self.nomeFicheiros) < 2:
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione as imagens antes de continuar e tente novamente..")
            else:
                nomeImagensCG.addItems(self.nomeFicheiros)

        def previsualizar_img():
            dimensaoImagensCG = dimensaoImagem(nomeImagensCG.currentItem().text())
            tamanhoImagensCG = tamanhoImagem(nomeImagensCG.currentItem().text())
            imagem = QPixmap(nomeImagensCG.currentItem().text())
            imagem_label.setPixmap(imagem.scaled(QSize(150, 150)))
            imagem_label.setToolTip("Está não é a dimensão original da imagem "
                                    "apenas foi adaptada para uma pré-visualização!")
            imagem_detail.setText(f"""
<b>Nome</b>: {nomeImagensCG.currentItem().text().split('/')[-1]}<br>
<b>Tamanho</b>: {tamanhoImagensCG}<br>
<b>Dimensões (original)</b>: {dimensaoImagensCG}
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

        layout = QFormLayout()
        layout.setSpacing(10)
        spacer = QLabel("<hr>")

        intro_label = QLabel("<h1><i>Converter para Gif</i></h1>")
        intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(intro_label)
        layout.addRow(spacer)

        imagem_layout = QHBoxLayout()
        imagem_label = QLabel("Procure pela imagem\npara puder\nprevisualiza-la..")
        imagem_label.setFixedSize(QSize(150, 150))
        imagem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagem_label.setStyleSheet('background-color: white; padding: 2px;')
        imagem_layout.addWidget(imagem_label)
        imagem_detail = QLabel(f"""
<b>Nome</b>: None<br>
<b>Tamanho</b>: None<br>
<b>Dimensões (original)</b>: None""")
        imagem_layout.addWidget(imagem_detail)
        layout.addRow(imagem_layout)
        layout.addRow(spacer)

        labelConverter = QLabel("<b><i>Procure pelas imagens para obter os seus nomes</i></b>")
        labelConverter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelConverter)

        nomeImagensCG = QListWidget()
        nomeImagensCG.setAlternatingRowColors(True)
        nomeImagensCG.itemClicked.connect(previsualizar_img)
        layout.addRow(nomeImagensCG)
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
            nomeImagemCI.setText(nomeFicheiro)
            previsualizar_img()

        def previsualizar_img():
            dimensaoImagensCI = dimensaoImagem(nomeImagemCI.text())
            tamanhoImagensCI = tamanhoImagem(nomeImagemCI.text())
            imagem = QPixmap(nomeImagemCI.text())
            imagem_label.setPixmap(imagem.scaled(QSize(150, 150)))
            imagem_label.setToolTip("Esta não é a dimensão original da imagem "
                                    "apenas foi adaptada para previsualização!")
            imagem_detail.setText(f"""
<b>Nome</b>: {nomeImagemCI.text().split('/')[-1]}<br>
<b>Tamanho</b>: {tamanhoImagensCI}<br>
<b>Dimensões (original)</b>: {dimensaoImagensCI}pxs""")

        def converter():
            if nomeImagemCI.text() == "" or nomeImagemCI.text().isspace():
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione a imagem antes de continuar e tente novamente..")
                self.procurarImagem()
            else:
                try:
                    QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Selecione onde salvar o arquivo")
                    ImagEditor(_dir_salvar=dirSalvar).convertendoIcone(_size=int(tamanhos.currentText()),
                                                                       _nome_imagem=nomeImagemCI.text())
                    QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"{erro}..")

        layout = QFormLayout()
        layout.setSpacing(10)

        labelIntro = QLabel("<h1><i>Converter para Ico</i></h1>")
        labelIntro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelIntro)
        layout.addRow(QLabel("<hr>"))

        imagem_layout = QHBoxLayout()
        imagem_label = QLabel("Procure pela imagem\npara puder\nprevisualiza-la..")
        imagem_label.setFixedSize(QSize(150, 150))
        imagem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagem_label.setStyleSheet("background-color: white; padding: 2px;")
        imagem_layout.addWidget(imagem_label)
        imagem_detail = QLabel(f"""
<b>Nome</b>: None<br>
<b>Tamanho</b>: None<br>
<b>Dimensões (original)</b>: None""")
        imagem_layout.addWidget(imagem_detail)
        layout.addRow(imagem_layout)

        nomeImagemCI = QLineEdit()
        nomeImagemCI.setReadOnly(True)
        nomeImagemCI.setPlaceholderText("Procure pela imagem para obter o seu nome..")

        botaoIco = QPushButton("Procurar Imagem")
        botaoIco.clicked.connect(procurarImagem)
        layout.addRow(botaoIco, nomeImagemCI)
        layout.addRow(QLabel("<hr>"))

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
            dimensaoImagensCP = dimensaoImagem(nomeImagensCP.currentItem().text())
            tamanhoImagensCP = tamanhoImagem(nomeImagensCP.currentItem().text())
            imagem = QPixmap(nomeImagensCP.currentItem().text())
            imagemLabel.setPixmap(imagem.scaled(QSize(150, 150)))
            imagemLabel.setToolTip("Esta não é a dimensão original da imagem "
                                   "apenas foi adaptada para uma previsualização!")
            imagemDetail.setText(f"""
<b>Nome</b>: {nomeImagensCP.currentItem().text().split('/')[-1]}<br>
<b>Tamanho</b>: {tamanhoImagensCP}<br>
<b>Dimensões (original)</b>: {dimensaoImagensCP}""")

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

        introLabel = QLabel("<h1><i>Converter para Pdf</i></h1>")
        introLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(introLabel)
        layout.addRow(QLabel("<hr>"))

        imagemLayout = QHBoxLayout()
        imagemLabel = QLabel("Pesquise a imagem\npara puder\nprevisualiza-la..")
        imagemLabel.setFixedSize(QSize(150, 150))
        imagemLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagemLabel.setStyleSheet('background-color: white; padding: 2px;')
        imagemLayout.addWidget(imagemLabel)
        imagemDetail = QLabel(f"""
<b>Nome</b>: None<br>
<b>Tamanho</b>: None<br>
<b>Dimensões (original)</b>: None""")
        imagemLayout.addWidget(imagemDetail)
        layout.addRow(imagemLayout)

        labelConverter = QLabel("<b><i>Procure pelas imagens para obter os seus nomes</i></b>")
        labelConverter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelConverter)

        nomeImagensCP = QListWidget()
        nomeImagensCP.setAlternatingRowColors(True)
        nomeImagensCP.setToolTip("Aqui serão apresentados os nomes das imagens!")
        nomeImagensCP.itemClicked.connect(previsualizarImg)
        layout.addRow(nomeImagensCP)
        layout.addRow(QLabel("<hr>"))

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
            previsualizarImg()

        def previsualizarImg():
            dimensaoImagemRI = dimensaoImagem(nomeImagemRI.text())
            tamanhoImagemRI = tamanhoImagem(nomeImagemRI.text())
            imagem = QPixmap(nomeImagemRI.text())
            imagemLabel.setPixmap(imagem.scaled(QSize(150, 150)))
            imagemLabel.setToolTip("Esta não é dimensão original da imagem "
                                   "apenas foi adaptada para uma previsualização!")
            imagemDetail.setText(f"""
<b>Nome</b>: {nomeImagemRI.text().split('/')[-1]}<br>
<b>Tamanho</b>: {tamanhoImagemRI}<br>
<b>Dimensões (original)</b>: {dimensaoImagemRI}pxs""")

        def redimensionar():
            if nomeImagemRI.text() == "" or nomeImagemRI.text().isspace():
                QMessageBox.critical(self.ferramentas, "Erro",
                                     f"Selecione a imagem antes de continuar e tente novamente..")
                self.procurarImagem()
            else:
                try:
                    QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione onde salvar o arquivo..')
                    dirSalvar = QFileDialog.getExistingDirectory(self.ferramentas,
                                                                 caption="Selecione onde salvar o arquivo")
                    ImagEditor(_dir_salvar=dirSalvar).redimensionarImagem(_resizer=int(divisor.currentText()) / 100,
                                                                          _nome_imagem=nomeImagemRI.text())
                    QMessageBox.information(self.ferramentas, "Concluido", "Operação bem Sucedida..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"{erro}..")

        layout = QFormLayout()
        layout.setSpacing(10)

        labelIntro = QLabel("<h1><i>Redimensionar Imagem</i></h1>")
        labelIntro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelIntro)
        layout.addRow(QLabel("<hr>"))

        imagemLayout = QHBoxLayout()
        imagemLabel = QLabel("Procure pela imagem\npara puder\nprevisualiza-la..")
        imagemLabel.setFixedSize(QSize(150, 150))
        imagemLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagemLabel.setStyleSheet('background-color: white; padding: 2px;')
        imagemLayout.addWidget(imagemLabel)
        imagemDetail = QLabel(f"""
<b>Nome</b>: None<br>
<b>Tamanho</b>: None<br>
<b>Dimensões (original)</b>: None""")
        imagemLayout.addWidget(imagemDetail)
        layout.addRow(imagemLayout)

        nomeImagemRI = QLineEdit()
        nomeImagemRI.setReadOnly(True)
        nomeImagemRI.setPlaceholderText("Procure pela imagem para obter o seu nome..")

        botaoIco = QPushButton("Procurar Imagem")
        botaoIco.clicked.connect(procurarImagem)
        layout.addRow(botaoIco, nomeImagemRI)
        layout.addRow(QLabel("<hr>"))

        labelConverter = QLabel("<b><i>Defina a percentagem para redimensionar a imagem:</i></b>")
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
