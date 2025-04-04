from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def add_leaving_soon_badge(image_path: Path, output_path: Path) -> Path:
    print(f"Editing image: {image_path}")
    with Image.open(image_path).convert("RGBA") as img:
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Draw badge rectangle
        badge_height = int(height * 0.1)
        draw.rectangle([(0, height - badge_height), (width, height)], fill=(255, 0, 0, 180))

        # Add text
        font = ImageFont.load_default()
        text = "Leaving Soon"
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]  # width = right - left
        text_height = bbox[3] - bbox[1]  # height = bottom - top

        text_position = ((width - text_width) // 2, height - badge_height + (badge_height - text_height) // 2)
        draw.text(text_position, text, font=font, fill=(255, 255, 255, 255))

        img.save(output_path)
        print(f"Edited image saved to: {output_path}")
        return output_path

