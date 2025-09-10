"""Base validation classes and utilities."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    """Result of a validation check."""
    is_valid: bool
    message: str
    file_path: str
    line_number: Optional[int] = None
    severity: str = "info"  # error, warning, info
    rule: Optional[str] = None


class BaseValidator:
    """Base class for all validators."""
    
    def __init__(self, project_root: str = "."):
        """Initialize validator with project root."""
        self.project_root = project_root
        self.issues: list[ValidationResult] = []
    
    def validate(self) -> list[ValidationResult]:
        """Run validation and return results."""
        raise NotImplementedError("Subclasses must implement validate method")
    
    def get_summary(self) -> dict[str, int]:
        """Get validation summary."""
        summary = {"total": len(self.issues), "errors": 0, "warnings": 0, "info": 0}
        
        for issue in self.issues:
            summary[issue.severity + "s"] += 1
        
        return summary
