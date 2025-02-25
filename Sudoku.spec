# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Sudoku.py'],
    pathex=[],
    binaries=[],
    datas=[('0.png', '.'), ('1.png', '.'), ('2.png', '.'), ('3.png', '.'), ('4.png', '.'), ('5.png', '.'), ('6.png', '.'), ('7.png', '.'), ('8.png', '.'), ('9.png', '.'), ('1_button.png', '.'), ('2_button.png', '.'), ('3_button.png', '.'), ('4_button.png', '.'), ('5_button.png', '.'), ('6_button.png', '.'), ('7_button.png', '.'), ('8_button.png', '.'), ('9_button.png', '.'), ('10_button.png', '.'), ('no.png', '.'), ('quit.png', '.'), ('quit_prompt.png', '.'), ('skip.png', '.'), ('skip_prompt.png', '.'), ('start.png', '.'), ('yes.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Sudoku',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
