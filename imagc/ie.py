"""
 * (c) 2019-2021. Nurul GC
 * Jovem Programador
 * Estudante de Engenharia de Telecomunicações
 * Tecnologia de Informação e de Medicina.
 * Foco Fé Força Paciência
 * Allah no Comando.

 - MODULO RESPONSAVEL PELA EDIÇÃO DAS IMAGENS
"""

# ******************************************************************************
#  (c) 2020-2021 Nurul-GC.                                                     *
# ******************************************************************************

import logging
import os
import shutil
from datetime import date
from subprocess import getoutput
from typing import List

import imageio
import PIL
from fpdf import FPDF


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


def debugpath() -> str:
    if os.name == 'posix':
        home = getoutput('echo $HOME')
        return os.path.join(home, '.ima-debug')
    return '.ima-debug'


def tempdir() -> str:
    os.makedirs(f"{debugpath()}/temp", exist_ok=True)
    return f"{debugpath()}/temp"


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
                        continue
                    elif filename in LOGO_FILENAME:
                        continue
                    else:
                        im = PIL.Image.open(f"{_dir_imagens}/{filename}")
                        width, height = im.size

                        im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                        im.save(os.path.join(f'{self.dir_salvar}', f"imagc-{filename}"))
                        logging.debug(f"Adding logo to the '{filename}'... SUCCESSFULL!")
                except Exception as erro:
                    logging.critical(f"- {erro}..")
                    continue
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
            imagem = os.path.join(f"{self.dir_salvar}/", f"imagc-{filename.split('/')[-1]}")

            try:
                im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                im.save(imagem)
                logging.debug(f"Adding logo to the '{imagem}'... SUCCESSFULL!")
            except Exception as erro:
                logging.critical(f"{erro}..")
                raise Exception(erro)

    def convertendo_gif(self, _images: List[str]):
        """função conversora (images to gif)

        :param _images: lista de imagens
        :return: nova imagem (.gif),
         salva no directorio selecionado pelo utilizador"""
        dados_imagem = []
        if self.dir_salvar.endswith('.gif'):
            try:
                for image in _images:
                    shutil.copyfile(image, tempdir())
                    for imagem in os.listdir(tempdir()):
                        img = PIL.Image.open(imagem)
                        img.save(imagem, sizes=[(500, 500)])

                        imgData = imageio.imread(imagem)
                        dados_imagem.append(imgData)
                imageio.mimsave(self.dir_salvar, dados_imagem, duration=1.0)
                logging.debug(f"Creating the file '{self.dir_salvar}'.. SUCCESSFULL!")

                for file in os.listdir(tempdir()):
                    os.remove(file)
                os.removedirs(tempdir())
            except Exception as erro:
                logging.critical(f"- {erro}..")
        else:
            raise NameError('Invalid Name for file, should end with ".gif"...')

    def convertendo_icone(self, _size: int, _nome_imagem: str):
        """funcão conversora (image to ico)

        :param _nome_imagem: nome e localização da imagem
        :param _size: dimensão do icone
        :return: um novo ficheiro (.ico), salvo no directorio selecionado pelo utilizador"""
        nome = ""
        try:
            SIZES = [[(16, 16)], [(32, 32)], [(128, 128)], [(256, 256)]]
            img_to_icon = PIL.Image.open(_nome_imagem)
            if _size == 16:
                size = SIZES[0]
                for sz in size[0]:
                    nome = f"{self.dir_salvar}/imagc-{sz}x{sz}.ico"
                img_to_icon.save(nome, sizes=size)
                logging.debug(f"Creating the icon '{nome}'.. SUCCESSFULL!")
            elif _size == 32:
                size = SIZES[1]
                for sz in size[1]:
                    nome = f"{self.dir_salvar}/imagc-{sz}x{sz}.ico"
                img_to_icon.save(nome, sizes=size)
                logging.debug(f"Creating the icon '{nome}'.. SUCCESSFULL!")
            elif _size == 64:
                size = SIZES[2]
                for sz in size[2]:
                    nome = f"{self.dir_salvar}/imagc-{sz}x{sz}.ico"
                img_to_icon.save(nome, sizes=size)
                logging.debug(f"Creating the icon '{nome}'.. SUCCESSFULL!")
            elif _size == 256:
                size = SIZES[3]
                for sz in size[3]:
                    nome = f"{self.dir_salvar}/imagc-{sz}x{sz}.ico"
                img_to_icon.save(nome, sizes=size)
                logging.debug(f"Creating the icon '{nome}'.. SUCCESSFULL!")
            else:
                pass
        except Exception as erro:
            logging.critical(f"- {erro}..")
            raise Exception(erro)

    def convertendo_pdf(self, _images: List[str]):
        """função conversora (images to pdf)

        :param _images: lista de imagens
        :return: novo documento (.pdf) contendo a imagem(ns) selecionada(s),
         salva no directorio selecionado pelo utilizador"""
        if self.dir_salvar.endswith('.pdf'):
            try:
                for image in _images:
                    width, height = dimensao_imagem(_filename=image)
                    if width > height:
                        self.pdf.add_page('L')
                        self.pdf.image(image, x=0, y=0, w=int(1122 / 3.75), h=int(793 / 3.75))
                    elif width < height:
                        self.pdf.add_page('P')
                        self.pdf.image(image, x=0, y=0, w=int(793 / 3.75), h=int(1122 / 3.75))
                    else:
                        self.pdf.add_page('L')
                        self.pdf.image(image, x=0, y=0, w=int(1122 / 3.75), h=int(793 / 3.75))

                self.pdf.output(self.dir_salvar, 'F')
                logging.debug(f"Creating the file '{self.dir_salvar}'.. SUCCESSFULL!")
            except Exception as erro:
                logging.critical(f"{erro}..")
        else:
            raise NameError('Invalid Name for file, should end with ".pdf"...')


logging.basicConfig(
    filename=f"{debugpath()}/{date.today()}-imagc.log",
    level=logging.DEBUG, format='\n %(asctime)s - %(levelname)s - %(message)s'
)
logging.info(f"{'*' * 25} NEW DEBUG {'*' * 25}")
