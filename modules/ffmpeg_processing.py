import re
import subprocess
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, FilePath
from rich import print

from modules.utils import format_bandwidth, format_duration

FFMPEG_PATH = Path("ffmpeg/bin/ffmpeg.exe")


class VideoInfo(BaseModel):
    """Class to hold video information.
    Attributes:
        source (str): The video source path or identifier.
        width (str): The width of the video in pixels.
        height (str): The height of the video in pixels.
        fps (str): The frames per second of the video.
        total_frames (str): The total number of frames in the video.
    """

    source_path: Optional[FilePath]
    width: int
    height: int
    fps: float
    total_frames: int
    bit_rate: str
    duration: str


def load_video_info(source: FilePath) -> VideoInfo:
    """Load video information using ffprobe.
    Args:
        ffmpeg_path (Path): Path to the ffmpeg executable.
        source (str): The video source path or identifier.
    Returns:
        VideoInfo: An instance of VideoInfo containing video details.
    Raises:
        IOError: If the video information cannot be retrieved.
    """
    try:
        result = subprocess.run(
            [
                str(FFMPEG_PATH.parent / "ffprobe"),
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height,r_frame_rate,nb_frames,duration,codec_name,bit_rate",
                "-of",
                "default=noprint_wrappers=1",
                source,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        info = {}
        for line in result.stdout.split("\n"):
            if "=" in line:
                key, value = line.split("=")
                info[key.strip()] = value.strip()

        video_bitrate = format_bandwidth(float(info.get("bit_rate", 0.0)))
        video_duration = format_duration(float(info.get("duration", 0.0)))

        return VideoInfo(
            source_path=source,
            width=info.get("width", 0),
            height=info.get("height", 0),
            fps=eval(info.get("r_frame_rate", 0.0)),
            total_frames=info.get("nb_frames", 0),
            bit_rate=video_bitrate,
            duration=video_duration,
        )
    except Exception as e:
        raise IOError(f"❌ Failed to get video info: {str(e)}")


def ffmpeg_process(video_info: VideoInfo, components: dict) -> subprocess.Popen:
    output_path = (
        Path(video_info.source_path).parent
        / f"{Path(video_info.source_path).stem}_FFMPEG_EDITED.mp4"
    )
    cmd = [
        str(FFMPEG_PATH),
        "-hwaccel",
        "cuda",
        "-y",
        "-an",
        "-i",
        video_info.source_path,
        "-c:v",
        "h264_nvenc",
    ]
    video_filters = []

    if components["bitrate_input"].value != "":
        if components["unit_selector"].value == "Kbps":
            bitrate_value = float(components["bitrate_input"].value) / 1000
        elif components["unit_selector"].value == "Gbps":
            bitrate_value = float(components["bitrate_input"].value) * 1000
        else:
            bitrate_value = int(components["bitrate_input"].value)

        cmd.extend(["-b:v", f"{bitrate_value}M"])

    if (
        components["width_input"].value != ""
        or components["height_input"].value != ""
    ):
        video_filters.append(
            f"scale={components['width_input'].value}:{components['height_input'].value}"
        )

    interpolations = {
        "Duplicate": "mi_mode=dup",
        "Blend": "mi_mode=blend",
        "Motion-Compensated": "mi_mode=mci",
    }
    compensations = {"Adaptive": "mc_mode=aobmc", "Overlapped": "mc_mode=obmc"}
    estimations = {
        "Bidirectional": "me_mode=bidir",
        "Bilateral": "me_mode=bilat",
    }

    if components["fps_input"].value != "":
        if float(components["fps_input"].value) > video_info.fps:
            interpolation_filter = (
                f"minterpolate=fps={components['fps_input'].value}"
            )
            interpolation_filter += (
                f":{interpolations[components['interpolation_modes'].value]}"
            )
            if components["interpolation_modes"].value == "Motion-Compensated":
                interpolation_filter += (
                    f":{compensations[components['compensation_modes'].value]}"
                )
                interpolation_filter += (
                    f":{estimations[components['estimation_algorithms'].value]}"
                )
        else:
            interpolation_filter = f"fps={components['fps_input'].value}"
        video_filters.append(interpolation_filter)

    if video_filters:
        cmd.extend(["-vf", f"{(',').join(video_filters)}"])
    if components["fps_input"].value != "":
        cmd.extend(["-r", f"{components['fps_input'].value}"])
    cmd.append(str(output_path))
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    return process


def monitor_process(
    process: subprocess.Popen, components: dict
) -> tuple[str, str, str, str]:
    """Monitor the FFmpeg process and display progress."""
    progress_pattern = re.compile(
        r"frame=\s*(\d+).*?fps=\s*([\d\.]+).*?time=\s*(\d+:\d+:\d+\.\d+).*?speed=\s*([\d\.]+)x"
    )

    while True:
        line = process.stderr.readline()
        if not line:
            break
        line = line.strip()

        # Show errors
        if "Error" in line or "Invalid" in line or "failed" in line.lower():
            print(f"[bold red]Error:[/bold red] {line}")

        # Match progress line
        match = progress_pattern.search(line)
        if match:
            frame, fps, timestamp, speed = match.groups()

            components["process_frame_text"].value = frame
            components["process_frame_text"].update()
            components["process_frame_rate_text"].value = fps
            components["process_frame_rate_text"].update()
            components["process_video_time_text"].value = timestamp
            components["process_video_time_text"].update()
            components["process_speed_text"].value = speed
            components["process_speed_text"].update()


def crop_detect(ffmpeg_path: Path, config) -> subprocess.Popen:
    cmd = [
        str(ffmpeg_path),
        "-i",
        config.source,
        "-vf",
        "cropdetect",
        "-an",
        "-t",
        "1",
        "-f",
        "null",
        "-",
    ]

    # Launch process
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    return process


def crop_result(process: subprocess.Popen) -> tuple[str, str, str, str]:
    progress_pattern = re.compile(r"crop=\s*(\d+:\d+:\d+\:\d+)")

    while True:
        line = process.stderr.readline()
        if not line:
            break
        line = line.strip()

        # Show errors
        if "Error" in line or "Invalid" in line or "failed" in line.lower():
            print(f"[bold red]Error:[/bold red] {line}")

        # Match progress line
        match = progress_pattern.search(line)
        if match:
            width, height, x, y = match.groups()[0].split(":")

            return (width, height, x, y)


def crop_video(
    ffmpeg_path: Path, config, crop_area: tuple[str, str, str, str]
) -> subprocess.Popen:
    # Build output path
    output_path = Path(config.source).with_stem(
        f"{Path(config.source).stem}_FFMPEG_CROPPED.mp4"
    )
    width, height, x, y = crop_area
    cmd = [
        str(ffmpeg_path),
        "-i",
        config.source,
        "-c:v",
        "h264_nvenc",
        "-vf",
        f"crop={width}:{height}:{x}:{y}",
        f"{output_path}",
    ]

    # Launch process
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    return process
