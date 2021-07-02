# ***********************************************
#  (c) 2019-2021. Nurul GC                      *
#                                               *
#  Jovem Programador                            *
#  Estudante de Engenharia de Telecomunicações  *
#  Tecnologia de Informação e de Medicina.      *
#  Foco Fé Força Paciência                      *
#  Allah no Comando.                            *
# ***********************************************
from random import randint
from sys import argv
from time import sleep
from PyQt5.Qt import *
from imagc.en import EN
from imagc.pt import PT

theme = open('themes/imagc.qss').read().strip()


class ImaGC_GUI:
    def __init__(self):
        self.gc = QApplication(argv)
        self.janela = QWidget()
        self.janela.setWindowTitle("ImaGC")
        self.janela.setWindowIcon(QIcon("img/imagc-icon.png"))
        self.janela.setPalette(QPalette(QColor('orange')))
        self.janela.setStyleSheet(theme)

        layout = QVBoxLayout()

        label = QLabel()
        label.setPixmap(QPixmap("img/imagc.png").scaled(QSize(400, 400)))
        layout.addWidget(label)

        listaIdiomas = ['Set the language - Defina o idioma', 'English', 'Português']
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
                sleep(0.2)
                n += randint(1, 5)
            self.janela.destroy()
            app = EN()
            app.ferramentas.show()
        elif self.idiomas.currentText() == 'Português':
            while n < 101:
                self.barraIniciar.setValue(n)
                sleep(0.2)
                n += randint(1, 5)
            self.janela.destroy()
            app = PT()
            app.ferramentas.show()
        else:
            QMessageBox.information(self.janela, "Info", "- Please select a language!\n- Por favor selecione um idioma!")


if __name__ == '__main__':
    gcApp = ImaGC_GUI()
    gcApp.janela.show()
    gcApp.gc.exec_()
