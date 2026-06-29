"""
测试脚本 - 用于验证标注系统是否正常工作

使用方法：
    python test_app.py

功能：
    1. 检查依赖是否安装
    2. 检查文件结构是否完整
    3. 模拟启动标注程序
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖包"""
    print("检查依赖包...")

    required_packages = ['streamlit', 'pandas']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package} 已安装")
        except ImportError:
            print(f"  ✗ {package} 未安装")
            missing_packages.append(package)

    if missing_packages:
        print("\n缺少依赖包，请运行以下命令安装：")
        print(f"pip install {' '.join(missing_packages)}")
        return False

    return True


def check_file_structure():
    """检查文件结构"""
    print("\n检查文件结构...")

    required_files = [
        'annotation_app.py',
        'config.json',
        'requirements.txt',
        '启动标注程序.bat',
        '医生使用说明.md'
    ]

    all_exist = True
    for file in required_files:
        file_path = Path(__file__).parent / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} 缺失")
            all_exist = False

    # 检查videos文件夹
    videos_dir = Path(__file__).parent / 'videos'
    if videos_dir.exists():
        video_files = list(videos_dir.glob('*'))
        video_count = len([f for f in video_files if f.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.wmv']])
        print(f"  ✓ videos文件夹存在，包含 {video_count} 个视频文件")
    else:
        print(f"  ✗ videos文件夹不存在")
        all_exist = False

    return all_exist


def test_launch():
    """测试启动程序"""
    print("\n测试启动程序...")

    try:
        import streamlit.web.cli as st_cli
        print("  ✓ Streamlit模块可正常导入")

        print("\n启动测试服务器...")
        print("  访问地址：http://localhost:8501")
        print("  按 Ctrl+C 可停止测试服务器")

        # 启动Streamlit（测试模式）
        os.system("streamlit run annotation_app.py")

    except Exception as e:
        print(f"  ✗ 启动失败：{e}")
        return False

    return True


def main():
    print("="*50)
    print("  手术视频标注系统 - 测试脚本")
    print("="*50)

    # 切换到脚本所在目录
    os.chdir(Path(__file__).parent)

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 检查文件结构
    if not check_file_structure():
        print("\n文件结构不完整，请检查缺失文件")
        sys.exit(1)

    print("\n" + "="*50)
    print("  所有检查通过！系统可以正常使用")
    print("="*50)

    # 询问是否启动测试
    print("\n是否启动测试服务器？(y/n)")
    choice = input().strip().lower()

    if choice == 'y':
        test_launch()


if __name__ == "__main__":
    main()