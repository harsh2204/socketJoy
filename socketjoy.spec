# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import platform
from PyInstaller.utils.hooks import collect_submodules


APP = 'socketjoy'
block_cipher = None

hidden_imports = [
	'engineio.async_drivers.eventlet',
	*collect_submodules('eventlet.hubs'),
	*collect_submodules('dns'),
]

static_files = [(f'{APP}/static', 'static'), (f'{APP}/index.html', '.')]

linux_data = [
	(f'assets/tk.harshg.{APP}.desktop', 'usr/share/applications'),
	(f'assets/tk.harshg.{APP}.svg', 'usr/share/icons/hicolor'),
	(f'assets/tk.harshg.{APP}.appdata.xml', 'usr/share/metainfo'),
]

a = Analysis([f'{APP}/app.py'],
             pathex=[Path.cwd()],
             binaries=[],
             datas=static_files + linux_data,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=APP,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name=APP)
			   
try:
	launcher = Path(f'{DISTPATH}/{APP}/tk.harshg.{APP}.desktop')
	if launcher.exists():
		launcher.unlink()
	launcher.symlink_to(f'usr/share/applications/tk.harshg.{APP}.desktop')
	icon = Path(f'{DISTPATH}/{APP}/tk.harshg.{APP}.svg')
	if icon.exists():
		icon.unlink()
	icon.symlink_to(f'usr/share/icons/hicolor/tk.harshg.{APP}.svg')
	dir_icon = Path(f'{DISTPATH}/{APP}/.DirIcon')
	if dir_icon.exists():
		dir_icon.unlink()
	dir_icon.symlink_to(f'usr/share/icons/hicolor/tk.harshg.{APP}.svg')
	app_run = Path(f'{DISTPATH}/{APP}/AppRun')
	if app_run.exists():
		app_run.unlink()
	app_run.symlink_to(f'{APP}')
except Exception as e:
	print(f'ERROR CREATING SYMLINKS::{e.errno}')