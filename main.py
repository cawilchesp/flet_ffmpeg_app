import flet as ft
from ui.main_view import main_view
from core.i18n import load_config, set_language, t

from ui.components import set_components_language


def main(page: ft.Page):
    config = load_config()
    
    # Configurar idioma
    set_language(config.get("language", "es"))
    set_components_language(t)

    # Configurar tema
    if config.get("theme", "light") == "dark":
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT

    page.title = "Video Converter"
    page.window.min_width = 1630
    page.window.min_height = 970
    page.window.width = 1630
    page.window.height = 970

    page.add(main_view(page))


if __name__ == "__main__":
    ft.app(target=main)
