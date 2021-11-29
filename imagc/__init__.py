# ******************************************************************************
#  (c) 2020-2021 Nurul-GC.                                                     *
# ******************************************************************************

# ***********************************************
#  (c) 2019-2021. Nurul GC                      *
#                                               *
#  Jovem Programador                            *
#  Estudante de Engenharia de Telecomunicações  *
#  Tecnologia de Informação e de Medicina.      *
#  Foco Fé Força Paciência                      *
#  Allah no Comando.                            *
# ***********************************************

"""
__AUTHOR__ = "Nurul Carvalho"
__EMAIL__ = "nuruldecarvalho@gmail.com"
__GITHUB_PROFILE__ = "https://github.com/Nurul-GC"
__VERSION__ = "0.8-112021"
__COPYRIGHT__ = "© 2021 Nurul-GC"
__TRADEMARK__ = "ArtesGC Inc"
__TRADE_WEBSITE_ = "https://artesgc.home.blog"
"""

import os
from configparser import ConfigParser
from random import randint
from sys import argv, exit
from time import sleep

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from imagc.en import EN
from imagc.ie import debugpath
from imagc.pt import PT


class ImaGC:
    def __init__(self):
        self.gc = QApplication(argv)

        # application font
        QFontDatabase.addApplicationFont("./ima-fonts/lifesavers.ttf")

        img = QPixmap("./ima-icons/favicon-512x512.png").scaled(QSize(500, 500))
        self.align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignAbsolute)
        self.janela = QSplashScreen(img)
        self.janela.setStyleSheet(theme)
        self.janela.show()
        self.iniciar()

    def iniciar(self):
        inifile = ConfigParser()
        load = ''
        while len(load) < 100:
            self.janela.showMessage(f"{load}", self.align, Qt.GlobalColor.black)
            sleep(0.5)
            load += '|'*randint(5, 10)
        if os.path.exists(f'{debugpath()}/imagc.ini'):
            inifile.read(f'{debugpath()}/imagc.ini')
            if inifile['MAIN']['lang'] == 'English':
                app = EN()
                self.janela.close()
                app.ferramentas.show()
            elif inifile['MAIN']['lang'] == 'Portugues':
                app = PT()
                self.janela.close()
                app.ferramentas.show()
            else:
                self.lang()
                self.janela.close()
        else:
            app = EN()
            self.janela.close()
            app.ferramentas.show()

    def lang(self):
        def alterar():
            try:
                config = ConfigParser()
                if escolha_idioma.currentText() == 'Portugues':
                    config['MAIN'] = {'lang':escolha_idioma.currentText()}
                elif escolha_idioma.currentText() == 'English':
                    config['MAIN'] = {'lang':escolha_idioma.currentText()}
                with open(f'{debugpath()}/imagc.ini', 'w') as INIFILE:
                    config.write(INIFILE)
                QMessageBox.information(self.janela, 'Sucessso', '- The language set will be loaded after restart the program!\n'
                                                                 '- O idioma definido será carregado após o reinício do programa!')
                janela.close()
                exit(0)
            except Exception as erro:
                QMessageBox.warning(self.janela, 'Aviso', f'[!] - While processing your request the following error was found!\n'
                                                          f'[!] - Enquanto processava o seu pedido, o seguinte erro foi encontrado!\n\n'
                                                          f'- {erro}')

        janela = QDialog(self.janela)
        janela.setWindowTitle('Error - Erro')
        janela.setFixedSize(QSize(500, 200))
        layout = QVBoxLayout()

        labelInfo = QLabel('<h4>- Am sorry, the language set in your [imagc.ini] file is unsupported,<br>Set the right language!<br><br>'
                           '- Lamento, o idioma definido no seu ficheiro [imagc.ini] não é suportado,<br>Selecione o idioma correto!<br></h4>')
        layout.addWidget(labelInfo)

        idiomas = ['Portugues', 'English']
        escolha_idioma = QComboBox()
        escolha_idioma.addItems(idiomas)
        layout.addWidget(escolha_idioma)

        btnSalvar = QPushButton('Save | Salvar')
        btnSalvar.clicked.connect(alterar)
        layout.addWidget(btnSalvar)

        janela.setLayout(layout)
        janela.show()


if __name__ == '__main__':
    os.makedirs(debugpath(), exist_ok=True)
    theme = open("./ima-themes/imagc.qss").read().strip()
    gcApp = ImaGC()
    gcApp.gc.exec()
