"""
鼻内镜手术视频标注系统
专为医学专业人士设计的轻量化标注工具
"""

import streamlit as st
import json
import os
import sys
from pathlib import Path
from datetime import datetime


def get_bundle_dir():
    """返回应用资源所在目录"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def get_data_dir():
    """返回可写数据目录，打包后为 exe 同级目录"""
    data_dir = os.environ.get('NASAL_LABEL_DATA_DIR')
    if data_dir:
        path = Path(data_dir)
    else:
        path = get_bundle_dir()
    path.mkdir(exist_ok=True)
    return path


BUNDLE_DIR = get_bundle_dir()
DATA_DIR = get_data_dir()
MAX_VIDEO_SCAN_DEPTH = 3
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
TAIL_FRAME_SEEK_OFFSETS = (1, 2, 5, 10, 30, 60, 120)
LEGACY_VALUE_MAPS = {
    '内窥镜距器械距离': {
        '太近': '过近',
        '比较近': '过近',
        '合适': '合适',
        '比较远': '过远',
        '太远': '过远',
    },
    '距左腔壁': {
        '危险': '高风险',
        '警告': '中风险',
        '安全': '低风险',
        '即将接触': '高风险',
        '靠近': '中风险',
        '合适': '低风险',
    },
    '距右腔壁': {
        '危险': '高风险',
        '警告': '中风险',
        '安全': '低风险',
        '即将接触': '高风险',
        '靠近': '中风险',
        '合适': '低风险',
    },
}
LEGACY_FIELD_NAMES = {
    '内窥镜距器械距离': '离器械距离',
    '距左腔壁': '腔壁风险-左侧',
    '距右腔壁': '腔壁风险-右侧',
}

# 页面配置
st.set_page_config(
    page_title="鼻内镜手术视频标注系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.3rem;
        color: #333;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #1f77b4;
    }
    .category-label {
        font-size: 1rem;
        color: #555;
        font-weight: 600;
        margin-top: 0.8rem;
        margin-bottom: 0.3rem;
    }
    .video-container {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        background-color: #f9f9f9;
        margin-bottom: 1rem;
    }
    .frame-container {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        background-color: #f9f9f9;
        margin-bottom: 1rem;
    }
    .annotation-container {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        background-color: #ffffff;
    }
    .risk-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    .risk-item {
        padding: 0.5rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #fafafa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 28px;
        text-align: center;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    div[data-baseweb="select"] > div {
        background-color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)


def load_config():
    """加载配置文件"""
    config_path = DATA_DIR / "config.json"
    if not config_path.exists():
        config_path = BUNDLE_DIR / "config.json"

    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error("配置文件 config.json 不存在！")
        st.stop()


def scan_videos(max_depth=MAX_VIDEO_SCAN_DEPTH):
    """扫描 videos 目录及其子目录中的视频"""
    video_dir = DATA_DIR / "videos"
    video_dir.mkdir(exist_ok=True)

    videos = []

    for root, dirs, files in os.walk(video_dir):
        root_path = Path(root)
        relative_root = root_path.relative_to(video_dir)
        depth = 0 if relative_root == Path('.') else len(relative_root.parts)

        if depth >= max_depth:
            dirs[:] = []

        for filename in files:
            file = root_path / filename
            if file.suffix.lower() in VIDEO_EXTENSIONS:
                videos.append(file.relative_to(video_dir).as_posix())

    return sorted(videos, key=lambda name: name.lower())


def load_annotations():
    """加载已有的标注数据"""
    annotation_file = DATA_DIR / "annotations.json"
    if annotation_file.exists():
        with open(annotation_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_annotation(video_name, annotations):
    """保存单个视频的标注数据"""
    all_annotations = load_annotations()
    all_annotations[video_name] = {
        "annotations": annotations,
        "annotated_at": datetime.now().isoformat()
    }

    annotation_file = DATA_DIR / "annotations.json"
    with open(annotation_file, 'w', encoding='utf-8') as f:
        json.dump(all_annotations, f, ensure_ascii=False, indent=2)


@st.cache_data(show_spinner=False)
def extract_tail_frame(video_path, modified_time, file_size):
    """读取视频最后一个可解码帧，返回 RGB 图像数组"""
    try:
        import cv2
    except ImportError:
        return None, "缺少 opencv-python-headless，无法读取视频尾帧。"

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, "无法打开视频文件，尾帧读取失败。"

    try:
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        frame = None

        if frame_count > 0:
            for offset in TAIL_FRAME_SEEK_OFFSETS:
                start_index = max(frame_count - offset, 0)
                cap.set(cv2.CAP_PROP_POS_FRAMES, start_index)

                candidate = None
                while True:
                    success, current_frame = cap.read()
                    if not success or current_frame is None:
                        break
                    candidate = current_frame

                if candidate is not None:
                    frame = candidate
                    break
        else:
            while True:
                success, current_frame = cap.read()
                if not success or current_frame is None:
                    break
                frame = current_frame

        if frame is None:
            return None, "未能读取到视频尾帧。"

        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), None
    finally:
        cap.release()


def render_tail_frame(video_path):
    """渲染视频尾帧显示框"""
    st.markdown('<div class="frame-container">', unsafe_allow_html=True)
    st.subheader("🖼️ 视频尾帧")

    if not video_path.exists():
        st.warning("视频文件不存在，无法显示尾帧。")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    stat = video_path.stat()
    with st.spinner("正在读取视频尾帧..."):
        tail_frame, error = extract_tail_frame(str(video_path), stat.st_mtime, stat.st_size)

    if tail_frame is not None:
        st.image(tail_frame, caption="最后一个可解码画面", channels="RGB", width="stretch")
    else:
        st.warning(error or "尾帧读取失败。")

    st.markdown("</div>", unsafe_allow_html=True)


def get_annotation_value(annotations, field_name, default_value):
    """读取新字段，并尽量兼容旧标注字段"""
    if field_name in annotations:
        return annotations[field_name]

    legacy_field = LEGACY_FIELD_NAMES.get(field_name)
    if not legacy_field:
        return default_value

    legacy_value = annotations.get(legacy_field)
    return LEGACY_VALUE_MAPS.get(field_name, {}).get(legacy_value, default_value)


def widget_key(video_name, field_key):
    """为每个视频生成独立控件 key，避免切换视频时复用旧状态"""
    return f"{video_name}::{field_key}"


def select_annotation(field_name, label, category, annotations, default_value, key):
    """渲染单选标注项"""
    options = category['options']
    current_value = get_annotation_value(annotations, field_name, default_value)
    index = options.index(current_value) if current_value in options else options.index(default_value)

    return st.selectbox(
        label,
        options,
        index=index,
        key=key
    )


def initialize_session_state():
    """初始化会话状态"""
    if 'current_video_index' not in st.session_state:
        st.session_state.current_video_index = 0

    if 'config' not in st.session_state:
        st.session_state.config = load_config()

    if 'videos' not in st.session_state:
        st.session_state.videos = scan_videos()


def render_annotation_section(config, current_annotations, selected_video):
    """渲染标注区域"""
    categories = config['categories']

    video_annotations = {}

    # 第一部分：图像质量
    st.markdown('<div class="section-header">📷 图像质量</div>', unsafe_allow_html=True)
    cat = categories['图像质量']
    video_annotations['图像质量'] = st.selectbox(
        "选择图像质量状态",
        cat['options'],
        index=cat['options'].index(current_annotations.get('图像质量', cat['options'][0])) if current_annotations.get('图像质量') in cat['options'] else 0,
        key=widget_key(selected_video, 'img_quality')
    )

    # 第二部分：内窥镜距器械距离
    st.markdown('<div class="section-header">📏 内窥镜距器械距离</div>', unsafe_allow_html=True)
    cat = categories['内窥镜距器械距离']
    video_annotations['内窥镜距器械距离'] = select_annotation(
        '内窥镜距器械距离',
        "选择距离评估",
        cat,
        current_annotations,
        '合适',
        widget_key(selected_video, 'distance')
    )

    # 第三部分：内窥镜压迫腔壁风险
    st.markdown('<div class="section-header">⚠️ 内窥镜压迫腔壁的风险评估</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        cat = categories['距左腔壁']
        video_annotations['距左腔壁'] = select_annotation(
            '距左腔壁',
            "⬅️ 距左腔壁",
            cat,
            current_annotations,
            '低风险',
            widget_key(selected_video, 'risk_left')
        )

    with col2:
        cat = categories['距右腔壁']
        video_annotations['距右腔壁'] = select_annotation(
            '距右腔壁',
            "➡️ 距右腔壁",
            cat,
            current_annotations,
            '低风险',
            widget_key(selected_video, 'risk_right')
        )

    # 第四部分：上下方向偏移
    st.markdown('<div class="section-header">↕️ 上下方向偏移</div>', unsafe_allow_html=True)
    cat = categories['上下方向偏移']
    video_annotations['上下方向偏移'] = select_annotation(
        '上下方向偏移',
        "选择上下方向偏移状态",
        cat,
        current_annotations,
        '合适',
        widget_key(selected_video, 'vertical_offset')
    )

    # 备注
    st.markdown('<div class="section-header">📝 备注</div>', unsafe_allow_html=True)
    video_annotations['备注'] = st.text_area(
        "补充说明（可选）",
        value=current_annotations.get('备注', ''),
        height=80,
        placeholder="输入其他需要记录的信息...",
        key=widget_key(selected_video, 'notes')
    )

    return video_annotations


def main():
    """主函数"""
    initialize_session_state()

    # 标题
    st.markdown('<div class="main-header">🏥 鼻内镜手术视频标注系统</div>', unsafe_allow_html=True)

    # 检查视频文件
    if len(st.session_state.videos) == 0:
        st.error("⚠️ 未找到视频文件！")
        st.info("""
        **使用说明：**
        1. 在当前目录下创建 `videos` 文件夹
        2. 将手术视频文件放入该文件夹或其 3 级以内子文件夹
        3. 重新启动程序

        支持的视频格式：MP4, AVI, MOV, MKV, WMV
        """)
        return

    # 侧边栏
    with st.sidebar:
        st.header("📊 标注进度")

        all_annotations = load_annotations()
        total_videos = len(st.session_state.videos)
        annotated_count = sum(1 for video in st.session_state.videos if video in all_annotations)
        progress = annotated_count / total_videos if total_videos > 0 else 0

        st.metric("总视频数", total_videos)
        st.metric("已标注", annotated_count)
        st.metric("完成率", f"{progress:.1%}")

        st.progress(progress)

        st.markdown("---")
        st.header("🎬 视频导航")

        selected_video = st.selectbox(
            "选择视频",
            st.session_state.videos,
            index=st.session_state.current_video_index
        )

        st.session_state.current_video_index = st.session_state.videos.index(selected_video)

        st.markdown("---")
        st.header("ℹ️ 标注说明")
        st.markdown("""
        **标注维度：**
        1. **图像质量**：清晰/模糊/遮挡
        2. **内窥镜距器械距离**：过近/合适/过远
        3. **内窥镜压迫腔壁的风险评估**：距左腔壁/距右腔壁
        4. **上下方向偏移**：过于偏上/过于偏下/合适

        **操作流程：**
        1. 观看视频
        2. 选择各项标注
        3. 点击保存
        """)

    # 主内容区 - 左右布局
    col_video, col_anno = st.columns([3, 2])

    with col_video:
        # 视频播放区
        video_path = DATA_DIR / "videos" / Path(selected_video)
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.subheader(f"🎥 {selected_video}")

        if video_path.exists():
            with open(video_path, 'rb') as video_file:
                video_bytes = video_file.read()
                st.video(video_bytes)

        st.markdown("</div>", unsafe_allow_html=True)
        render_tail_frame(video_path)

    with col_anno:
        # 标注区
        st.markdown('<div class="annotation-container">', unsafe_allow_html=True)
        st.subheader("📝 标注信息")

        current_annotations = all_annotations.get(selected_video, {}).get('annotations', {})

        video_annotations = render_annotation_section(st.session_state.config, current_annotations, selected_video)

        st.markdown("---")

        # 保存按钮
        if st.button("💾 保存标注"):
            save_annotation(selected_video, video_annotations)
            st.success(f"✅ 标注已保存！")
            st.rerun()

        # 显示最后保存时间
        if selected_video in all_annotations:
            saved_time = all_annotations[selected_video]['annotated_at']
            st.caption(f"最后保存：{datetime.fromisoformat(saved_time).strftime('%Y-%m-%d %H:%M:%S')}")

        st.markdown("</div>", unsafe_allow_html=True)

    # 底部导航按钮
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 1.5, 1.5])

    with col1:
        if st.button("⏮️ 上一个", use_container_width=True):
            if st.session_state.current_video_index > 0:
                st.session_state.current_video_index -= 1
                st.rerun()

    with col2:
        st.info(f"**第 {st.session_state.current_video_index + 1} / {total_videos} 个**")

    with col3:
        # 快速状态概览
        if selected_video in all_annotations:
            st.success("✅ 已标注")
        else:
            st.warning("⏳ 待标注")

    with col4:
        if st.button("下一个 ⏭️", use_container_width=True):
            if st.session_state.current_video_index < total_videos - 1:
                st.session_state.current_video_index += 1
                st.rerun()

    with col5:
        unannotated = [v for v in st.session_state.videos if v not in all_annotations]
        if unannotated:
            if st.button("⏩ 下个未标注", use_container_width=True):
                next_video = unannotated[0]
                st.session_state.current_video_index = st.session_state.videos.index(next_video)
                st.rerun()


if __name__ == "__main__":
    main()
