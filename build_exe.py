"""
兼容旧命令的打包入口。

推荐使用：
    python build.py

旧命令仍可使用：
    python build_exe.py
"""

from build import main


if __name__ == '__main__':
    main()
