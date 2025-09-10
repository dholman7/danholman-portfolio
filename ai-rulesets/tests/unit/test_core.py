"""
Tests for core AI test generation functionality.
"""

import pytest
from pathlib import Path
import tempfile
import yaml

from ai_rulesets.core import GuidanceItem, GuidanceTemplateMetadata, GuidanceTemplate


@pytest.mark.unit
class TestGuidanceItem:
    """Test GuidanceItem class functionality."""
    
    @pytest.mark.unit
    def test_rule_creation(self):
        """Test creating a rule."""
        rule = GuidanceItem(
            name="Test GuidanceItem",
            description="A test rule",
            content="Test content",
            tags=["test"],
            priority=1
        )
        
        assert rule.name == "Test GuidanceItem"
        assert rule.description == "A test rule"
        assert rule.content == "Test content"
        assert rule.tags == ["test"]
        assert rule.priority == 1
    
    @pytest.mark.unit
    def test_rule_to_dict(self):
        """Test converting rule to dictionary."""
        rule = GuidanceItem(
            name="Test GuidanceItem",
            description="A test rule",
            content="Test content",
            tags=["test"],
            priority=1
        )
        
        rule_dict = rule.to_dict()
        
        assert rule_dict["name"] == "Test GuidanceItem"
        assert rule_dict["description"] == "A test rule"
        assert rule_dict["content"] == "Test content"
        assert rule_dict["tags"] == ["test"]
        assert rule_dict["priority"] == 1


@pytest.mark.unit
class TestGuidanceTemplateMetadata:
    """Test GuidanceTemplateMetadata class functionality."""
    
    def test_metadata_creation(self):
        """Test creating metadata."""
        metadata = GuidanceTemplateMetadata(
            name="Test GuidanceItem Set",
            version="1.0.0",
            description="A test rule set",
            languages=["python"],
            frameworks=["pytest"],
            categories=["unit"],
            author="Test Author"
        )
        
        assert metadata.name == "Test GuidanceItem Set"
        assert metadata.version == "1.0.0"
        assert metadata.description == "A test rule set"
        assert metadata.languages == ["python"]
        assert metadata.frameworks == ["pytest"]
        assert metadata.categories == ["unit"]
        assert metadata.author == "Test Author"
    
    def test_metadata_to_dict(self):
        """Test converting metadata to dictionary."""
        metadata = GuidanceTemplateMetadata(
            name="Test GuidanceItem Set",
            version="1.0.0",
            description="A test rule set",
            languages=["python"],
            frameworks=["pytest"],
            categories=["unit"]
        )
        
        metadata_dict = metadata.to_dict()
        
        assert metadata_dict["name"] == "Test GuidanceItem Set"
        assert metadata_dict["version"] == "1.0.0"
        assert metadata_dict["description"] == "A test rule set"
        assert metadata_dict["languages"] == ["python"]
        assert metadata_dict["frameworks"] == ["pytest"]
        assert metadata_dict["categories"] == ["unit"]


@pytest.mark.unit
class TestGuidanceTemplate:
    """Test GuidanceTemplate class functionality."""
    
    def test_template_creation(self):
        """Test creating a rule set."""
        metadata = GuidanceTemplateMetadata(
            name="Test GuidanceItem Set",
            version="1.0.0",
            description="A test rule set",
            languages=["python"],
            frameworks=["pytest"],
            categories=["unit"]
        )
        
        template = GuidanceTemplate(metadata=metadata)
        
        assert template.metadata == metadata
        assert template.guidance == []
    
    def test_add_guidance(self):
        """Test adding guidance to rule set."""
        metadata = GuidanceTemplateMetadata(
            name="Test GuidanceItem Set",
            version="1.0.0",
            description="A test rule set",
            languages=["python"],
            frameworks=["pytest"],
            categories=["unit"]
        )
        
        template = GuidanceTemplate(metadata=metadata)
        
        rule1 = GuidanceItem("GuidanceItem 1", "First rule", "Content 1", priority=2)
        rule2 = GuidanceItem("GuidanceItem 2", "Second rule", "Content 2", priority=1)
        
        template.add_guidance(rule1)
        template.add_guidance(rule2)
        
        # GuidanceItems should be sorted by priority (highest first)
        assert template.guidance[0] == rule1  # priority 2 (higher)
        assert template.guidance[1] == rule2  # priority 1 (lower)
    
    def test_get_guidance_by_tag(self):
        """Test getting guidance by tag."""
        metadata = GuidanceTemplateMetadata(
            name="Test GuidanceItem Set",
            version="1.0.0",
            description="A test rule set",
            languages=["python"],
            frameworks=["pytest"],
            categories=["unit"]
        )
        
        template = GuidanceTemplate(metadata=metadata)
        
        rule1 = GuidanceItem("GuidanceItem 1", "First rule", "Content 1", tags=["test", "unit"])
        rule2 = GuidanceItem("GuidanceItem 2", "Second rule", "Content 2", tags=["integration"])
        rule3 = GuidanceItem("GuidanceItem 3", "Third rule", "Content 3", tags=["test", "e2e"])
        
        template.add_guidance(rule1)
        template.add_guidance(rule2)
        template.add_guidance(rule3)
        
        test_guidance = template.get_guidance_by_tag("test")
        assert len(test_guidance) == 2
        assert rule1 in test_guidance
        assert rule3 in test_guidance
        assert rule2 not in test_guidance
    
    def test_to_yaml(self):
        """Test converting rule set to YAML."""
        metadata = GuidanceTemplateMetadata(
            name="Test GuidanceItem Set",
            version="1.0.0",
            description="A test rule set",
            languages=["python"],
            frameworks=["pytest"],
            categories=["unit"]
        )
        
        template = GuidanceTemplate(metadata=metadata)
        template.add_guidance(GuidanceItem("Test GuidanceItem", "A test rule", "Test content"))
        
        yaml_content = template.to_yaml()
        
        # Should be valid YAML
        parsed = yaml.safe_load(yaml_content)
        assert parsed["metadata"]["name"] == "Test GuidanceItem Set"
        assert len(parsed["guidance"]) == 1
        assert parsed["guidance"][0]["name"] == "Test GuidanceItem"
    
    def test_from_yaml(self):
        """Test creating rule set from YAML."""
        yaml_content = """
metadata:
  name: "Test GuidanceItem Set"
  version: "1.0.0"
  description: "A test rule set"
  languages: ["python"]
  frameworks: ["pytest"]
  categories: ["unit"]

guidance:
  - name: "Test GuidanceItem"
    description: "A test rule"
    content: "Test content"
    tags: ["test"]
    priority: 1
"""
        
        template = GuidanceTemplate.from_yaml(yaml_content)
        
        assert template.metadata.name == "Test GuidanceItem Set"
        assert template.metadata.version == "1.0.0"
        assert len(template.guidance) == 1
        assert template.guidance[0].name == "Test GuidanceItem"
    
    def test_save_and_load_file(self):
        """Test saving and loading rule set to/from file."""
        metadata = GuidanceTemplateMetadata(
            name="Test GuidanceItem Set",
            version="1.0.0",
            description="A test rule set",
            languages=["python"],
            frameworks=["pytest"],
            categories=["unit"]
        )
        
        template = GuidanceTemplate(metadata=metadata)
        template.add_guidance(GuidanceItem("Test GuidanceItem", "A test rule", "Test content"))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            # Save to file
            template.save_to_file(temp_path)
            
            # Load from file
            loaded_template = GuidanceTemplate.from_file(temp_path)
            
            assert loaded_template.metadata.name == template.metadata.name
            assert len(loaded_template.guidance) == len(template.guidance)
            assert loaded_template.guidance[0].name == template.guidance[0].name
        
        finally:
            # Clean up
            temp_path.unlink()
