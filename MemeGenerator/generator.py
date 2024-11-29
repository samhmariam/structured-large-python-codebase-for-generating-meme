from PIL import Image, ImageDraw, ImageFont
import os
import random

class MemeEngine:
    """A class to generate memes with text and author on images."""

    def __init__(self, output_dir):
        """
        Initialize the MemeEngine with an output directory.

        :param output_dir: The directory where the generated memes will be saved.
        """
        self.output_dir = output_dir
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
        font = ImageFont.truetype("arial.ttf", size=20)
        text_position = (random.randint(0, width - 100), random.randint(0, new_height - 50))
        draw.text(text_position, f'{text} - {author}', font=font, fill='white')

        output_path = os.path.join(self.output_dir, f'meme_{random.randint(0, 1000000)}.jpg')
        img.save(output_path)
        return output_path
