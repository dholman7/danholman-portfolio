"""Code quality validation ruleset."""

from ai_rulesets.sources.processor import SourceProcessor
from ai_rulesets.core import Ruleset


def get_code_quality_ruleset() -> Ruleset:
    """Get the code quality validation ruleset."""
    processor = SourceProcessor()
    return processor.process_markdown_file(
        "ai_rulesets/src/ai_rulesets/sources/quality/code-quality.md"
    )
