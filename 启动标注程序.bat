@echo off
chcp 65001 >nul
title 手术视频标注系统

echo ============================================
echo     手术视频标注系统 - 启动中...
echo ============================================
echo.

REM 切换到程序所在目录
cd /d "%~dp0"

REM 检查Python是否已安装
where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% neq 0 (
        echo [错误] 未检测到Python环境！
        echo.
        echo 请按照以下步骤安装：
        echo 1. 双击运行 "安装Python.bat"
        echo 2. 安装完成后，再次双击此文件启动程序
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

REM 检查是否首次运行（检查依赖是否已安装）
if not exist ".installed" (
    echo 首次运行，正在安装依赖包...
    %PYTHON_CMD% -m pip install -r requirements.txt -q
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo done > .installed
    echo 依赖安装完成！
    echo.
)

REM 检查videos目录
if not exist "videos" (
    echo [提示] 正在创建videos文件夹...
    mkdir videos
    echo 请将手术视频文件放入 videos 文件夹后重新运行程序
    pause
    exit /b 0
)

REM 检查videos目录及子目录是否有视频文件
dir /s /b videos\*.mp4 videos\*.avi videos\*.mov videos\*.mkv videos\*.wmv 2>nul | findstr . >nul
if %errorlevel% neq 0 (
    echo [警告] videos文件夹中没有视频文件！
    echo 请将手术视频文件放入 videos 文件夹或其子文件夹
    echo.
    pause
    exit /b 0
)

echo ============================================
echo  程序已启动！
echo  浏览器将自动打开，如未打开请查看下方控制台输出的访问地址
echo ============================================
echo.
echo  关闭此窗口将退出程序
echo.

REM 启动程序
%PYTHON_CMD% launcher.py

pause
