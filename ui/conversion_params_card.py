import flet as ft

from ui.components import (
    conversion_card_title,
    scale_filter,
    width_field,
    height_field,
    keep_aspect,
    bitrate_filter,
    video_bitrate,
    crf_filter,
    crf,
    output_format,
    output_dropdown,
    codec_filter,
    video_codec,
    preset,
    tune_dropdown,
    frame_rate_filter,
    frame_rate,
    mi_mode_dropdown,
    mc_mode_dropdown,
    me_mode_dropdown,
    edition_card_title,
    remove_audio,
    extract_audio,
    time_crop_edition,
    start_time,
    duration,
    area_crop_edition,
    crop
)


def ConversionParamsCard() -> ft.Card:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    conversion_card_title,
                    ft.Row(
                        [
                            bitrate_filter,
                            video_bitrate,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    ft.Row(
                        [crf_filter, crf],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    ft.Row(
                        [output_format, output_dropdown],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    ft.Row(
                        [codec_filter, video_codec, preset, tune_dropdown],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    ft.Row(
                        [scale_filter, width_field, height_field, keep_aspect],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    ft.Row(
                        [frame_rate_filter, frame_rate],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    mi_mode_dropdown,
                    mc_mode_dropdown,
                    me_mode_dropdown,
                    edition_card_title,
                    remove_audio,
                    extract_audio,
                    ft.Row(
                        [
                            time_crop_edition,
                            start_time,
                            duration,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    ft.Row(
                        [area_crop_edition, crop],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                ],
                spacing=10,
            ),
            padding=15,
        ),
        elevation=2,
    )
