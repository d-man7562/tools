from PIL import Image
import os
import sys
def convert_webp_to_jpg(webp_path, jpg_path=None):
    """
    Converts a WebP image file to a JPG image file using the Pillow library.

    Args:
        webp_path (str): The file path of the input WebP image.
        jpg_path (str, optional): The file path for the output JPG image.
                                  If None, a new path is created based on the 
                                  input path (e.g., 'image.webp' -> 'image.jpg').
    Returns:
        bool: True if conversion was successful, False otherwise.
    """
    try:
        # Open the image file
        img = Image.open(webp_path)

        # Determine the output path if not provided
        if jpg_path is None:
            base, _ = os.path.splitext(webp_path)
            jpg_path = base + ".jpg"

        # Save the image in JPEG format
        # The 'quality' parameter (0-100) controls the compression level.
        # Higher quality means a larger file size.
        img.save(jpg_path, "jpeg", quality=90)
        
        print(f"Successfully converted '{webp_path}' to '{jpg_path}'")
        return True
        
    except FileNotFoundError:
        print(f"Error: Input file not found at '{webp_path}'")
        return False
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return False

# --- Example Usage ---

# 1. Define your input WebP file path

input_file = sys.argv[1]

# 2. Define your output JPG file path (optional, will be derived if None)
output_file = sys.argv[2]


# Example call 1 (specifying output file):
# Note: Ensure a file named 'my_photo.webp' exists in the same directory 
# for this to run successfully.
convert_webp_to_jpg(input_file, output_file)

# Example call 2 (letting the function determine the output name):
# convert_webp_to_jpg(input_file)
#convert_webp_to_jpg('c:\\Users\\owner\\Desktop\\imgbin-osi-model-conceptual-model-communication-protocol-class-diagram-computer-network-others-g4gCiFtSjmGKqQcVKBxP46Gkr_t.webp','c:\\Users\\owner\\Downloads')