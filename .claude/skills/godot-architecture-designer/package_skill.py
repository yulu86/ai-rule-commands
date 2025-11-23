#!/usr/bin/env python3
"""
Godot架构设计技能打包工具
用于将技能打包为.skill文件
"""

import os
import zipfile
import json
from pathlib import Path
from typing import Dict, List
import shutil

def validate_skill(skill_path: str) -> tuple[bool, List[str]]:
    """验证技能结构"""
    errors = []
    
    # 检查必需文件
    required_files = ["SKILL.md"]
    for file in required_files:
        file_path = os.path.join(skill_path, file)
        if not os.path.exists(file_path):
            errors.append(f"缺少必需文件: {file}")
    
    # 检查SKILL.md格式
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if os.path.exists(skill_md_path):
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查YAML frontmatter
        if not content.startswith("---"):
            errors.append("SKILL.md 缺少 YAML frontmatter")
        else:
            # 提取frontmatter内容
            try:
                frontmatter_end = content.find("---", 3)
                if frontmatter_end == -1:
                    errors.append("SKILL.md frontmatter 格式错误")
                else:
                    frontmatter = content[3:frontmatter_end].strip()
                    
                    # 简单检查必需字段
                    if "name:" not in frontmatter:
                        errors.append("frontmatter 缺少 name 字段")
                    if "description:" not in frontmatter:
                        errors.append("frontmatter 缺少 description 字段")
            except Exception as e:
                errors.append(f"解析 frontmatter 时出错: {e}")
    
    # 检查目录结构
    expected_dirs = ["scripts", "references", "assets"]
    for dir_name in expected_dirs:
        dir_path = os.path.join(skill_path, dir_name)
        if not os.path.exists(dir_path):
            errors.append(f"缺少推荐目录: {dir_name}")
    
    return len(errors) == 0, errors

def create_skill_metadata(skill_path: str) -> Dict:
    """创建技能元数据"""
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    
    # 读取SKILL.md内容
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析frontmatter
    frontmatter_end = content.find("---", 3)
    frontmatter_content = content[3:frontmatter_end].strip()
    
    metadata = {
        "format_version": "1.0",
        "skill_type": "architecture_design",
        "category": "godot",
        "files": []
    }
    
    # 解析YAML frontmatter (简化版本)
    for line in frontmatter_content.split('\n'):
        if line.startswith('name:'):
            metadata['name'] = line.split(':', 1)[1].strip().strip('"\'')
        elif line.startswith('description:'):
            metadata['description'] = line.split(':', 1)[1].strip().strip('"\'')
    
    # 收集文件列表
    for root, dirs, files in os.walk(skill_path):
        # 跳过隐藏文件和目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files[:] = [f for f in files if not f.startswith('.') and f != 'package_skill.py']
        
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, skill_path)
            
            # 获取文件信息
            stat = os.stat(file_path)
            file_info = {
                "path": relative_path,
                "size": stat.st_size,
                "type": "directory" if os.path.isdir(file_path) else "file"
            }
            metadata["files"].append(file_info)
    
    return metadata

def package_skill(skill_path: str, output_path: str = None) -> str:
    """打包技能"""
    skill_name = os.path.basename(skill_path)
    
    if output_path is None:
        output_path = f"{skill_name}.skill"
    
    # 验证技能
    is_valid, errors = validate_skill(skill_path)
    if not is_valid:
        print("❌ 技能验证失败:")
        for error in errors:
            print(f"  - {error}")
        return None
    
    print("✅ 技能验证通过")
    
    # 创建元数据
    metadata = create_skill_metadata(skill_path)
    print(f"📦 打包技能: {metadata.get('name', skill_name)}")
    
    # 创建ZIP文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加metadata.json
        metadata_json = json.dumps(metadata, indent=2, ensure_ascii=False)
        zipf.writestr("metadata.json", metadata_json)
        
        # 添加技能文件
        for root, dirs, files in os.walk(skill_path):
            # 跳过隐藏文件和目录
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files[:] = [f for f in files if not f.startswith('.') and f != 'package_skill.py']
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, skill_path)
                
                # 添加到ZIP
                zipf.write(file_path, relative_path)
                print(f"  + {relative_path}")
    
    print(f"✅ 技能已打包到: {output_path}")
    
    # 显示包信息
    package_size = os.path.getsize(output_path)
    print(f"📊 包大小: {package_size / 1024:.1f} KB")
    print(f"📄 文件数量: {len(metadata['files'])}")
    
    return output_path

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python package_skill.py <技能路径> [输出路径]")
        return
    
    skill_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(skill_path):
        print(f"❌ 技能路径不存在: {skill_path}")
        return
    
    if not os.path.isdir(skill_path):
        print(f"❌ 技能路径不是目录: {skill_path}")
        return
    
    result = package_skill(skill_path, output_path)
    if result:
        print("🎉 技能打包完成!")

if __name__ == "__main__":
    main()