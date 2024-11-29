"""
QuoteEngine package.

This package contains modules for ingesting and processing quotes.
"""

from .quote import Ingestor  # Ensure Ingestor is correctly imported
from .quote import QuoteModel  # Ensure QuoteModel is correctly imported

__all__ = ['Ingestor', 'QuoteModel']
