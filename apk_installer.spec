# -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

#block_cipher = None


a = Analysis(['apk_installer.py'],
             pathex=['/Users/takam/Documents/program/kivy'],
             hiddenimports=[],
             #hookspath=None,
             runtime_hooks=None,)
             #cipher=block_cipher)
pyz = PYZ(a.pure,)
             #cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='apk_installer',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               Tree('.'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='apk_installer')
app = BUNDLE(coll,
             name='apk_installer.app',
             icon=None)
