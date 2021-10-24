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
from datetime import date
from subprocess import getoutput
from typing import List
import imageio
import PIL
from fpdf import FPDF

__AUTHOR__ = "Nurul Carvalho"
__EMAIL__ = "nuruldecarvalho@gmail.com"
__GITHUB_PROFILE__ = "https://github.com/Nurul-GC"
__VERSION__ = "0.7-102021"
__COPYRIGHT__ = "© 2021 Nurul-GC"
__TRADEMARK__ = "ArtesGC Inc"
__TRADE_WEBSITE_ = "https://artesgc.home.blog"

if os.name == 'posix':
    home = getoutput('echo $HOME')
    os.makedirs(os.path.join(home, f".ima-debug"), exist_ok=True)
else:
    os.makedirs(f".ima-debug", exist_ok=True)
logging.basicConfig(filename=f".ima-debug/{date.today()}-imagc.log",
                    level=logging.DEBUG, format='\n %(asctime)s - %(levelname)s - %(message)s')
logging.info(f"{'*' * 25} NEW DEBUG {'*' * 25}")


def dimensao_imagem(_filename: str):
    """identifica as dimensões da imagem

    :param _filename: nome e localização da imagem
    :return: uma tupla contendo a largura e a altura da imagem"""
    imagem = PIL.Image.open(_filename)
    return imagem.size


def tamanho_imagem(_filename: str):
    """calcula a quantidade de bytes da imagem

    :param _filename: nome e localização da imagem
    :return: o tamanho que a imagem ocupa no disco"""
    num = os.path.getsize(_filename)
    for x in ['bytes', 'KB', 'MB']:
        if num < 1024.0:
            return f"{num:3.1f}{x}"
        num /= 1024.0


class ImagEditor:
    """ImaGC backend class"""
    def __init__(self, _dir_salvar: str = None):
        self.pdf = FPDF()
        self.dir_salvar = _dir_salvar

    def add_logo(self, _nome_logotipo: str, _nome_imagem: str = None, _dir_imagens: str = None):
        """adicionar logotipo a outra imagem

        :param _nome_imagem: nome e localização da imagem
        :param _nome_logotipo: nome e localização do logotipo
        :param _dir_imagens: localização do directorio contendo as imagens
        :return: uma nova imagem contendo o logotipo no canto inferior direito"""
        if _dir_imagens and _nome_logotipo:
            SQUARE_FIT_SIZE = 100
            LOGO_FILENAME = _nome_logotipo
            logoIm = PIL.Image.open(LOGO_FILENAME)
            logoWidth, logoHeight = logoIm.size

            if (logoWidth and logoHeight) > SQUARE_FIT_SIZE:
                logoWidth = SQUARE_FIT_SIZE
                logoHeight = SQUARE_FIT_SIZE
                logoIm = logoIm.resize((logoWidth, logoHeight))

            for filename in os.listdir(_dir_imagens):
                try:
                    if not filename.endswith(".png") and not filename.endswith(".jpg") and not filename.endswith(".jpeg"):
                        raise TypeError("Formato de imagem não suportado..")
                    if filename in LOGO_FILENAME:
                        raise NameError("Nome do ficheiro semelhante ao do logotipo..")

                    im = PIL.Image.open(f"{_dir_imagens}/{filename}")
                    width, height = im.size

                    im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                    im.save(os.path.join(f'{self.dir_salvar}', f"imagc-{filename}"))
                    logging.debug(f"Adicionando logotipo a imagem '{filename}'... CONCLUIDO!")
                except Exception as erro:
                    logging.critical(f"{erro}..")
                    raise Exception(erro)
        elif _nome_imagem and _nome_logotipo:
            SQUARE_FIT_SIZE = 100
            LOGO_FILENAME = _nome_logotipo
            logoIm = PIL.Image.open(LOGO_FILENAME)
            logoWidth, logoHeight = logoIm.size

            if (logoWidth and logoHeight) > SQUARE_FIT_SIZE:
                logoWidth = SQUARE_FIT_SIZE
                logoHeight = SQUARE_FIT_SIZE
                logoIm = logoIm.resize((logoWidth, logoHeight))

            filename = _nome_imagem
            im = PIL.Image.open(filename)
            width, height = im.size

            try:
                im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                im.save(os.path.join(f"{self.dir_salvar}/", f"imagc-{filename.split('/')[-1]}"))
                logging.debug(f"Adicionando logo a imagem '{filename}'... CONCLUIDO!")
            except Exception as erro:
                logging.critical(f"{erro}..")
                raise Exception(erro)
        else:
            logging.warning("Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n")

    def convertendo_gif(self, _images: List[str]):
        """função conversora (images to gif)

        :param _images: lista de imagens
        :return: nova imagem (.gif),
         salva no directorio selecionado pelo utilizador"""
        dados_imagem = []
        if _images:
            try:
                for image in _images:
                    imgData = imageio.imread(image)
                    dados_imagem.append(imgData)
                imageio.mimsave(f"{self.dir_salvar}/imagc.gif", dados_imagem, duration=1.0)
                logging.debug(f"Criando o arquivo '{self.dir_salvar}/imagc.gif'.. CONCLUIDO!")
            except Exception as erro:
                logging.critical(f"- {erro}..")
                raise Exception(erro)
        else:
            logging.warning("Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n")

    def convertendo_icone(self, _size: int, _nome_imagem: str):
        """funcão conversora (image to ico)

        :param _nome_imagem: nome e localização da imagem
        :param _size: dimensão do icone
        :return: um novo ficheiro (.ico), salvo no directorio selecionado pelo utilizador"""
        nome = ""
        if _nome_imagem:
            try:
                SIZES = [[(16, 16)], [(32, 32)], [(128, 128)], [(256, 256)]]
                img_to_icon = PIL.Image.open(_nome_imagem)
                if _size == 16:
                    size = SIZES[0]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}.ico"
                    img_to_icon.save(nome, sizes=size)
                    logging.debug(f"Criando o icone '{nome}'.. CONCLUIDO!")
                elif _size == 32:
                    size = SIZES[1]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}.ico"
                    img_to_icon.save(nome, sizes=size)
                    logging.debug(f"Criando o icone '{nome}'.. CONCLUIDO!")
                elif _size == 64:
                    size = SIZES[2]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}.ico"
                    img_to_icon.save(nome, sizes=size)
                    logging.debug(f"Criando o icone '{nome}'.. CONCLUIDO!")
                elif _size == 256:
                    size = SIZES[3]
                    for sz in size:
                        for s in sz:
                            nome = f"{self.dir_salvar}/imagc-{s}x{s}.ico"
                    img_to_icon.save(nome, sizes=size)
                    logging.debug(f"Criando o icone '{nome}'.. CONCLUIDO!")
                else:
                    pass
            except Exception as erro:
                logging.critical(f"- {erro}..")
                raise Exception(erro)
        else:
            logging.warning("Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n")

    def convertendo_pdf(self, _images: List[str]):
        """função conversora (images to pdf)

        :param _images: lista de imagens
        :return: novo documento (.pdf) contendo a imagem(ns) selecionada(s),
         salva no directorio selecionado pelo utilizador"""
        if _images:
            try:
                for image in _images:
                    width, height = dimensao_imagem(_filename=image)
                    if not image.endswith(".png") and not image.endswith(".jpg") and not image.endswith(".jpeg"):
                        raise TypeError("Formato de ficheiro não suportado..")
                    if width > height:
                        self.pdf.add_page('L')
                        self.pdf.image(image, x=0, y=0, w=int(1122/3.75), h=int(793/3.75))
                    elif width < height:
                        self.pdf.add_page('P')
                        self.pdf.image(image, x=0, y=0, w=int(793/3.75), h=int(1122/3.75))
                self.pdf.output(f'{self.dir_salvar}/imagc.pdf', 'F')
                logging.debug(f"Criando o arquivo '{self.dir_salvar}/imagc.pdf'.. CONCLUIDO!")
            except Exception as erro:
                logging.critical(f"{erro}..")
                raise Exception(erro)
        else:
            logging.warning("Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n")
