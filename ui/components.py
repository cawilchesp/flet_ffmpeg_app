import flet as ft

# Title Card Components
title_card_title = ft.Text(style="headlineMedium", expand=True)
theme_icon = ft.IconButton()
lang_dropdown = ft.Dropdown(
    options=[
        ft.dropdown.Option("es", "Español (ES)"),
        ft.dropdown.Option("en", "English (EN)"),
    ],
    width=180,
)

# File Select Card Components
select_file_button = ft.ElevatedButton()
select_folder_button = ft.ElevatedButton()
selected_path = ft.TextField(expand=True)
select_output_button = ft.ElevatedButton()
output_folder_path = ft.TextField(expand=True)

# Video Info Card Components
video_info_title = ft.Text(style="titleMedium")
video_info_text = ft.Text()
video_filename_text = ft.Text()
video_filename_value = ft.Text()
video_duration_text = ft.Text()
video_duration_value = ft.Text()
video_size_text = ft.Text()
video_size_value = ft.Text()
video_bitrate_text = ft.Text()
video_bitrate_value = ft.Text()
video_resolution_text = ft.Text()
video_resolution_value = ft.Text()
video_codec_text = ft.Text()
video_codec_value = ft.Text()
video_frame_rate_text = ft.Text()
video_frame_rate_value = ft.Text()
video_total_frames_text = ft.Text()
video_total_frames_value = ft.Text()

# Conversion Parameters Card Components
conversion_card_title = ft.Text(style="titleMedium")
scale_filter = ft.Checkbox(value=False)
width_field = ft.TextField(width=120)
height_field = ft.TextField(width=120)
keep_aspect = ft.Checkbox(value=True)
bitrate_filter = ft.Checkbox(value=False)
video_bitrate = ft.TextField(width=200)
crf_filter = ft.Checkbox(value=False)
crf = ft.TextField(width=200)
output_format = ft.Checkbox(value=False)
output_dropdown = ft.Dropdown(
    options=[
        ft.dropdown.Option("mp4"),
        ft.dropdown.Option("mkv"),
        ft.dropdown.Option("mov"),
        ft.dropdown.Option("avi"),
        ft.dropdown.Option("webm"),
    ],
    width=200,
)
codec_filter = ft.Checkbox(value=False)
video_codec = ft.Dropdown(
    options=[
        ft.dropdown.Option("libx264", "libx264 (CPU)"),
        ft.dropdown.Option("libx265", "libx265 (CPU)"),
        ft.dropdown.Option("mpeg4", "mpeg4 (CPU)"),
        ft.dropdown.Option("copy", "copy (sin recodificar)"),
        ft.dropdown.Option("h264_nvenc", "h264_nvenc (NVIDIA GPU)"),
        ft.dropdown.Option("hevc_nvenc", "hevc_nvenc (NVIDIA GPU)"),
    ],
    width=200,
)
preset_options_cpu = [
    ft.dropdown.Option("ultrafast", "ultrafast (muy rápido, menor compresión)"),
    ft.dropdown.Option("superfast", "superfast"),
    ft.dropdown.Option("veryfast", "veryfast"),
    ft.dropdown.Option("faster", "faster"),
    ft.dropdown.Option("fast", "fast"),
    ft.dropdown.Option("medium", "medium (por defecto)"),
    ft.dropdown.Option("slow", "slow"),
    ft.dropdown.Option("slower", "slower"),
    ft.dropdown.Option("veryslow", "veryslow (mejor compresión, más lento)"),
]
preset_options_nvenc = [
    ft.dropdown.Option("p1", "P1 (balanceado)"),
    ft.dropdown.Option("p2", "P2 (mejor compresión/calidad)"),
    ft.dropdown.Option("p3", "P3 (más rápido)"),
    ft.dropdown.Option("p4", "P4 (alta calidad)"),
    ft.dropdown.Option("p5", "P5 (alto rendimiento)"),
    ft.dropdown.Option("p6", "P6 (baja latencia)"),
    ft.dropdown.Option("p7", "P7 (baja latencia, alta calidad)"),
]
preset = ft.Dropdown(options=preset_options_cpu, width=200)
tune_options_nvenc = [
    ft.dropdown.Option("hq", "HQ (High Quality)"),
    ft.dropdown.Option("ll", "LL (Low Latency)"),
    ft.dropdown.Option("ull", "ULL (Ultra Low Latency)"),
    ft.dropdown.Option("lossless", "Lossless"),
]
tune_dropdown = ft.Dropdown(options=tune_options_nvenc, width=200)

frame_rate_filter = ft.Checkbox(value=False)
frame_rate = ft.TextField(width=200)
mi_mode_dropdown = ft.Dropdown(
    options=[
        ft.dropdown.Option("dup", "Duplicate"),
        ft.dropdown.Option("blend", "Blend"),
        ft.dropdown.Option("mci", "Motion Compensated Interpolation"),
    ],
    width=330,
    value="dup",
)
mc_mode_dropdown = ft.Dropdown(
    options=[
        ft.dropdown.Option("obmc", "Overlapped Block Motion Compensation"),
        ft.dropdown.Option(
            "aobmc", "Adaptive Overlapped Block Motion Compensation"
        ),
    ],
    width=450,
    value="aobmc",
    disabled=True,
)
me_mode_dropdown = ft.Dropdown(
    options=[
        ft.dropdown.Option("bidir", "Bidirectional"),
        ft.dropdown.Option("bilat", "Bilateral"),
    ],
    width=160,
    value="bilat",
    disabled=True,
)

edition_card_title = ft.Text(style="titleMedium")
remove_audio = ft.Checkbox(value=False)
extract_audio = ft.Checkbox(value=False)
time_crop_edition = ft.Checkbox(value=False)
start_time = ft.TextField(width=200)
duration = ft.TextField(width=200)
area_crop_edition = ft.Checkbox(value=False)
crop = ft.TextField(width=200)


# Progress Card Components
progress_card_title = ft.Text(style="titleMedium")
command_text = ft.Text()
start_button = ft.ElevatedButton(
    bgcolor=ft.Colors.GREEN_400,
    color=ft.Colors.WHITE,
)
cancel_button = ft.ElevatedButton(
    bgcolor=ft.Colors.RED_400,
    color=ft.Colors.WHITE,
    disabled=True,
)
progress_bar = ft.ProgressBar(value=0, expand=True, color=ft.Colors.GREEN_400)
status_text = ft.Text()


def set_components_language(t):
    title_card_title.value = t("app_title")
    theme_icon.tooltip = t("theme")
    lang_dropdown.label = t("language")
    select_file_button.text = t("select_file")
    select_folder_button.text = t("select_folder")
    selected_path.label = t("selected_input_path")
    select_output_button.text = t("select_output_folder")
    output_folder_path.label = t("output_folder_path")

    video_info_title.value = t("video_info")
    video_filename_text.value = t("video_filename_text")
    video_duration_text.value = t("video_duration_text")
    video_size_text.value = t("video_size_text")
    video_bitrate_text.value = t("video_bitrate_text")
    video_resolution_text.value = t("video_resolution_text")
    video_codec_text.value = t("video_codec_text")
    video_frame_rate_text.value = t("video_frame_rate_text")
    video_total_frames_text.value = t("video_total_frames_text")

    conversion_card_title.value = t("conversion_params")
    scale_filter.label = t("scale_filter")
    width_field.label = t("width")
    height_field.label = t("height")
    keep_aspect.label = t("keep_aspect")
    bitrate_filter.label = t("bitrate_filter")
    video_bitrate.label = t("video_bitrate")
    crf_filter.label = t("crf_filter")
    crf.label = t("crf")
    output_format.label = t("output_format")
    output_dropdown.label = t("output_format")
    codec_filter.label = t("video_codec")
    video_codec.label = t("video_codec")
    preset.label = t("preset")
    tune_dropdown.label = t("tune")

    frame_rate.label = t("frame_rate")
    frame_rate_filter.label = t("frame_rate")
    mi_mode_dropdown.label = t("mi_mode")
    mc_mode_dropdown.label = t("mc_mode")
    me_mode_dropdown.label = t("me_mode")

    edition_card_title.value = t("edition")
    remove_audio.label = t("remove_audio")
    extract_audio.label = t("extract_audio")
    time_crop_edition.label = t("time_crop_edition")
    start_time.label = t("start_time")
    duration.label = t("duration")
    area_crop_edition.label = t("area_crop_edition")
    crop.label = t("crop")
    crop.hint_text = t("crop_hint")

    progress_card_title.value = t("progress_title")
    start_button.text = t("start_conversion")
    cancel_button.text = t("cancel_conversion")
