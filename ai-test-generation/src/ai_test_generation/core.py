"""
Core data structures for AI test generation guidance templates.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class GuidanceItem:
    """Represents a single guidance item within a guidance template."""
    
    name: str
    description: str
    content: str
    tags: List[str] = field(default_factory=list)
    priority: int = 1  # 1 = highest priority
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert guidance item to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "content": self.content,
            "tags": self.tags,
            "priority": self.priority,
        }


@dataclass
class GuidanceTemplateMetadata:
    """Metadata for a guidance template."""
    
    name: str
    version: str
    description: str
    languages: List[str]
    frameworks: List[str]
    categories: List[str]
    author: Optional[str] = None
    license: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary representation."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "languages": self.languages,
            "frameworks": self.frameworks,
            "categories": self.categories,
            "author": self.author,
            "license": self.license,
        }


@dataclass
class GuidanceTemplate:
    """A collection of guidance items for a specific testing framework or language."""
    
    metadata: GuidanceTemplateMetadata
    guidance: List[GuidanceItem] = field(default_factory=list)
    
    def add_guidance(self, guidance_item: GuidanceItem) -> None:
        """Add a guidance item to the template."""
        self.guidance.append(guidance_item)
        # Sort by priority (highest first)
        self.guidance.sort(key=lambda g: g.priority, reverse=True)
    
    def get_guidance_by_tag(self, tag: str) -> List[GuidanceItem]:
        """Get all guidance items that contain the specified tag."""
        return [item for item in self.guidance if tag in item.tags]
    
    def get_guidance_by_priority(self, min_priority: int = 1) -> List[GuidanceItem]:
        """Get all guidance items with priority >= min_priority."""
        return [item for item in self.guidance if item.priority >= min_priority]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert guidance template to dictionary representation."""
        return {
            "metadata": self.metadata.to_dict(),
            "guidance": [item.to_dict() for item in self.guidance],
        }
    
    def to_yaml(self) -> str:
        """Convert guidance template to YAML string."""
        return yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GuidanceTemplate":
        """Create guidance template from dictionary."""
        metadata_data = data["metadata"]
        metadata = GuidanceTemplateMetadata(
            name=metadata_data["name"],
            version=metadata_data["version"],
            description=metadata_data["description"],
            languages=metadata_data["languages"],
            frameworks=metadata_data["frameworks"],
            categories=metadata_data["categories"],
            author=metadata_data.get("author"),
            license=metadata_data.get("license"),
        )
        
        guidance = []
        for guidance_data in data.get("guidance", []):
            guidance_item = GuidanceItem(
                name=guidance_data["name"],
                description=guidance_data["description"],
                content=guidance_data["content"],
                tags=guidance_data.get("tags", []),
                priority=guidance_data.get("priority", 1),
            )
            guidance.append(guidance_item)
        
        return cls(metadata=metadata, guidance=guidance)
    
    @classmethod
    def from_yaml(cls, yaml_content: str) -> "GuidanceTemplate":
        """Create guidance template from YAML string."""
        data = yaml.safe_load(yaml_content)
        return cls.from_dict(data)
    
    @classmethod
    def from_file(cls, file_path: Path) -> "GuidanceTemplate":
        """Load guidance template from YAML file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return cls.from_yaml(f.read())
    
    def save_to_file(self, file_path: Path) -> None:
        """Save guidance template to YAML file."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.to_yaml())
    
    @classmethod
    def load(cls, language: str, framework: str) -> "GuidanceTemplate":
        """Load a predefined guidance template by language and framework."""
        # This would load from the templates directory
        # For now, return a placeholder
        raise NotImplementedError("Predefined guidance templates not yet implemented")
