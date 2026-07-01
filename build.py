"""
自动打包脚本
在 Windows 上运行此脚本来生成 .exe 文件

使用方法：
    python build.py

注意：
    打包过程需要在 Windows 系统上进行
    程序会在 build/ 目录下生成 .exe 文件
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path


def configure_utf8_output():
    """确保 Windows CI 控制台可以输出中文日志"""
    os.environ.setdefault('PYTHONUTF8', '1')
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')


def install_dependencies():
    """安装打包所需的依赖"""
    print("安装打包依赖...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)

    requirements = Path('requirements.txt')
    if requirements.exists():
        subprocess.run([
            sys.executable, '-m', 'pip', 'install',
            '-r', str(requirements), 'pyinstaller'
        ], check=True)
    else:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install',
            'pyinstaller', 'streamlit', 'pandas'
        ], check=True)


def build_exe():
    """执行打包"""
    print("\n开始打包...")

    # 使用 PyInstaller 打包
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        'build.spec',
        '--clean',
        '--noconfirm'
    ], check=True)

    print("\n打包完成！")
    print(f"输出目录：dist/手术视频标注系统")
    print(f"主程序：dist/手术视频标注系统/手术视频标注系统.exe")


def copy_to_dist():
    """复制必要的文件到输出目录"""
    dist_dir = Path('dist') / '手术视频标注系统'
    dist_dir.mkdir(parents=True, exist_ok=True)

    # 创建 videos 目录
    videos_dir = dist_dir / 'videos'
    videos_dir.mkdir(exist_ok=True)

    config_file = Path('config.json')
    if config_file.exists():
        shutil.copy2(config_file, dist_dir / 'config.json')

    usage_file = Path('使用说明.txt')
    if usage_file.exists():
        shutil.copy2(usage_file, dist_dir / '使用说明.txt')

    print(f"输出目录：{dist_dir.absolute()}")


def main():
    print("=" * 60)
    print("  手术视频标注系统 - 打包脚本")
    print("=" * 60)

    # 检查是否在 Windows 上
    if sys.platform != 'win32':
        print("\n警告：当前不是 Windows 系统！")
        print("打包后的 .exe 只能在 Windows 上运行。")
        print("是否继续？(y/n): ", end='')
        choice = input().strip().lower()
        if choice != 'y':
            return

    try:
        install_dependencies()
        build_exe()
        copy_to_dist()

        print("\n" + "=" * 60)
        print("  打包成功！")
        print("=" * 60)
        print("\n输出文件：")
        print("  dist/手术视频标注系统/手术视频标注系统.exe")
        print("  dist/手术视频标注系统/videos/  (将视频放入此目录)")
        print("\n分发给医生：")
        print("  1. 将 dist/手术视频标注系统/ 目录压缩为 zip 文件")
        print("  2. 医生解压后，双击 手术视频标注系统.exe 即可运行")

    except Exception as e:
        print(f"\n打包失败：{e}")
        sys.exit(1)


if __name__ == '__main__':
    configure_utf8_output()
    main()
