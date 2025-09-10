"""
AI Rulesets - Organizational development standards and utilities.

This package provides organizational AI rulesets and utilities for creating custom
development standards and guidelines that AI coding assistants can follow
across all projects and teams.
"""

__version__ = "0.1.0"
__author__ = "Dan Holman"
__email__ = "danxholman@gmail.com"

from .core import Ruleset, RulesetItem, RulesetManager
from .renderers import CursorRenderer, CopilotRenderer, GenericRenderer

__all__ = [
    "Ruleset",
    "RulesetItem", 
    "RulesetManager",
    "CursorRenderer",
    "CopilotRenderer",
    "GenericRenderer",
]
