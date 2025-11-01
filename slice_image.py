from PIL import Image
import os

def slice_image(image_path, rows, cols):
    img = Image.open(image_path)
    width, height = img.size
    tile_width = width // cols
    tile_height = height // rows

    output_dir = 'static/tiles'
    os.makedirs(output_dir, exist_ok=True)

    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height

            tile = img.crop((left, upper, right, lower))
            tile.save(os.path.join(output_dir, f'tile_{row}_{col}.png'))

# Example usage for a 3x3 puzzle
slice_image('static/surprise_image.jpg', 4, 4)
