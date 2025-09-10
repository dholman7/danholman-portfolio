"""
CI/CD standards rulesets.

This module provides CI/CD guidelines including GitHub Actions, deployment,
and infrastructure patterns.
"""

from .github_actions import GitHubActionsRuleset
from .deployment import DeploymentRuleset


class CICDDomain:
    """CI/CD standards domain."""
    
    def __init__(self):
        self.github_actions = GitHubActionsRuleset()
        self.deployment = DeploymentRuleset()
    
    def apply_all(self, output_dir: str = ".cursor/rules"):
        """Apply all CI/CD rulesets to the specified output directory."""
        self.github_actions.apply(output_dir)
        self.deployment.apply(output_dir)
    
    def list_rulesets(self):
        """List all available CI/CD rulesets."""
        return {
            "github_actions": self.github_actions.metadata.name,
            "deployment": self.deployment.metadata.name,
        }


# Convenience imports
github_actions = GitHubActionsRuleset()
deployment = DeploymentRuleset()

__all__ = [
    "CICDDomain",
    "GitHubActionsRuleset",
    "DeploymentRuleset",
    "github_actions",
    "deployment",
]
