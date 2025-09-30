import flet as ft

from ui.components import (select_file_button,
                           select_folder_button,
                           selected_path,
                           select_output_button,
                           output_folder_path)


def FileSelectCard(
    file_picker: ft.FilePicker,
    output_folder_picker: ft.FilePicker,
) -> ft.Card:
    def open_picker(e):
        file_picker.pick_files(allow_multiple=False)

    def open_folder_picker(e):
        file_picker.get_directory_path()

    def open_output_folder_picker(e):
        output_folder_picker.get_directory_path()

    select_file_button.on_click = open_picker
    select_folder_button.on_click = open_folder_picker
    select_output_button.on_click = open_output_folder_picker

    return ft.Card(
        ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            select_file_button,
                            select_folder_button
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    selected_path,
                    select_output_button,
                    output_folder_path,
                ],
                spacing=10
            ),
            padding=15,
        ),
        elevation=2
    )
