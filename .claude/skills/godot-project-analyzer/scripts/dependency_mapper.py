#!/usr/bin/env python3
"""
Godot项目依赖关系映射脚本

该脚本用于分析Godot项目中脚本文件之间的依赖关系，构建依赖图和模块关系。
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any
from collections import defaultdict, deque
import ast


class GodotDependencyMapper:
    """Godot项目依赖关系映射器"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.scripts = {}
        self.dependencies = defaultdict(set)
        self.dependency_graph = {}
        self.circular_dependencies = []
    
    def find_script_files(self) -> List[Path]:
        """查找所有脚本文件"""
        script_files = []
        for pattern in ["**/*.gd", "**/*.cs", "**/*.vs"]:
            script_files.extend(self.project_path.glob(pattern))
        return sorted(script_files)
    
    def parse_gdscript_dependencies(self, script_file: Path) -> Dict:
        """解析GDScript文件的依赖关系"""
        try:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dependencies = {
                'file_path': str(script_file),
                'relative_path': str(script_file.relative_to(self.project_path)),
                'extends': None,
                'preloads': [],
                'class_name': None,
                'tool': False,
                'imports': [],
                'scenes': [],
                'resources': [],
                'constants': {},
                'functions': [],
                'signals': [],
                'exports': []
            }
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # 解析extends
                if line.startswith('extends '):
                    extends_match = re.match(r'extends\s+["\']?([^"\']+)["\']?', line)
                    if extends_match:
                        dependencies['extends'] = extends_match.group(1)
                
                # 解析class_name
                elif line.startswith('class_name '):
                    class_match = re.match(r'class_name\s+([A-Za-z_][A-Za-z0-9_]*)', line)
                    if class_match:
                        dependencies['class_name'] = class_match.group(1)
                
                # 解析tool
                elif line.startswith('tool'):
                    dependencies['tool'] = True
                
                # 解析preload
                elif 'preload(' in line:
                    preload_matches = re.findall(r'preload\(\s*["\']([^"\']+)["\']\s*\)', line)
                    dependencies['preloads'].extend(preload_matches)
                
                # 解析load
                elif 'load(' in line and 'res://' in line:
                    load_matches = re.findall(r'load\(\s*["\']([^"\']+)["\']\s*\)', line)
                    dependencies['imports'].extend(load_matches)
                
                # 解析场景实例化
                elif '.instantiate()' in line or '.instance()' in line:
                    # 尝试找到场景文件引用
                    scene_matches = re.findall(r'["\']([^"\']*\.tscn)["\']', line)
                    dependencies['scenes'].extend(scene_matches)
                
                # 解析资源加载
                elif 'ResourceLoader' in line or 'load(' in line:
                    resource_matches = re.findall(r'["\']([^"\']*\.(tres|res|json|xml))["\']', line)
                    dependencies['resources'].extend([match[0] for match in resource_matches])
                
                # 解析常量定义
                elif line.startswith('const '):
                    const_match = re.match(r'const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=', line)
                    if const_match:
                        dependencies['constants'][const_match.group(1)] = line_num
                
                # 解析函数定义
                elif line.startswith('func '):
                    func_match = re.match(r'func\s+([A-Za-z_][A-Za-z0-9_]*)', line)
                    if func_match:
                        dependencies['functions'].append({
                            'name': func_match.group(1),
                            'line': line_num
                        })
                
                # 解析信号定义
                elif 'signal ' in line:
                    signal_match = re.match(r'signal\s+([A-Za-z_][A-Za-z0-9_]*)', line)
                    if signal_match:
                        dependencies['signals'].append(signal_match.group(1))
                
                # 解析export变量
                elif line.startswith('export '):
                    export_match = re.match(r'export\s*(?:\([^)]*\))?\s*([A-Za-z_][A-Za-z0-9_]*)', line)
                    if export_match:
                        dependencies['exports'].append(export_match.group(1))
            
            return dependencies
            
        except Exception as e:
            print(f"解析脚本文件失败 {script_file}: {e}")
            return {}
    
    def parse_csharp_dependencies(self, script_file: Path) -> Dict:
        """解析C#脚本的依赖关系"""
        try:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dependencies = {
                'file_path': str(script_file),
                'relative_path': str(script_file.relative_to(self.project_path)),
                'extends': None,
                'preloads': [],
                'class_name': None,
                'tool': False,
                'imports': [],
                'scenes': [],
                'resources': [],
                'constants': {},
                'functions': [],
                'signals': [],
                'exports': [],
                'using_statements': []
            }
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                
                # 解析using语句
                if line.startswith('using '):
                    dependencies['using_statements'].append(line[6:].strip().rstrip(';'))
                
                # 解析类继承
                if 'class ' in line and ':' in line:
                    # 例如: public class Player : Node
                    class_match = re.search(r'class\s+(\w+).*?:\s*([^\s{]+)', line)
                    if class_match:
                        dependencies['class_name'] = class_match.group(1)
                        dependencies['extends'] = class_match.group(2)
                elif 'class ' in line:
                    class_match = re.search(r'class\s+(\w+)', line)
                    if class_match:
                        dependencies['class_name'] = class_match.group(1)
            
            return dependencies
            
        except Exception as e:
            print(f"解析C#脚本文件失败 {script_file}: {e}")
            return {}
    
    def analyze_all_scripts(self) -> Dict:
        """分析所有脚本文件"""
        script_files = self.find_script_files()
        
        print(f"🔍 找到 {len(script_files)} 个脚本文件")
        
        for script_file in script_files:
            print(f"📄 分析脚本: {script_file.name}")
            
            if script_file.suffix.lower() == '.gd':
                script_data = self.parse_gdscript_dependencies(script_file)
            elif script_file.suffix.lower() == '.cs':
                script_data = self.parse_csharp_dependencies(script_file)
            else:
                continue
            
            if script_data:
                self.scripts[str(script_file)] = script_data
        
        return self.scripts
    
    def build_dependency_graph(self) -> Dict:
        """构建依赖关系图"""
        for script_path, script_data in self.scripts.items():
            file_deps = set()
            
            # 处理extends依赖
            if script_data.get('extends'):
                extends_target = script_data['extends']
                if '.' not in extends_target:  # 排除内置类型
                    for other_path, other_data in self.scripts.items():
                        if other_data.get('class_name') == extends_target:
                            file_deps.add(other_path)
                            break
            
            # 处理preload依赖
            for preload_path in script_data.get('preloads', []):
                full_path = self.project_path / preload_path
                if full_path.exists() and str(full_path) != script_path:
                    file_deps.add(str(full_path))
            
            # 处理import依赖
            for import_path in script_data.get('imports', []):
                if import_path.startswith('res://'):
                    local_path = import_path[6:]  # 移除 'res://' 前缀
                    full_path = self.project_path / local_path
                    if full_path.exists() and str(full_path) != script_path:
                        file_deps.add(str(full_path))
            
            self.dependencies[script_path] = file_deps
        
        # 转换为依赖图
        self.dependency_graph = {
            script_path: list(deps) 
            for script_path, deps in self.dependencies.items()
        }
        
        return self.dependency_graph
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """检测循环依赖"""
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node, path):
            if node in rec_stack:
                # 找到循环，提取循环部分
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.dependencies.get(node, []):
                if neighbor in self.scripts:  # 只检查项目内的文件
                    dfs(neighbor, path.copy())
            
            rec_stack.remove(node)
        
        for script_path in self.scripts.keys():
            if script_path not in visited:
                dfs(script_path, [])
        
        self.circular_dependencies = cycles
        return cycles
    
    def get_module_analysis(self) -> Dict:
        """获取模块分析结果"""
        if not self.scripts:
            return {}
        
        analysis = {
            'total_scripts': len(self.scripts),
            'language_distribution': defaultdict(int),
            'class_count': 0,
            'function_count': 0,
            'signal_count': 0,
            'export_count': 0,
            'constants_count': 0,
            'dependencies_count': sum(len(deps) for deps in self.dependencies.values()),
            'circular_dependencies': len(self.circular_dependencies),
            'modules': []
        }
        
        for script_data in self.scripts.values():
            # 语言分布
            ext = Path(script_data['file_path']).suffix.lower()
            analysis['language_distribution'][ext] += 1
            
            # 统计信息
            if script_data.get('class_name'):
                analysis['class_count'] += 1
            analysis['function_count'] += len(script_data.get('functions', []))
            analysis['signal_count'] += len(script_data.get('signals', []))
            analysis['export_count'] += len(script_data.get('exports', []))
            analysis['constants_count'] += len(script_data.get('constants', {}))
            
            # 模块信息
            module_info = {
                'file': script_data['relative_path'],
                'class_name': script_data.get('class_name'),
                'extends': script_data.get('extends'),
                'functions': len(script_data.get('functions', [])),
                'signals': len(script_data.get('signals', [])),
                'exports': len(script_data.get('exports', [])),
                'dependencies': len(self.dependencies.get(script_data['file_path'], []))
            }
            analysis['modules'].append(module_info)
        
        return analysis
    
    def get_dependency_report(self) -> str:
        """生成依赖关系报告"""
        if not self.scripts:
            return "❌ 没有找到有效的脚本文件"
        
        report = []
        report.append("🔗 Godot依赖关系分析报告")
        report.append("=" * 50)
        
        # 模块分析
        module_analysis = self.get_module_analysis()
        
        report.append(f"📊 模块统计:")
        report.append(f"  • 脚本文件总数: {module_analysis['total_scripts']}")
        report.append(f"  • 类定义数量: {module_analysis['class_count']}")
        report.append(f"  • 函数定义数量: {module_analysis['function_count']}")
        report.append(f"  • 信号定义数量: {module_analysis['signal_count']}")
        report.append(f"  • 导出变量数量: {module_analysis['export_count']}")
        report.append(f"  • 常量定义数量: {module_analysis['constants_count']}")
        report.append(f"  • 依赖关系数量: {module_analysis['dependencies_count']}")
        report.append(f"  • 循环依赖数量: {module_analysis['circular_dependencies']}")
        
        # 语言分布
        if module_analysis['language_distribution']:
            report.append(f"\n💻 编程语言分布:")
            for lang, count in module_analysis['language_distribution'].items():
                report.append(f"  • {lang}: {count}")
        
        # 依赖最多的模块
        modules_by_deps = sorted(
            module_analysis['modules'], 
            key=lambda x: x['dependencies'], 
            reverse=True
        )[:5]
        
        if modules_by_deps:
            report.append(f"\n🔗 依赖最多的模块:")
            for module in modules_by_deps:
                if module['dependencies'] > 0:
                    report.append(f"  • {module['file']}: {module['dependencies']} 个依赖")
        
        # 循环依赖警告
        if self.circular_dependencies:
            report.append(f"\n⚠️  循环依赖警告:")
            for cycle in self.circular_dependencies[:3]:  # 只显示前3个
                cycle_str = " → ".join([Path(f).name for f in cycle])
                report.append(f"  • {cycle_str}")
        
        return "\n".join(report)


def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description='Godot依赖关系映射器')
    parser.add_argument('--project', '-p', default='.', help='项目路径 (默认: 当前目录)')
    parser.add_argument('--output', '-o', help='输出详细分析结果到JSON文件')
    parser.add_argument('--graphviz', '-g', help='输出依赖图的Graphviz DOT文件')
    args = parser.parse_args()
    
    mapper = GodotDependencyMapper(args.project)
    
    print("🔗 Godot依赖关系映射器")
    print("=" * 50)
    
    # 分析所有脚本
    mapper.analyze_all_scripts()
    
    # 构建依赖图
    mapper.build_dependency_graph()
    
    # 检测循环依赖
    mapper.detect_circular_dependencies()
    
    # 生成报告
    report = mapper.get_dependency_report()
    print(report)
    
    # 输出详细结果
    if args.output:
        detailed_results = {
            'module_analysis': mapper.get_module_analysis(),
            'dependency_graph': mapper.dependency_graph,
            'circular_dependencies': mapper.circular_dependencies,
            'scripts': mapper.scripts
        }
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(detailed_results, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n💾 详细分析结果已保存到: {args.output}")
    
    # 输出Graphviz格式
    if args.graphviz:
        mapper.generate_graphviz_file(args.graphviz)


if __name__ == "__main__":
    main()