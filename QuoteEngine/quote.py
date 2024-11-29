"""
This module provides classes and methods to ingest and parse quotes from various file formats.
"""

import os
import csv
import docx
import subprocess
import tempfile
from abc import ABC, abstractmethod
from typing import List, Type
import pandas as pd


class QuoteModel:
    """A class to encapsulate a quote and its author."""

    def __init__(self, body, author):
        """
        Initialize a new QuoteModel instance.

        :param body: The body of the quote.
        :param author: The author of the quote.
        """
        self.body = body
        self.author = author

    def __str__(self):
        """
        Return a string representation of the QuoteModel instance.

        :return: A string in the format '"body" - author'.
        """
        return f'"{self.body}" - {self.author}'


class IngestorInterface(ABC):
    """An abstract base class for all ingestors."""

    @classmethod
    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the given file can be ingested.

        :param path: The path to the file.
        :return: True if the file can be ingested, False otherwise.
        """
        pass

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the given file and return a list of QuoteModel instances.

        :param path: The path to the file.
        :return: A list of QuoteModel instances.
        """
        pass


class CSVIngestor(IngestorInterface):
    """An ingestor for CSV files."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the given file is a CSV file.

        :param path: The path to the file.
        :return: True if the file is a CSV file, False otherwise.
        """
        return path.endswith('.csv')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the given CSV file and return a list of QuoteModel instances.

        :param path: The path to the CSV file.
        :return: A list of QuoteModel instances.
        """
        quotes = []
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            new_quote = QuoteModel(row['body'], row['author'])
            quotes.append(new_quote)
        return quotes


class DocxIngestor(IngestorInterface):
    """An ingestor for DOCX files."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the given file is a DOCX file.

        :param path: The path to the file.
        :return: True if the file is a DOCX file, False otherwise.
        """
        return path.endswith('.docx')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the given DOCX file and return a list of QuoteModel instances.

        :param path: The path to the DOCX file.
        :return: A list of QuoteModel instances.
        """
        quotes = []
        doc = docx.Document(path)
        for para in doc.paragraphs:
            if para.text != "":
                body, author = para.text.split(' - ')
                new_quote = QuoteModel(body, author)
                quotes.append(new_quote)
        return quotes


class PDFIngestor(IngestorInterface):
    """An ingestor for PDF files."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the given file is a PDF file.

        :param path: The path to the file.
        :return: True if the file is a PDF file, False otherwise.
        """
        return path.endswith('.pdf')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the given PDF file and return a list of QuoteModel instances.

        :param path: The path to the PDF file.
        :return: A list of QuoteModel instances.
        """
        quotes = []
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
            temp_filename = temp_file.name
            subprocess.call(['pdftotext', path, temp_filename])
            with open(temp_filename, 'r') as file:
                content = file.read()
                for line in content.split('\n'):
                    if line.strip() != "":
                        try:
                            body, author = line.split(' - ')
                        except ValueError:
                            continue  # Skip lines that don't have exactly one ' - '
                        new_quote = QuoteModel(body.strip(), author.strip())
                        quotes.append(new_quote)
        os.remove(temp_filename)
        return quotes


class TXTIngestor(IngestorInterface):
    """An ingestor for TXT files."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the given file is a TXT file.

        :param path: The path to the file.
        :return: True if the file is a TXT file, False otherwise.
        """
        return path.endswith('.txt')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the given TXT file and return a list of QuoteModel instances.

        :param path: The path to the TXT file.
        :return: A list of QuoteModel instances.
        """
        quotes = []
        with open(path, 'r') as file:
            for line in file:
                if line != "":
                    try:
                        body, author = line.split(' - ')
                    except ValueError:
                        continue  # Skip lines that don't have exactly one ' - '
                    new_quote = QuoteModel(body, author)
                    quotes.append(new_quote)
        return quotes


class Ingestor(IngestorInterface):
    """A class to encapsulate all ingestors and provide a single interface."""

    ingestors = [CSVIngestor, DocxIngestor, PDFIngestor, TXTIngestor]

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the given file can be ingested by any of the available ingestors.

        :param path: The path to the file.
        :return: True if the file can be ingested, False otherwise.
        """
        ext = os.path.splitext(path)[1]
        return ext in ['.csv', '.docx', '.pdf', '.txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the given file using the appropriate ingestor and return a list of QuoteModel instances.

        :param path: The path to the file.
        :return: A list of QuoteModel instances.
        :raises ValueError: If the file cannot be ingested.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f'Cannot ingest file with extension {os.path.splitext(path)[1]}')
