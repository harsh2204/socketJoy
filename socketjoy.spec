# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import platform
from PyInstaller.utils.hooks import collect_submodules


block_cipher = None

hidden_imports = [
	'engineio.async_drivers.eventlet',
	*collect_submodules('eventlet.hubs'),
	*collect_submodules('dns'),
]
static_files = [('socketjoy/static', 'static'), 
				('socketjoy/index.html', '.')
				]

windows_binaries = [
	('C:/Windows/System32/msvcp140.dll', '.'),
	('C:/Windows/System32/concrt140.dll', '.'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-runtime-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-heap-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-string-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-locale-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-stdio-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-filesystem-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-time-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-environment-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-math-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-convert-l1-1-0.dll', 'crt'),
	('C:/Windows/System32/downlevel/api-ms-win-crt-utility-l1-1-0.dll', 'crt'),
	('socketjoy/win/ViGEm/x64/ViGEmClient.dll', 'x64'),
	('socketjoy/win/ViGEm/x86/ViGEmClient.dll', 'x86'),
]


if platform.system() == 'Linux':
	a = Analysis(['socketjoy/app.py'],
				pathex=[Path.cwd()],
				binaries=[],
				datas=static_files,
				hiddenimports=hidden_imports,
				hookspath=[],
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
			name='socketjoy',
			debug=False,
			bootloader_ignore_signals=False,
			strip=False,
			upx=True,
			upx_exclude=[],
			runtime_tmpdir=None,
			console=True)
else:
	a = Analysis(
		['socketjoy/app.py'],
		pathex=[Path.cwd()],
		binaries=windows_binaries,
		datas= static_files,
		hiddenimports=hidden_imports,
		hookspath=[],
		runtime_hooks=[],
		excludes=[],
		win_no_prefer_redirects=False,
		win_private_assemblies=False,
		cipher=block_cipher,
		noarchive=False,
	)
	pyz = PYZ(
		a.pure,
		a.zipped_data,
		cipher=block_cipher,
	)
	exe = EXE(
		pyz,
		a.scripts,
		a.binaries,
		a.zipfiles,
		a.datas,
		[],
		name=APP,
		debug=DEBUG,
		bootloader_ignore_signals=False,
		strip=False,
		upx=True,
		upx_exclude=['vcruntime140.dll'],
		runtime_tmpdir=None,
		console=True,
		icon='socketjoy/static/socketjoy.ico',
		version='assets/version.rc',
	)