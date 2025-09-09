import flet as ft

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
        options=[
            ft.dropdown.Option("Adaptive"),
            ft.dropdown.Option("Overlapped"),
        ],
        value="Adaptive",
        disabled=False,
    )
    estimation_algorithms = ft.Dropdown(
        label="Motion estimation algorithm",
        width=300,
        options=[
            ft.dropdown.Option("Bidirectional"),
            ft.dropdown.Option("Bilateral"),
        ],
        value="Bidirectional",
        disabled=False,
    )

    # Conversion Buttons
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
