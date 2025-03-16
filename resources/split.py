import os
import sys
from PIL import Image
from glob import glob

def split_image_into_tiles(input_image_path, output_dir, tile_height=32, tile_width=32, start_width_offset=0, width_padding=0):
    """
    Splits the input image into tiles of size tile_size x tile_size and saves them as separate PNG files.

    :param input_image_path: Path to the input PNG image.
    :param output_dir: Directory where the tile images will be saved.
    :param tile_size: Size of each tile (default is 32).
    """
    try:
        # Open the input image
        with Image.open(input_image_path) as img:
            width, height = img.size
            print(f"Input image size: {width}x{height}")

            # Calculate the number of tiles in each dimension
            tiles_x = width // tile_width
            tiles_y = height // tile_height
            print(f"Number of tiles: {tiles_x} horizontally x {tiles_y} vertically")

            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Iterate over each tile position
            for y in range(tiles_y):
                for x in range(tiles_x):
                    left = (x * tile_width) + (x * width_padding) + start_width_offset
                    upper = y * tile_height
                    right = left + tile_width
                    lower = upper + tile_height

                    # Define the bounding box of the tile
                    bbox = (left, upper, right, lower)
                    tile = img.crop(bbox)

                    # Define the tile filename
                    tile_filename = f"tile_{y}_{x}.png"
                    tile_path = os.path.join(output_dir, tile_filename)

                    # Save the tile
                    tile.save(tile_path)
                    print(f"Saved {tile_path}")

            print("Image successfully split into tiles.")

    except FileNotFoundError:
        print(f"Error: The file {input_image_path} was not found.")
    except IOError:
        print(f"Error: The file {input_image_path} is not a valid image or cannot be opened.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    #for fname in glob("tileset/*.png"):
    #    split_image_into_tiles(fname, fname.split('.')[0])
    split_image_into_tiles("tiles.png", "tiles_output", tile_height=16, tile_width=16, start_width_offset=0, width_padding=0)
    
if __name__ == "__main__":
    main()