from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

# Get the environment variables
TEXT_SIZE = int(os.getenv("TEXT_SIZE", 80))  # Default to 80 pixels if not set
CORNER_RADIUS = int(os.getenv("CORNER_RADIUS", 20))  # Default to 20 if not set for rounded corners
PADDING = int(os.getenv("BADGE_PADDING", 10))  # Padding for the badge (default is 10 pixels)
HORIZONTAL_ALIGN = os.getenv("HORIZONTAL_ALIGN", "left").lower()  # Default to left
VERTICAL_ALIGN = os.getenv("VERTICAL_ALIGN", "bottom").lower()  # Default to bottom

# Offsets for positioning the text
HORIZONTAL_OFFSET = int(os.getenv("HORIZONTAL_OFFSET", 10))  # Default offset is 10 pixels
VERTICAL_OFFSET = int(os.getenv("VERTICAL_OFFSET", 10))  # Default offset is 10 pixels

def add_leaving_soon_badge(image_path: Path, output_path: Path) -> Path:
    print(f"Editing image: {image_path}")
    with Image.open(image_path).convert("RGBA") as img:
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Set the font size based on the defined environment variable
        try:
            font = ImageFont.truetype("arial.ttf", TEXT_SIZE)
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font if .ttf isn't found

        # Calculate the width and height of the text
        text = "Leaving Soon"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]  # width = right - left
        text_height = bbox[3] - bbox[1]  # height = bottom - top

        # Add padding around the text
        badge_width = text_width + 2 * PADDING
        badge_height = text_height + 2 * PADDING  # Height based on text height + padding

        # Calculate the position for the badge
        if HORIZONTAL_ALIGN == "left":
            x_position = PADDING  # Default to left
        elif HORIZONTAL_ALIGN == "center":
            x_position = (width - badge_width) // 2  # Center horizontally
        elif HORIZONTAL_ALIGN == "right":
            x_position = width - badge_width - PADDING  # Align to the right

        if VERTICAL_ALIGN == "top":
            y_position = PADDING  # Align to the top
        elif VERTICAL_ALIGN == "middle":
            y_position = (height - badge_height) // 2  # Center vertically
        elif VERTICAL_ALIGN == "bottom":
            y_position = height - badge_height - PADDING  # Align to the bottom

        # Apply horizontal offset
        if HORIZONTAL_ALIGN == "left":
            x_position += HORIZONTAL_OFFSET
        elif HORIZONTAL_ALIGN == "center":
            x_position += HORIZONTAL_OFFSET
        elif HORIZONTAL_ALIGN == "right":
            x_position -= HORIZONTAL_OFFSET

        # Apply vertical offset
        if VERTICAL_ALIGN == "top":
            y_position += VERTICAL_OFFSET
        elif VERTICAL_ALIGN == "middle":
            y_position += VERTICAL_OFFSET
        elif VERTICAL_ALIGN == "bottom":
            y_position -= VERTICAL_OFFSET

        # Draw the badge rectangle with rounded corners
        badge_box = [(x_position, y_position), (x_position + badge_width, y_position + badge_height)]
        draw.rounded_rectangle(badge_box, radius=CORNER_RADIUS, fill=(255, 0, 0, 180))

        # Position the text inside the badge area
        text_x = x_position + (badge_width - text_width) // 2
        text_y = y_position + (badge_height - text_height) // 2
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

        img.save(output_path)
        print(f"Edited image saved to: {output_path}")
        return output_path
