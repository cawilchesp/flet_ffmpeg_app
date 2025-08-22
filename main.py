import flet as ft
from pathlib import Path
from modules.ffmpeg_processing import process_video, load_video_info


def main(page: ft.Page):
    # Page configuration
    page.title = "Simple File Picker"
    page.window.width = 800
    page.window.height = 600
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

    process_button = ft.ElevatedButton(
        text="Process Video",
        icon=ft.Icons.PLAY_CIRCLE_FILLED,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_700,
        disabled=True,
        on_click=lambda _: process_video()
    )

    duplicates_list = ft.ListView(
        expand=True,
        spacing=10,
        height=200,
        auto_scroll=True
    )

    delete_all_button = ft.ElevatedButton(
        text="Delete All Duplicates",
        icon=ft.Icons.DELETE_SWEEP,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_700,
        visible=False,
        on_click=lambda _: delete_all_duplicates()
    )

    def handle_file_picker(e: ft.FilePickerResultEvent):
        if e.files:
            # Get video information
            video_info = load_video_info(
                ffmpeg_path=ffmpeg_path,
                source=e.files[0].path )

            selected_file_text.value = f"Selected file: {video_info.source_name}"
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
            process_button.disabled = False
            process_button.update()
            

    # def scan_directory(directory):
    #     duplicates_list.controls.clear()
    #     state["current_duplicates"] = find_duplicate_files(directory)

    #     if not state["current_duplicates"]:
    #         result_text.value = "No duplicate files found."
    #         result_text.color = ft.Colors.GREEN_200
    #         delete_all_button.visible = False
    #     else:
    #         result_text.value = f"{len(state["current_duplicates"])} duplicate files found."
    #         result_text.color = ft.Colors.ORANGE_200
    #         delete_all_button.visible = True

    #         for duplicated_file, original in state["current_duplicates"]:
    #             duplicate_row = ft.Row([
    #                 ft.Text(
    #                     f"Duplicate: {duplicated_file}\nOriginal: {original}",
    #                     size=12,
    #                     color=ft.Colors.BLUE_200,
    #                     expand=True
    #                 ),
    #                 ft.ElevatedButton(
    #                     text="Delete",
    #                     icon=ft.Icons.DELETE,
    #                     color=ft.Colors.WHITE,
    #                     bgcolor=ft.Colors.RED_700,
    #                     on_click=lambda e, file_path=duplicated_file: delete_duplicate(file_path)
    #                 )
    #             ])
    #             duplicates_list.controls.append(duplicate_row)
    #     duplicates_list.update()
    #     result_text.update()
    #     delete_all_button.update()

    # def delete_duplicate(file_path):
    #     if delete_file(file_path):
    #         result_text.value = f"Deleted: {file_path}"
    #         result_text.color = ft.Colors.GREEN_200
    #         for control in duplicates_list.controls:
    #             if file_path in control.controls[0].value:
    #                 duplicates_list.controls.remove(control)
    #         state["current_duplicates"] = [(dup, orig) for dup, orig in state["current_duplicates"] if dup[0] != file_path]
    #         if not state["current_duplicates"]:
    #             delete_all_button.visible = False
    #     else:
    #         result_text.value = f"Failed to delete: {file_path}"
    #         result_text.color = ft.Colors.RED_200
    #     duplicates_list.update()
    #     result_text.update()
    #     delete_all_button.update()


    # def delete_all_duplicates():
    #     deleted_count = 0
    #     failed_count = 0
    #     for duplicated_file, _ in state["current_duplicates"]:
    #         if delete_file(duplicated_file):
    #             deleted_count += 1
    #         else:
    #             failed_count += 1

    #     duplicates_list.controls.clear()
    #     state["current_duplicates"] = []
    #     delete_all_button.visible = False

    #     if failed_count == 0:
    #         result_text.value = f"Successfully deleted {deleted_count} duplicate files."
    #         result_text.color = ft.Colors.GREEN_200
    #     else:
    #         result_text.value = f"Deleted {deleted_count} files, failed to delete {failed_count} files."
    #         result_text.color = ft.Colors.RED_200

    #     duplicates_list.update()
    #     result_text.update()
    #     delete_all_button.update()

    def process_video():
        # Build output path
        output_path = Path(config.source).with_stem(f"{Path(config.source).stem}_FFMPEG_EDITED.mp4")
        
        # Build FFmpeg command
        cmd = [
            str(ffmpeg_path),
            "-hwaccel", "cuda",
            "-y",
            "-an",
            "-i", config.source,
            "-c:v", "h264_nvenc"
        ]

        # Video encoding options
        options = {
            "bitrate": ["-b:v", f"{config.bitrate}M"],
            "resolution": ["-vf", f"scale={config.resolution}"],
            "fps": ["-r", f"{config.fps}"]
        }

        for key, args in options.items():
            if getattr(config, key):
                cmd.extend(args)

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
            ft.Container(
                content=process_button,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Container(
                content=result_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Container(
                content=duplicates_list,
                border=ft.border.all(2, ft.Colors.GREY_600),
                expand=True,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800
            ),
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