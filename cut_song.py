import sys
import re
from pathlib import Path
from pydub import AudioSegment

def get_next_filename(input_path: Path) -> Path:
    """
    Generates a new path with an incremented number appended to the title.
    - If file.mp3 exists -> generates file_1.mp3
    - If file_1.mp3 exists -> generates file_2.mp3
    """
    stem = input_path.stem
    parent = input_path.parent
    extension = input_path.suffix

    # Check if the filename already ends with a number (e.g., 'song_1' or 'song 1')
    match = re.search(r'^(.*?)[_ -]?(\d+)$', stem)
    
    if match:
        base_title = match.group(1)
        start_num = int(match.group(2))
    else:
        base_title = stem
        start_num = 0

    counter = start_num + 1
    
    while True:
        # Tries 'title_1.mp3', 'title_2.mp3', etc.
        candidate = parent / f"{base_title}_{counter}{extension}"
        if not candidate.exists():
            return candidate
        counter += 1

def trim_mp3(input_file_str: str, seconds_to_trim_str: str):
    input_path = Path(input_file_str)

    if not input_path.is_file():
        print(f"Error: File '{input_file_str}' does not exist.")
        sys.exit(1)

    try:
        seconds_to_trim = float(seconds_to_trim_str)
    except ValueError:
        print(f"Error: Trim duration '{seconds_to_trim_str}' must be a valid number (float).")
        sys.exit(1)

    # Convert seconds to milliseconds for pydub
    start_ms = int(seconds_to_trim * 1000)

    print(f"Loading '{input_path.name}'...")
    audio = AudioSegment.from_file(input_path, format="mp3")

    if start_ms >= len(audio):
        print("Error: The requested trim duration is longer than or equal to the total length of the audio.")
        sys.exit(1)

    # Trim audio from start_ms to the end
    trimmed_audio = audio[start_ms:]

    # Get the unique incremented output path
    output_path = get_next_filename(input_path)

    print(f"Trimming {seconds_to_trim} seconds from the start...")
    trimmed_audio.export(output_path, format="mp3")
    print(f"Saved trimmed clip to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python trim_audio.py <path_to_mp3> <seconds_to_trim_from_start>")
        sys.exit(1)

    trim_mp3(sys.argv[1], sys.argv[2])