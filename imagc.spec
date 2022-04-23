# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['./imagc/__init__.py'],
             pathex=['./imagc/'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib', 'pyside2', 'tkinter', 'pygame', 'pyqt5'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='imagc',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon="./imagc/ima-icons/favicon-256x256.ico",
          disable_windowed_traceback=False,
          target_arch=['x86_64-linux-gnu', 'Win-x86_64'],
          codesign_identity='Nurul-GC',)
