#!/bin/bash
# 在 Git Bash、WSL 或 Linux shell 中执行

echo "=== 手术视频标注系统 - 本地构建 ==="

# 1. 安装依赖
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller

# 2. 清理旧的构建
rm -rf build dist

# 3. 使用 PyInstaller 打包
pyinstaller build.spec --clean --noconfirm

# 4. 准备可写数据目录和配置文件
cp config.json dist/手术视频标注系统/
mkdir -p dist/手术视频标注系统/videos
cat > dist/手术视频标注系统/使用说明.txt <<'EOF'
双击“手术视频标注系统.exe”启动程序。
请将需要标注的视频放入同级 videos 文件夹。
标注结果会保存为同级 annotations.json。
EOF

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
echo "  4. 等待浏览器自动打开，或按控制台显示的地址手动访问"
