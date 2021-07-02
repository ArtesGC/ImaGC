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
from typing import List
import imageio
from PIL import Image
from fpdf import FPDF

__author__ = "Nurul Carvalho"
__email__ = "nuruldecarvalho@gmail.com"
__github_profile__ = "https://github.com/Nurul-GC"
__version__ = "0.5-072021"
__copyright__ = "© 2021 Nurul-GC"
__trademark__ = "ArtesGC Inc"
__trade_website_ = "https://artesgc.home.blog"

os.makedirs("./Debug", exist_ok=True)
logging.basicConfig(filename=f"./Debug/{datetime.date(datetime.today())}-imagc.log", level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('*' * 25 + ' NEW DEBUG ' + '*' * 25)


class ImaGC:
    def __init__(self, _dir_salvar: str = None):
        self.pdf = FPDF()
        self.dir_salvar = _dir_salvar

    def addLogo(self, _nome_logotipo: str, _nome_imagem: str = None, _dir_imagens: str = None):
        if _dir_imagens and _nome_logotipo:
            SQUARE_FIT_SIZE = 100
            LOGO_FILENAME = _nome_logotipo
            logoIm = Image.open(LOGO_FILENAME)
            logoWidth, logoHeight = logoIm.size

            if (logoWidth and logoHeight) > SQUARE_FIT_SIZE:
                logoWidth = SQUARE_FIT_SIZE
                logoHeight = SQUARE_FIT_SIZE
                logoIm = logoIm.resize((logoWidth, logoHeight))

            for filename in os.listdir(_dir_imagens):
                try:
                    if (not filename.endswith("png")) \
                            or (not filename.endswith("jpg")) or (not filename.endswith("jpeg")) \
                            or (filename == LOGO_FILENAME) or os.path.isdir(filename):
                        continue

                    im = Image.open(f"{_dir_imagens}/{filename}")
                    width, height = im.size

                    im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                    im.save(os.path.join(f'{self.dir_salvar}', f"imagc-{filename}"))
                    logging.debug(f"- Adicionando logo a imagem '{filename}'... SUCESSO!")
                except Exception as erro:
                    logging.critical(f"- {erro}..")
                    continue
        elif _nome_imagem and _nome_logotipo:
            SQUARE_FIT_SIZE = 100
            LOGO_FILENAME = _nome_logotipo
            logoIm = Image.open(LOGO_FILENAME)
            logoWidth, logoHeight = logoIm.size

            if (logoWidth and logoHeight) > SQUARE_FIT_SIZE:
                logoWidth = SQUARE_FIT_SIZE
                logoHeight = SQUARE_FIT_SIZE
                logoIm = logoIm.resize((logoWidth, logoHeight))

            filename = _nome_imagem
            im = Image.open(filename)
            width, height = im.size

            try:
                im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                im.save(f"{self.dir_salvar}/imagc-{filename}")
                logging.debug(f"- Adicionando logo a imagem '{filename}'... SUCESSO!")
            except Exception as erro:
                logging.critical(f"- {erro}..")
        else:
            logging.critical("- Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n")

    def convertendoGif(self, _images: List[str]):
        """função conversora (images to gif)

        :param _images: lista de imagens
        :return: nova imagem (.gif),
         salva no directorio selecionado pelo utilizador"""
        dados_imagem = []
        for image in _images:
            imgData = imageio.imread(image)
            dados_imagem.append(imgData)
        imageio.mimsave(f'{self.dir_salvar}/imagc.gif', dados_imagem, duration=1.0)

    def convertendoIcone(self, _size: int, _nome_imagem: str):
        """funcão conversora (image to ico)

        :param _nome_imagem: nome e localização da imagem
        :param _size: dimensão do icone
        :return: um novo ficheiro (.ico),
         salvo no directorio selecionado pelo utilizador"""
        nome = ""
        if _nome_imagem:
            try:
                SIZES = [[(16, 16)], [(32, 32)], [(128, 128)], [(256, 256)]]
                img_to_icon = Image.open(_nome_imagem)
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

    def convertendoPdf(self, _images: List[str]):
        """função conversora (images to pdf)

        :param _images: lista de imagens
        :return: novo documento (.pdf) contendo a imagem(ns) selecionada(s),
         salva no directorio selecionado pelo utilizador"""
        for image in _images:
            self.pdf.add_page('P')
            self.pdf.image(image, x=0, y=0, w=1080, h=1920)
        self.pdf.output(f'{self.dir_salvar}/imagc.pdf', 'F')

    def dimensaoImagem(self, _filename: str):
        """identifica as dimensões da imagem

        :param _filename: nome e localização da imagem
        :return: uma tupla contendo a largura e a altura da imagem"""
        imagem = Image.open(_filename)
        return imagem.size

    def redimensionarImagem(self, _resizer: float, _nome_imagem: str):
        """função redimensionadora

        :param _resizer: faça (n/100) para calcurar a percentagem a ser reduzida
        :param _nome_imagem: nome e localização da imagem
        :return: uma nova imagem redimensionada ou uma mensagem de erro gravada no arquivo de debug"""
        nome = ""
        if _nome_imagem:
            try:
                resize_img = Image.open(_nome_imagem)
                width, heigth = self.dimensaoImagem(_nome_imagem)
                SIZES = [(width/_resizer, heigth/_resizer)]
                for size in SIZES[0]:
                    nome = f"{self.dir_salvar}/imagc-{size}x{size}-{_nome_imagem}"
                resize_img.save(nome, sizes=SIZES)
                logging.debug(f"- Criando o icone '{nome}'.. SUCESSO!")
            except Exception as erro:
                logging.critical(f"- {erro}..")
        else:
            logging.critical("- Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n")

    def tamanhoImagem(self, _filename: str):
        """calcula a quantidade de bytes da imagem

        :param _filename: nome e localização da imagem
        :return: o tamanho que a imagem ocupa no disco"""
        num = os.path.getsize(_filename)
        for x in ['bytes', 'KB', 'MB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0
