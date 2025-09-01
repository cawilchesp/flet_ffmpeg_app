import re
import flet as ft
from pathlib import Path
import subprocess
from modules.ffmpeg_processing import (
    load_video_info,
    monitor_process,
    VideoInfo
)

FFMPEG_PATH = Path("ffmpeg/bin/ffmpeg.exe")

def create_ui_components():
    # Labels and Texts
    selected_file_label = ft.Text("Select a video to process",
        size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200)
    selected_file_text = ft.Text("No file selected",
        size=20, color=ft.Colors.BLUE_200)
    target_label = ft.Text("Target Conversion",
        size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200)
    video_size_text = ft.Text("Size: ", 
        size=14, weight=ft.FontWeight.BOLD)
    video_frame_rate_text = ft.Text("Frame Rate: ", 
        size=14, weight=ft.FontWeight.BOLD)
    video_total_frames_text = ft.Text("Total Frames: ", 
        size=14, weight=ft.FontWeight.BOLD)
    fps_options_text = ft.Text("Frame Rate Options", 
        size=20, color=ft.Colors.BLUE_200)
    
    processing_title = ft.Text("Processing...", 
        size=20, color=ft.Colors.BLUE_200)

    process_frame_label = ft.Text("Frame", size=14, weight=ft.FontWeight.BOLD)
    process_frame_rate_label = ft.Text("Frame Rate", size=14, weight=ft.FontWeight.BOLD)
    process_video_time_label = ft.Text("Video Time", size=14, weight=ft.FontWeight.BOLD)
    process_speed_label = ft.Text("Speed", size=14, weight=ft.FontWeight.BOLD)

    process_frame_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    process_frame_rate_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    process_video_time_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    process_speed_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    
    result_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)

    # Inputs
    bitrate_input = ft.TextField(label="Bitrate value", 
        hint_text="Enter a number from 1 to 999", 
        keyboard_type=ft.KeyboardType.NUMBER, max_length=3, width=150, disabled=True)
    unit_selector = ft.Dropdown(label="", 
        width=120, 
        options=[ft.dropdown.Option("Kbps"), 
            ft.dropdown.Option("Mbps"), 
            ft.dropdown.Option("Gbps")], 
        value="Mbps", disabled=True)
    width_input = ft.TextField(label="Width value", hint_text="Enter width value in pixels", keyboard_type=ft.KeyboardType.NUMBER, max_length=4, width=150, disabled=True)
    height_input = ft.TextField(label="Height value", hint_text="Enter height value in pixels", keyboard_type=ft.KeyboardType.NUMBER, max_length=4, width=150, disabled=True)
    fps_input = ft.TextField(label="Frame rate value", hint_text="Enter frame rate value", keyboard_type=ft.KeyboardType.NUMBER, max_length=3, width=150, disabled=True)

    # Dropdowns
    interpolation_modes = ft.Dropdown(
        label="Motion interpolation mode", width=300,
        options=[ft.dropdown.Option("Motion-Compensated"),
            ft.dropdown.Option("Duplicate"),
            ft.dropdown.Option("Blend")],
        value="Motion-Compensated", disabled=False
    )
    compensation_modes = ft.Dropdown(
        label="Motion compensation mode", width=300,
        options=[ft.dropdown.Option("Adaptive"),
            ft.dropdown.Option("Overlapped")],
        value="Adaptive", disabled=False
    )
    estimation_algorithms = ft.Dropdown(
        label="Motion estimation algorithm", width=300,
        options=[ft.dropdown.Option("Bidirectional"),
            ft.dropdown.Option("Bilateral")],
        value="Bidirectional", disabled=False
    )

    # Buttons
    process_button = ft.ElevatedButton(
        text="Process Video", icon=ft.Icons.PLAY_CIRCLE_FILLED,
        color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_700,
        disabled=True
    )
    selected_file_button = ft.ElevatedButton(
        text="Select Video", icon=ft.Icons.FOLDER_OPEN,
        color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_900
    )

    return {
        "selected_file_label": selected_file_label,
        "selected_file_text": selected_file_text,
        "selected_file_button": selected_file_button,
        "target_label": target_label,
        "video_size_text": video_size_text,
        "video_frame_rate_text": video_frame_rate_text,
        "video_total_frames_text": video_total_frames_text,
        "bitrate_input": bitrate_input,
        "unit_selector": unit_selector,
        "width_input": width_input,
        "height_input": height_input,
        "fps_input": fps_input,
        "fps_options_text": fps_options_text,
        "interpolation_modes": interpolation_modes,
        "compensation_modes": compensation_modes,
        "estimation_algorithms": estimation_algorithms,
        "process_button": process_button,
        "processing_title": processing_title,
        "process_frame_label": process_frame_label,
        "process_frame_rate_label": process_frame_rate_label,
        "process_video_time_label": process_video_time_label,
        "process_speed_label": process_speed_label,
        "process_frame_text": process_frame_text,
        "process_frame_rate_text": process_frame_rate_text,
        "process_video_time_text": process_video_time_text,
        "process_speed_text": process_speed_text,
        "result_text": result_text,
    }

def interpolation_mode_on_change(e, components):
    if e.control.value == "Motion-Compensated":
        components["compensation_modes"].disabled = False
        components["compensation_modes"].update()
        components["estimation_algorithms"].disabled = False
        components["estimation_algorithms"].update()
    else:
        components["compensation_modes"].disabled = True
        components["compensation_modes"].update()
        components["estimation_algorithms"].disabled = True
        components["estimation_algorithms"].update()


def build_layout(components):
    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    components["selected_file_label"],
                    components["selected_file_button"]
                ]),
                width=580, padding=10, bgcolor=ft.Colors.GREY_800, border_radius=10,
            ),
            ft.Container(
                content=ft.Column([
                    components["selected_file_text"],
                    components["video_size_text"],
                    components["video_frame_rate_text"],
                    components["video_total_frames_text"]
                ]),
                width=580, padding=10, bgcolor=ft.Colors.GREY_800, border_radius=10,
            ),
            ft.Container(
                content=ft.Column([
                    components["target_label"],
                    ft.Row([components["bitrate_input"], components["unit_selector"]]),
                    ft.Row([components["width_input"], ft.Text("x", size=20, weight=ft.FontWeight.BOLD), components["height_input"]]),
                    components["fps_input"],
                    components["fps_options_text"],
                    components["interpolation_modes"],
                    components["compensation_modes"],
                    components["estimation_algorithms"],
                    components["process_button"]
                ]),
                width=580, padding=10, bgcolor=ft.Colors.GREY_800, border_radius=10,
            ),
            ft.Container(
                content=ft.Column([
                    components["processing_title"],
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(components["process_frame_label"]),
                            ft.DataColumn(components["process_frame_rate_label"]),
                            ft.DataColumn(components["process_video_time_label"]),
                            ft.DataColumn(components["process_speed_label"]),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(components["process_frame_text"]),
                                    ft.DataCell(components["process_frame_rate_text"]),
                                    ft.DataCell(components["process_video_time_text"]),
                                    ft.DataCell(components["process_speed_text"])
                                ]
                            )
                        ],
                    ),
                    components["result_text"],
                ]),
                width=580, padding=10, bgcolor=ft.Colors.GREY_800, border_radius=10,
            ),
        ]),
        padding=10, expand=True
    )

def handle_file_picker(e, video_info, components):
    if e.files:
        file_info = load_video_info(ffmpeg_path=FFMPEG_PATH, source=e.files[0].path)
        video_info.source_path = file_info.source_path
        video_info.width = file_info.width
        video_info.height = file_info.height
        video_info.fps = file_info.fps
        video_info.total_frames = file_info.total_frames

        components["selected_file_text"].value = f"Selected file: {Path(video_info.source_path).name}"
        components["selected_file_text"].update()
        components["video_size_text"].value = f"Size: {video_info.width} X {video_info.height} px"
        components["video_size_text"].update()
        components["video_frame_rate_text"].value = f"Frame Rate: {video_info.fps} fps"
        components["video_frame_rate_text"].update()
        components["video_total_frames_text"].value = f"Total Frames: {video_info.total_frames}"
        components["video_total_frames_text"].update()

        for key in ["bitrate_input", "unit_selector", "width_input", "height_input", "fps_input", "process_button"]:
            components[key].disabled = False
            components[key].update()

def build_ffmpeg_command(video_info, components):
    output_path = Path(video_info.source_path).parent / f"{Path(video_info.source_path).stem}_FFMPEG_EDITED.mp4"
    cmd = [
        str(FFMPEG_PATH), "-hwaccel", "cuda", "-y", "-an",
        "-i", video_info.source_path, "-c:v", "h264_nvenc"
    ]
    video_filters = []
    if components["bitrate_input"].value != "":
        cmd.extend(["-b:v", f"{components['bitrate_input'].value}M"])
    if components["width_input"].value != "" or components["height_input"].value != "":
        video_filters.append(f"scale={components['width_input'].value}:{components['height_input'].value}")

    interpolations = {"Duplicate": "mi_mode=dup", "Blend": "mi_mode=blend", "Motion-Compensated": "mi_mode=mci"}
    compensations = {"Adaptive": "mc_mode=aobmc", "Overlapped": "mc_mode=obmc"}
    estimations = {"Bidirectional": "me_mode=bidir", "Bilateral": "me_mode=bilat"}

    if components["fps_input"].value != "":
        if float(components["fps_input"].value) > video_info.fps:
            interpolation_filter = f"minterpolate=fps={components['fps_input'].value}"
            interpolation_filter += f":{interpolations[components['interpolation_modes'].value]}"
            if components['interpolation_modes'].value == "Motion-Compensated":
                interpolation_filter += f":{compensations[components['compensation_modes'].value]}"
                interpolation_filter += f":{estimations[components['estimation_algorithms'].value]}"
        else:
            interpolation_filter = f"fps={components['fps_input'].value}"
        video_filters.append(interpolation_filter)

    if video_filters:
        cmd.extend(["-vf", f"{(',').join(video_filters)}"])
    if components["fps_input"].value != "":
        cmd.extend(["-r", f"{components['fps_input'].value}"])
    cmd.append(str(output_path))
    return cmd

def process_video(video_info, components):
    cmd = build_ffmpeg_command(video_info, components)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def click_process_button(video_info, components):
    components["result_text"].value = ''
    components["result_text"].update()
    process = process_video(video_info, components)

    progress_pattern = re.compile(r"frame=\s*(\d+).*?fps=\s*([\d\.]+).*?time=\s*(\d+:\d+:\d+\.\d+).*?speed=\s*([\d\.]+)x")
    
    while True:
        line = process.stderr.readline()
        if not line:
            break
        line = line.strip()

        # Show errors
        if "Error" in line or "Invalid" in line or "failed" in line.lower():
            print(f"[bold red]Error:[/bold red] {line}")

        # Match progress line
        match = progress_pattern.search(line)
        if match:
            frame, fps, timestamp, speed = match.groups()

            components["process_frame_text"].value = frame
            components["process_frame_text"].update()
            components["process_frame_rate_text"].value = fps
            components["process_frame_rate_text"].update()
            components["process_video_time_text"].value = timestamp
            components["process_video_time_text"].update()
            components["process_speed_text"].value = speed
            components["process_speed_text"].update()
    
    process.wait()
    components["result_text"].value = 'Video processed successfully! ✅' if process.returncode == 0 else "Error processing video: ❌"
    components["result_text"].update()

def main(page: ft.Page):
    # Page configuration
    page.title = "FFMPEG Video Converter"
    page.window.width = 600
    page.window.height = 1020
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_900
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE,
            secondary=ft.Colors.GREEN,
            background=ft.Colors.GREY_500,
            surface=ft.Colors.GREY_800
        )
    )

    video_info = VideoInfo("", "", 0, 0, 0)
    components = create_ui_components()

    file_picker = ft.FilePicker(on_result=lambda e: handle_file_picker(e, video_info, components))
    page.overlay.append(file_picker)

    components["interpolation_modes"].on_change = lambda e: interpolation_mode_on_change(e, components)
    components["selected_file_button"].on_click = lambda _: file_picker.pick_files(allow_multiple=False)
    components["process_button"].on_click = lambda _: click_process_button(video_info, components)

    content_area = ft.Container(content=build_layout(components), expand=True)
    page.add(ft.Row([content_area], expand=True))

if __name__ == "__main__":
    ft.app(target=main)