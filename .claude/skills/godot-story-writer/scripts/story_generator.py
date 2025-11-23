#!/usr/bin/env python3
"""
Godot Story生成器辅助脚本
用于识别Godot项目和生成Story文档结构
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional

class GodotStoryGenerator:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.docs_path = self.project_path / "docs"
        
    def is_godot_project(self) -> bool:
        """检查是否为Godot项目"""
        return (self.project_path / "project.godot").exists()
    
    def get_project_info(self) -> Dict:
        """获取Godot项目基本信息"""
        project_file = self.project_path / "project.godot"
        if not project_file.exists():
            return {}
            
        config = {}
        with open(project_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 提取项目名称
        name_match = re.search(r'config/name\s*=\s*"([^"]*)"', content)
        if name_match:
            config['name'] = name_match.group(1)
            
        return config
    
    def create_docs_structure(self, modules: List[str]) -> Dict[str, str]:
        """创建文档目录结构"""
        self.docs_path.mkdir(exist_ok=True)
        
        created_dirs = {}
        
        for i, module in enumerate(modules, 1):
            module_dir = self.docs_path / f"{i:02d}_{module}"
            module_dir.mkdir(exist_ok=True)
            created_dirs[module] = str(module_dir)
            
        return created_dirs
    
    def get_next_story_number(self, module_dir: Path) -> int:
        """获取下一个Story文件编号"""
        if not module_dir.exists():
            return 1
            
        story_files = list(module_dir.glob("*.md"))
        if not story_files:
            return 1
            
        numbers = []
        for file in story_files:
            match = re.match(r"(\d+)_.*\.md", file.name)
            if match:
                numbers.append(int(match.group(1)))
                
        return max(numbers) + 1 if numbers else 1

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python story_generator.py <project_path>")
        sys.exit(1)
        
    project_path = sys.argv[1]
    generator = GodotStoryGenerator(project_path)
    
    if not generator.is_godot_project():
        print("错误：指定路径不是Godot项目")
        sys.exit(1)
        
    project_info = generator.get_project_info()
    print(f"检测到Godot项目: {project_info.get('name', '未知项目')}")
    
    # 示例：创建模块目录
    modules = ["gameplay", "ui", "audio", "graphics"]
    dirs = generator.create_docs_structure(modules)
    print(f"创建的文档目录: {dirs}")