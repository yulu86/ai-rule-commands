#!/usr/bin/env python3
"""
手动技能打包脚本
"""

import os
import zipfile
from pathlib import Path

def package_skill(skill_path: Path, output_dir: Path = None):
    if output_dir is None:
        output_dir = skill_path.parent
    
    skill_name = skill_path.name
    output_file = output_dir / f"{skill_name}.skill"
    
    # 创建zip文件
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历技能目录中的所有文件
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # 计算相对路径
                arcname = file_path.relative_to(skill_path)
                zipf.write(file_path, arcname)
                print(f"Added: {arcname}")
    
    print(f"\n✅ 技能已打包到: {output_file}")
    return output_file

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        skill_path = Path(sys.argv[1])
    else:
        skill_path = Path(".")
    
    output_dir = Path(".") if len(sys.argv) <= 2 else Path(sys.argv[2])
    
    package_skill(skill_path, output_dir)