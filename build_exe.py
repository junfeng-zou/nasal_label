"""
手术视频标注系统 - 打包工具
使用方法：
    python build_exe.py

注意：需要在 Windows 系统上运行此脚本
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def check_environment():
    """检查运行环境"""
    if sys.platform != 'win32':
        print("错误：当前不是 Windows 系统！")
        print("请在 Windows 系统上运行此脚本来生成 .exe 文件")
        sys.exit(1)

    # 检查是否安装了必要的依赖
    required = ['pyinstaller', 'streamlit']
    for pkg in required:
        try:
            __import__(pkg.replace('-', '_'))
        except ImportError:
            print(f"缺少 {pkg}，正在安装...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', pkg], check=True)


def clean_build():
    """清理构建目录"""
    if (Path('build') / 'dist').exists():
        shutil.rmtree(Path('build') / 'dist')
    if (Path('build') / '__pycache__').exists():
        shutil.rmtree(Path('build') / '__pycache__')


def copy_files():
    """复制必要文件到输出目录"""
    output = Path('build') / 'dist'
    output.mkdir(parents=True, exist_ok=True)

    # 复制主程序
    src = Path(__file__).parent
    dst = output / '手术视频标注系统.exe'
    shutil.copy(src / 'launcher.py', dst)
    shutil.copy(src / 'annotation_app.py', dst)
    shutil.copy(src / 'config.json', dst)

    # 复制 videos 目录
    videos_src = src / 'videos'
    videos_dst = output / 'videos'
    if videos_src.exists():
        shutil.copytree(videos_src, videos_dst)

    return output


def main():
    print("=" * 60)
    print("  手术视频标注系统 - 打包工具")
    print("=" * 60)

    check_environment()

    print("\n开始打包...")

    # 执行 PyInstaller
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--name=手术视频标注系统',
        '--noconfirm',
        '--onedir',
        'launcher.py'
    ])

    # 复制额外文件
    output = copy_files()

    print("\n" + "=" * 60)
    print("  打包完成！")
    print("=" * 60)
    print(f"\n输出目录：{output.absolute()}")
    print("\n分发给医生：")
    print("  将整个 output/ 目录压缩为 zip 文件发送给医生")
    print("  医生解压后，双击 手术视频标注系统.exe 即可运行")


if __name__ == '__main__':
    main()