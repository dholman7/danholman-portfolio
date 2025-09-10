"""
Hierarchical rulesets for organizational standards.

This module provides a hierarchical structure for organizing rulesets by domain
and purpose. Developers can import rulesets at different levels of granularity
based on their needs.

Organization:
- python/          # Python-specific rulesets (coding, testing, security)
- typescript/      # TypeScript-specific rulesets (coding, testing)
- documentation/   # Documentation standards (style, structure)
- ci-cd/          # CI/CD standards (github-actions, deployment)
- security/       # Cross-cutting security standards
- testing/        # Cross-cutting testing standards
"""

from .python import PythonDomain
from .typescript import TypeScriptDomain
from .documentation import DocumentationDomain
from .ci_cd import CICDDomain
from .security import SecurityDomain
from .testing import TestingDomain

# Domain-level imports
python = PythonDomain()
typescript = TypeScriptDomain()
documentation = DocumentationDomain()
ci_cd = CICDDomain()
security = SecurityDomain()
testing = TestingDomain()

__all__ = [
    "python",
    "typescript", 
    "documentation",
    "ci_cd",
    "security",
    "testing",
    "PythonDomain",
    "TypeScriptDomain",
    "DocumentationDomain",
    "CICDDomain",
    "SecurityDomain",
    "TestingDomain",
]