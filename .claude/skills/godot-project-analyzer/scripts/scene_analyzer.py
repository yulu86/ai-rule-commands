#!/usr/bin/env python3
"""
Godot场景分析脚本

该脚本用于分析Godot场景文件的结构，提取节点层次、脚本绑定和组件关系。
"""

import os
import xml.etree.ElementTree as ET
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import re


class GodotSceneAnalyzer:
    """Godot场景文件分析器"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.scenes = []
        self.analysis_results = {}
    
    def find_scene_files(self) -> List[Path]:
        """查找所有场景文件"""
        scene_files = []
        for pattern in ["**/*.tscn", "**/*.scn"]:
            scene_files.extend(self.project_path.glob(pattern))
        return sorted(scene_files)
    
    def parse_scene_file(self, scene_file: Path) -> Dict:
        """解析单个场景文件"""
        try:
            with open(scene_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Godot场景文件使用类似INI的格式，不是标准XML
            # 使用正则表达式解析
            scene_data = {
                'file_path': str(scene_file),
                'relative_path': str(scene_file.relative_to(self.project_path)),
                'nodes': [],
                'connections': [],
                'resources': [],
                'external_resources': []
            }
            
            # 解析节点定义
            node_pattern = r'\[node name="([^"]+)" type="([^"]+)"(?: parent="([^"]+)")?(?: instance=ExtResource\(\s*(\d+)\s*\))?]'
            
            for match in re.finditer(node_pattern, content):
                node_name = match.group(1)
                node_type = match.group(2)
                parent_path = match.group(3) if match.group(3) else None
                instance_id = match.group(4) if match.group(4) else None
                
                node_info = {
                    'name': node_name,
                    'type': node_type,
                    'parent': parent_path,
                    'instance_id': instance_id,
                    'script': None,
                    'properties': {},
                    'groups': []
                }
                
                # 提取节点属性和脚本信息
                node_section_start = content.find(match.group(0))
                if node_section_start != -1:
                    node_section = self._extract_node_section(content, node_section_start)
                    node_info.update(self._parse_node_properties(node_section))
                
                scene_data['nodes'].append(node_info)
            
            # 解析外部资源引用
            ext_resource_pattern = r'\[ext_resource path="([^"]+)" type="([^"]+)" id=(\d+)\]'
            for match in re.finditer(ext_resource_pattern, content):
                scene_data['external_resources'].append({
                    'path': match.group(1),
                    'type': match.group(2),
                    'id': match.group(3)
                })
            
            # 解析信号连接
            connection_pattern = r'\[connection signal="([^"]+)" from="([^"]+)" to="([^"]+)"(?: method="([^"]+)")?(?: flags=(\d+))?]'
            for match in re.finditer(connection_pattern, content):
                scene_data['connections'].append({
                    'signal': match.group(1),
                    'from': match.group(2),
                    'to': match.group(3),
                    'method': match.group(4) if match.group(4) else match.group(1),
                    'flags': match.group(5) if match.group(5) else None
                })
            
            return scene_data
            
        except Exception as e:
            print(f"解析场景文件失败 {scene_file}: {e}")
            return {}
    
    def _extract_node_section(self, content: str, start_pos: int) -> str:
        """提取节点定义的完整部分"""
        lines = content[start_pos:].split('\n')
        node_lines = []
        indent_level = None
        
        for line in lines:
            if not line.strip():
                node_lines.append(line)
                continue
            
            current_indent = len(line) - len(line.lstrip())
            
            if indent_level is None:
                indent_level = current_indent
            elif current_indent <= indent_level and line.strip().startswith('['):
                # 遇到下一个节定义，停止
                break
            
            node_lines.append(line)
        
        return '\n'.join(node_lines)
    
    def _parse_node_properties(self, node_section: str) -> Dict:
        """解析节点属性"""
        properties = {}
        script = None
        groups = []
        
        lines = node_section.split('\n')
        for line in lines:
            line = line.strip()
            
            # 解析脚本
            if line.startswith('script = ExtResource('):
                script_id = re.search(r'ExtResource\(\s*(\d+)\s*\)', line)
                if script_id:
                    script = script_id.group(1)
            
            # 解析属性
            elif '=' in line and not line.startswith('['):
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # 清理值中的引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    
                    properties[key] = value
                except:
                    continue
            
            # 解析组
            elif line.startswith('groups = ['):
                groups_match = re.search(r'groups = \[(.*?)\]', line)
                if groups_match:
                    groups_str = groups_match.group(1)
                    groups = [g.strip().strip('"') for g in groups_str.split(',') if g.strip()]
        
        return {
            'script': script,
            'properties': properties,
            'groups': groups
        }
    
    def analyze_all_scenes(self) -> Dict:
        """分析所有场景文件"""
        scene_files = self.find_scene_files()
        
        print(f"🔍 找到 {len(scene_files)} 个场景文件")
        
        for scene_file in scene_files:
            print(f"📄 分析场景: {scene_file.name}")
            scene_data = self.parse_scene_file(scene_file)
            if scene_data:
                self.analysis_results[str(scene_file)] = scene_data
        
        return self.analysis_results
    
    def get_scene_hierarchy(self, scene_data: Dict) -> Dict:
        """构建场景层次结构"""
        nodes = scene_data.get('nodes', [])
        
        # 创建节点映射
        node_map = {node['name']: node.copy() for node in nodes}
        root_nodes = []
        
        # 构建层次结构
        for node in nodes:
            node_name = node['name']
            parent_path = node.get('parent')
            
            if parent_path:
                parent_node = node_map.get(parent_path)
                if parent_node:
                    if 'children' not in parent_node:
                        parent_node['children'] = []
                    parent_node['children'].append(node_map[node_name])
            else:
                root_nodes.append(node_map[node_name])
        
        return {
            'scene_file': scene_data.get('file_path'),
            'root_nodes': root_nodes,
            'total_nodes': len(nodes)
        }
    
    def analyze_script_bindings(self) -> Dict[str, List[Dict]]:
        """分析脚本绑定关系"""
        script_bindings = {}
        
        for scene_path, scene_data in self.analysis_results.items():
            scene_scripts = []
            
            for node in scene_data.get('nodes', []):
                if node.get('script'):
                    scene_scripts.append({
                        'node_name': node['name'],
                        'node_type': node['type'],
                        'script_id': node['script'],
                        'script_path': self._get_script_path_by_id(
                            scene_data, 
                            node['script']
                        )
                    })
            
            if scene_scripts:
                script_bindings[scene_path] = scene_scripts
        
        return script_bindings
    
    def _get_script_path_by_id(self, scene_data: Dict, script_id: str) -> Optional[str]:
        """根据资源ID获取脚本路径"""
        for resource in scene_data.get('external_resources', []):
            if resource['id'] == script_id and resource['type'] == 'Script':
                return resource['path']
        return None
    
    def analyze_signal_connections(self) -> Dict[str, List[Dict]]:
        """分析信号连接关系"""
        signal_analysis = {}
        
        for scene_path, scene_data in self.analysis_results.items():
            connections = scene_data.get('connections', [])
            
            if connections:
                signal_analysis[scene_path] = connections
        
        return signal_analysis
    
    def generate_analysis_report(self) -> str:
        """生成分析报告"""
        if not self.analysis_results:
            return "❌ 没有找到有效的场景文件"
        
        report = []
        report.append("🎬 Godot场景分析报告")
        report.append("=" * 50)
        
        total_scenes = len(self.analysis_results)
        total_nodes = sum(len(scene.get('nodes', [])) for scene in self.analysis_results.values())
        total_connections = sum(len(scene.get('connections', [])) for scene in self.analysis_results.values())
        
        report.append(f"📊 统计信息:")
        report.append(f"  • 场景文件数量: {total_scenes}")
        report.append(f"  • 节点总数: {total_nodes}")
        report.append(f"  • 信号连接数: {total_connections}")
        
        # 脚本绑定分析
        script_bindings = self.analyze_script_bindings()
        script_count = sum(len(scripts) for scripts in script_bindings.values())
        report.append(f"  • 脚本绑定数: {script_count}")
        
        report.append("\n📋 场景详情:")
        for scene_path, scene_data in self.analysis_results.items():
            scene_name = Path(scene_path).stem
            node_count = len(scene_data.get('nodes', []))
            connection_count = len(scene_data.get('connections', []))
            
            report.append(f"  🎬 {scene_name}")
            report.append(f"    • 节点数: {node_count}")
            report.append(f"    • 信号连接: {connection_count}")
            
            # 主要节点类型
            node_types = {}
            for node in scene_data.get('nodes', []):
                node_type = node['type']
                node_types[node_type] = node_types.get(node_type, 0) + 1
            
            if node_types:
                main_types = sorted(node_types.items(), key=lambda x: x[1], reverse=True)[:3]
                types_str = ", ".join([f"{t}({c})" for t, c in main_types])
                report.append(f"    • 主要节点类型: {types_str}")
        
        return "\n".join(report)


def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description='Godot场景分析器')
    parser.add_argument('--project', '-p', default='.', help='项目路径 (默认: 当前目录)')
    parser.add_argument('--output', '-o', help='输出详细分析结果到JSON文件')
    args = parser.parse_args()
    
    analyzer = GodotSceneAnalyzer(args.project)
    
    print("🔍 Godot场景分析器")
    print("=" * 50)
    
    # 分析所有场景
    analyzer.analyze_all_scenes()
    
    # 生成报告
    report = analyzer.generate_analysis_report()
    print(report)
    
    # 输出详细结果
    if args.output:
        detailed_results = {
            'summary': {
                'total_scenes': len(analyzer.analysis_results),
                'total_nodes': sum(len(scene.get('nodes', [])) for scene in analyzer.analysis_results.values()),
                'total_connections': sum(len(scene.get('connections', [])) for scene in analyzer.analysis_results.values())
            },
            'script_bindings': analyzer.analyze_script_bindings(),
            'signal_connections': analyzer.analyze_signal_connections(),
            'scenes': analyzer.analysis_results
        }
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(detailed_results, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n💾 详细分析结果已保存到: {args.output}")


if __name__ == "__main__":
    main()