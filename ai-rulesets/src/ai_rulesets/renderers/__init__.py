"""
Renderers for different AI coding assistants.
"""

from .cursor import CursorRenderer
from .copilot import CopilotRenderer
from .generic import GenericRenderer

__all__ = ["CursorRenderer", "CopilotRenderer", "GenericRenderer"]
