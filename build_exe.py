"""
手术视频标注系统 - 打包工具（改进版）

使用方法：
    python build_exe.py

输出：dist/手术视频标注系统/ 文件夹，可直接分发给医生
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    print("=" * 60)
    print("  手术视频标注系统 - 打包工具")
    print("=" * 60)

    if sys.platform != 'win32':
        print("\n警告：当前不是 Windows 系统")
        print("建议在 Windows 上打包以获得最佳兼容性\n")

    # 1. 创建输出目录
    print("\n[1/4] 创建输出目录...")
    output_dir = Path('dist') / '手术视频标注系统'
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 2. 复制应用文件
    print("[2/4] 复制应用文件...")
    src_dir = Path(__file__).parent

    files_to_copy = [
        'annotation_app.py',
        'config.json',
        '启动系统.bat'
    ]

    for file in files_to_copy:
        src_file = src_dir / file
        if src_file.exists():
            shutil.copy2(src_file, output_dir / file)
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ 找不到 {file}")

    # 3. 创建 videos 目录
    print("[3/4] 创建数据目录...")
    videos_dir = output_dir / 'videos'
    videos_dir.mkdir(exist_ok=True)
    print(f"  ✓ {videos_dir}")

    # 4. 创建安装说明
    print("[4/4] 创建安装说明...")
    readme_content = """# 手术视频标注系统 安装说明

## 系统要求
- Windows 10 或更高版本
- Python 3.8 或更高版本

## 安装步骤

### 方法一：自动安装（推荐）
1. 双击 `启动系统.bat`
2. 程序会自动检测并安装依赖
3. 安装完成后会自动打开浏览器

### 方法二：手动安装
1. 打开命令提示符（cmd）
2. 进入此目录
3. 运行以下命令：
   ```
   pip install streamlit pandas
   streamlit run annotation_app.py
   ```

## 使用说明
1. 启动后浏览器会自动打开系统
2. 如未自动打开，手动访问 http://localhost:8501
3. 关闭命令行窗口将退出程序

## 常见问题

Q: 提示找不到 Python
A: 请先安装 Python：https://www.python.org/downloads/
   安装时勾选 "Add Python to PATH"

Q: 浏览器没有自动打开
A: 手动在浏览器中访问 http://localhost:8501

## 技术支持
如有问题请联系开发团队
"""

    readme_path = output_dir / '安装说明.txt'
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f"  ✓ {readme_path}")

    # 创建压缩包
    print("\n正在创建压缩包...")
    zip_path = Path('dist') / '手术视频标注系统.zip'
    if zip_path.exists():
        zip_path.unlink()

    # 使用 shutil 创建 zip
    shutil.make_archive(
        str(zip_path.with_suffix('')),
        'zip',
        Path('dist'),
        '手术视频标注系统'
    )

    print("\n" + "=" * 60)
    print("  打包完成！")
    print("=" * 60)
    print(f"\n输出目录: {output_dir.absolute()}")
    print(f"压缩包:   {zip_path.absolute()}")
    print("\n分发方式:")
    print("  将 '手术视频标注系统.zip' 发送给医生")
    print("  医生解压后双击 '启动系统.bat' 即可使用")
    print("\n注意事项:")
    print("  - 医生电脑需要安装 Python 3.8+")
    print("  - 首次运行会自动安装依赖")


if __name__ == '__main__':
    main()
