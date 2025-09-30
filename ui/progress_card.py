import flet as ft

from ui.components import (
    progress_card_title,
    command_text,
    start_button,
    cancel_button,
    progress_bar,
    status_text
)

def ProgressCard() -> ft.Card:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    progress_card_title,
                    command_text,
                    ft.Row(
                        [start_button, cancel_button],
                        alignment=ft.MainAxisAlignment.END,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    progress_bar,
                    status_text
                ],
                spacing=10,
            ),
            padding=15,
        ),
        elevation=2,
    )