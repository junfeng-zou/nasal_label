"""
手术视频标注系统 - 独立桌面应用程序
使用 PyInstaller 打包为 .exe

使用方法：
    python build.py  # 在 Windows 上运行此脚本打包
    dist/手术视频标注系统/手术视频标注系统.exe  # 打包后的可执行文件
"""

import os
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

# 获取程序和资源目录
BUNDLE_DIR = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
RUNTIME_DIR = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else BUNDLE_DIR


def find_free_port():
    """查找可用端口"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        return s.getsockname()[1]


def open_browser_when_ready(url, timeout=30):
    """等待 Streamlit 服务就绪后打开一次浏览器"""
    health_url = f"{url}/_stcore/health"
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            with urllib.request.urlopen(health_url, timeout=1) as response:
                if response.status == 200:
                    webbrowser.open(url)
                    return
        except Exception:
            time.sleep(0.5)

    print(f"浏览器未能自动打开，请手动访问: {url}")


def start_streamlit():
    """启动 Streamlit 服务"""
    port = find_free_port()

    # 应用文件路径
    app_path = BUNDLE_DIR / 'annotation_app.py'
    work_dir = RUNTIME_DIR

    # 确保 videos 目录存在
    videos_dir = work_dir / 'videos'
    videos_dir.mkdir(exist_ok=True)
    os.environ['NASAL_LABEL_DATA_DIR'] = str(work_dir)

    print(f"\n正在启动服务器...")
    print(f"访问地址：http://localhost:{port}")
    print(f"工作目录：{work_dir}")

    # 设置工作目录
    os.chdir(work_dir)

    url = f"http://localhost:{port}"
    print(f"\n等待服务器启动，稍后将打开浏览器: {url}")

    print("\n" + "=" * 50)
    print("  手术视频标注系统已启动！")
    print("  请在浏览器中使用系统")
    print("  关闭此窗口将退出程序")
    print("=" * 50)

    try:
        from streamlit.web import cli as stcli

        threading.Thread(
            target=open_browser_when_ready,
            args=(url,),
            daemon=True
        ).start()

        sys.argv = [
            'streamlit',
            'run',
            str(app_path),
            f'--server.port={port}',
            '--server.headless=true',
            '--browser.gatherUsageStats=false',
            '--server.fileWatcherType=none',
            '--global.developmentMode=false',
        ]
        stcli.main()
    except KeyboardInterrupt:
        print("\n正在关闭程序...")
    except Exception as e:
        print(f"\n错误: 无法启动服务器")
        print(f"原因: {e}")
        print("\n按任意键退出...")
        input()
        sys.exit(1)


if __name__ == '__main__':
    print("=" * 60)
    print("   手术视频标注系统 v1.0.1")
    print("=" * 60)

    start_streamlit()
