import flet as ft


# --- State ---
class AppState:
    def __init__(self):
        self.file_path = ft.TextField(label="Selected file", read_only=True, expand=True)

        self.number_input = ft.TextField(
            label="Bitrate value",
            hint_text="Enter a number from 1 to 999",
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=3,
            width=150,
        )

        self.unit_selector = ft.Dropdown(
            label="",
            width=120,
            options=[
                ft.dropdown.Option("Kbps"),
                ft.dropdown.Option("Mbps"),
                ft.dropdown.Option("Gbps"),
            ],
            value="Mbps",  # default
        )

        self.width_input = ft.TextField(
            label="Width value",
            hint_text="Enter width value in pixels",
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=4,
            width=150,
        )

        self.height_input = ft.TextField(
            label="Height value",
            hint_text="Enter height value in pixels",
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=4,
            width=150,
        )


# --- Event Handlers ---
def on_file_picked(e: ft.FilePickerResultEvent, state: AppState):
    if e.files:
        state.file_path.value = e.files[0].name
    else:
        state.file_path.value = "No file selected"
    state.file_path.update()


def on_select_file(_e, file_picker: ft.FilePicker):
    file_picker.pick_files(allow_multiple=False)


# --- UI Builder ---
def build_ui(page: ft.Page):
    state = AppState()

    # File picker dialog
    file_picker = ft.FilePicker(on_result=lambda e: on_file_picked(e, state))
    page.overlay.append(file_picker)

    # Button row
    select_button = ft.ElevatedButton(
        "Select file",
        icon=ft.Icons.FILE_OPEN,
        on_click=lambda e: on_select_file(e, file_picker),
    )

    # Add everything to page
    page.add(
        ft.Row([select_button, state.file_path],
            alignment=ft.MainAxisAlignment.START),
        ft.Row([state.number_input, state.unit_selector],
            alignment=ft.MainAxisAlignment.START),
        ft.Row([state.width_input, state.height_input],
            alignment=ft.MainAxisAlignment.START)
    )


# --- App Entry ---
def main(page: ft.Page):
    page.title = "Simple File Picker"
    build_ui(page)


if __name__ == "__main__":
    ft.app(target=main)