# ******************************************************************************
#  (c) 2019-2021. Nurul GC                                                     *
#                                                                              *
#  Jovem Programador                                                           *
#  Estudante de Engenharia de Telecomunicações                                 *
#  Tecnologia de Informação e de Medicina.                                     *
#  Foco Fé Força Paciência                                                     *
#  Allah no Comando.                                                           *
# ******************************************************************************

import os
from PIL import Image
from typing import Tuple


class ImaGC:
    def __init__(self, nome_logotipo: str = None, nome_imagem: str = None, dir_imagem: str = None, dimensao_ico: tuple = None):
        self.nome_logotipo = nome_logotipo
        self.nome_imagem = nome_imagem
        self.dir_imagem = dir_imagem
        self.dimensao_ico = dimensao_ico

    def addLogo(self):
        if self.dir_imagem and self.nome_logotipo:
            SQUARE_FIT_SIZE = 100
            LOGO_FILENAME = self.nome_logotipo
            logoIm = Image.open(LOGO_FILENAME)
            logoWidth, logoHeight = logoIm.size
            os.makedirs('../ImaGC-logo', exist_ok=True)

            if (logoWidth and logoHeight) > SQUARE_FIT_SIZE:
                logoWidth = SQUARE_FIT_SIZE
                logoHeight = SQUARE_FIT_SIZE
                logoIm = logoIm.resize((logoWidth, logoHeight))

            for filename in os.listdir(self.dir_imagem):
                im = Image.open(f"{self.dir_imagem}/{filename}")
                width, height = im.size

                if not (filename.endswith("png") or filename.endswith("jpg") or filename.endswith("jpeg")) or filename == LOGO_FILENAME:
                    continue

                try:
                    # Add logo.
                    print(f'Adicionando logo a imagem {filename}...')
                    im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                    # Save changes.
                    im.save(os.path.join('../ImaGC-logo', f"{filename}"))
                except Exception as erro:
                    print(f"[x] - {erro}..")
                    continue
        elif self.nome_imagem and self.nome_logotipo:
            SQUARE_FIT_SIZE = 100
            LOGO_FILENAME = self.nome_logotipo
            logoIm = Image.open(LOGO_FILENAME)
            logoWidth, logoHeight = logoIm.size
            os.makedirs('../ImaGC-logo', exist_ok=True)

            if (logoWidth and logoHeight) > SQUARE_FIT_SIZE:
                logoWidth = SQUARE_FIT_SIZE
                logoHeight = SQUARE_FIT_SIZE
                logoIm = logoIm.resize((logoWidth, logoHeight))

            filename = self.nome_imagem
            im = Image.open(filename)
            width, height = im.size

            try:
                # Add logo.
                print(f'[i] - Adicionando logo a imagem {filename}...')
                im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
                # Save changes.
                im.save(os.path.join('../ImaGC-logo', f"{filename}"))
            except Exception as erro:
                print(f"[x] - {erro}..")
        else:
            return "\t***[Adicionando Logo]***\n" + "[x_x] - Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n"

    def convertendoIcone(self):
        os.makedirs('../ImaGC-ico', exist_ok=True)
        if self.nome_imagem:
            try:
                img_to_icon = Image.open(self.nome_imagem)
                for size in self.dimensao_ico:
                    nome = f"../ImaGC-ico/imagc-{size}x{size}.ico"
                print(f"[i] - Criando o icone {nome}..")
                img_to_icon.resize(self.dimensao_ico)
                img_to_icon.save(nome)
            except Exception as erro:
                print(f"[x] - {erro}..")
        else:
            return "\t***[Convertendo para Ico]***\n" + "[x_x] - Operação Incompleta, identifique o nome e localização dos ficheiros antes de iniciar..\n"


if __name__ == '__main__':
    print("""
    [***] ImaGC [***]
-------------------------
""")
    try:
        ImaGC().addLogo()
    finally:
        ImaGC().convertendoIcone()
