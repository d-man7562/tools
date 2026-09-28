import os
import subprocess
import sys


def create_tiny_mp4_with_cover(
    mp3_path: str, image_path: str, output_mp4: str
) -> None:
    """Compresses both static video and audio streams so the output easily fits in Gmail (< 25 MB)."""
    if not os.path.exists(mp3_path) or not os.path.exists(image_path):
        raise FileNotFoundError("Input MP3 or image file not found.")

    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        image_path,
        "-i",
        mp3_path,
        # --- VIDEO COMPRESSION ---
        "-c:v",
        "libx264",
        "-crf",
        "51",  # Maximum possible H.264 video compression
        "-preset",
        "ultrafast",  # Fast processing speed
        "-s",
        "320x320",  # Downscale artwork to 320x320
        "-r",
        "1",  # 1 frame per second
        "-tune",
        "stillimage",
        "-pix_fmt",
        "yuv420p",
        # --- AUDIO COMPRESSION ---
        "-c:a",
        "aac",  # Re-encode audio to AAC
        "-b:a",
        "96k",  # 96 kbps bitrate keeps size very small with great audio quality
        "-shortest",
        output_mp4,
    ]

    try:
        subprocess.run(cmd, check=True)

        size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
        print(f"Success! Output MP4 size: {size_mb:.2f} MB")

        if size_mb > 25.0:
            print(
                "Warning: File is still over 25 MB. The audio length may be too long."
            )
        else:
            print("File is ready to attach directly to Gmail!")

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed with exit code {e.returncode}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_mp3> <input_image> <output_mp4>")
        sys.exit(1)

    create_tiny_mp4_with_cover(sys.argv[1], sys.argv[2], sys.argv[3])