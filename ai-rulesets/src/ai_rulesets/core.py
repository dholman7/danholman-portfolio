"""
Core data structures for AI rulesets and organizational standards.
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from pathlib import Path
import yaml
import json


@dataclass
class RulesetItem:
    """Represents a single rule or guideline within a ruleset."""
    
    name: str
    description: str
    content: str
    tags: List[str] = field(default_factory=list)
    priority: int = 1  # 1 = highest priority
    category: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ruleset item to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "content": self.content,
            "tags": self.tags,
            "priority": self.priority,
            "category": self.category,
        }


@dataclass
class RulesetMetadata:
    """Metadata for a ruleset."""
    
    name: str
    version: str
    description: str
    categories: List[str]
    tags: List[str] = field(default_factory=list)
    author: Optional[str] = None
    maintainer: Optional[str] = None
    license: Optional[str] = None
    target_tools: List[str] = field(default_factory=lambda: ["cursor", "copilot"])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary representation."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "categories": self.categories,
            "tags": self.tags,
            "author": self.author,
            "maintainer": self.maintainer,
            "license": self.license,
            "target_tools": self.target_tools,
        }


@dataclass
class Ruleset:
    """A collection of rules and guidelines for organizational standards."""
    
    metadata: RulesetMetadata
    rules: List[RulesetItem] = field(default_factory=list)
    
    def add_rule(self, rule_item: RulesetItem) -> None:
        """Add a rule item to the ruleset."""
        self.rules.append(rule_item)
        # Sort by priority (highest first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def get_rules_by_tag(self, tag: str) -> List[RulesetItem]:
        """Get all rules that contain the specified tag."""
        return [rule for rule in self.rules if tag in rule.tags]
    
    def get_rules_by_category(self, category: str) -> List[RulesetItem]:
        """Get all rules in the specified category."""
        return [rule for rule in self.rules if rule.category == category]
    
    def get_rules_by_priority(self, min_priority: int = 1) -> List[RulesetItem]:
        """Get all rules with priority >= min_priority."""
        return [rule for rule in self.rules if rule.priority >= min_priority]
    
    def get_all_tags(self) -> Set[str]:
        """Get all unique tags used in this ruleset."""
        tags = set()
        for rule in self.rules:
            tags.update(rule.tags)
        return tags
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ruleset to dictionary representation."""
        return {
            "metadata": self.metadata.to_dict(),
            "rules": [rule.to_dict() for rule in self.rules],
        }
    
    def to_yaml(self) -> str:
        """Convert ruleset to YAML string."""
        return yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False)
    
    def to_json(self) -> str:
        """Convert ruleset to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ruleset":
        """Create ruleset from dictionary."""
        metadata_data = data["metadata"]
        metadata = RulesetMetadata(
            name=metadata_data["name"],
            version=metadata_data["version"],
            description=metadata_data["description"],
            categories=metadata_data["categories"],
            tags=metadata_data.get("tags", []),
            author=metadata_data.get("author"),
            maintainer=metadata_data.get("maintainer"),
            license=metadata_data.get("license"),
            target_tools=metadata_data.get("target_tools", ["cursor", "copilot"]),
        )
        
        rules = []
        for rule_data in data.get("rules", []):
            rule_item = RulesetItem(
                name=rule_data["name"],
                description=rule_data["description"],
                content=rule_data["content"],
                tags=rule_data.get("tags", []),
                priority=rule_data.get("priority", 1),
                category=rule_data.get("category"),
            )
            rules.append(rule_item)
        
        return cls(metadata=metadata, rules=rules)
    
    @classmethod
    def from_yaml(cls, yaml_content: str) -> "Ruleset":
        """Create ruleset from YAML string."""
        data = yaml.safe_load(yaml_content)
        return cls.from_dict(data)
    
    @classmethod
    def from_json(cls, json_content: str) -> "Ruleset":
        """Create ruleset from JSON string."""
        data = json.loads(json_content)
        return cls.from_dict(data)
    
    @classmethod
    def from_file(cls, file_path: Path) -> "Ruleset":
        """Load ruleset from YAML or JSON file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if file_path.suffix.lower() in [".yaml", ".yml"]:
            return cls.from_yaml(content)
        elif file_path.suffix.lower() == ".json":
            return cls.from_json(content)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def save_to_file(self, file_path: Path) -> None:
        """Save ruleset to YAML or JSON file."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.suffix.lower() in [".yaml", ".yml"]:
            content = self.to_yaml()
        elif file_path.suffix.lower() == ".json":
            content = self.to_json()
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)


class RulesetManager:
    """Manages multiple rulesets and provides organizational standards."""
    
    def __init__(self):
        self.rulesets: Dict[str, Ruleset] = {}
        self.standard_rulesets_path = Path(__file__).parent / "rulesets"
    
    def add_ruleset(self, ruleset: Ruleset) -> None:
        """Add a ruleset to the manager."""
        self.rulesets[ruleset.metadata.name] = ruleset
    
    def get_ruleset(self, name: str) -> Optional[Ruleset]:
        """Get a ruleset by name."""
        return self.rulesets.get(name)
    
    def list_rulesets(self) -> List[str]:
        """List all available ruleset names."""
        return list(self.rulesets.keys())
    
    def load_ruleset_from_file(self, file_path: Path) -> Ruleset:
        """Load a ruleset from file and add to manager."""
        ruleset = Ruleset.from_file(file_path)
        self.add_ruleset(ruleset)
        return ruleset
    
    def load_standard_rulesets(self) -> None:
        """Load all standard rulesets from the package."""
        if not self.standard_rulesets_path.exists():
            return
        
        for ruleset_file in self.standard_rulesets_path.rglob("*.yaml"):
            try:
                self.load_ruleset_from_file(ruleset_file)
            except Exception as e:
                print(f"Warning: Failed to load ruleset {ruleset_file}: {e}")
    
    def get_rulesets_by_category(self, category: str) -> List[Ruleset]:
        """Get all rulesets that contain the specified category."""
        return [
            ruleset for ruleset in self.rulesets.values()
            if category in ruleset.metadata.categories
        ]
    
    def get_rulesets_by_tag(self, tag: str) -> List[Ruleset]:
        """Get all rulesets that contain the specified tag."""
        return [
            ruleset for ruleset in self.rulesets.values()
            if tag in ruleset.metadata.tags
        ]
    
    def export_all_rulesets(self, output_dir: Path) -> None:
        """Export all rulesets to a directory."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for name, ruleset in self.rulesets.items():
            output_file = output_dir / f"{name}.yaml"
            ruleset.save_to_file(output_file)
    
    def validate_ruleset(self, ruleset: Ruleset) -> List[str]:
        """Validate a ruleset and return any issues found."""
        issues = []
        
        # Check metadata
        if not ruleset.metadata.name:
            issues.append("Ruleset name is required")
        if not ruleset.metadata.description:
            issues.append("Ruleset description is required")
        if not ruleset.metadata.categories:
            issues.append("At least one category is required")
        
        # Check rules
        if not ruleset.rules:
            issues.append("At least one rule is required")
        
        for i, rule in enumerate(ruleset.rules):
            if not rule.name:
                issues.append(f"Rule {i+1}: Name is required")
            if not rule.content:
                issues.append(f"Rule {i+1}: Content is required")
        
        return issues