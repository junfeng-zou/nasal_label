"""
手术视频标注系统 - 独立桌面应用程序
使用 PyInstaller 打包为 .exe

使用方法：
    python build_exe.py  # 在 Windows 上运行此脚本打包
    dist/手术视频标注系统.exe  # 打包后的可执行文件
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# 获取当前目录
CURRENT_DIR = Path(__file__).parent if not hasattr(sys, '_MEIPASS') else Path(sys._MEIPASS)


def find_free_port():
    """查找可用端口"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        return s.getsockname()[1]


def get_python_executable():
    """获取 Python 解释器路径"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后，需要找到嵌入式 Python
        # PyInstaller 会将 Python 带到 dist 目录
        base_dir = Path(sys._MEIPASS)

        # 可能的 Python 位置
        possible_paths = [
            base_dir / 'python.exe',
            base_dir / 'python3.exe',
            Path(sys.executable).parent / 'python.exe',
        ]

        for path in possible_paths:
            if path.exists():
                return str(path)

        # 如果都找不到，尝试使用 sys.executable 的父目录
        return str(Path(sys.executable).parent / 'python.exe')
    else:
        # 开发环境
        return sys.executable


def start_streamlit():
    """启动 Streamlit 服务"""
    port = find_free_port()

    # 应用文件路径
    if hasattr(sys, '_MEIPASS'):
        # 打包后的路径
        app_path = Path(sys._MEIPASS) / 'annotation_app.py'
        work_dir = Path(sys.executable).parent
    else:
        # 开发环境
        app_path = CURRENT_DIR / 'annotation_app.py'
        work_dir = CURRENT_DIR

    # 确保 videos 目录存在
    videos_dir = work_dir / 'videos'
    videos_dir.mkdir(exist_ok=True)

    print(f"\n正在启动服务器...")
    print(f"访问地址：http://localhost:{port}")
    print(f"工作目录：{work_dir}")

    # 设置工作目录
    os.chdir(work_dir)

    # 启动 Streamlit
    python_exe = get_python_executable()
    print(f"Python 路径: {python_exe}")

    cmd = [
        python_exe,
        '-m', 'streamlit', 'run',
        str(app_path),
        '--server.port', str(port),
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false',
        '--server.fileWatcherType', 'none'
    ]

    try:
        process = subprocess.Popen(cmd)
    except Exception as e:
        print(f"\n错误: 无法启动服务器")
        print(f"原因: {e}")
        print("\n按任意键退出...")
        input()
        sys.exit(1)

    # 等待服务启动
    max_wait = 10
    print(f"\n等待服务器启动...")
    for i in range(max_wait):
        time.sleep(1)
        print(f"  {i+1}/{max_wait} 秒...")
        # 检查进程是否还活着
        if process.poll() is not None:
            print(f"\n错误: 服务器意外退出 (退出码: {process.returncode})")
            print("按任意键退出...")
            input()
            sys.exit(1)

    url = f"http://localhost:{port}"

    # 打开浏览器
    print(f"\n正在打开浏览器: {url}")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"无法自动打开浏览器: {e}")
        print(f"请手动访问: {url}")

    print("\n" + "=" * 50)
    print("  手术视频标注系统已启动！")
    print("  请在浏览器中使用系统")
    print("  关闭此窗口将退出程序")
    print("=" * 50)

    # 保持进程运行直到用户关闭
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n正在关闭程序...")
        process.terminate()
        process.wait()


if __name__ == '__main__':
    print("=" * 60)
    print("   手术视频标注系统 v1.0.1")
    print("=" * 60)

    start_streamlit()
