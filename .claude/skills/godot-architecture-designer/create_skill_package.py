#!/usr/bin/env python3
"""
简单的技能打包工具
"""

import os
import zipfile
import json
from pathlib import Path

def create_skill_package():
    """创建技能包"""
    skill_path = "."
    output_file = "godot-architecture-designer.skill"
    
    # 验证SKILL.md存在
    if not os.path.exists("SKILL.md"):
        print("[ERROR] SKILL.md not found")
        return False
    
    print("[INFO] Creating skill package...")
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历所有文件
        for root, dirs, files in os.walk(skill_path):
            # 跳过隐藏文件和脚本文件
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files[:] = [f for f in files if not f.startswith('.') and f not in ['create_skill_package.py', 'package_skill.py']]
            
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, skill_path)
                
                zipf.write(file_path, arc_name)
                print(f"[ADD] {arc_name}")
    
    # 显示包信息
    size = os.path.getsize(output_file) / 1024
    print(f"[OK] Package created: {output_file}")
    print(f"[INFO] Package size: {size:.1f} KB")
    
    return True

if __name__ == "__main__":
    create_skill_package()