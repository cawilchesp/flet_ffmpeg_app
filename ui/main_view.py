import flet as ft
from pathlib import Path

from ui.title_card import TitleCard
from ui.file_select_card import FileSelectCard
from ui.conversion_params_card import ConversionParamsCard
from ui.video_info_card import VideoInfoCard
from ui.progress_card import ProgressCard

from core.ffmpeg_wrapper import VideoConverter
from core.i18n import get_current_language, save_config, set_language, t
from core.video_utils import get_video_info, get_ffmpeg_path

from ui.components import (
    set_components_language,
    theme_icon,
    lang_dropdown,
    selected_path,
    output_folder_path,
    video_filename_value,
    video_duration_value,
    video_size_value,
    video_bitrate_value,
    video_resolution_value,
    video_codec_value,
    video_frame_rate_value,
    video_total_frames_value,
    bitrate_filter,
    video_bitrate,
    crf_filter,
    crf,
    output_format,
    output_dropdown,
    codec_filter,
    video_codec,
    preset,
    preset_options_nvenc,
    preset_options_cpu,
    tune_dropdown,
    scale_filter,
    width_field,
    height_field,
    keep_aspect,
    frame_rate_filter,
    frame_rate,
    mi_mode_dropdown,
    mc_mode_dropdown,
    me_mode_dropdown,
    remove_audio,
    extract_audio,
    time_crop_edition,
    start_time,
    duration,
    area_crop_edition,
    crop,
    command_text,
    start_button,
    cancel_button,
    progress_bar,
    status_text,
)


def main_view(page: ft.Page):
    # Estado de tema
    theme_icon.icon = (
        ft.Icons.DARK_MODE
        if page.theme_mode == ft.ThemeMode.DARK
        else ft.Icons.LIGHT_MODE
    )

    def toggle_theme(e: ft.ControlEvent) -> None:
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_icon.icon = ft.Icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_icon.icon = ft.Icons.LIGHT_MODE
        save_config(
            "dark" if page.theme_mode == ft.ThemeMode.DARK else "light",
            lang_dropdown.value,
        )
        page.update()

    theme_icon.on_click = toggle_theme

    # Idioma
    lang_dropdown.value = get_current_language()

    def on_lang_change(e: ft.ControlEvent) -> None:
        set_language(lang_dropdown.value)
        set_components_language(t)
        save_config(
            "dark" if page.theme_mode == ft.ThemeMode.DARK else "light",
            lang_dropdown.value,
        )
        page.update()

    lang_dropdown.on_change = on_lang_change

    # FilePicker para archivo o carpeta de origen
    def pick_files_result(e: ft.FilePickerResultEvent) -> None:
        path = None
        if e.files and len(e.files) > 0:
            path = e.files[0].path
        elif hasattr(e, "paths") and e.paths and len(e.paths) > 0:
            path = e.paths[0]
        if path:
            selected_path.value = path
            progress_bar.value = 0  # Reiniciar barra
            if Path(path).is_file():
                info = get_video_info(path)
                video_filename_value.value = info["filename"]
                video_duration_value.value = info["duration"]
                video_size_value.value = info["size"]
                video_bitrate_value.value = info["bitrate"]
                video_resolution_value.value = info["resolution"]
                video_codec_value.value = info["codec"]
                video_frame_rate_value.value = info["frame_rate"]
                video_total_frames_value.value = info["total_frames"]
            codec_filter.value = False

        page.update()

    file_picker = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(file_picker)

    # FilePicker para carpeta de destino
    def pick_output_folder_result(e: ft.FilePickerResultEvent) -> None:
        path = None
        if hasattr(e, "path") and e.path:
            path = e.path
        elif hasattr(e, "paths") and e.paths and len(e.paths) > 0:
            path = e.paths[0]
        if path:
            output_folder_path.value = path
            page.update()

    output_folder_picker = ft.FilePicker(on_result=pick_output_folder_result)
    page.overlay.append(output_folder_picker)

    def on_video_codec_change(e: ft.ControlEvent) -> None:
        if video_codec.value in ("h264_nvenc", "hevc_nvenc"):
            preset.options = preset_options_nvenc
        else:
            preset.options = preset_options_cpu
        page.update()
        update_command(None)

    video_codec.on_change = on_video_codec_change

    # Función para actualizar ancho/alto manteniendo aspect ratio
    def update_width(e: ft.ControlEvent) -> None:
        if keep_aspect.value:
            width, height = None, None
            target_height = (
                int(height_field.value) if height_field.value else None
            )
            width, height = video_resolution_value.value.split("x")
            if target_height and width and height:
                w_calc = int(
                    round(target_height * float(width) / float(height))
                )
                width_field.value = str(w_calc)
                page.update()
        update_command(None)

    def update_height(e: ft.ControlEvent) -> None:
        if keep_aspect.value:
            width, height = None, None
            target_width = int(width_field.value) if width_field.value else None
            width, height = video_resolution_value.value.split("x")
            if target_width and width and height:
                h_calc = int(round(target_width * float(height) / float(width)))
                height_field.value = str(h_calc)
                page.update()
        update_command(None)

    width_field.on_change = update_height
    height_field.on_change = update_width

    def on_mi_mode_change(e: ft.ControlEvent) -> None:
        if mi_mode_dropdown.value == "mci":
            mc_mode_dropdown.disabled = False
            me_mode_dropdown.disabled = False
        else:
            mc_mode_dropdown.disabled = True
            me_mode_dropdown.disabled = True
        page.update()
        update_command(None)

    mi_mode_dropdown.on_change = on_mi_mode_change

    def update_command(e: ft.ControlEvent):
        command = f"{get_ffmpeg_path()} -i {selected_path.value}"
        if bitrate_filter.value:
            command += f" -b:v {video_bitrate.value}"
        if crf_filter.value:
            command += f" -crf {crf.value}"
        if output_format.value and output_dropdown.value:
            command += f" -f {output_dropdown.value}"
        else:
            output_dropdown.key = " "
            output_dropdown.value = ""

        if codec_filter.value:
            command += f" -c:v {video_codec.value}"
            if preset.value:
                command += f" -preset {preset.value}"
            if tune_dropdown.value:
                command += f" -tune {tune_dropdown.value}"
        else:
            video_codec.key = " "
            video_codec.value = ""
            preset.key = " "
            preset.value = ""
            tune_dropdown.key = " "
            tune_dropdown.value = ""

        if (
            scale_filter.value
            or frame_rate_filter.value
            or area_crop_edition.value
            or time_crop_edition.value
        ):
            command += " -vf "
        video_filter_command = []
        if scale_filter.value and width_field.value and height_field.value:
            video_filter_command.append(
                f"scale={width_field.value}:{height_field.value}"
            )
        interpolation_command = []
        if frame_rate_filter.value and frame_rate.value:
            original_frame_rate = eval(video_frame_rate_value.value)
            if float(frame_rate.value) > original_frame_rate:
                interpolation_command.append(
                    f"minterpolate=fps={frame_rate.value}"
                )
                if mi_mode_dropdown.value:
                    interpolation_command.append(
                        f"mi_mode={mi_mode_dropdown.value}"
                    )
                    if mi_mode_dropdown.value == "mci":
                        if mc_mode_dropdown.value:
                            interpolation_command.append(
                                f"mc_mode={mc_mode_dropdown.value}"
                            )
                        if me_mode_dropdown.value:
                            interpolation_command.append(
                                f"me_mode={me_mode_dropdown.value}"
                            )
                video_filter_command.append(":".join(interpolation_command))
            else:
                video_filter_command.append(f"fps={frame_rate.value}")
        if area_crop_edition.value:
            video_filter_command.append(f"crop={crop.value}")
        if video_filter_command:
            command += ",".join(video_filter_command)

        if remove_audio.value:
            command += " -an"

        original_path = Path(selected_path.value)
        output_path = (
            Path(output_folder_path.value)
            if output_folder_path.value
            else Path(selected_path.value).parent
        )
        output_extension = (
            output_dropdown.value if output_dropdown.value else "mp4"
        )
        output_filename = f"{original_path.stem}_converted.{output_extension}"
        output = output_path / output_filename
        n = 1
        while output.exists():
            n += 1
            output_filename = (
                f"{original_path.stem}_converted_{n}.{output_extension}"
            )
            output = output_path / output_filename
        command += f" {output}"

        output_audio_base = f"{original_path.stem}_audio.aac"
        if extract_audio.value:
            command += f" -map 0:a -c:a copy {output_audio_base}"

        if time_crop_edition.value:
            command += f" -ss {start_time.value} -t {duration.value}"

        command_text.value = command
        page.update()

    # Call the update_command function whenever a checkbox is toggled
    bitrate_filter.on_change = update_command
    video_bitrate.on_change = update_command
    crf_filter.on_change = update_command
    crf.on_change = update_command
    output_format.on_change = update_command
    output_dropdown.on_change = update_command
    codec_filter.on_change = update_command
    preset.on_change = update_command
    tune_dropdown.on_change = update_command

    scale_filter.on_change = update_command
    frame_rate_filter.on_change = update_command
    frame_rate.on_change = update_command
    mc_mode_dropdown.on_change = update_command
    me_mode_dropdown.on_change = update_command
    area_crop_edition.on_change = update_command
    crop.on_change = update_command

    remove_audio.on_change = update_command
    extract_audio.on_change = update_command
    time_crop_edition.on_change = update_command
    start_time.on_change = update_command
    duration.on_change = update_command

    video_converter = VideoConverter()

    def on_start_conversion(e: ft.ControlEvent) -> None:
        progress_bar.value = 0
        cancel_button.disabled = False
        page.update()
        video_converter.convert_video(command_text.value)
        video_converter.wait()

        status_text.value = (
            "Video processed successfully! ✅"
            if video_converter.ffmpeg_process.returncode == 0
            else "Error processing video: ❌"
        )
        status_text.update()

    start_button.on_click = on_start_conversion

    def on_cancel_conversion(e: ft.ControlEvent) -> None:
        progress_bar.value = 0
        cancel_button.disabled = True
        page.update()
        video_converter.cancel_conversion()
        status_text.value = "Processing video cancelled: ❌"

    cancel_button.on_click = on_cancel_conversion

    return ft.Container(
        content=ft.Column(
            [
                TitleCard(),
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    FileSelectCard(
                                        file_picker=file_picker,
                                        output_folder_picker=output_folder_picker,
                                    ),
                                    VideoInfoCard(),
                                ],
                            ),
                            expand=1,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ConversionParamsCard(),
                                ]
                            ),
                            expand=2,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ProgressCard(),
                                ]
                            ),
                            expand=1,
                        ),
                    ],
                ),
            ]
        ),
        expand=True,
    )
