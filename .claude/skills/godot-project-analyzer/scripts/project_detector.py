#!/usr/bin/env python3
"""
Godot项目检测脚本

该脚本用于检测当前目录是否为有效的Godot项目，并提供项目基本信息。
"""

import os
import json
import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GodotProjectDetector:
    """Godot项目检测器"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
        self.godot_files = {
            'project_file': None,
            'scene_files': [],
            'script_files': [],
            'resource_files': [],
            'config_files': []
        }
    
    def is_godot_project(self) -> bool:
        """检测是否为Godot项目"""
        # 查找.project文件
        project_files = list(self.base_path.glob("**/*.project"))
        
        if not project_files:
            return False
        
        # 验证项目文件内容
        for project_file in project_files:
            try:
                with open(project_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'application/config/name' in content or 'application/run/main_scene' in content:
                        self.godot_files['project_file'] = project_file
                        return True
            except Exception:
                continue
        
        return False
    
    def get_project_info(self) -> Dict:
        """获取项目基本信息"""
        if not self.godot_files['project_file']:
            return {}
        
        try:
            with open(self.godot_files['project_file'], 'r', encoding='utf-8') as f:
                # 简单的INI格式解析
                lines = f.readlines()
                info = {}
                
                for line in lines:
                    line = line.strip()
                    if '=' in line and not line.startswith(';'):
                        key, value = line.split('=', 1)
                        info[key.strip()] = value.strip().strip('"')
                
                return info
        except Exception as e:
            print(f"解析项目文件失败: {e}")
            return {}
    
    def scan_project_files(self) -> Dict[str, List[Path]]:
        """扫描项目中的所有Godot相关文件"""
        file_patterns = {
            'scene_files': ["**/*.tscn", "**/*.scn"],
            'script_files': ["**/*.gd", "**/*.cs", "**/*.vs"],
            'resource_files': ["**/*.tres", "**/*.res", "**/*.import"],
            'config_files': ["**/*.cfg", "**/*.json"]
        }
        
        for file_type, patterns in file_patterns.items():
            for pattern in patterns:
                files = list(self.base_path.glob(pattern))
                self.godot_files[file_type].extend(files)
            
            # 去重并排序
            self.godot_files[file_type] = sorted(list(set(self.godot_files[file_type])))
        
        return self.godot_files
    
    def analyze_project_structure(self) -> Dict:
        """分析项目结构"""
        if not self.is_godot_project():
            return {}
        
        files = self.scan_project_files()
        
        structure_analysis = {
            'project_root': str(self.base_path),
            'total_files': sum(len(file_list) for file_list in files.values() if isinstance(file_list, list)),
            'file_counts': {
                'scenes': len(files['scene_files']),
                'scripts': len(files['script_files']),
                'resources': len(files['resource_files']),
                'configs': len(files['config_files'])
            },
            'main_scene': None,
            'script_types': {},
            'directory_structure': self._get_directory_structure()
        }
        
        # 分析主场景
        project_info = self.get_project_info()
        if 'application/run/main_scene' in project_info:
            main_scene_path = self.base_path / project_info['application/run/main_scene']
            if main_scene_path.exists():
                structure_analysis['main_scene'] = str(main_scene_path)
        
        # 分析脚本类型
        for script_file in files['script_files']:
            ext = script_file.suffix
            structure_analysis['script_types'][ext] = structure_analysis['script_types'].get(ext, 0) + 1
        
        return structure_analysis
    
    def _get_directory_structure(self) -> Dict:
        """获取目录结构"""
        def build_tree(path: Path, max_depth: int = 3, current_depth: int = 0) -> Dict:
            if current_depth >= max_depth or not path.is_dir():
                return {'name': path.name, 'type': 'file' if path.is_file() else 'dir', 'children': []}
            
            tree = {'name': path.name, 'type': 'dir', 'children': []}
            
            try:
                for item in sorted(path.iterdir()):
                    if item.name.startswith('.') or item.name == '__pycache__':
                        continue
                    
                    if item.is_file() and item.suffix in ['.gd', '.tscn', '.tres', '.cs', '.vs']:
                        tree['children'].append({
                            'name': item.name,
                            'type': 'file',
                            'size': item.stat().st_size
                        })
                    elif item.is_dir() and current_depth < max_depth - 1:
                        tree['children'].append(build_tree(item, max_depth, current_depth + 1))
            except PermissionError:
                pass
            
            return tree
        
        return build_tree(self.base_path)
    
    def get_analysis_report(self) -> str:
        """生成分析报告"""
        if not self.is_godot_project():
            return "❌ 当前目录不是有效的Godot项目"
        
        structure = self.analyze_project_structure()
        project_info = self.get_project_info()
        
        report = []
        report.append("✅ Godot项目检测成功")
        report.append(f"📁 项目路径: {structure['project_root']}")
        
        if 'application/config/name' in project_info:
            report.append(f"📋 项目名称: {project_info['application/config/name']}")
        
        if structure['main_scene']:
            report.append(f"🎬 主场景: {structure['main_scene']}")
        
        report.append("\n📊 文件统计:")
        report.append(f"  • 场景文件: {structure['file_counts']['scenes']}")
        report.append(f"  • 脚本文件: {structure['file_counts']['scripts']}")
        report.append(f"  • 资源文件: {structure['file_counts']['resources']}")
        report.append(f"  • 配置文件: {structure['file_counts']['configs']}")
        report.append(f"  • 总计文件: {structure['total_files']}")
        
        if structure['script_types']:
            report.append("\n🔧 脚本类型分布:")
            for script_type, count in structure['script_types'].items():
                report.append(f"  • {script_type}: {count}")
        
        return "\n".join(report)


def main():
    """主函数"""
    detector = GodotProjectDetector()
    
    print("🔍 Godot项目检测器")
    print("=" * 50)
    
    # 检测项目
    if not detector.is_godot_project():
        print("❌ 当前目录不是有效的Godot项目")
        print("请确保:")
        print("  • 存在 .project 文件")
        print("  • 项目文件包含有效的Godot配置")
        return
    
    # 输出分析报告
    report = detector.get_analysis_report()
    print(report)
    
    # 可选：输出详细结构到JSON文件
    import argparse
    parser = argparse.ArgumentParser(description='Godot项目检测器')
    parser.add_argument('--output', '-o', help='输出详细分析结果到JSON文件')
    args = parser.parse_args()
    
    if args.output:
        structure = detector.analyze_project_structure()
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(structure, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n💾 详细分析结果已保存到: {args.output}")


if __name__ == "__main__":
    main()