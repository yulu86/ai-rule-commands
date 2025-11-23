#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Godot项目脚手架生成器
创建新的Godot项目，拷贝模板文件并配置项目设置
"""

import os
import sys
import shutil
import json
from pathlib import Path

def copy_template_files(src_templates: Path, dest_dir: Path):
    """拷贝模板文件到目标目录"""
    print(f"拷贝模板文件到 {dest_dir}")
    
    # 如果目标目录不存在，创建它
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # 拷贝所有文件和目录
    for item in src_templates.iterdir():
        src_path = src_templates / item.name
        dest_path = dest_dir / item.name
        
        if src_path.is_dir():
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dest_path)
    
    print("模板文件拷贝完成")

def update_project_config(project_dir: Path, project_name: str, godot_version: str, renderer: str):
    """更新project.godot配置文件"""
    project_file = project_dir / "project.godot"
    
    if not project_file.exists():
        raise FileNotFoundError(f"project.godot文件不存在: {project_file}")
    
    # 读取原文件内容
    with open(project_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换项目名称
    content = content.replace('config/name="hello-world"', f'config/name="{project_name}"')
    
    # 更新版本信息
    features_line = f'config/features=PackedStringArray("{godot_version}", "GL Compatibility")'
    content = content.replace(
        'config/features=PackedStringArray("4.5", "GL Compatibility")',
        features_line
    )
    
    # 更新渲染器配置
    renderer_config = f'renderer/rendering_method="{renderer}"'
    renderer_mobile_config = f'renderer/rendering_method.mobile="{renderer}"'
    
    content = content.replace(
        'renderer/rendering_method="gl_compatibility"',
        renderer_config
    )
    content = content.replace(
        'renderer/rendering_method.mobile="gl_compatibility"',
        renderer_mobile_config
    )
    
    # 写回文件
    with open(project_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"项目配置已更新: {project_name}, Godot {godot_version}, 渲染器: {renderer}")

def update_readme(project_dir: Path, project_name: str):
    """更新README.md文件"""
    readme_file = project_dir / "README.md"
    
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换标题
    content = content.replace('# hello-world', f'# {project_name}')
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"README.md已更新: {project_name}")

def validate_godot_version(version: str) -> bool:
    """验证Godot版本号格式"""
    try:
        major, minor = version.split('.')
        major = int(major)
        minor = int(minor)
        
        # 最低版本要求：4.5
        if major < 4 or (major == 4 and minor < 5):
            print(f"警告：Godot {version} 可能不兼容，建议使用4.5或更高版本")
            return False
        
        return True
    except ValueError:
        print(f"错误：无效的版本号格式 '{version}'，请使用类似 '4.5' 的格式")
        return False

def validate_renderer(renderer: str) -> bool:
    """验证渲染器类型"""
    valid_renderers = ["forward_plus", "mobile", "gl_compatibility"]
    renderer_map = {
        "forward+": "forward_plus",
        "移动": "mobile",
        "兼容": "gl_compatibility"
    }
    
    # 处理中文映射
    if renderer in renderer_map:
        renderer = renderer_map[renderer]
    
    if renderer in valid_renderers:
        return renderer
    else:
        print(f"错误：无效的渲染器类型 '{renderer}'")
        print(f"可用选项: Forward+ (forward_plus), 移动 (mobile), 兼容 (gl_compatibility)")
        return None

def create_godot_project(project_name: str, godot_version: str, renderer: str, output_dir: str = "."):
    """创建Godot项目"""
    
    # 获取模板目录路径
    script_dir = Path(__file__).parent.parent
    templates_dir = script_dir / "templates"
    
    if not templates_dir.exists():
        raise FileNotFoundError(f"模板目录不存在: {templates_dir}")
    
    # 创建项目目录
    project_dir = Path(output_dir) / project_name
    print(f"创建项目目录: {project_dir}")
    
    # 拷贝模板文件
    copy_template_files(templates_dir, project_dir)
    
    # 验证并标准化渲染器名称
    validated_renderer = validate_renderer(renderer)
    if not validated_renderer:
        return False
    renderer = validated_renderer
    
    # 更新配置文件
    update_project_config(project_dir, project_name, godot_version, renderer)
    update_readme(project_dir, project_name)
    
    print(f"\n[成功] Godot项目 '{project_name}' 创建成功！")
    print(f"项目路径: {project_dir.absolute()}")
    print(f"Godot版本: {godot_version}")
    print(f"渲染器: {renderer}")
    print("\n使用以下命令启动项目:")
    print(f"cd {project_dir.absolute()}")
    print("godot --editor")
    
    return True

def main():
    """主函数"""
    if len(sys.argv) < 4:
        print("用法: python create_godot_project.py <项目名称> <Godot版本> <渲染器类型> [输出目录]")
        print("\n示例:")
        print("  python create_godot_project.py 我的新游戏 4.5 forward+ .")
        print("  python create_godot_project.py 平台跳跃 4.6 mobile ./games")
        print("\n渲染器类型:")
        print("  forward+ 或 Forward+ - 高质量渲染")
        print("  mobile 或 移动 - 移动设备优化")
        print("  gl_compatibility 或 兼容 - 兼容性渲染")
        return 1
    
    project_name = sys.argv[1]
    godot_version = sys.argv[2]
    renderer = sys.argv[3]
    output_dir = sys.argv[4] if len(sys.argv) > 4 else "."
    
    # 验证版本号
    if not validate_godot_version(godot_version):
        return 1
    
    # 创建项目
    if create_godot_project(project_name, godot_version, renderer, output_dir):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())