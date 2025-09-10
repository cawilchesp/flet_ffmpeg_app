import flet as ft


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
                                    ft.DataCell(
                                        ft.Text("Size", style="label_medium")
                                    ),
                                    ft.DataCell(components["video_size_text"]),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Text(
                                            "Frame Rate", style="label_medium"
                                        )
                                    ),
                                    ft.DataCell(
                                        components["video_frame_rate_text"]
                                    ),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Text(
                                            "Total Frames", style="label_medium"
                                        )
                                    ),
                                    ft.DataCell(
                                        components["video_total_frames_text"]
                                    ),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Text(
                                            "Bit Rate", style="label_medium"
                                        )
                                    ),
                                    ft.DataCell(
                                        components["video_bit_rate_text"]
                                    ),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Text(
                                            "Duration", style="label_medium"
                                        )
                                    ),
                                    ft.DataCell(
                                        components["video_duration_text"]
                                    ),
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
                    ft.Row(
                        [
                            components["bitrate_input"],
                            components["unit_selector"],
                        ]
                    ),
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
                            ft.DataColumn(
                                ft.Text("Frame", style="label_medium")
                            ),
                            ft.DataColumn(
                                ft.Text("Frame Rate", style="label_medium")
                            ),
                            ft.DataColumn(
                                ft.Text("Video Time", style="label_medium")
                            ),
                            ft.DataColumn(
                                ft.Text("Speed", style="label_medium")
                            ),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        components["process_frame_text"]
                                    ),
                                    ft.DataCell(
                                        components["process_frame_rate_text"]
                                    ),
                                    ft.DataCell(
                                        components["process_video_time_text"]
                                    ),
                                    ft.DataCell(
                                        components["process_speed_text"]
                                    ),
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
                        [
                            card_file, 
                            card_info, 
                            card_options
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    width=400,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            card_target,
                            card_process
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                    expand=True,
                ),
            ]
        ),
        expand=True,
    )