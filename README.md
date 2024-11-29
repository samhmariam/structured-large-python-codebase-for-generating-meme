# Structured Large Python Codebase for Generating Meme

## Introduction

The goal of this project is to build a "meme generator" – a multimedia application to dynamically generate memes, including an image with an overlaid quote. The application will be able to load quotes from a variety of file types and also load, manipulate, and save images. The application will be able to accept dynamic user input to build and save a new meme.

## Getting Started

### Environment Setup

1. Create a virtual environment and activate it.
2. Install the dependencies using 

    `pip install -r requirements.txt`.

### Project Structure

The project module is structured as follows:

1. QuoteEngine Module: This module is responsible for ingesting many types of files that contain quotes. The quotes are stored in a QuoteModel object. The module is also responsible for ingesting files that contain authors of quotes. The authors are stored in an Author object. 
2. MemeGenerator Module: This module is responsible for manipulating and drawing text onto images. The module is also responsible for loading, manipulating, and saving images. 

### Running the Application

The application can be run using the following two options:

1. Command line interface. The application can be run using the following command:

    ```
        > python meme.py
    ```

    or alternatively with the following optional arguments:

    1. `--body`: The body of the quote.
    2. `--author`: The author of the quote.
    3. `--path`: The path to the image file.

    For example:

    ```
        > python meme.py --body "quote" --author "author" --path "path/to/image"
    ```


2. Web interface. The application can be run using the following command:

    ```
        > python app.py
    ```

    The application can be accessed at the following URL:
    
    ```http://127.0.0.1:5000/```

    






`

