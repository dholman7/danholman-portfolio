"""
AI Test Generation Framework - Guidance templates for AI-powered test generation.

This package provides structured guidance templates for generating tests across different
testing frameworks and languages, designed to work with AI coding assistants
like Cursor, GitHub Copilot, and others.
"""

__version__ = "0.1.0"
__author__ = "Dan Holman"
__email__ = "danxholman@gmail.com"

from .core import GuidanceTemplate, GuidanceItem
from .renderers import CursorRenderer, CopilotRenderer

__all__ = [
    "GuidanceTemplate",
    "GuidanceItem", 
    "CursorRenderer",
    "CopilotRenderer",
]
