#!/usr/bin/env python3
"""
Skill packaging script for auto-commit
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_skill_zip(skill_dir: str, output_dir: str = None) -> str:
    """
    Create .skill zip file from skill directory
    
    Args:
        skill_dir: Path to skill directory
        output_dir: Output directory for .skill file (default: same as skill_dir)
    
    Returns:
        Path to created .skill file
    """
    skill_path = Path(skill_dir)
    skill_name = skill_path.name
    
    if output_dir is None:
        output_dir = skill_path.parent
    else:
        output_dir = Path(output_dir)
    
    # Output file path
    output_file = output_dir / f"{skill_name}.skill"
    
    # Create zip file
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through skill directory
        for root, dirs, files in os.walk(skill_path):
            # Skip __pycache__ and other temp directories
            dirs[:] = [d for d in dirs if not d.startswith('__pycache__') and not d.startswith('.')]
            
            for file in files:
                if file.endswith('.pyc'):
                    continue
                    
                file_path = Path(root) / file
                arc_path = file_path.relative_to(skill_path)
                
                zipf.write(file_path, arc_path)
    
    print(f"✅ Skill packaged: {output_file}")
    return str(output_file)

def validate_skill(skill_dir: str) -> list:
    """
    Validate skill structure and requirements
    
    Args:
        skill_dir: Path to skill directory
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    skill_path = Path(skill_dir)
    
    # Check if skill directory exists
    if not skill_path.exists():
        errors.append(f"Skill directory does not exist: {skill_dir}")
        return errors
    
    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md is required")
    else:
        # Check SKILL.md content
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for YAML frontmatter
        if not content.startswith('---'):
            errors.append("SKILL.md must start with YAML frontmatter")
        
        # Check required fields
        if 'name:' not in content:
            errors.append("SKILL.md must have 'name' field in frontmatter")
        if 'description:' not in content:
            errors.append("SKILL.md must have 'description' field in frontmatter")
    
    # Check directories structure
    required_dirs = ['scripts', 'references', 'assets']
    for dir_name in required_dirs:
        dir_path = skill_path / dir_name
        if not dir_path.exists():
            errors.append(f"Directory '{dir_name}' not found (optional but recommended)")
    
    return errors

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill_directory> [output_directory]")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Validate skill
    print("🔍 Validating skill...")
    errors = validate_skill(skill_dir)
    
    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("✅ Skill validation passed")
    
    # Package skill
    print("📦 Packaging skill...")
    try:
        output_file = create_skill_zip(skill_dir, output_dir)
        print(f"🎉 Successfully created skill: {output_file}")
    except Exception as e:
        print(f"❌ Failed to package skill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()