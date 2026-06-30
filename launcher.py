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

    # 应用文件路径 - PyInstaller 打包后的路径处理
    if hasattr(sys, '_MEIPASS'):
        # 打包后的路径
        base_path = Path(sys._MEIPASS)
        app_path = base_path / 'annotation_app.py'
        config_path = base_path / 'config.json'
        # 工作目录设为 exe 所在目录
        work_dir = Path(sys.executable).parent
    else:
        # 开发环境
        app_path = CURRENT_DIR / 'annotation_app.py'
        config_path = CURRENT_DIR / 'config.json'
        work_dir = CURRENT_DIR

    # 确保 videos 目录存在
    videos_dir = work_dir / 'videos'
    videos_dir.mkdir(exist_ok=True)

    print(f"\n正在启动服务器...")
    print(f"访问地址：http://localhost:{port}")
    print(f"工作目录：{work_dir}")

    # 启动 Streamlit - 使用 headless 模式，不自动打开浏览器
    cmd = [
        sys.executable,
        '-m', 'streamlit', 'run',
        str(app_path),
        '--server.port', str(port),
        '--server.headless', 'true',  # 改为 true，禁止 Streamlit 自动打开浏览器
        '--browser.gatherUsageStats', 'false',
        '--server.fileWatcherType', 'none'
    ]

    # 设置工作目录
    os.chdir(work_dir)

    process = subprocess.Popen(cmd)

    # 等待服务启动
    time.sleep(2)
    url = f"http://localhost:{port}"

    # 只打开一次浏览器
    print(f"\n正在打开浏览器...")
    webbrowser.open(url)

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
    print("   手术视频标注系统 v1.0.0")
    print("=" * 60)

    start_streamlit()