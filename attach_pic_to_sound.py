import os
import subprocess
import sys


def create_mp4_with_cover(mp3_path: str, image_path: str, output_mp4: str) -> None:
    """Creates a static-image MP4 video with lossless audio stream copying."""
    if not os.path.exists(mp3_path):
        raise FileNotFoundError(f"Input MP3 not found: {mp3_path}")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        image_path,
        "-i",
        mp3_path,
        "-c:v",
        "libx264",
        "-tune",
        "stillimage",
        "-crf",
        "18",
        "-c:a",
        "copy",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        output_mp4,
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully created MP4: {output_mp4}")
    except FileNotFoundError:
        print("Error: FFmpeg is not installed or not in system PATH.")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed with exit code {e.returncode}")


if __name__ == "__main__":
    # Expects exactly 3 arguments after the script name
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_mp3> <input_image> <output_mp4>")
        sys.exit(1)

    mp3_file = sys.argv[1]
    image_file = sys.argv[2]
    output_file = sys.argv[3]  # The last argument is the output file name

    create_mp4_with_cover(mp3_file, image_file, output_file)