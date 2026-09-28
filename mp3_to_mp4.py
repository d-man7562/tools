import os
import subprocess
import sys

def convert_mp3_to_black_screen_mp4(
    input_mp3_path: str, output_mp4_path: str
) -> None:
    """Converts an MP3 file into an MP4 with a solid black screen.

    - Audio stream is copied directly without re-encoding (zero quality loss).
    - Resolution is minimal (2x2 pixels) and framerate is 1 FPS to keep size extremely low.
    """
    if not os.path.exists(input_mp3_path):
        raise FileNotFoundError(f"Source audio file not found: {input_mp3_path}")

    # FFmpeg Command Breakdown:
    # -f lavfi -i color=c=black:s=1080x1080:r=1 -> Generates a 1080x1080 black frame at 1 fps
    # -i input_mp3_path -> Input audio file
    # -c:a copy -> Direct audio stream copy (no quality loss)
    # -c:v libx264 -preset ultrafast -crf 51 -> Maximum video compression
    # -tune stillimage -> Optimizes video codec for still/static video frames
    # -pix_fmt yuv420p -> Ensures maximum MP4 hardware/software playback compatibility
    # -shortest -> Truncates output video duration to match audio length exact match
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "color=c=black:s=1080x1080:r=30",
        "-i",
        input_mp3_path,
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-ar",
        "44100",
        "-c:v",
        "copy",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "51",
        "-tune",
        "stillimage",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        output_mp4_path,
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Successfully created: {output_mp4_path}")
    except FileNotFoundError:
        print(
            "Error: FFmpeg is not installed or not available in PATH. Please install FFmpeg."
        )
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg execution failed:\n{e.stderr.decode()}")


if __name__ == "__main__":
    # Specify your filenames here
    audio_file = sys.argv[1]
    video_file = sys.argv[2]

    convert_mp3_to_black_screen_mp4(audio_file, video_file)