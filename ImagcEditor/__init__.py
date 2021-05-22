"""
 * (c) 2019-2021. Nurul GC
 * Jovem Programador
 * Estudante de Engenharia de Telecomunicações
 * Tecnologia de Informação e de Medicina.
 * Foco Fé Força Paciência
 * Allah no Comando.

 - MODULO RESPONSAVEL PELA EDIÇÃO DAS IMAGENS
"""

import logging
import os
from datetime import datetime

from PIL import Image

__author__ = "Nurul Carvalho"
__email__ = "nuruldecarvalho@gmail.com"
__github_profile__ = "https://github.com/Nurul-GC"
__version__ = "0.3-042021"
__copyright__ = "© 2021 Nurul-GC"
__trademark__ = "ArtesGC Inc"
__trade_website_ = "https://artesgc.home.blog"

os.makedirs("./Debug", exist_ok=True)
logging.basicConfig(filename=f"./Debug/{datetime.date(datetime.today())}-imagc.log", level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('*' * 25 + 'NEW DEBUG' + '*' * 25)


class ImaGC:
    def __init__(self, _dir_salvar: str = None, _nome_logotipo: str = None, _nome_imagem: str = None, _dir_imagem: str = None):
        self.nome_logotipo = _nome_logotipo
        self.nome_imagem = _nome_imagem
        self.dir_imagem = _dir_imagem
        self.dir_salvar = _dir_salvar

    def addLogo(self):
        if self.dir_imagem and self.nome_logotipo:
            SQUARE_FIT_SIZE = 100
            LOGO_FILENAME = self.nome_logotipo
            logoIm = Image.open(LOGO_FILENAME)
            logoWidth, logoHeight = logoIm.size

            if (logoWidth and logoHeight) > SQUARE_FIT_SIZE:
                logoWidth = SQUARE_FIT_SIZE
                logoHeight = SQUARE_FIT_SIZE
                logoIm = logoIm.resize((logoWidth, logoHeight))

            for filename in os.listdir(self.dir_imagem):
                im = Image.open(f"{self.dir_imagem}/{filename}")
                width, height = im.size

                if (not filename.endswith("png")) or (not filename.endswith("jpg")) or (not filename.endswith("jpeg")) or (filename == LOGO_FILENAME) or os.path.isdir(filename):
                    continue

                try:
                    # Add logo.
                    logging.debug(f"- Adicionando logo a imagem '{filename}'... SUCESSO!")
                    im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                    # Save changes.
                    im.save(os.path.join(f'{self.dir_salvar}', f"imagc-{filename}"))
                except Exception as erro:
                    logging.critical(f"- {erro}..")
                    continue
        elif self.nome_imagem and self.nome_logotipo:
            SQUARE_FIT_SIZE = 100
            LOGO_FILENAME = self.nome_logotipo
            logoIm = Image.open(LOGO_FILENAME)
            logoWidth, logoHeight = logoIm.size

            if (logoWidth and logoHeight) > SQUARE_FIT_SIZE:
                logoWidth = SQUARE_FIT_SIZE
                logoHeight = SQUARE_FIT_SIZE
                logoIm = logoIm.resize((logoWidth, logoHeight))

            filename = self.nome_imagem
            im = Image.open(filename)
            width, height = im.size

            try:
                # Add logo.
                logging.debug(f"- Adicionando logo a imagem '{filename}'... SUCESSO!")
                im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                # Save changes.
                im.save(f"{self.dir_salvar}/imagc-{filename}")
            except Exception as erro:
                logging.critical(f"- {erro}..")
        else:
            logging.critical("- Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n")

    def convertendoIcone(self, _size: int = None):
        nome = ""
        if self.nome_imagem:
            try:
                SIZES = [[(16, 16)], [(32, 32)], [(128, 128)], [(256, 256)]]
                img_to_icon = Image.open(self.nome_imagem)
                if _size == 16:
                    size = SIZES[0]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}.ico"
                    img_to_icon.save(nome, sizes=size)
                    logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
                elif _size == 32:
                    size = SIZES[1]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}.ico"
                    img_to_icon.save(nome, sizes=size)
                    logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
                elif _size == 64:
                    size = SIZES[2]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}.ico"
                    img_to_icon.save(nome, sizes=size)
                    logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
                elif _size == 256:
                    size = SIZES[3]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}.ico"
                    img_to_icon.save(nome, sizes=size)
                    logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
                else:
                    pass
            except Exception as erro:
                logging.critical(f"- {erro}..")
        else:
            logging.critical("- Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n")

    def redimensionarImagem(self, _size: int):
        nome = ""
        if self.nome_imagem:
            try:
                SIZES = [[(200, 200)], [(400, 400)], [(600, 600)], [(800, 800)], [(1200, 1200)]]
                resize_img = Image.open(self.nome_imagem)
                if _size == 200:
                    size = SIZES[0]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}-{self.nome_imagem}"
                    resize_img.save(nome, sizes=size)
                    logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
                elif _size == 400:
                    size = SIZES[1]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}-{self.nome_imagem}"
                    resize_img.save(nome, sizes=size)
                    logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
                elif _size == 600:
                    size = SIZES[2]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}-{self.nome_imagem}"
                    resize_img.save(nome, sizes=size)
                    logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
                elif _size == 800:
                    size = SIZES[3]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}-{self.nome_imagem}"
                    resize_img.save(nome, sizes=size)
                    logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
                elif _size == 1200:
                    size = SIZES[4]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}-{self.nome_imagem}"
                    resize_img.save(nome, sizes=size)
                    logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
                else:
                    pass
            except Exception as erro:
                logging.critical(f"- {erro}..")
        else:
            logging.critical("- Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n")

    def dimensaoImagem(self, _filename: str):
        imagem = Image.open(_filename)
        return imagem.size

    def tamanhoImagem(self, _filename: str):
        num = os.path.getsize(_filename)
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0
