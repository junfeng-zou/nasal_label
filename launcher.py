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
import threading
import time
import webbrowser
from pathlib import Path

# 获取当前目录
CURRENT_DIR = Path(__file__).parent

def find_free_port():
    """查找可用端口"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        return s.getsockname()[1]


def start_streamlit():
    """启动 Streamlit 服务"""
    port = find_free_port()

    # 应用文件路径
    if hasattr(sys, '_MEIPASS'):
        app_path = Path(sys._MEIPASS) / 'annotation_app.py'
        config_path = Path(sys._MEIPASS) / 'config.json'
    else:
        app_path = CURRENT_DIR / 'annotation_app.py'
        config_path = CURRENT_DIR / 'config.json'

    # 确保 videos 目录存在
    videos_dir = CURRENT_DIR / 'videos'
    videos_dir.mkdir(exist_ok=True)

    print(f"\n正在启动服务器...")
    print(f"访问地址：http://localhost:{port}")

    # 启动 Streamlit
    cmd = [
        sys.executable if not hasattr(sys, '_MEIPASS') else sys.executable,
        '-m', 'streamlit', 'run',
        str(app_path),
        '--server.port', str(port),
        '--server.headless', 'false',
        '--browser.gatherUsageStats', 'false',
        '--server.fileWatcherType', 'none'
    ]

    process = subprocess.Popen(cmd)

    # 等待服务启动并打开浏览器
    time.sleep(3)
    url = f"http://localhost:{port}"
    try:
        webbrowser.open(url)
    except Exception:
        pass  # 浏览器可能无法自动打开

    print("\n手术视频标注系统已启动！")
    print("=" * 50)
    print("关闭此窗口将退出程序")
    print("=" * 50)

    # 保持进程运行直到用户关闭
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()


if __name__ == '__main__':
    print("=" * 60)
    print("   手术视频标注系统 v1.0.0")
    print("=" * 60)

    start_streamlit()