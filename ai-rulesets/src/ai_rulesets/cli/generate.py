"""
Generate rulesets from source files.
"""

import click
from pathlib import Path
from typing import List, Optional

from ai_rulesets.sources.processor import SourceProcessor
from ai_rulesets.renderers import CursorRenderer, CopilotRenderer, GenericRenderer


@click.command()
@click.option("--sources", "-s", type=click.Path(), default="src/ai_rulesets/sources",
              help="Source directory containing markdown files")
@click.option("--output", "-o", type=click.Path(), default="src/ai_rulesets/rulesets",
              help="Output directory for generated rulesets")
@click.option("--format", "-f", type=click.Choice(["cursor", "copilot", "generic", "all"]),
              default="all", help="Output format for rulesets")
@click.option("--domain", "-d", help="Specific domain to generate (python, typescript, etc.)")
@click.option("--category", "-c", help="Specific category to generate (coding, testing, etc.)")
def generate_rulesets(sources: str, output: str, format: str, domain: Optional[str], category: Optional[str]):
    """Generate rulesets from source markdown files."""
    sources_path = Path(sources)
    output_path = Path(output)
    
    if not sources_path.exists():
        click.echo(f"Error: Sources directory {sources_path} does not exist")
        return
    
    click.echo(f"Generating rulesets from: {sources_path}")
    click.echo(f"Output directory: {output_path}")
    click.echo(f"Format: {format}")
    
    processor = SourceProcessor(sources_path)
    
    if domain and category:
        # Generate specific domain/category
        source_file = sources_path / domain / f"{category}.md"
        if not source_file.exists():
            click.echo(f"Error: Source file {source_file} does not exist")
            return
        
        ruleset = processor.process_markdown_file(source_file, domain, category)
        _generate_ruleset_files(ruleset, output_path, format, domain, category)
        
    elif domain:
        # Generate all categories for domain
        domain_dir = sources_path / domain
        if not domain_dir.exists():
            click.echo(f"Error: Domain directory {domain_dir} does not exist")
            return
        
        for source_file in domain_dir.glob("*.md"):
            category = source_file.stem
            ruleset = processor.process_markdown_file(source_file, domain, category)
            _generate_ruleset_files(ruleset, output_path, format, domain, category)
            
    else:
        # Generate all domains and categories
        all_rulesets = processor.process_all_sources()
        
        for domain_name, categories in all_rulesets.items():
            for category_name, ruleset in categories.items():
                _generate_ruleset_files(ruleset, output_path, format, domain_name, category_name)
    
    click.echo("Ruleset generation completed!")


def _generate_ruleset_files(ruleset, output_path: Path, format: str, domain: str, category: str):
    """Generate ruleset files in the specified format(s)."""
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create domain directory
    domain_dir = output_path / domain
    domain_dir.mkdir(exist_ok=True)
    
    formats = [format] if format != "all" else ["cursor", "copilot", "generic"]
    
    for fmt in formats:
        if fmt == "cursor":
            renderer = CursorRenderer()
            filename = f"{domain}-{category}-standards.mdc"
        elif fmt == "copilot":
            renderer = CopilotRenderer()
            filename = f"{domain}-{category}-standards.instructions.md"
        else:  # generic
            renderer = GenericRenderer()
            filename = f"{domain}-{category}-standards.md"
        
        output_file = domain_dir / filename
        renderer.render_file(ruleset, output_file)
        click.echo(f"Generated: {output_file}")


@click.command()
@click.option("--sources", "-s", type=click.Path(), default="src/ai_rulesets/sources",
              help="Source directory containing markdown files")
@click.option("--output", "-o", type=click.Path(), default=".cursor/rules",
              help="Output directory for generated rulesets")
@click.option("--format", "-f", type=click.Choice(["cursor", "copilot", "generic"]),
              default="cursor", help="Output format for rulesets")
def generate_from_sources(sources: str, output: str, format: str):
    """Generate rulesets from source files and output to specified directory."""
    sources_path = Path(sources)
    output_path = Path(output)
    
    if not sources_path.exists():
        click.echo(f"Error: Sources directory {sources_path} does not exist")
        return
    
    click.echo(f"Generating {format} rulesets from: {sources_path}")
    click.echo(f"Output directory: {output_path}")
    
    processor = SourceProcessor(sources_path)
    all_rulesets = processor.process_all_sources()
    
    for domain_name, categories in all_rulesets.items():
        for category_name, ruleset in categories.items():
            _generate_ruleset_files(ruleset, output_path, format, domain_name, category_name)
    
    click.echo(f"Generated {format} rulesets in {output_path}")
