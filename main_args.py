import argparse
import itertools
from pathlib import Path

# Local modules
from modules.process_config import ProcessConfig, create_config
from modules.ffmpeg_processing import (load_video_info,
                                        process_video,
                                        monitor_process,
                                        crop_detect,
                                        crop_result,
                                        crop_video)

# Local tools
from tools.messages import step_message, source_message


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for the video conversion tool using FFMPEG.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Video conversion tool using FFMPEG")
    parser.add_argument('--source', type=str, required=True, help='video source')
    parser.add_argument('--ffmpeg', type=str, default='ffmpeg/bin/ffmpeg.exe', help='ffmpeg path')
    parser.add_argument('--bitrate', type=str, nargs='?', const='3', default=False, help='bitrate in Mbps')
    parser.add_argument('--resolution', type=str, nargs='?', const='1920:1080', default=False, help='video resolution')
    parser.add_argument('--fps', type=str, nargs='?', const='30', default=False, help='video fps')
    parser.add_argument('--crop-detect', action='store_true', help='detect crop area')

    return parser.parse_args()


def main(config: ProcessConfig) -> None:
    # Initialize process counter
    step_count = itertools.count(1)

    ffmpeg_path = Path(config.ffmpeg_path)

    if not ffmpeg_path.exists():
        raise IOError("FFmpeg not found in specified path ❌")
        
    step_message(str(next(step_count)), "FFMPEG Initialized :white_check_mark:")

    # Get video information
    video_info = load_video_info(
        ffmpeg_path=ffmpeg_path,
        source=config.source )
    
    step_message(str(next(step_count)), "Video Source :white_check_mark:")
    source_message(video_info=video_info)

    if config.crop_detect:
        process = crop_detect(ffmpeg_path=ffmpeg_path, config=config)
        crop_area = crop_result(process)

        if crop_area[2] == '0' and crop_area[3] == '0':
            step_message(next(step_count), 'Crop area not detected ❌')
            return
        step_message(next(step_count), 'Crop area detected ✅')
        
        process = crop_video(ffmpeg_path=ffmpeg_path, config=config, crop_area=crop_area)
    else:
        step_message(next(step_count), 'Conversion Started ✅')
        
        process = process_video(ffmpeg_path=ffmpeg_path, config=config)
    
    monitor_process(process)
    
    # Wait for process to finish
    process.wait()

    # Final message
    if process.returncode == 0:
        step_message(next(step_count), 'Video processed successfully! ✅')
    else:
        step_message(next(step_count), "Error processing video: ❌")
    

if __name__ == "__main__":
    options = parse_arguments()
    config = create_config(options)

    main(config)
