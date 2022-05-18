# ******************************************************************************
#  (c) 2020-2021 Nurul-GC.                                                     *
# ******************************************************************************

import os
import webbrowser
from configparser import ConfigParser
from sys import exit
from time import time

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from imagc.ie import debugpath, dimensao_imagem, ImagEditor, tamanho_imagem

theme = open(f'{os.path.abspath(os.curdir)}/ima-themes/imagc.qss').read().strip()


class PT:
    """portuguese-program"""

    def __init__(self):
        # ******* layout-principal *******
        layout_principal = QVBoxLayout()

        self.ferramentas = QDialog()
        self.ferramentas.setFixedSize(QSize(800, 620))
        self.ferramentas.setWindowTitle("ImaGC")
        self.ferramentas.setWindowIcon(QIcon(f"{os.path.abspath(os.curdir)}/ima-icons/favicon-192x192.png"))
        self.ferramentas.setStyleSheet(theme)

        # ******* background-image *******
        bg_image = QImage(f"{os.path.abspath(os.curdir)}/ima-icons/bg.jpg")
        set_bg_image = bg_image.scaled(QSize(800, 620))  # resize Image to widget's size
        palette = QPalette()
        palette.setBrush(palette.ColorGroup.All, palette.ColorRole.Window, QBrush(set_bg_image))
        self.ferramentas.setPalette(palette)

        # ******* global-vars *******
        self.nomeFicheiros = None

        # ******* menu *******
        menu = QMenuBar()
        layout_principal.setMenuBar(menu)

        hlp = menu.addMenu("Ajuda")
        conf = hlp.addAction("Idioma")
        conf.triggered.connect(self._conf)

        instr = hlp.addAction("Instruções")
        instr.triggered.connect(self._instr)
        hlp.addSeparator()

        debug = hlp.addAction("Registo de erros")
        debug.triggered.connect(self._janeladebug)
        hlp.addSeparator()

        _sair = lambda: exit(0)
        sair = hlp.addAction("Sair")
        sair.triggered.connect(_sair)

        menu.addSeparator()
        sobre = menu.addAction("Sobre")
        sobre.triggered.connect(self._sobre)

        # ******* list-options *******
        self.listaJanelas = QListWidget(self.ferramentas)
        self.listaJanelas.setAlternatingRowColors(True)
        self.listaJanelas.setFixedSize(QSize(200, 100))
        self.listaJanelas.addItem("Adicionar Logotipo")
        self.listaJanelas.addItem("Converter para Gif")
        self.listaJanelas.addItem("Converter para Ico")
        self.listaJanelas.addItem("Converter para Pdf")

        # ******* init-windows *******
        self.janela1 = QWidget()
        self.adicionar_logo()

        self.janela2 = QWidget()
        self.converter_gif()

        self.janela3 = QWidget()
        self.converter_ico()

        self.janela4 = QWidget()
        self.converter_pdf()

        # ******* stack *******
        self.stack = QStackedWidget(self.ferramentas)
        self.stack.addWidget(self.janela1)
        self.stack.addWidget(self.janela2)
        self.stack.addWidget(self.janela3)
        self.stack.addWidget(self.janela4)

        # ******* layout-janelas *******
        hbox = QHBoxLayout()
        hbox.addWidget(self.listaJanelas)
        hbox.addWidget(self.stack)
        layout_principal.addLayout(hbox)

        # ******* label-copyright *******
        browser = lambda: webbrowser.open('https://artesgc.home.blog')
        labelCopyright = QLabel("<hr><a href='#' style='text-decoration:none;'>ArtesGC Inc.</a>")
        labelCopyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        labelCopyright.setToolTip('Acesso a pagina oficial da ArtesGC!')
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
                with open(f'{debugpath()}/imagc.ini', 'w') as INIFILE:
                    config.write(INIFILE)
                QMessageBox.information(self.ferramentas, 'Sucessso', 'O idioma definido será carregado após o reinício do programa!')
                janela.close()
            except Exception as erro:
                QMessageBox.warning(self.ferramentas, 'Aviso', f'Enquanto processava o seu pedido, o seguinte erro foi encontrado:\n- {erro}')

        janela = QDialog(self.ferramentas)
        janela.setWindowTitle('ImaGC - Idioma')
        janela.setFixedSize(QSize(300, 150))
        layout = QVBoxLayout()

        labelInfo = QLabel('<h3>Escolha o idioma:</h3>')
        layout.addWidget(labelInfo)

        idiomas = ['Portugues', 'English']
        escolha_idioma = QComboBox()
        escolha_idioma.addItems(idiomas)
        layout.addWidget(escolha_idioma)

        btnSalvar = QPushButton('Salvar')
        btnSalvar.clicked.connect(alterar)
        layout.addWidget(btnSalvar)

        janela.setLayout(layout)
        janela.show()

    def _instr(self):
        QMessageBox.information(
            self.ferramentas, "ImaGC - Instruções",
            """<h2>Breve Apresentação</h2><hr>

Olaa caro usuário!<br>
É com muito prazer e orgulho que apresento te o ImaGC<br>
Um programa simples e cheio de funcionalidades Das quais a sua principal função é de personalizar imagens!

<ul>
<li>Para O Adicionar O Logotipo,<br>
A imagem do logotipo Deve Ter O Fundo Ou Mascara Transparente;</li>
<li>Para A Conversão De (.ico),<br>
O Programa Subescreve Os Dados Binários Da Imagem E Redefine As Dimensões Da Mesma;</li>
<li>Para A Conversão De (.gif),<br>
O Programa Copia Os Dados Das Imagens<br>
E Cria Um Ciclo Alternado Entre Elas Com Duração De 1 Segundo Por Quadro;</li>
<li>Para A Conversão De (.pdf),<br>
O Programa Copia Igualmente (A Ou As) Imagens E Cria Um Arquivo Pdf Com ela(s) Automaticamente Redimensionadas;</li>
</ul>

Muito Obrigado pelo apoio!<br>
© 2021 Nurul GC<br>
™ ArtesGC Inc"""
        )

    def _sobre(self):
        QMessageBox.information(
            self.ferramentas, "ImaGC - Sobre",
            """<h2>Informações sobre o Programa</h2><hr>
<ul>
<li>Nome: <b>ImaGC</b></li>
<li>Versão: <b>0.9-042022</b></li>
<li>Programador & Designer: <b>Nurul-GC</b></li>
<li>Empresa: <b>&trade;ArtesGC Inc.</b></li>
</ul>"""
        )

    def _janeladebug(self):
        def leitura_log():
            registo.clear()
            with open(f'{debugpath()}/{lista_registo.currentItem().text()}', 'r') as log_file:
                registo.setText(log_file.read())

        janela_debug = QDialog(self.ferramentas)
        janela_debug.setFixedSize(QSize(700, 500))
        janela_debug.setWindowTitle("ImaGC - Registo de erros")
        layout_janela_debug = QFormLayout()

        layout_registo = QHBoxLayout()
        lista_registo = QListWidget()
        lista_registo.setFixedWidth(150)
        lista_registo.setSortingEnabled(True)
        lista_registo.setAlternatingRowColors(True)
        lista_registo.itemClicked.connect(leitura_log)
        for log in os.listdir(debugpath()):
            if log.endswith('.log'):
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
        layout_janela_debug.addRow(botao_fechar)

        janela_debug.setLayout(layout_janela_debug)
        janela_debug.show()

    # ******* windows *******
    def adicionar_logo(self):
        def procurar_imagem():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(
                self.ferramentas, caption="Selecione a Imagem",
                filter="Image Files (*.png *.jpg *.jpeg)"
            )
            nomeImagemAL.setText(nomeFicheiro)

        def procurar_logo():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(
                self.ferramentas, caption="Selecione o Logotipo",
                filter="Image Files (*.png *.jpg *.jpeg)"
            )
            nomeLogo.setText(nomeFicheiro)

        def add_logo_imagem():
            if nomeLogo.text() != "":
                try:
                    inicio = time()
                    QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione aonde salvar o arquivo..')
                    dirSalvar = QFileDialog.getExistingDirectory(
                        self.ferramentas,
                        caption="Selecione aonde salvar o arquivo"
                    )
                    ImagEditor(_dir_salvar=dirSalvar).add_logo(_nome_logotipo=nomeLogo.text(), _nome_imagem=nomeImagemAL.text())
                    QMessageBox.information(self.ferramentas, "Sucedido", f"Operação Concluida em {int(time() - inicio)}s..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"Durante o processamento do pedido ocorreu o seguinte erro:\n-{erro}")
            else:
                QMessageBox.critical(self.ferramentas, "Erro", "Selecione o logotipo antes de continuar e tente novamente..")
                procurar_logo()

        def procurar_directorio():
            if nomeLogo.text() != "":
                try:
                    inicio = time()
                    nomeDirectorio = QFileDialog.getExistingDirectory(self.ferramentas, caption="Selecione a Imagem")
                    dirImagem.setText(nomeDirectorio)
                    QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione aonde salvar o arquivo..')
                    dirSalvar = QFileDialog.getExistingDirectory(
                        self.ferramentas,
                        caption="Selecione aonde salvar o arquivo"
                    )
                    ImagEditor(_dir_salvar=dirSalvar).add_logo(
                        _nome_logotipo=nomeLogo.text(),
                        _dir_imagens=dirImagem.text()
                    )
                    QMessageBox.information(self.ferramentas, "Sucedido", f"Operação Concluida em {int(time() - inicio)}s..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"Durante o processamento do pedido ocorreu o seguinte erro:\n-{erro}")
            else:
                QMessageBox.critical(self.ferramentas, "Erro", "Selecione o logotipo antes de continuar e tente novamente..")
                procurar_logo()

        def visualizar_logo():
            if nomeLogo.text() == "" or nomeLogo.text().isspace():
                QMessageBox.warning(
                    self.ferramentas, "Falha ao apresentar a imagem",
                    "Por favor selecione a imagem antes de prosseguir.."
                )
            else:
                janelaLogo = QDialog(self.ferramentas)
                janelaLogo.setWindowTitle("ImaGC - Visualizar Logotipo")
                janelaLogo.setPalette(QPalette(QColor("orange")))

                layoutJanelaLogo = QVBoxLayout()
                labelLogo = QLabel()
                labelLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelLogo.setToolTip("Apresentação do logotipo!")
                labelLogo.setPixmap(QPixmap(f"{nomeLogo.text()}").scaled(QSize(250, 250)))
                layoutJanelaLogo.addWidget(labelLogo)

                infoImage = QLabel(
                    f"""<h3><i>Detalhes</i></h3>
<b>Nome</b>: {nomeLogo.text().split('/')[-1]}<br>
<b>Dimensões (original)</b>: {dimensao_imagem(_filename=nomeLogo.text())}pxs<br>
<b>Tamanho</b>: {tamanho_imagem(nomeLogo.text())}"""
                )
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
                QMessageBox.warning(
                    self.ferramentas, "Falha ao apresentar a imagem",
                    "Por favor selecione a imagem antes de prosseguir.."
                )
            else:
                janelaImagem = QDialog(self.ferramentas)
                janelaImagem.setWindowIcon(QIcon(f"{os.path.abspath(__file__)}/ima-icons/imagc.png"))
                janelaImagem.setWindowTitle("ImaGC - Visualizar Imagem")
                janelaImagem.setPalette(QPalette(QColor("orange")))

                layoutJanelaImagem = QVBoxLayout()
                labelImagem = QLabel()
                labelImagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
                labelImagem.setToolTip("Apresentação da Imagem!")
                labelImagem.setPixmap(QPixmap(f"{nomeImagemAL.text()}").scaled(QSize(250, 250)))
                layoutJanelaImagem.addWidget(labelImagem)

                infoImage = QLabel(
                    f"""<h3><i>Detalhes</i></h3>
<b>Nome</b>: {nomeImagemAL.text().split('/')[-1]}<br>
<b>Dimensões (originais)</b>: {dimensao_imagem(_filename=nomeImagemAL.text())}pxs<br>
<b>Tamanho</b>: {tamanho_imagem(nomeImagemAL.text())}"""
                )
                layoutJanelaImagem.addWidget(infoImage)

                _fechar = lambda: janelaImagem.close()
                botaoFechar = QPushButton("Fechar")
                botaoFechar.setDefault(True)
                botaoFechar.clicked.connect(_fechar)
                layoutJanelaImagem.addWidget(botaoFechar)

                janelaImagem.setLayout(layoutJanelaImagem)
                janelaImagem.show()

        layout = QFormLayout()

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
        layout.addRow(QLabel("<br><h3>Personalizando apenas uma imagem:</h3>"))

        nomeImagemAL = QLineEdit()
        nomeImagemAL.setReadOnly(True)
        nomeImagemAL.setPlaceholderText("Procure pela imagem para obter o seu nome..")
        layout.addRow(nomeImagemAL)

        nomeImagemBotao = QPushButton("Procurar Imagem")
        nomeImagemBotao.setDefault(True)
        nomeImagemBotao.clicked.connect(procurar_imagem)

        botao_ver_imagem = QPushButton("Visualizar Imagem")
        botao_ver_imagem.setDefault(True)
        botao_ver_imagem.clicked.connect(visualizar_imagem)
        layout.addRow(nomeImagemBotao, botao_ver_imagem)

        botao_add_logo_imagem = QPushButton("Adicionar Logotipo a Imagem")
        botao_add_logo_imagem.setDefault(True)
        botao_add_logo_imagem.clicked.connect(add_logo_imagem)
        layout.addRow(botao_add_logo_imagem)

        layout.addRow(QLabel("<br><h3>Personalizando varias imagens:</h3>"))
        dirImagem = QLineEdit()
        dirImagem.setReadOnly(True)
        dirImagem.setPlaceholderText("Localize o diretório contendo as imagens..")
        layout.addRow(dirImagem)

        dir_imagem_botao = QPushButton("Localizar Directório")
        dir_imagem_botao.setDefault(True)
        dir_imagem_botao.clicked.connect(procurar_directorio)
        layout.addRow(QLabel("<ul><li>O logotipo sera adicionado as imagens automaticamente!</li></ul>"))
        layout.addRow(dir_imagem_botao)

        self.janela1.setLayout(layout)

    def converter_gif(self):
        def procurar_imagens():
            nomeImagensCG.clear()
            self.nomeFicheiros, filtroFicheiros = QFileDialog.getOpenFileNames(
                self.ferramentas,
                caption="Selecione a Imagem",
                filter="Image Files (*.png *.jpg *.jpeg)"
            )
            if len(self.nomeFicheiros) < 2:
                QMessageBox.critical(
                    self.ferramentas, "Erro",
                    "Selecione as imagens antes de continuar e tente novamente.."
                )
            else:
                nomeImagensCG.addItems(self.nomeFicheiros)

        def previsualizar_img():
            dimensaoImagensCG = dimensao_imagem(nomeImagensCG.currentItem().text())
            tamanhoImagensCG = tamanho_imagem(nomeImagensCG.currentItem().text())
            imagem = QPixmap(nomeImagensCG.currentItem().text())
            imagem_label.setPixmap(imagem.scaled(QSize(150, 150)))
            imagem_label.setToolTip(
                "Está não é a dimensão original da imagem "
                "apenas foi adaptada para uma pré-visualização!"
            )
            imagem_detail.setText(
                f"""
<b>Nome</b>: {nomeImagensCG.currentItem().text().split('/')[-1]}<br>
<b>Tamanho</b>: {tamanhoImagensCG}<br>
<b>Dimensões (originais)</b>: {dimensaoImagensCG}pxs"""
            )

        def converter():
            if self.nomeFicheiros is None:
                QMessageBox.critical(self.ferramentas, "Erro", "Selecione as imagens antes de continuar e tente novamente..")
                procurar_imagens()
            else:
                try:
                    inicio = time()
                    QMessageBox.warning(self.ferramentas, 'Aviso', 'Selecione aonde salvar e o nome do arquivo..')
                    dirSalvar = QFileDialog.getSaveFileName(
                        self.ferramentas,
                        filter='GIF (*.gif)', caption='Selecione aonde salvar e o nome do arquivo..'
                    )[0]
                    ImagEditor(_dir_salvar=dirSalvar).convertendo_gif(_images=self.nomeFicheiros)
                    QMessageBox.information(self.ferramentas, "Sucedido", f"Operação Concluida em {int(time() - inicio)}s..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"Durante o processamento do pedido ocorreu o seguinte erro:\n-{erro}")

        layout = QFormLayout()
        layout.setSpacing(10)

        intro_label = QLabel("<h1><i>Converter para Gif</i></h1>")
        intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(intro_label)
        layout.addRow(QLabel("<hr>"))

        imagem_layout = QHBoxLayout()
        imagem_label = QLabel("Procure a imagem\npara puder\nprevisualiza-la..")
        imagem_label.setFixedSize(QSize(150, 150))
        imagem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagem_label.setStyleSheet('background-color: white; padding: 2px;')
        imagem_layout.addWidget(imagem_label)
        imagem_detail = QLabel(
            """
<b>Nome</b>: None<br>
<b>Tamanho</b>: None<br>
<b>Dimensões (originais)</b>: None"""
        )
        imagem_layout.addWidget(imagem_detail)
        layout.addRow(imagem_layout)

        layout.addRow(QLabel("<h3><i>Procure as imagens para obter os seus nomes:</i></h3>"))
        nomeImagensCG = QListWidget()
        nomeImagensCG.setAlternatingRowColors(True)
        nomeImagensCG.setToolTip("Aqui serão apresentados os nomes das imagens!")
        nomeImagensCG.itemClicked.connect(previsualizar_img)
        layout.addRow(nomeImagensCG)

        layout_btns = QHBoxLayout()
        procurar_btn = QPushButton("Procurar Imagens")
        procurar_btn.clicked.connect(procurar_imagens)
        layout_btns.addWidget(procurar_btn)

        converter_btn = QPushButton("Converter Imagens")
        converter_btn.clicked.connect(converter)
        layout_btns.addWidget(converter_btn)
        layout.addRow(layout_btns)

        self.janela2.setLayout(layout)

    def converter_ico(self):
        def procurar_imagem():
            nomeFicheiro, filtroFicheiros = QFileDialog.getOpenFileName(
                self.ferramentas, caption="Selecione a Imagem",
                filter="Image Files (*.png *.jpg *.jpeg)"
            )
            nomeImagemCI.setText(nomeFicheiro)
            previsualizar_img()

        def previsualizar_img():
            if nomeImagemCI.text() == "" or nomeImagemCI.text().isspace():
                QMessageBox.critical(self.ferramentas, "Erro", "Selecione a imagem antes de continuar e tente novamente..")
            else:
                dimensaoImagensCI = dimensao_imagem(nomeImagemCI.text())
                tamanhoImagensCI = tamanho_imagem(nomeImagemCI.text())
                imagem = QPixmap(nomeImagemCI.text())
                imagem_label.setPixmap(imagem.scaled(QSize(150, 150)))
                imagem_label.setToolTip(
                    "Esta não é a dimensão original da imagem "
                    "apenas foi adaptada para previsualização!"
                )
                imagem_detail.setText(
                    f"""
    <b>Nome</b>: {nomeImagemCI.text().split('/')[-1]}<br>
    <b>Tamanho</b>: {tamanhoImagensCI}<br>
    <b>Dimensões (originais)</b>: {dimensaoImagensCI}pxs"""
                )

        def converter():
            if nomeImagemCI.text() == "" or nomeImagemCI.text().isspace():
                QMessageBox.critical(
                    self.ferramentas, "Erro",
                    "Selecione a imagem antes de continuar e tente novamente.."
                )
                procurar_imagem()
            else:
                try:
                    inicio = time()
                    QMessageBox.information(self.ferramentas, 'Aviso', 'Selecione aonde salvar o arquivo..')
                    dirSalvar = QFileDialog.getExistingDirectory(
                        self.ferramentas,
                        caption="Selecione aonde salvar o arquivo"
                    )
                    ImagEditor(_dir_salvar=dirSalvar).convertendo_icone(
                        _size=int(tamanhos.currentText()),
                        _nome_imagem=nomeImagemCI.text()
                    )
                    QMessageBox.information(self.ferramentas, "Sucedido", f"Operação Concluida em {int(time() - inicio)}s..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"Durante o processamento do pedido ocorreu o seguinte erro:\n-{erro}")

        layout = QFormLayout()

        labelIntro = QLabel("<h1><i>Converter para Ico</i></h1>")
        labelIntro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(labelIntro)
        layout.addRow(QLabel("<hr><br>"))

        imagem_layout = QHBoxLayout()
        imagem_label = QLabel("Procure pela imagem\npara puder\nprevisualiza-la..")
        imagem_label.setFixedSize(QSize(150, 150))
        imagem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagem_label.setStyleSheet("background-color: white; padding: 2px;")
        imagem_layout.addWidget(imagem_label)
        imagem_detail = QLabel(
            """
<b>Nome</b>: None<br>
<b>Tamanho</b>: None<br>
<b>Dimensões (originais)</b>: None"""
        )
        imagem_layout.addWidget(imagem_detail)
        layout.addRow(imagem_layout)

        nomeImagemCI = QLineEdit()
        nomeImagemCI.setReadOnly(True)
        nomeImagemCI.setPlaceholderText("Procure pela imagem para obter o seu nome..")

        botaoIco = QPushButton("Procurar Imagem")
        botaoIco.clicked.connect(procurar_imagem)
        layout.addRow(botaoIco, nomeImagemCI)

        layout.addRow(QLabel("<br><h3><i>Converta para ícone com dimensões diferentes:</i></h3>"))
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
        def procurar_imagens():
            nomeImagensCP.clear()
            self.nomeFicheiros, filtroFicheiros = QFileDialog.getOpenFileNames(
                self.ferramentas,
                caption="Selecione a Imagem",
                filter="Image Files (*.png *.jpg *.jpeg)"
            )
            if len(self.nomeFicheiros) < 1:
                QMessageBox.critical(
                    self.ferramentas, "Erro",
                    "Selecione 'as imagens' antes de continuar e tente novamente.."
                )
            else:
                nomeImagensCP.addItems(self.nomeFicheiros)

        def previsualizar_img():
            dimensaoImagensCP = dimensao_imagem(nomeImagensCP.currentItem().text())
            tamanhoImagensCP = tamanho_imagem(nomeImagensCP.currentItem().text())
            imagem = QPixmap(nomeImagensCP.currentItem().text())
            imagemLabel.setPixmap(imagem.scaled(QSize(150, 150)))
            imagemLabel.setToolTip(
                "Esta não é a dimensão original da imagem "
                "apenas foi adaptada para uma previsualização!"
            )
            imagemDetail.setText(
                f"""
<b>Nome</b>: {nomeImagensCP.currentItem().text().split('/')[-1]}<br>
<b>Tamanho</b>: {tamanhoImagensCP}<br>
<b>Dimensões (originais)</b>: {dimensaoImagensCP}pxs"""
            )

        def converter():
            if self.nomeFicheiros is None:
                QMessageBox.critical(
                    self.ferramentas, "Erro",
                    "Selecione as imagens antes de continuar e tente novamente.."
                )
                procurar_imagens()
            else:
                try:
                    inicio = time()
                    QMessageBox.warning(self.ferramentas, 'Aviso', 'Selecione aonde salvar e o nome do arquivo..')
                    dirSalvar = QFileDialog.getSaveFileName(
                        self.ferramentas,
                        filter='PDF (*.pdf)', initialFilter='PDF (*.pdf)',
                        caption="Selecione aonde salvar e o nome do arquivo.."
                    )[0]
                    ImagEditor(_dir_salvar=dirSalvar).convertendo_pdf(_images=self.nomeFicheiros)
                    QMessageBox.information(self.ferramentas, "Sucedido", f"Operação Concluida em {int(time() - inicio)}s..")
                except Exception as erro:
                    QMessageBox.critical(self.ferramentas, "Erro", f"Durante o processamento do pedido ocorreu o seguinte erro:\n-{erro}")

        layout = QFormLayout()
        layout.setSpacing(10)

        introLabel = QLabel("<h1><i>Converter para Pdf</i></h1>")
        introLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(introLabel)
        layout.addRow(QLabel("<hr>"))

        imagemLayout = QHBoxLayout()
        imagemLabel = QLabel("Procure a imagem\npara puder\nprevisualiza-la..")
        imagemLabel.setFixedSize(QSize(150, 150))
        imagemLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagemLabel.setStyleSheet('background-color: white; padding: 2px;')
        imagemLayout.addWidget(imagemLabel)
        imagemDetail = QLabel(
            """
<b>Nome</b>: None<br>
<b>Tamanho</b>: None<br>
<b>Dimensões (originais)</b>: None"""
        )
        imagemLayout.addWidget(imagemDetail)
        layout.addRow(imagemLayout)

        layout.addRow(QLabel("<h3><i>Procure as imagens para obter os seus nomes:</i></h3>"))
        nomeImagensCP = QListWidget()
        nomeImagensCP.setAlternatingRowColors(True)
        nomeImagensCP.setToolTip("Aqui serão apresentados os nomes das imagens!")
        nomeImagensCP.itemClicked.connect(previsualizar_img)
        layout.addRow(nomeImagensCP)

        layoutBtns = QHBoxLayout()
        procurarBtn = QPushButton("Procurar Imagens")
        procurarBtn.clicked.connect(procurar_imagens)
        layoutBtns.addWidget(procurarBtn)

        converterBtn = QPushButton("Converter Imagens")
        converterBtn.clicked.connect(converter)
        layoutBtns.addWidget(converterBtn)
        layout.addRow(layoutBtns)

        self.janela4.setLayout(layout)

    def alterar_janela(self, index):
        self.stack.setCurrentIndex(index)
