import flet as ft

from ui.components import (video_info_title,
                           video_filename_text,
                           video_filename_value,
                           video_duration_text,
                           video_duration_value,
                           video_size_text,
                           video_size_value,
                           video_bitrate_text,
                           video_bitrate_value,
                           video_resolution_text,
                           video_resolution_value,
                           video_codec_text,
                           video_codec_value,
                           video_frame_rate_text,
                           video_frame_rate_value,
                           video_total_frames_text,
                           video_total_frames_value,
                           )


def VideoInfoCard() -> ft.Card:
    return ft.Card(
        ft.Container(
            content=ft.Column(
                [
                    video_info_title,
                    ft.Row([video_filename_text,video_filename_value]),
                    ft.Row([video_duration_text,video_duration_value]),
                    ft.Row([video_size_text,video_size_value]),
                    ft.Row([video_bitrate_text,video_bitrate_value]),
                    ft.Row([video_resolution_text,video_resolution_value]),
                    ft.Row([video_codec_text,video_codec_value]),
                    ft.Row([video_frame_rate_text,video_frame_rate_value]),
                    ft.Row([video_total_frames_text,video_total_frames_value])
                ],
                spacing=10,
            ),
            padding=15,
            expand=True,
        ),
        elevation=2,
    )
