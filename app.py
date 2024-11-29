"""
This module provides a Flask web application for generating memes.

It allows users to create memes with random quotes or user-defined quotes
and images.
"""

import os
import random
import requests
from flask import Flask, render_template, abort, request

from MemeGenerator import MemeEngine
from QuoteEngine import Ingestor

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources."""
    quote_files = [
        './_data/DogQuotes/DogQuotesTXT.txt',
        './_data/DogQuotes/DogQuotesDOCX.docx',
        './_data/DogQuotes/DogQuotesPDF.pdf',
        './_data/DogQuotes/DogQuotesCSV.csv'
    ]

    # Use the Ingestor class to parse all files in the quote_files variable
    quotes = []
    for file in quote_files:
        quotes.extend(Ingestor.parse(file))

    images_path = "./_data/photos/dog/"

    # find all images within the images_path directory
    imgs = [
        os.path.join(images_path, img)
        for img in os.listdir(images_path)
        if img.endswith(('jpg', 'jpeg', 'png'))
    ]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme.
    1. Use requests to save the image to a temp local file.
    2. Use the meme object to generate a meme.
    3. Remove the temporary saved image.
    """
    # 1. Use requests to save the image to a temp local file.
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    try:
        r = requests.get(image_url)
        r.raise_for_status()
        img_path = f'./tmp/{random.randint(0, 1000000)}.png'
        with open(img_path, 'wb') as file:
            file.write(r.content)

        # 2. Use the meme object to generate a meme.
        path = meme.make_meme(img_path, body, author)

        # 3. Remove the temporary saved image.
        os.remove(img_path)

        return render_template('meme.html', path=path)
    except requests.exceptions.RequestException as e:
        # Show a friendly message to the user
        return render_template(
            'meme_form.html',
            error="Invalid image URL. Please try again."
        )
    except Exception as e:
        print(f'Error: {e}')
        return render_template('meme_error.html')


if __name__ == "__main__":
    app.run()
