import flet as ft
from pathlib import Path
import subprocess
from modules.ffmpeg_processing import (process_video,
                                       load_video_info,
                                       monitor_process,
                                       VideoInfo)


def main(page: ft.Page):
    # Page configuration
    page.title = "Simple File Picker"
    page.window.width = 1300
    page.window.height = 800
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_700
    page.theme_mode = ft.ThemeMode.DARK

    # Theme configuration
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

    # Variables
    ffmpeg_path = Path("ffmpeg/bin/ffmpeg.exe")

    video_info = VideoInfo("", "", 0, 0, 0)

    state = { "current_duplicates": [] }


    # UI Components
    selected_file_label = ft.Text("Select a video to process", size=20, 
        weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200 )
    
    selected_file_text = ft.Text("No file selected", size=20, color=ft.Colors.BLUE_200)

    selected_file_button = ft.ElevatedButton(text="Select Video",
        icon=ft.Icons.FOLDER_OPEN, color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_900,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
    )

    result_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    video_size_text = ft.Text("Width: ", size=14, weight=ft.FontWeight.BOLD)
    video_frame_rate_text = ft.Text("Frame Rate: ", size=14, weight=ft.FontWeight.BOLD)
    video_total_frames_text = ft.Text("Total Frames: ", size=14, weight=ft.FontWeight.BOLD)

    bitrate_input = ft.TextField(
        label="Bitrate value",
        hint_text="Enter a number from 1 to 999",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=3,
        width=150,
        disabled=True,
    )

    unit_selector = ft.Dropdown(
        label="",
        width=120,
        options=[
            ft.dropdown.Option("Kbps"),
            ft.dropdown.Option("Mbps"),
            ft.dropdown.Option("Gbps"),
        ],
        value="Mbps",  # default
        disabled=True,
    )

    width_input = ft.TextField(
        label="Width value",
        hint_text="Enter width value in pixels",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=4,
        width=150,
        disabled=True,
    )

    height_input = ft.TextField(
        label="Height value",
        hint_text="Enter height value in pixels",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=4,
        width=150,
        disabled=True,
    )

    fps_input = ft.TextField(
        label="Frame rate value",
        hint_text="Enter frame rate value",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=3,
        width=150,
        disabled=True,
    )

    process_button = ft.ElevatedButton(
        text="Process Video",
        icon=ft.Icons.PLAY_CIRCLE_FILLED,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_700,
        disabled=True,
        on_click=lambda _: click_process_button()
    )

    def handle_file_picker(e: ft.FilePickerResultEvent):
        if e.files:
            # Get video information
            file_info = load_video_info(
                ffmpeg_path=ffmpeg_path,
                source=e.files[0].path )
            
            video_info.source_path = file_info.source_path
            video_info.width = file_info.width
            video_info.height = file_info.height
            video_info.fps = file_info.fps
            video_info.total_frames = file_info.total_frames

            selected_file_text.value = f"Selected file: {Path(video_info.source_path).name}"
            selected_file_text.update()
            video_size_text.value = f"Size: {video_info.width} X {video_info.height} px"
            video_size_text.update()
            video_frame_rate_text.value = f"Frame Rate: {video_info.fps} fps"
            video_frame_rate_text.update()
            video_total_frames_text.value = f"Total Frames: {video_info.total_frames}"
            video_total_frames_text.update()

            bitrate_input.disabled = False
            bitrate_input.update()
            unit_selector.disabled = False
            unit_selector.update()
            width_input.disabled = False
            width_input.update()
            height_input.disabled = False
            height_input.update()
            fps_input.disabled = False
            fps_input.update()
            process_button.disabled = False
            process_button.update()

    def click_process_button():
        process = process_video()
        monitor_process(process)
        
        # Wait for process to finish
        process.wait()

        # Final message
        if process.returncode == 0:
            step_message(next(step_count), 'Video processed successfully! ✅')
        else:
            step_message(next(step_count), "Error processing video: ❌")



    def process_video():
        # Build output path
        output_path = Path(video_info.source_path).parent / f"{Path(video_info.source_path).stem}_FFMPEG_EDITED.mp4"

        # Build FFmpeg command
        cmd = [
            str(ffmpeg_path),
            "-hwaccel", "cuda",
            "-y",
            "-an",
            "-i", video_info.source_path,
            "-c:v", "h264_nvenc"
        ]

        # Video encoding options
        if bitrate_input.value != "":
            cmd.extend(["-b:v", f"{bitrate_input.value}M"])
        if width_input.value != "" or height_input.value != "":
            cmd.extend(["-vf", f"scale={width_input.value}:{height_input.value}"])
        if fps_input.value != "":
            cmd.extend(["-r", f"{fps_input.value}"])

        cmd.append(f"{output_path}")
        
        # Launch process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        return process







        
    file_picker = ft.FilePicker(on_result=handle_file_picker)
    page.overlay.append(file_picker)

    # Vista de archivos duplicados
    duplicate_files_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=selected_file_label,
                margin=ft.margin.only(bottom=20)
            ),
            selected_file_button,
            ft.Container(
                content=selected_file_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Container(
                content=video_size_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Container(
                content=video_frame_rate_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Container(
                content=video_total_frames_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Row([
                bitrate_input,
                unit_selector,
            ]),
            ft.Row([
                width_input,
                ft.Text("x", size=20, weight=ft.FontWeight.BOLD),
                height_input,
            ]),
            fps_input,
            ft.Container(
                content=process_button,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Container(
                content=result_text,
                margin=ft.margin.only(top=10, bottom=10)
            )
        ]),
        padding=30,
        expand=True
    )

    content_area = ft.Container(
        content=duplicate_files_view,
        expand=True,
    )

    page.add(
        ft.Row(
            [
                content_area
            ],
            expand=True
        )
    )


if __name__ == "__main__":
    ft.app(target=main)