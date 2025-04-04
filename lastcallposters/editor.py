from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import yaml
import os
from datetime import datetime, timedelta

def get_config():
    config_path = os.getenv("CONFIG_PATH", "/app/config.yaml")
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)

config = get_config()

badge_config = config["badge_customization"]
text_config = config["text_positioning"]

TEXT_SCALE = badge_config["text_scale"]
PADDING_SCALE = badge_config["padding_scale"]
CORNER_RADIUS_SCALE = badge_config["corner_radius_scale"]
HORIZONTAL_ALIGN = text_config["horizontal_align"]
VERTICAL_ALIGN = text_config["vertical_align"]
HORIZONTAL_OFFSET_SCALE = text_config["horizontal_offset_scale"]
VERTICAL_OFFSET_SCALE = text_config["vertical_offset_scale"]

def add_leaving_soon_badge(image_path: Path, output_path: Path, add_date: str, delete_after_days: int) -> Path:
    print(f"Editing image: {image_path}")
    with Image.open(image_path).convert("RGBA") as img:
        width, height = img.size

        # Create a transparent overlay
        overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        # Parse the new date format
        add_date_obj = datetime.strptime(add_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = add_date_obj + timedelta(days=delete_after_days)

        # Determine the suffix for the day
        day = end_date.day
        if 11 <= day <= 13:  # Special case for 11th, 12th, 13th
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

        # Format the date as "Aug 20th / Jan 3rd / Feb 18th"
        end_date_str = end_date.strftime(f"%b {day}{suffix}")
        print(f"End date for badge: {end_date_str}")

        # Scaled values
        font_size = int(height * TEXT_SCALE)
        padding = int(height * PADDING_SCALE)
        corner_radius = int(height * CORNER_RADIUS_SCALE)
        horizontal_offset = int(height * HORIZONTAL_OFFSET_SCALE)
        vertical_offset = int(height * VERTICAL_OFFSET_SCALE)

        # Set the font size and load the AvenirNextLTPro-Bold font
        font_path = "fonts/AvenirNextLTPro-Bold.ttf" 
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Font not found at {font_path}. Falling back to default font.")
            font = ImageFont.load_default()

        text = f"Leaving {end_date_str}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        badge_width = text_width + 2 * padding
        badge_height = text_height + 2 * padding

        # Horizontal alignment
        if HORIZONTAL_ALIGN == "center":
            x_position = (width - badge_width) // 2 + horizontal_offset
        elif HORIZONTAL_ALIGN == "right":
            x_position = width - badge_width - horizontal_offset
        else:  # left
            x_position = horizontal_offset

        # Vertical alignment
        if VERTICAL_ALIGN == "middle":
            y_position = (height - badge_height) // 2 + vertical_offset
        elif VERTICAL_ALIGN == "top":
            y_position = vertical_offset
        else:  # bottom
            y_position = height - badge_height - vertical_offset

        badge_box = [(x_position, y_position), (x_position + badge_width, y_position + badge_height)]
        draw.rounded_rectangle(badge_box, radius=corner_radius, fill=(255, 0, 0, 110))  # Semi-transparent red

        text_x = x_position + (badge_width - text_width) // 2
        text_y = y_position + (badge_height - text_height) // 2
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

        # Composite the overlay with the original image
        combined = Image.alpha_composite(img, overlay)
        combined.save(output_path)
        print(f"Edited image saved to: {output_path}")
        return output_path
