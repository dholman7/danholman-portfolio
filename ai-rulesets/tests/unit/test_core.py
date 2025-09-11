"""
Tests for core AI test generation functionality.
"""

import pytest
from pathlib import Path
import tempfile
import yaml

from ai_rulesets.core import RulesetItem, RulesetMetadata, Ruleset


@pytest.mark.unit
class TestRulesetItem:
    """Test RulesetItem class functionality."""
    
    @pytest.mark.unit
    def test_rule_creation(self):
        """Test creating a rule."""
        rule = RulesetItem(
            name="Test RulesetItem",
            description="A test rule",
            content="Test content",
            tags=["test"],
            priority=1
        )
        
        assert rule.name == "Test RulesetItem"
        assert rule.description == "A test rule"
        assert rule.content == "Test content"
        assert rule.tags == ["test"]
        assert rule.priority == 1
    
    @pytest.mark.unit
    def test_rule_to_dict(self):
        """Test converting rule to dictionary."""
        rule = RulesetItem(
            name="Test RulesetItem",
            description="A test rule",
            content="Test content",
            tags=["test"],
            priority=1
        )
        
        rule_dict = rule.to_dict()
        
        assert rule_dict["name"] == "Test RulesetItem"
        assert rule_dict["description"] == "A test rule"
        assert rule_dict["content"] == "Test content"
        assert rule_dict["tags"] == ["test"]
        assert rule_dict["priority"] == 1


@pytest.mark.unit
class TestRulesetMetadata:
    """Test RulesetMetadata class functionality."""
    
    def test_metadata_creation(self):
        """Test creating metadata."""
        metadata = RulesetMetadata(
            name="Test RulesetItem Set",
            version="1.0.0",
            description="A test rule set",
            categories=["unit"],
            author="Test Author"
        )
        
        assert metadata.name == "Test RulesetItem Set"
        assert metadata.version == "1.0.0"
        assert metadata.description == "A test rule set"
        assert metadata.categories == ["unit"]
        assert metadata.author == "Test Author"
    
    def test_metadata_to_dict(self):
        """Test converting metadata to dictionary."""
        metadata = RulesetMetadata(
            name="Test RulesetItem Set",
            version="1.0.0",
            description="A test rule set",
            categories=["unit"]
        )
        
        metadata_dict = metadata.to_dict()
        
        assert metadata_dict["name"] == "Test RulesetItem Set"
        assert metadata_dict["version"] == "1.0.0"
        assert metadata_dict["description"] == "A test rule set"
        assert metadata_dict["categories"] == ["unit"]


@pytest.mark.unit
class TestRuleset:
    """Test Ruleset class functionality."""
    
    def test_template_creation(self):
        """Test creating a rule set."""
        metadata = RulesetMetadata(
            name="Test RulesetItem Set",
            version="1.0.0",
            description="A test rule set",
            categories=["unit"]
        )
        
        template = Ruleset(metadata=metadata)
        
        assert template.metadata == metadata
        assert template.rules == []
    
    def test_add_rule(self):
        """Test adding rule to rule set."""
        metadata = RulesetMetadata(
            name="Test RulesetItem Set",
            version="1.0.0",
            description="A test rule set",
            categories=["unit"]
        )
        
        template = Ruleset(metadata=metadata)
        
        rule1 = RulesetItem("RulesetItem 1", "First rule", "Content 1", priority=2)
        rule2 = RulesetItem("RulesetItem 2", "Second rule", "Content 2", priority=1)
        
        template.add_rule(rule1)
        template.add_rule(rule2)
        
        # RulesetItems should be sorted by priority (highest first)
        assert template.rules[0] == rule1  # priority 2 (higher)
        assert template.rules[1] == rule2  # priority 1 (lower)
    
    def test_get_rules_by_tag(self):
        """Test getting rules by tag."""
        metadata = RulesetMetadata(
            name="Test RulesetItem Set",
            version="1.0.0",
            description="A test rule set",
            categories=["unit"]
        )
        
        template = Ruleset(metadata=metadata)
        
        rule1 = RulesetItem("RulesetItem 1", "First rule", "Content 1", tags=["test", "unit"])
        rule2 = RulesetItem("RulesetItem 2", "Second rule", "Content 2", tags=["integration"])
        rule3 = RulesetItem("RulesetItem 3", "Third rule", "Content 3", tags=["test", "e2e"])
        
        template.add_rule(rule1)
        template.add_rule(rule2)
        template.add_rule(rule3)
        
        test_rules = template.get_rules_by_tag("test")
        assert len(test_rules) == 2
        assert rule1 in test_rules
        assert rule3 in test_rules
        assert rule2 not in test_rules
    
    def test_to_yaml(self):
        """Test converting rule set to YAML."""
        metadata = RulesetMetadata(
            name="Test RulesetItem Set",
            version="1.0.0",
            description="A test rule set",
            categories=["unit"]
        )
        
        template = Ruleset(metadata=metadata)
        template.add_rule(RulesetItem("Test RulesetItem", "A test rule", "Test content"))
        
        yaml_content = template.to_yaml()
        
        # Should be valid YAML
        parsed = yaml.safe_load(yaml_content)
        assert parsed["metadata"]["name"] == "Test RulesetItem Set"
        assert len(parsed["rules"]) == 1
        assert parsed["rules"][0]["name"] == "Test RulesetItem"
    
    def test_from_yaml(self):
        """Test creating rule set from YAML."""
        yaml_content = """
metadata:
  name: "Test RulesetItem Set"
  version: "1.0.0"
  description: "A test rule set"
  categories: ["unit"]

rules:
  - name: "Test RulesetItem"
    description: "A test rule"
    content: "Test content"
    tags: ["test"]
    priority: 1
"""
        
        template = Ruleset.from_yaml(yaml_content)
        
        assert template.metadata.name == "Test RulesetItem Set"
        assert template.metadata.version == "1.0.0"
        assert len(template.rules) == 1
        assert template.rules[0].name == "Test RulesetItem"
    
    def test_save_and_load_file(self):
        """Test saving and loading rule set to/from file."""
        metadata = RulesetMetadata(
            name="Test RulesetItem Set",
            version="1.0.0",
            description="A test rule set",
            categories=["unit"]
        )
        
        template = Ruleset(metadata=metadata)
        template.add_rule(RulesetItem("Test RulesetItem", "A test rule", "Test content"))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            # Save to file
            template.save_to_file(temp_path)
            
            # Load from file
            loaded_template = Ruleset.from_file(temp_path)
            
            assert loaded_template.metadata.name == template.metadata.name
            assert len(loaded_template.rules) == len(template.rules)
            assert loaded_template.rules[0].name == template.rules[0].name
        
        finally:
            # Clean up
            temp_path.unlink()
