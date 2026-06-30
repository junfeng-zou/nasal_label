@echo off
chcp 65001 >nul
title 手术视频标注系统

echo ============================================================
echo    手术视频标注系统 v1.0.1
echo ============================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查是否安装了必要的库
echo [检查依赖...]
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install streamlit pandas
)

REM 启动 Streamlit
echo.
echo [启动服务器...]
echo 系统将在浏览器中自动打开
echo 关闭此窗口将退出程序
echo.

streamlit run annotation_app.py --server.headless=false --browser.gatherUsageStats=false

pause
