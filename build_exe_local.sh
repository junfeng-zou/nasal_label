#!/bin/bash
# 在 Windows 上手动执行以下命令：

echo "=== 手术视频标注系统 - 本地构建 ==="

# 1. 安装依赖
pip install pyinstaller streamlit pandas

# 2. 清理旧的构建
rm -rf build dist
mkdir -p build/dist

# 3. 使用 PyInstaller 打包
pyinstaller --clean --name=手术视频标注系统 --onedir --noconfirm launcher.py

# 4. 复制配置文件
cp annotation_app.py dist/手术视频标注系统/
cp config.json dist/手术视频标注系统/
mkdir -p dist/手术视频标注系统/videos

# 5. 创建 zip 包
cd dist
zip -r "手术视频标注系统.zip" "手术视频标注系统/"

echo ""
echo "=== 构建完成 ==="
echo "ZIP 文件位置: $(pwd)/手术视频标注系统.zip"
echo ""
echo "使用方法："
echo "  1. 解压到任意目录"
echo "  2. 进入 手术视频标注系统 文件夹"
echo "  3. 双击 手术视频标注系统.exe 启动"
echo "  4. 等待浏览器自动打开或手动访问 http://localhost:8501"
