import flet as ft

from ui.components import title_card_title, theme_icon, lang_dropdown


def TitleCard() -> ft.Card:
    return ft.Card(
        ft.Container(
            content=ft.Row(
                [
                    title_card_title,
                    theme_icon,
                    lang_dropdown,
                ],
            ),
            padding=15,
        ),
        elevation=2,
    )
