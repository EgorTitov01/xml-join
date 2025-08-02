# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['xml_join/scripts/start_join.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.ico', '.')],  # Включаем иконку в сборку
    hiddenimports=[
        'toga',
        'toga.core',
        'toga.window',
        'toga.app',
        'toga.box',
        'toga.label',
        'toga.button',
        'toga.main_window',
        'toga.style',
        'toga.style.pack',
        'lxml',
        'lxml.etree',
        'pyexcelerate',
        'pyexcelerate.Workbook',
        'pyexcelerate.Style',
        'pyexcelerate.Font',
        'xml_join',
        'xml_join.join',
        'xml_join.scripts',
        'xml_join.scripts.start_join',
        'pathlib',
        'os',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='XML Join',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False для GUI приложения
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Путь к иконке от корня проекта
) 