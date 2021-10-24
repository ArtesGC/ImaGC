# ***********************************************
#  (c) 2019-2021. Nurul GC                      *
#                                               *
#  Jovem Programador                            *
#  Estudante de Engenharia de Telecomunicações  *
#  Tecnologia de Informação e de Medicina.      *
#  Foco Fé Força Paciência                      *
#  Allah no Comando.                            *
# ***********************************************
import os
from configparser import ConfigParser
from random import randint
from subprocess import getoutput
from sys import argv
from time import sleep

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from imagc.en import EN
from imagc.pt import PT


class ImaGC:
    def __init__(self):
        self.gc = QApplication(argv)

        # application font
        QFontDatabase.addApplicationFont("./ima-fonts/lifesavers.ttf")

        img = QPixmap("./ima-icons/imagc.png").scaled(QSize(400, 400))
        self.align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignAbsolute)
        self.janela = QSplashScreen(img)
        self.janela.setStyleSheet(theme)
        self.janela.show()
        self.iniciar()

    @property
    def debugpath(self) -> str:
        if os.name == 'posix':
            home = getoutput('echo $HOME')
            return os.path.join(home, '.ima-debug')
        return '.ima-debug'

    def iniciar(self):
        n = 0
        inifile = ConfigParser()
        load = ''
        while len(load) < 120:
            self.janela.showMessage(f"{load}", self.align, Qt.GlobalColor.yellow)
            sleep(0.5)
            load += '|'*randint(1, 10)
        if os.path.exists(f'{self.debugpath}/imagc.ini'):
            inifile.read(f'{self.debugpath}/imagc.ini')
            if inifile['MAIN']['lang'] == 'English':
                app = EN()
                app.ferramentas.show()
            elif inifile['MAIN']['lang'] == 'Portugues':
                app = PT()
                app.ferramentas.show()
            else:
                QMessageBox.critical(QWidget, 'Error', "- Am sorry, the language set in your [imagc.ini] file is unsupported!\n"
                                                       "- Lamento, o idioma definido no seu ficheiro [imagc.ini] não é suportado!")
        else:
            app = EN()
            app.ferramentas.show()


if __name__ == '__main__':
    theme = open("./ima-themes/imagc.qss").read().strip()
    gcApp = ImaGC()
    gcApp.gc.exec()
