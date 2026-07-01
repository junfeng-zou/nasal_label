# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 配置文件
用于打包手术视频标注系统为 macOS .app
"""

from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules, copy_metadata

block_cipher = None
current_dir = Path(SPECPATH)


def safe_collect_data(package):
    try:
        return collect_data_files(package)
    except Exception:
        return []


def safe_collect_submodules(package):
    try:
        return collect_submodules(package)
    except Exception:
        return []


def safe_copy_metadata(package):
    try:
        return copy_metadata(package)
    except Exception:
        return []


def safe_collect_dynamic_libs(package):
    try:
        return collect_dynamic_libs(package)
    except Exception:
        return []


datas = [
    ('annotation_app.py', '.'),
    ('config.json', '.'),
]
datas += safe_collect_data('streamlit')
datas += safe_copy_metadata('streamlit')
datas += safe_copy_metadata('altair')
datas += safe_copy_metadata('pydeck')
datas += safe_copy_metadata('pandas')
datas += safe_copy_metadata('opencv-python-headless')

binaries = []
binaries += safe_collect_dynamic_libs('cv2')

hiddenimports = [
    'cv2',
    'pandas',
    'json',
    'datetime',
    'pathlib',
]
hiddenimports += safe_collect_submodules('streamlit')

a = Analysis(
    ['launcher.py'],
    pathex=[str(current_dir)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy.testing'],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='手术视频标注系统',
    debug=False,
    bootloader_ignore_signals=False,
    exclude_binaries=True,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='手术视频标注系统',
)

app = BUNDLE(
    coll,
    name='手术视频标注系统.app',
    icon='icon.icns' if (current_dir / 'icon.icns').exists() else None,
    bundle_identifier='com.nasallabel.annotation',
    info_plist={
        'NSHighResolutionCapable': True,
    },
)
