"""
Source file processor for generating rulesets from markdown files.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..core import Ruleset, RulesetMetadata, RulesetItem


class SourceProcessor:
    """Processes markdown source files to generate rulesets."""
    
    def __init__(self, sources_dir: Path):
        self.sources_dir = sources_dir
    
    def process_markdown_file(self, file_path: Path, domain: str, category: str) -> Ruleset:
        """Process a markdown file and generate a ruleset."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from first H1
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem.title()
        
        # Create metadata
        metadata = RulesetMetadata(
            name=title,
            version="1.0.0",
            description=f"Organizational {title.lower()} guidelines and best practices",
            categories=[domain, category],
            tags=[domain, category, "standards"],
            author="Dan Holman",
            maintainer="engineering@company.com"
        )
        
        ruleset = Ruleset(metadata=metadata)
        
        # Parse content into rules
        rules = self._parse_markdown_content(content)
        for rule in rules:
            ruleset.add_rule(rule)
        
        return ruleset
    
    def _parse_markdown_content(self, content: str) -> List[RulesetItem]:
        """Parse markdown content into rules."""
        rules = []
        
        # Split content by H2 headers
        sections = re.split(r'^## (.+)$', content, flags=re.MULTILINE)
        
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                rule_name = sections[i].strip()
                rule_content = sections[i + 1].strip()
                
                # Clean up the content
                rule_content = self._clean_markdown_content(rule_content)
                
                # Determine category based on rule name
                category = self._determine_category(rule_name)
                
                # Extract tags from content
                tags = self._extract_tags(rule_content)
                
                rule = RulesetItem(
                    name=rule_name,
                    description=f"{rule_name} guidelines and best practices",
                    content=rule_content,
                    tags=tags,
                    priority=1,
                    category=category
                )
                rules.append(rule)
        
        return rules
    
    def _clean_markdown_content(self, content: str) -> str:
        """Clean markdown content for ruleset."""
        # Remove code block markers but keep the content
        content = re.sub(r'^```\w*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'^```$', '', content, flags=re.MULTILINE)
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = content.strip()
        
        return content
    
    def _determine_category(self, rule_name: str) -> str:
        """Determine category based on rule name."""
        rule_lower = rule_name.lower()
        
        if any(word in rule_lower for word in ['style', 'formatting', 'linting']):
            return 'code-quality'
        elif any(word in rule_lower for word in ['test', 'fixture', 'mock']):
            return 'testing'
        elif any(word in rule_lower for word in ['security', 'encrypt', 'auth']):
            return 'security'
        elif any(word in rule_lower for word in ['performance', 'optimization']):
            return 'performance'
        elif any(word in rule_lower for word in ['error', 'exception', 'handling']):
            return 'error-handling'
        else:
            return 'general'
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from content."""
        tags = []
        
        # Common tag patterns
        tag_patterns = {
            'pytest': ['pytest', 'test'],
            'black': ['black', 'formatting'],
            'ruff': ['ruff', 'linting'],
            'mypy': ['mypy', 'typing'],
            'security': ['security', 'encryption', 'authentication'],
            'performance': ['performance', 'optimization', 'caching'],
            'error-handling': ['error', 'exception', 'logging'],
            'testing': ['test', 'fixture', 'mock', 'coverage']
        }
        
        content_lower = content.lower()
        for tag, keywords in tag_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def process_all_sources(self) -> Dict[str, Dict[str, Ruleset]]:
        """Process all source files and return organized rulesets."""
        rulesets = {}
        
        for domain_dir in self.sources_dir.iterdir():
            if domain_dir.is_dir():
                domain = domain_dir.name
                rulesets[domain] = {}
                
                for source_file in domain_dir.glob('*.md'):
                    category = source_file.stem
                    ruleset = self.process_markdown_file(source_file, domain, category)
                    rulesets[domain][category] = ruleset
        
        return rulesets
