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
        QFontDatabase.addApplicationFont("fonts/lifesavers.ttf")

        img = QPixmap("icons/imagc.png").scaled(QSize(400, 400))
        self.align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignAbsolute)
        self.janela = QSplashScreen(img)
        self.janela.show()
        self.iniciar()

    def iniciar(self):
        n = 0
        inifile = ConfigParser()
        while n < 101:
            self.janela.showMessage(f"Loading... {n}%", self.align, Qt.GlobalColor.yellow)
            sleep(0.5)
            n += randint(1, 10)
        if os.path.exists('imagc.ini'):
            inifile.read('imagc.ini')
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
    theme = open('themes/imagc.qss').read().strip()
    gcApp = ImaGC()
    gcApp.gc.exec()
