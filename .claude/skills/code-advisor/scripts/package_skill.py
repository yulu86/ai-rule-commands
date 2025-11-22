#!/usr/bin/env python3
"""
技能打包脚本 - 将技能打包为.skill文件
"""

import os
import zipfile
import json
from pathlib import Path

def create_skill_package(skill_dir: str, output_dir: str = ".") -> None:
    """创建技能包"""

    skill_path = Path(skill_dir)
    skill_name = skill_path.name
    output_path = Path(output_dir) / f"{skill_name}.skill"

    # 验证必需文件
    required_files = ['SKILL.md']
    for file_name in required_files:
        file_path = skill_path / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"缺少必需文件: {file_name}")

    # 读取SKILL.md验证格式
    skill_md_path = skill_path / 'SKILL.md'
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 验证YAML前置内容
    if not content.startswith('---'):
        raise ValueError("SKILL.md必须以YAML前置内容开头")

    # 创建zip文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加所有文件到zip
        for file_path in skill_path.rglob('*'):
            if file_path.is_file() and file_path.name != 'package_skill.py':
                arcname = file_path.relative_to(skill_path)
                zipf.write(file_path, arcname)

    print(f"技能包已创建: {output_path}")
    print(f"包大小: {output_path.stat().st_size} bytes")

if __name__ == "__main__":
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    skill_dir = current_dir.parent

    try:
        create_skill_package(skill_dir)
        print("✅ 技能打包成功！")
    except Exception as e:
        print(f"❌ 打包失败: {e}")