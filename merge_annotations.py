"""
标注数据合并与导出工具
用于将多位医生的标注数据合并，并导出为Excel/CSV格式

使用方法：
    python merge_annotations.py
"""

import json
import os
import pandas as pd
from pathlib import Path
from datetime import datetime


def merge_annotation_files(annotation_dir):
    """合并多个医生的标注文件"""
    all_records = []

    annotation_files = []
    for root, dirs, files in os.walk(annotation_dir):
        for file in files:
            if file == 'annotations.json':
                annotation_files.append(Path(root) / file)

    if not annotation_files:
        print("未找到任何标注文件！")
        print(f"请在 {annotation_dir} 目录下创建子目录，每个医生一个目录")
        return None

    print(f"找到 {len(annotation_files)} 个标注文件")

    for ann_file in annotation_files:
        doctor_name = ann_file.parent.name

        with open(ann_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for video_name, video_data in data.items():
            annotations = video_data.get('annotations', {})

            record = {
                '医生': doctor_name,
                '视频文件': video_name,
                '标注时间': video_data.get('annotated_at', ''),
                '图像质量': annotations.get('图像质量', ''),
                '离器械距离': annotations.get('离器械距离', ''),
                '腔壁风险-左侧': annotations.get('腔壁风险-左侧', ''),
                '腔壁风险-右侧': annotations.get('腔壁风险-右侧', ''),
                '腔壁风险-上方': annotations.get('腔壁风险-上方', ''),
                '腔壁风险-下方': annotations.get('腔壁风险-下方', ''),
                '备注': annotations.get('备注', '')
            }

            all_records.append(record)

    df = pd.DataFrame(all_records)
    return df


def print_statistics(df):
    """打印统计信息"""
    print("\n" + "="*60)
    print("标注统计信息")
    print("="*60)

    print(f"\n总标注记录数：{len(df)}")
    print(f"参与医生数：{df['医生'].nunique()}")
    print(f"标注视频数：{df['视频文件'].nunique()}")

    print("\n各医生标注数量：")
    print(df['医生'].value_counts().to_string())

    # 各分类的标签分布
    categories = ['图像质量', '离器械距离', '腔壁风险-左侧', '腔壁风险-右侧', '腔壁风险-上方', '腔壁风险-下方']

    for cat in categories:
        print(f"\n【{cat}】标签分布：")
        print(df[cat].value_counts().to_string())

    # 腔壁风险汇总统计
    print("\n" + "="*60)
    print("腔壁风险汇总统计")
    print("="*60)

    risk_cols = ['腔壁风险-左侧', '腔壁风险-右侧', '腔壁风险-上方', '腔壁风险-下方']
    for risk_level in ['危险', '警告', '安全']:
        count = sum((df[col] == risk_level).sum() for col in risk_cols)
        print(f"{risk_level}：{count} 次")


def main():
    print("="*60)
    print("  鼻内镜手术视频标注数据合并工具")
    print("="*60)

    current_dir = Path(__file__).parent
    annotations_dir = current_dir / "collected_annotations"

    if not annotations_dir.exists():
        print(f"\n请在当前目录下创建 'collected_annotations' 文件夹")
        print("目录结构示例：")
        print("  collected_annotations/")
        print("    ├── 医生A/")
        print("    │   └── annotations.json")
        print("    ├── 医生B/")
        print("    │   └── annotations.json")
        print("    └── 医生C/")
        print("        └── annotations.json")
        return

    df = merge_annotation_files(annotations_dir)
    if df is None or len(df) == 0:
        return

    print_statistics(df)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    excel_path = current_dir / f"merged_annotations_{timestamp}.xlsx"
    csv_path = current_dir / f"merged_annotations_{timestamp}.csv"

    df.to_excel(excel_path, index=False, engine='openpyxl')
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')

    print(f"\n数据已导出：")
    print(f"  Excel: {excel_path}")
    print(f"  CSV: {csv_path}")

    print("\n" + "="*60)
    print("合并完成！")
    print("="*60)


if __name__ == "__main__":
    main()
