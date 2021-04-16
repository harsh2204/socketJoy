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
windows_data = [
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
else:
    a = Analysis(
        [f'{APP}/app.py'],
        pathex=[Path.cwd()],
        binaries=windows_data,
        datas=[],
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
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=['vcruntime140.dll'],
        runtime_tmpdir=None,
        console=True,
        icon=f'assets/tk.harshg.{APP}.ico',
        version='assets/version.rc',
    )