import subprocess
import re
import time

from ui.components import video_duration_value, progress_bar, status_text

from core.video_utils import format_duration, seconds, list_seconds


class VideoConverter:
    def __init__(self):
        self.ffmpeg_process = None

    def convert_video(self, cmd: str) -> None:
        self.ffmpeg_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self.monitor_process()

    def monitor_process(self) -> None:
        """Monitor the FFmpeg process and display progress."""
        progress_pattern = re.compile(
            r"frame=\s*(\d+).*?fps=\s*([\d\.]+).*?time=\s*(\d+:\d+:\d+\.\d+).*?speed=\s*([\d\.]+)x"
        )

        while True:
            line = self.ffmpeg_process.stderr.readline()
            if not line:
                if self.ffmpeg_process.poll() is not None:
                    break
                time.sleep(0.1)
                continue
            line = line.strip()

            # Show errors
            if "Error" in line or "Invalid" in line or "failed" in line.lower():
                print(f"[bold red]Error:[/bold red] {line}")

            # Match progress line
            match = progress_pattern.search(line)
            if match:
                frame, fps, timestamp, speed = match.groups()

                total_time = seconds(video_duration_value.value)
                current_time = list_seconds(timestamp.replace(":", " ").split())

                progress_bar.value = current_time / total_time if total_time > 0 else 0
                progress_bar.update()

                status_text.value = f"""
                Converting...({current_time / total_time * 100:.2f} %)\n
                {format_duration(current_time)} / {format_duration(total_time)}\n
                Processed Frames: {frame}\n
                Processing speed: {fps} FPS  ({speed}x)
                """
                status_text.update()

    def cancel_conversion(self) -> None:
        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            self.ffmpeg_process.terminate()
            return True
        return False

    def wait(self) -> None:
        self.ffmpeg_process.wait()
