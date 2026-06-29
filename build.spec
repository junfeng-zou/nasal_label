# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 配置文件
用于打包手术视频标注系统为 Windows .exe
"""

import sys
from pathlib import Path

block_cipher = None

# 获取当前目录
current_dir = Path(SPECPATH)

a = Analysis(
    ['launcher.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=[
        ('annotation_app.py', '.'),
        ('config.json', '.'),
        ('videos', 'videos'),  # 包含示例视频目录结构
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner',
        'pandas',
        'json',
        'datetime',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy.testing'],
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
    name='手术视频标注系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if (current_dir / 'icon.ico').exists() else None,
)