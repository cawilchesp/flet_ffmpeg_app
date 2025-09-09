from pathlib import Path

import flet as ft

from modules.ffmpeg_processing import (
    VideoInfo,
    ffmpeg_process,
    load_video_info,
    monitor_process,
)


def create_ui_components():
    # Texts
    selected_file_text = ft.Text("No file selected", style="label_medium")
    video_size_text = ft.Text("", style="label_medium")
    video_frame_rate_text = ft.Text("", style="label_medium")
    video_total_frames_text = ft.Text("", style="label_medium")
    video_bit_rate_text = ft.Text("", style="label_medium")
    video_duration_text = ft.Text("", style="label_medium")

    process_frame_text = ft.Text("", style="label_medium")
    process_frame_rate_text = ft.Text("", style="label_medium")
    process_video_time_text = ft.Text("", style="label_medium")
    process_speed_text = ft.Text("", style="label_medium")
    result_text = ft.Text("", style="label_medium")

    # Inputs
    bitrate_input = ft.TextField(
        label="Bitrate value",
        hint_text="Enter a number greater than 0",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=5,
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
        value="Mbps",
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

    # Dropdowns
    interpolation_modes = ft.Dropdown(
        label="Motion interpolation mode",
        width=300,
        options=[
            ft.dropdown.Option("Motion-Compensated"),
            ft.dropdown.Option("Duplicate"),
            ft.dropdown.Option("Blend"),
        ],
        value="Motion-Compensated",
        disabled=False,
    )
    compensation_modes = ft.Dropdown(
        label="Motion compensation mode",
        width=300,
        options=[ft.dropdown.Option("Adaptive"), ft.dropdown.Option("Overlapped")],
        value="Adaptive",
        disabled=False,
    )
    estimation_algorithms = ft.Dropdown(
        label="Motion estimation algorithm",
        width=300,
        options=[ft.dropdown.Option("Bidirectional"), ft.dropdown.Option("Bilateral")],
        value="Bidirectional",
        disabled=False,
    )

    # Buttons
    selected_file_button = ft.FilledButton(
        text="Select Video",
        icon=ft.Icons.FOLDER_OPEN,
    )
    process_button = ft.FilledButton(
        text="Process Video", icon=ft.Icons.PLAY_CIRCLE_FILLED, disabled=True
    )
    theme_button = ft.IconButton(
        icon=ft.Icons.DARK_MODE_OUTLINED,
    )

    return {
        "selected_file_button": selected_file_button,
        "selected_file_text": selected_file_text,
        "video_size_text": video_size_text,
        "video_frame_rate_text": video_frame_rate_text,
        "video_total_frames_text": video_total_frames_text,
        "video_bit_rate_text": video_bit_rate_text,
        "video_duration_text": video_duration_text,
        "bitrate_input": bitrate_input,
        "unit_selector": unit_selector,
        "width_input": width_input,
        "height_input": height_input,
        "fps_input": fps_input,
        "interpolation_modes": interpolation_modes,
        "compensation_modes": compensation_modes,
        "estimation_algorithms": estimation_algorithms,
        "process_button": process_button,
        "process_frame_text": process_frame_text,
        "process_frame_rate_text": process_frame_rate_text,
        "process_video_time_text": process_video_time_text,
        "process_speed_text": process_speed_text,
        "result_text": result_text,
        "theme_button": theme_button,
    }


def toggle_theme(page, components):
    if page.theme_mode == ft.ThemeMode.LIGHT:
        page.theme_mode = ft.ThemeMode.DARK
        components["theme_button"].icon = ft.Icons.DARK_MODE_OUTLINED
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
        components["theme_button"].icon = ft.Icons.WB_SUNNY_OUTLINED
    page.update()


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


def build_conversion_layout(components):
    card_file = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Select a video to process", style="title_large"),
                    components["selected_file_button"],
                ]
            ),
            padding=ft.padding.all(10),
        )
    )

    card_info = ft.Card(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Video Information", style="title_large"),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(
                                ft.Text("Selected File", style="label_medium")
                            ),
                            ft.DataColumn(components["selected_file_text"]),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Size", style="label_medium")),
                                    ft.DataCell(components["video_size_text"]),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Text("Frame Rate", style="label_medium")
                                    ),
                                    ft.DataCell(components["video_frame_rate_text"]),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Text("Total Frames", style="label_medium")
                                    ),
                                    ft.DataCell(components["video_total_frames_text"]),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Text("Bit Rate", style="label_medium")
                                    ),
                                    ft.DataCell(components["video_bit_rate_text"]),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Text("Duration", style="label_medium")
                                    ),
                                    ft.DataCell(components["video_duration_text"]),
                                ]
                            ),
                        ],
                    ),
                ]
            ),
            padding=ft.padding.all(10),
        ),
        expand=True,
    )

    card_options = ft.Card(
        ft.Container(
            content=ft.Column(
                [
                    components["theme_button"],
                ]
            ),
            padding=ft.padding.all(10),
        )
    )

    card_target = ft.Card(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Target Conversion", style="title_large"),
                    ft.Row([components["bitrate_input"], components["unit_selector"]]),
                    ft.Row(
                        [
                            components["width_input"],
                            ft.Text("x", style="label_medium"),
                            components["height_input"],
                        ]
                    ),
                    components["fps_input"],
                    ft.Text("Frame Rate Options", style="label_medium"),
                    components["interpolation_modes"],
                    components["compensation_modes"],
                    components["estimation_algorithms"],
                    components["process_button"],
                ]
            ),
            padding=ft.padding.all(10),
        ),
        expand=True,
    )

    card_process = ft.Card(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Processing...", style="title_large"),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Frame", style="label_medium")),
                            ft.DataColumn(ft.Text("Frame Rate", style="label_medium")),
                            ft.DataColumn(ft.Text("Video Time", style="label_medium")),
                            ft.DataColumn(ft.Text("Speed", style="label_medium")),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(components["process_frame_text"]),
                                    ft.DataCell(components["process_frame_rate_text"]),
                                    ft.DataCell(components["process_video_time_text"]),
                                    ft.DataCell(components["process_speed_text"]),
                                ]
                            )
                        ],
                    ),
                    components["result_text"],
                ]
            ),
            padding=ft.padding.all(10),
        )
    )

    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [card_file, card_info, card_options],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    width=400,
                ),
                ft.Container(
                    content=ft.Column(
                        [card_target, card_process],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    expand=True,
                ),
            ]
        ),
        expand=True,
    )


def build_gif_layout(components):
    return


def build_rail_layout():
    return ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME,
                selected_icon=ft.Icons.HOME_OUTLINED,
                label="Conversion",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS,
                selected_icon=ft.Icons.SETTINGS_OUTLINED,
                label="GIF",
            ),
        ],
        on_change=change_view,
        bgcolor=ft.Colors.GREY_900,
    )


def handle_file_picker(e, video_info, components):
    if e.files:
        file_info = load_video_info(source=e.files[0].path)
        video_info.source_path = file_info.source_path
        video_info.width = file_info.width
        video_info.height = file_info.height
        video_info.fps = file_info.fps
        video_info.total_frames = file_info.total_frames
        video_info.bit_rate = file_info.bit_rate
        video_info.duration = file_info.duration

        components["selected_file_text"].value = f"{Path(video_info.source_path).name}"
        components["selected_file_text"].update()
        components[
            "video_size_text"
        ].value = f"{video_info.width} X {video_info.height} px"
        components["video_size_text"].update()
        components["video_frame_rate_text"].value = f"{video_info.fps} fps"
        components["video_frame_rate_text"].update()
        components["video_total_frames_text"].value = f"{video_info.total_frames}"
        components["video_total_frames_text"].update()
        components["video_bit_rate_text"].value = f"{video_info.bit_rate}"
        components["video_bit_rate_text"].update()
        components["video_duration_text"].value = f"{video_info.duration}"
        components["video_duration_text"].update()

        for key in [
            "bitrate_input",
            "unit_selector",
            "width_input",
            "height_input",
            "fps_input",
            "process_button",
        ]:
            components[key].disabled = False
            components[key].update()


def click_process_button(video_info, components):
    components["result_text"].value = ""
    components["result_text"].update()
    process = ffmpeg_process(video_info, components)
    monitor_process(process=process, components=components)

    process.wait()
    components["result_text"].value = (
        "Video processed successfully! ✅"
        if process.returncode == 0
        else "Error processing video: ❌"
    )
    components["result_text"].update()


def change_view(e):
    selected = e.control.selected_index
    if selected == 0:
        content_area.content = duplicate_files_view
    elif selected == 1:
        content_area.content = ft.Text("Settings View", size=30)
    content_area.update()


def main(page: ft.Page):
    # Page configuration
    page.title = "FFMPEG Video Converter"
    page.window.min_width = 920
    page.window.min_height = 770
    page.window.width = 920
    page.window.height = 770

    page.theme_mode = ft.ThemeMode.DARK

    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_400,
            secondary=ft.Colors.CYAN_400,
            surface=ft.Colors.GREY_50,
            background=ft.Colors.WHITE,
            error=ft.Colors.RED_400,
            on_primary=ft.Colors.WHITE,
            on_secondary=ft.Colors.BLACK,
            on_surface=ft.Colors.BLACK,
            on_background=ft.Colors.BLACK,
        ),
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(
                size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900
            ),
            body_medium=ft.TextStyle(size=16, color=ft.Colors.GREY_800),
            label_medium=ft.TextStyle(size=14, color=ft.Colors.GREY_600),
        ),
    )
    page.dark_theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_200,
            secondary=ft.Colors.CYAN_200,
            surface=ft.Colors.GREY_900,
            background=ft.Colors.BLACK,
            error=ft.Colors.RED_300,
            on_primary=ft.Colors.BLACK,
            on_secondary=ft.Colors.WHITE,
            on_surface=ft.Colors.WHITE,
            on_background=ft.Colors.WHITE,
        ),
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(
                size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_100
            ),
            body_medium=ft.TextStyle(size=16, color=ft.Colors.GREY_300),
            label_medium=ft.TextStyle(size=14, color=ft.Colors.GREY_400),
        ),
    )

    video_info = VideoInfo(
        source_path=None,
        width=0,
        height=0,
        fps=0.0,
        total_frames=0,
        bit_rate="",
        duration="",
    )
    components = create_ui_components()

    file_picker = ft.FilePicker(
        on_result=lambda e: handle_file_picker(e, video_info, components)
    )
    page.overlay.append(file_picker)

    components["selected_file_button"].on_click = lambda _: file_picker.pick_files(
        allow_multiple=False
    )
    components["interpolation_modes"].on_change = (
        lambda e: interpolation_mode_on_change(e, components)
    )
    components["process_button"].on_click = lambda _: click_process_button(
        video_info, components
    )
    components["theme_button"].on_click = lambda _: toggle_theme(page, components)

    content_area = build_conversion_layout(components)

    rail = build_rail_layout()

    page.add(ft.Row([rail, content_area], expand=True))


if __name__ == "__main__":
    ft.app(target=main)
