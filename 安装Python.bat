@echo off
chcp 65001 >nul
title 安装Python环境

echo ============================================
echo     手术视频标注系统 - 环境安装
echo ============================================
echo.

REM 切换到程序所在目录
cd /d "%~dp0"

REM 检查Python是否已安装
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo Python已安装：
    python --version
    echo.
    echo 跳过安装步骤
    pause
    exit /b 0
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    echo Python已安装：
    py --version
    echo.
    echo 跳过安装步骤
    pause
    exit /b 0
)

echo 未检测到Python，正在下载安装包...
echo.
echo 请注意：
echo 1. 安装程序启动后，请勾选 "Add Python to PATH"
echo 2. 点击 "Install Now" 进行安装
echo 3. 安装完成后，重新双击 "启动标注程序.bat"
echo.

REM 检测系统位数并下载对应的Python安装包
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set PYTHON_INSTALLER=python-3.11.7-amd64.exe
) else (
    set PYTHON_INSTALLER=python-3.11.7.exe
)

set PYTHON_URL=https://www.python.org/ftp/python/3.11.7/%PYTHON_INSTALLER%

echo 正在下载 %PYTHON_INSTALLER% ...
echo 下载地址：%PYTHON_URL%
echo.

REM 使用PowerShell下载
powershell -Command "& { try { Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%' -UseBasicParsing } catch { Write-Host '下载失败，请手动下载：' ; Write-Host '%PYTHON_URL%' } }"

if exist "%PYTHON_INSTALLER%" (
    echo 下载完成，正在启动安装程序...
    start "" "%PYTHON_INSTALLER%"
) else (
    echo.
    echo [错误] 自动下载失败
    echo 请手动下载Python并安装：
    echo 下载地址：%PYTHON_URL%
    echo 安装时请务必勾选 "Add Python to PATH"
)

echo.
pause
