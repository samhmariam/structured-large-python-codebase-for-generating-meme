"""
This module contains the MemeEngine class which is used to generate memes
by adding text and author to images.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import random
import textwrap


class MemeEngine:
    """A class to generate memes with text and author on images."""

    def __init__(self, output_dir, font_path='./_data/fonts/Roboto-Bold.ttf'):
        """
        Initialize the MemeEngine with an output directory and font path.

        :param output_dir: The directory where the generated memes will be saved.
        :param font_path: The file path to the font to be used for the text.
        """
        self.output_dir = output_dir
        self.font_path = font_path
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def make_meme(self, img_path, text, author, width=500) -> str:
        """
        Create a meme with the given image, text, and author.

        :param img_path: The file path to the input image.
        :param text: The text to be added to the image.
        :param author: The author of the text.
        :param width: The desired width of the meme image. Default is 500.
        :return: The file path to the generated meme.
        """
        img = Image.open(img_path)
        original_width, original_height = img.size
        aspect_ratio = original_height / original_width
        new_height = int(width * aspect_ratio)
        img = img.resize((width, new_height), Image.LANCZOS)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font_path, size=20)
        
        # Wrap the text
        wrapped_text = textwrap.fill(text, width=40)
        full_text = f'{wrapped_text}\n- {author}'
        
        # Calculate text size using textbbox
        text_bbox = draw.textbbox((0, 0), full_text, font=font)
        text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
        
        # Calculate text size and position to center it
        text_x = (width - text_size[0]) / 2
        text_y = (new_height - text_size[1]) / 2
        
        draw.text((text_x, text_y), full_text, font=font, fill='white')

        output_path = os.path.join(
            self.output_dir, f'meme_{random.randint(0, 1000000)}.jpg'
        )
        img.save(output_path)
        return output_path
