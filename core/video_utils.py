import sys
import json
import subprocess
from pathlib import Path


def get_ffmpeg_path():
    """
    Returns the absolute path to ffmpeg executable.
    """
    ffmpeg_exe = "ffmpeg.exe" if sys.platform.startswith("win") else "ffmpeg"
    current_file_path = Path(__file__).resolve()
    ffmpeg_bin_path = (
        current_file_path.parents[1] / "ffmpeg" / "bin" / ffmpeg_exe
    )
    return ffmpeg_bin_path


def get_ffprobe_path():
    """
    Returns the absolute path to ffprobe executable.
    """
    ffprobe_exe = "ffprobe.exe" if sys.platform.startswith("win") else "ffprobe"
    current_file_path = Path(__file__).resolve()
    ffprobe_bin_path = (
        current_file_path.parents[1] / "ffmpeg" / "bin" / ffprobe_exe
    )
    return ffprobe_bin_path


def get_video_info(video_path):
    ffprobe_path = get_ffprobe_path()
    cmd = [
        ffprobe_path,
        "-v",
        "error",
        "-show_entries",
        "format=duration,size,bit_rate:stream=width,height,codec_name,avg_frame_rate,nb_frames",
        "-of",
        "json",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error al analizar el video: {result.stderr}"
    video_info = json.loads(result.stdout)
    video_data = video_info.get("format", {})
    stream_data = video_info.get("streams", [])[0]
    info = {
        "filename": Path(video_path).stem,
        "duration": format_duration(float(video_data.get("duration", 0))),
        "size": format_size(int(video_data.get("size", 0))),
        "bitrate": format_bandwidth(float(video_data.get("bit_rate", "-"))),
        "resolution": f"{stream_data.get('width', '-')}x{stream_data.get('height', '-')}",
        "codec": stream_data.get("codec_name", ""),
        "frame_rate": stream_data.get("avg_frame_rate", ""),
        "total_frames": stream_data.get("nb_frames", "-"),
    }
    return info


def format_duration(total_seconds: float) -> str:
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    parts = []
    if hours:
        parts.append(f"{hours:02d}h")
    if minutes:
        parts.append(f"{minutes:02d}m")
    parts.append(f"{seconds:02d}s")

    return " ".join(parts)


def format_size(size: float) -> str:
    if size < 1024:
        return f"{size:.2f} B"
    elif size < (1024 * 1024):
        kbps = size / 1024
        return f"{kbps:.2f} KB"
    elif size < (1024 * 1024 * 1024):
        mbps = size / (1024 * 1024)
        return f"{mbps:.2f} MB"
    else:
        gbps = size / (1024 * 1024 * 1024)
        return f"{gbps:.2f} GB"


def format_bandwidth(bps: float) -> str:
    if bps < 1_000:
        return f"{bps:.2f} bps"
    elif bps < 1_000_000:
        kbps = bps / 1_000
        return f"{kbps:.2f} Kbps"
    elif bps < 1_000_000_000:
        mbps = bps / 1_000_000
        return f"{mbps:.2f} Mbps"
    else:
        gbps = bps / 1_000_000_000
        return f"{gbps:.2f} Gbps"


def seconds(string_time: str) -> float:
    parts = string_time.split()
    if len(parts) == 3:
        hours = float(parts[0][:-1])
        minutes = float(parts[1][:-1])
        seconds = float(parts[2][:-1])
    elif len(parts) == 2:
        hours = 0
        minutes = float(parts[0][:-1])
        seconds = float(parts[1][:-1])
    return hours * 3600 + minutes * 60 + seconds


def list_seconds(string_list: list) -> float:
    hours = float(string_list[0])
    minutes = float(string_list[1])
    seconds = float(string_list[2])
    return hours * 3600 + minutes * 60 + seconds
