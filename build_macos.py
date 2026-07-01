"""
macOS 打包脚本。

输出目录：
    dist/手术视频标注系统-macOS/
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def configure_utf8_output():
    os.environ.setdefault('PYTHONUTF8', '1')
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')


def install_dependencies():
    print("安装 macOS 打包依赖...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
    subprocess.run([
        sys.executable, '-m', 'pip', 'install',
        '-r', 'requirements.txt', 'pyinstaller'
    ], check=True)


def build_app():
    print("\n开始打包 macOS .app...")
    subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        'build_macos.spec',
        '--clean',
        '--noconfirm',
    ], check=True)


def find_built_app():
    dist_dir = Path('dist')
    candidates = sorted(dist_dir.rglob('手术视频标注系统.app'))
    if not candidates:
        raise FileNotFoundError("未找到打包后的 手术视频标注系统.app")
    return candidates[0]


def prepare_distribution():
    built_app = find_built_app()
    output_dir = Path('dist') / '手术视频标注系统-macOS'

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(built_app, output_dir / built_app.name, symlinks=True)

    for filename in ['config.json', '使用说明.txt']:
        source = Path(filename)
        if source.exists():
            shutil.copy2(source, output_dir / filename)

    (output_dir / 'videos').mkdir(exist_ok=True)

    macos_note = output_dir / 'macOS打开说明.txt'
    macos_note.write_text(
        "如果 macOS 提示“无法验证开发者”或阻止打开：\n"
        "1. 先尝试右键点击“手术视频标注系统.app”，选择“打开”。\n"
        "2. 如果仍无法打开，可在终端进入本文件夹后运行：\n"
        "   xattr -dr com.apple.quarantine 手术视频标注系统.app\n"
        "3. 然后再次双击“手术视频标注系统.app”。\n",
        encoding='utf-8'
    )

    print("\nmacOS 打包完成！")
    print(f"输出目录：{output_dir.resolve()}")


def main():
    print("=" * 60)
    print("  手术视频标注系统 - macOS 打包脚本")
    print("=" * 60)

    if sys.platform != 'darwin':
        print("\n错误：macOS .app 必须在 macOS 环境中打包。")
        sys.exit(1)

    install_dependencies()
    build_app()
    prepare_distribution()


if __name__ == '__main__':
    configure_utf8_output()
    main()
