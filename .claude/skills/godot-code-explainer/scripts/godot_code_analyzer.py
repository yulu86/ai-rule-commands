#!/usr/bin/env python3
"""
Godot Code Analyzer - 专门用于分析 Godot 游戏引擎代码的工具
支持 GDScript 和 C# 代码分析，识别 Godot 特定的概念和模式
"""

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import xml.etree.ElementTree as ET

class GodotCodeAnalyzer:
    """Godot 代码分析器"""
    
    def __init__(self, godot_project_path: Optional[str] = None):
        self.godot_project_path = Path(godot_project_path) if godot_project_path else None
        self.godot_version = self._detect_godot_version()
        self.project_info = {}
        
        # Godot 内置类型和函数
        self.godot_builtin_types = {
            'Node', 'Node2D', 'Node3D', 'Control', 'CharacterBody2D', 'CharacterBody3D',
            'RigidBody2D', 'RigidBody3D', 'Area2D', 'Area3D', 'Sprite2D', 'Sprite3D',
            'Camera2D', 'Camera3D', 'CanvasLayer', 'Label', 'Button', 'LineEdit',
            'TileMap', 'CollisionShape2D', 'CollisionShape3D', 'AnimationPlayer',
            'AudioStreamPlayer', 'AudioStreamPlayer2D', 'AudioStreamPlayer3D',
            'Timer', 'PathFollow2D', 'PathFollow3D'
        }
        
        self.godot_lifecycle_methods = {
            '_ready', '_process', '_physics_process', '_input', '_unhandled_input',
            '_gui_input', '_draw', '_enter_tree', '_exit_tree', '_notification',
            '_set', '_get', '_get_property_list', '_property_can_revert',
            '_property_get_revert'
        }
        
        self.godot_builtins = {
            'Vector2', 'Vector3', 'Color', 'Rect2', 'Transform2D', 'Transform3D',
            'Basis', 'Quaternion', 'Plane', 'AABB', 'RID', 'NodePath', 'StringName',
            'Dictionary', 'Array', 'PackedByteArray', 'PackedInt32Array',
            'PackedInt64Array', 'PackedFloat32Array', 'PackedFloat64Array',
            'PackedStringArray', 'PackedVector2Array', 'PackedVector3Array',
            'PackedColorArray'
        }
        
        self.godot_keywords = {
            'extends', 'class_name', 'signal', 'enum', 'const', 'var', 'static',
            'func', 'pass', 'break', 'continue', 'return', 'if', 'elif', 'else',
            'while', 'for', 'match', 'as', 'in', 'and', 'or', 'not', 'self',
            'super', 'preload', 'load', 'yield', 'await', 'assert', 'remote',
            'master', 'puppet', 'sync', 'remotesync', 'mastersync', 'puppetsync'
        }
    
    def _detect_godot_version(self) -> str:
        """检测 Godot 版本"""
        if not self.godot_project_path:
            return "unknown"
            
        project_file = self.godot_project_path / "project.godot"
        if project_file.exists():
            try:
                with open(project_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "config_version=4" in content or "config/features=PackedStringArray" in content:
                        return "4.x"
                    else:
                        return "3.x"
            except:
                pass
        return "unknown"
    
    def load_project_info(self) -> Dict[str, Any]:
        """加载 Godot 项目信息"""
        if not self.godot_project_path:
            return {}
            
        project_file = self.godot_project_path / "project.godot"
        if not project_file.exists():
            return {}
            
        try:
            with open(project_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 简单解析 Godot 项目文件
            project_info = {
                'name': 'Untitled',
                'version': self.godot_version,
                'scenes': [],
                'scripts': [],
                'resources': []
            }
            
            # 提取项目名称
            name_match = re.search(r'config/name="?([^"\n]+)"?', content)
            if name_match:
                project_info['name'] = name_match.group(1)
            
            # 扫描项目文件
            for root, dirs, files in os.walk(self.godot_project_path):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.godot_project_path)
                    
                    if file.endswith('.tscn'):
                        project_info['scenes'].append(str(rel_path))
                    elif file.endswith('.gd') or file.endswith('.cs'):
                        project_info['scripts'].append(str(rel_path))
                    elif file.endswith('.tres') or file.endswith('.res'):
                        project_info['resources'].append(str(rel_path))
            
            self.project_info = project_info
            return project_info
            
        except Exception as e:
            print(f"Error loading project info: {e}")
            return {}
    
    def analyze_gdscript_file(self, file_path: str) -> Dict[str, Any]:
        """分析 GDScript 文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f"Failed to read file: {e}"}
        
        analysis = {
            'file_type': 'gdscript',
            'file_path': file_path,
            'language': 'gdscript',
            'extends': None,
            'class_name': None,
            'signals': [],
            'variables': [],
            'functions': [],
            'constants': [],
            'enums': [],
            'godot_features': [],
            'performance_notes': [],
            'scene_connections': [],
            'imports': [],
            'exports': []
        }
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # 解析 extends
            if line.startswith('extends '):
                analysis['extends'] = line.split('extends ')[1].split('#')[0].strip()
            
            # 解析 class_name
            elif line.startswith('class_name '):
                parts = line.split('class_name ')[1].split('#')[0].strip()
                analysis['class_name'] = parts.split()[0] if parts else None
            
            # 解析 signal
            elif line.startswith('signal '):
                signal_def = line.split('signal ')[1].split('#')[0].strip()
                analysis['signals'].append(self._parse_signal(signal_def, i+1))
            
            # 解析变量
            elif any(line.startswith(x) for x in ['var ', 'const ', 'export ', 'onready ']):
                var_info = self._parse_variable(line, i+1)
                if var_info:
                    analysis['variables'].append(var_info)
                    if line.startswith('export '):
                        analysis['exports'].append(var_info)
            
            # 解析函数
            elif line.startswith('func '):
                func_info = self._parse_function(lines, i)
                if func_info:
                    analysis['functions'].append(func_info)
            
            # 解析 enum
            elif line.startswith('enum '):
                enum_info = self._parse_enum(lines, i)
                if enum_info:
                    analysis['enums'].append(enum_info)
            
            # 检查导入
            elif line.startswith('preload(') or line.startswith('load('):
                import_info = self._parse_import(line, i+1)
                if import_info:
                    analysis['imports'].append(import_info)
        
        # 分析 Godot 特性
        analysis['godot_features'] = self._analyze_godot_features(analysis)
        analysis['performance_notes'] = self._analyze_performance(analysis)
        
        return analysis
    
    def analyze_scene_file(self, scene_path: str) -> Dict[str, Any]:
        """分析场景文件"""
        try:
            with open(scene_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f"Failed to read scene file: {e}"}
        
        analysis = {
            'file_type': 'scene',
            'file_path': scene_path,
            'language': 'scene',
            'root_node': None,
            'node_tree': [],
            'attached_scripts': [],
            'external_resources': [],
            'node_connections': []
        }
        
        try:
            root = ET.fromstring(content.replace('<?xml version="1.0" encoding="UTF-8"?>', ''))
            
            # 解析节点树
            for node in root.iter('node'):
                node_info = self._parse_scene_node(node)
                analysis['node_tree'].append(node_info)
                
                if node.get('path') == '.':
                    analysis['root_node'] = node_info
                
                # 检查附加的脚本
                for child in node:
                    if child.tag == 'node' and child.get('name') == 'Script':
                        script_path = child.get('script')
                        if script_path and script_path not in analysis['attached_scripts']:
                            analysis['attached_scripts'].append(script_path)
            
        except Exception as e:
            analysis['error'] = f"Failed to parse scene XML: {e}"
        
        return analysis
    
    def _parse_signal(self, signal_def: str, line_number: int) -> Dict[str, Any]:
        """解析信号定义"""
        signal_info = {
            'name': signal_def.split('(')[0].strip(),
            'parameters': [],
            'line_number': line_number
        }
        
        if '(' in signal_def and ')' in signal_def:
            params_str = signal_def.split('(')[1].split(')')[0].strip()
            if params_str:
                for param in params_str.split(','):
                    param = param.strip()
                    if param:
                        parts = param.split(':')
                        signal_info['parameters'].append({
                            'name': parts[0].strip(),
                            'type': parts[1].strip() if len(parts) > 1 else 'Variant'
                        })
        
        return signal_info
    
    def _parse_variable(self, line: str, line_number: int) -> Optional[Dict[str, Any]]:
        """解析变量定义"""
        # 移除前缀关键词
        clean_line = re.sub(r'^(onready|export|const|static|var)\s+', '', line)
        
        if ':' not in clean_line and '=' not in clean_line:
            return None
            
        var_info = {
            'name': '',
            'type': None,
            'default_value': None,
            'is_exported': line.startswith('export '),
            'is_onready': line.startswith('onready '),
            'is_const': line.startswith('const '),
            'is_static': 'static' in line,
            'line_number': line_number
        }
        
        # 解析变量名
        name_part = clean_line.split(':')[0].split('=')[0].strip()
        var_info['name'] = name_part
        
        # 解析类型
        if ':' in clean_line:
            type_part = clean_line.split(':')[1].split('=')[0].strip()
            var_info['type'] = type_part
        
        # 解析默认值
        if '=' in clean_line:
            value_part = clean_line.split('=')[1].strip()
            var_info['default_value'] = value_part
        
        return var_info
    
    def _parse_function(self, lines: List[str], start_line: int) -> Optional[Dict[str, Any]]:
        """解析函数定义"""
        func_line = lines[start_line].strip()
        if not func_line.startswith('func '):
            return None
        
        # 提取函数签名
        signature = func_line[5:]  # 移除 'func '
        func_name = signature.split('(')[0].strip()
        
        func_info = {
            'name': func_name,
            'parameters': [],
            'return_type': 'void',
            'is_static': 'static' in func_line,
            'is_private': func_name.startswith('_'),
            'line_number': start_line + 1,
            'body_lines': []
        }
        
        # 解析参数
        if '(' in signature:
            params_str = signature.split('(')[1].split(')')[0].strip()
            if params_str:
                for param in params_str.split(','):
                    param = param.strip()
                    if param:
                        parts = param.split(':')
                        func_info['parameters'].append({
                            'name': parts[0].strip(),
                            'type': parts[1].strip() if len(parts) > 1 else 'Variant'
                        })
        
        # 解析返回类型
        if '->' in signature:
            return_part = signature.split('->')[1].strip()
            func_info['return_type'] = return_part.split(':')[0].strip() if ':' in return_part else return_part
        
        # 收集函数体
        indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            if line.strip() == '':
                continue
                
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent_level and line.strip():
                break
                
            func_info['body_lines'].append(line.rstrip())
        
        return func_info
    
    def _parse_enum(self, lines: List[str], start_line: int) -> Optional[Dict[str, Any]]:
        """解析枚举定义"""
        enum_line = lines[start_line].strip()
        if not enum_line.startswith('enum '):
            return None
        
        enum_info = {
            'name': '',
            'values': [],
            'line_number': start_line + 1
        }
        
        # 提取枚举名
        name_part = enum_line[5:].split('{')[0].strip()
        enum_info['name'] = name_part if name_part else 'unnamed'
        
        # 解析枚举值
        if '{' in enum_line:
            values_str = enum_line.split('{')[1]
            if '}' not in values_str:
                # 多行枚举，需要收集后续行
                indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
                for i in range(start_line + 1, len(lines)):
                    line = lines[i].strip()
                    if line == '}' or not line:
                        break
                    values_str += ' ' + line
            
            # 清理并分割值
            values_str = values_str.split('}')[0].strip()
            for value in values_str.split(','):
                value = value.strip()
                if value:
                    if '=' in value:
                        name, val = value.split('=', 1)
                        enum_info['values'].append({'name': name.strip(), 'value': val.strip()})
                    else:
                        enum_info['values'].append({'name': value, 'value': None})
        
        return enum_info
    
    def _parse_import(self, line: str, line_number: int) -> Dict[str, Any]:
        """解析导入语句"""
        import_info = {
            'type': 'preload' if line.startswith('preload(') else 'load',
            'path': '',
            'line_number': line_number
        }
        
        if 'preload(' in line:
            path_match = re.search(r'preload\("([^"]+)"\)', line)
        else:
            path_match = re.search(r'load\("([^"]+)"\)', line)
        
        if path_match:
            import_info['path'] = path_match.group(1)
        
        return import_info
    
    def _parse_scene_node(self, node_element) -> Dict[str, Any]:
        """解析场景节点"""
        node_info = {
            'name': node_element.get('name', ''),
            'type': node_element.get('type', 'Node'),
            'path': node_element.get('path', ''),
            'parent': node_element.get('parent', ''),
            'properties': {},
            'children': []
        }
        
        # 解析节点属性
        for prop in node_element.findall('property'):
            prop_name = prop.get('name', '')
            prop_value = self._extract_property_value(prop)
            if prop_name:
                node_info['properties'][prop_name] = prop_value
        
        return node_info
    
    def _extract_property_value(self, prop_element) -> Any:
        """从XML元素提取属性值"""
        # 简化实现，实际需要处理各种类型
        return prop_element.text or ''
    
    def _analyze_godot_features(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分析 Godot 特定特性"""
        features = []
        
        # 检查生命周期方法
        lifecycle_methods = []
        for func in analysis['functions']:
            if func['name'] in self.godot_lifecycle_methods:
                lifecycle_methods.append(func['name'])
        
        if lifecycle_methods:
            features.append({
                'type': 'lifecycle',
                'methods': lifecycle_methods,
                'description': '使用了 Godot 节点生命周期方法'
            })
        
        # 检查继承类型
        if analysis['extends'] and analysis['extends'] in self.godot_builtin_types:
            features.append({
                'type': 'node_inheritance',
                'extends': analysis['extends'],
                'description': f'继承自 Godot 内置节点类型: {analysis["extends"]}'
            })
        
        # 检查信号使用
        if analysis['signals']:
            features.append({
                'type': 'signals',
                'count': len(analysis['signals']),
                'signals': [s['name'] for s in analysis['signals']],
                'description': f'定义了 {len(analysis["signals"])} 个自定义信号'
            })
        
        # 检查导出变量
        if analysis['exports']:
            features.append({
                'type': 'exported_variables',
                'count': len(analysis['exports']),
                'variables': [v['name'] for v in analysis['exports']],
                'description': f'定义了 {len(analysis["exports"])} 个可在编辑器中配置的变量'
            })
        
        # 检查 onready 变量
        onready_vars = [v for v in analysis['variables'] if v.get('is_onready')]
        if onready_vars:
            features.append({
                'type': 'onready_variables',
                'count': len(onready_vars),
                'variables': [v['name'] for v in onready_vars],
                'description': f'使用了 {len(onready_vars)} 个 onready 变量进行延迟初始化'
            })
        
        return features
    
    def _analyze_performance(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分析性能相关问题"""
        notes = []
        
        # 检查 _process 方法中的潜在性能问题
        for func in analysis['functions']:
            if func['name'] == '_process':
                body_text = '\n'.join(func['body_lines'])
                
                # 检查在 _process 中创建新对象
                if any(keyword in body_text for keyword in ['Vector2(', 'Vector3(', 'Color(', 'Dictionary()']):
                    notes.append({
                        'severity': 'warning',
                        'type': 'object_creation_in_process',
                        'function': func['name'],
                        'line': func['line_number'],
                        'description': '在 _process() 中创建新对象可能影响性能，考虑预分配对象'
                    })
                
                # 检查在 _process 中使用 load()
                if 'load(' in body_text:
                    notes.append({
                        'severity': 'warning',
                        'type': 'resource_loading_in_process',
                        'function': func['name'],
                        'line': func['line_number'],
                        'description': '在 _process() 中加载资源可能导致卡顿，建议使用 preload'
                    })
        
        # 检查可能的重计算
        for func in analysis['functions']:
            body_text = '\n'.join(func['body_lines'])
            if 'get_node(' in body_text:
                notes.append({
                    'severity': 'info',
                    'type': 'repeated_node_lookup',
                    'function': func['name'],
                    'line': func['line_number'],
                    'description': '重复使用 get_node() 可能影响性能，考虑缓存节点引用'
                })
        
        return notes

def main():
    parser = argparse.ArgumentParser(description='Godot Code Analyzer')
    parser.add_argument('--file', required=True, help='要分析的文件路径')
    parser.add_argument('--godot-project', help='Godot 项目根目录路径')
    parser.add_argument('--performance-analysis', action='store_true', help='启用性能分析')
    parser.add_argument('--scene', help='分析场景文件')
    parser.add_argument('--analyze-attached-scripts', action='store_true', help='分析场景中附加的脚本')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='输出格式')
    
    args = parser.parse_args()
    
    analyzer = GodotCodeAnalyzer(args.godot_project)
    
    if args.godot_project:
        analyzer.load_project_info()
        print(f"分析 Godot 项目: {analyzer.project_info.get('name', 'Unknown')}")
        print(f"Godot 版本: {analyzer.godot_version}")
        print()
    
    if args.scene:
        # 分析场景文件
        analysis = analyzer.analyze_scene_file(args.scene)
        
        if args.analyze_attached_scripts and analysis.get('attached_scripts'):
            for script in analysis['attached_scripts']:
                script_path = Path(args.scene).parent / script
                if script_path.exists():
                    script_analysis = analyzer.analyze_gdscript_file(str(script_path))
                    if 'error' not in script_analysis:
                        analysis[f'script_analysis_{script}'] = script_analysis
    else:
        # 分析代码文件
        if args.file.endswith('.gd'):
            analysis = analyzer.analyze_gdscript_file(args.file)
        elif args.file.endswith('.tscn'):
            analysis = analyzer.analyze_scene_file(args.file)
        else:
            print(f"不支持的文件类型: {args.file}")
            return
    
    if 'error' in analysis:
        print(f"错误: {analysis['error']}")
        sys.exit(1)
    
    # 输出结果
    if args.format == 'json':
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    else:
        print(f"\n=== {analysis['file_path']} 分析结果 ===\n")
        
        if analysis.get('extends'):
            print(f"继承类型: {analysis['extends']}")
        
        if analysis.get('class_name'):
            print(f"类名: {analysis['class_name']}")
        
        if analysis.get('functions'):
            print(f"\n函数 ({len(analysis['functions'])}):")
            for func in analysis['functions']:
                params = ', '.join([f"{p['name']}: {p['type']}" for p in func['parameters']])
                print(f"  • {func['name']}({params}) -> {func['return_type']} [行 {func['line_number']}]")
        
        if analysis.get('variables'):
            print(f"\n变量 ({len(analysis['variables'])}):")
            for var in analysis['variables']:
                type_info = f": {var['type']}" if var['type'] else ""
                value_info = f" = {var['default_value']}" if var['default_value'] else ""
                export_info = " [export]" if var.get('is_exported') else ""
                print(f"  • {var['name']}{type_info}{value_info}{export_info} [行 {var['line_number']}]")
        
        if analysis.get('signals'):
            print(f"\n信号 ({len(analysis['signals'])}):")
            for signal in analysis['signals']:
                params = ', '.join([f"{p['name']}: {p['type']}" for p in signal['parameters']]) if signal['parameters'] else ''
                print(f"  • {signal['name']}({params}) [行 {signal['line_number']}]")
        
        if analysis.get('godot_features'):
            print(f"\nGodot 特性:")
            for feature in analysis['godot_features']:
                print(f"  • {feature['description']}")
        
        if analysis.get('performance_notes'):
            print(f"\n性能提示:")
            for note in analysis['performance_notes']:
                severity = "⚠️ " if note['severity'] == 'warning' else "ℹ️ "
                print(f"  {severity}{note['description']} (行 {note['line']})")

if __name__ == '__main__':
    main()