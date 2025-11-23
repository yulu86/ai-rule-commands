#!/usr/bin/env python3
"""
Godot代码检查脚本
用于自动检视GDScript和Godot项目中的常见问题
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class GodotLinter:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.issues: List[Dict] = []
        
    def scan_project(self) -> List[Dict]:
        """扫描整个Godot项目"""
        print(f"Scanning Godot project at: {self.project_path}")
        
        # 扫描所有GDScript文件
        for gd_file in self.project_path.rglob("*.gd"):
            self.check_file(gd_file)
            
        # 扫描场景文件
        for tscn_file in self.project_path.rglob("*.tscn"):
            self.check_scene_file(tscn_file)
            
        return self.issues
    
    def check_file(self, file_path: Path):
        """检查单个GDScript文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            filename = str(file_path.relative_to(self.project_path))
            
            # 执行各种检查
            self.check_node_caching(filename, lines)
            self.check_signal_connections(filename, lines)
            self.check_performance_issues(filename, lines)
            self.check_memory_management(filename, lines)
            self.check_error_handling(filename, lines)
            
        except Exception as e:
            print(f"Error checking file {file_path}: {e}")
    
    def check_node_caching(self, filename: str, lines: List[str]):
        """检查节点缓存问题"""
        get_node_pattern = re.compile(r'get_node\s*\(')
        
        for i, line in enumerate(lines, 1):
            # 检查在_process中重复调用get_node
            if get_node_pattern.search(line) and '_process' in line:
                self.add_issue(
                    filename, i, line.strip(),
                    "PERFORMANCE", 
                    "在_process中调用get_node可能影响性能，建议使用@onready缓存节点引用"
                )
    
    def check_signal_connections(self, filename: str, lines: List[str]):
        """检查信号连接问题"""
        connect_pattern = re.compile(r'\.connect\s*\(')
        disconnect_pattern = re.compile(r'\.disconnect\s*\(')
        
        has_connect = False
        has_disconnect = False
        
        for i, line in enumerate(lines, 1):
            if connect_pattern.search(line):
                has_connect = True
            
            if disconnect_pattern.search(line):
                has_disconnect = True
        
        if has_connect and not has_disconnect:
            self.add_issue(
                filename, 0, "",
                "BEST_PRACTICE",
                "发现信号连接但没有找到断开连接的代码，建议在适当时候断开信号以避免内存泄漏"
            )
    
    def check_performance_issues(self, filename: str, lines: List[str]):
        """检查性能问题"""
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # 检查在_process中的重复计算
            if '_process' in line and any(keyword in line for keyword in ['calculate', 'compute', 'expensive']):
                self.add_issue(
                    filename, i, line,
                    "PERFORMANCE",
                    "在_process中发现可能的重复计算，建议缓存计算结果"
                )
            
            # 检查物理处理在_process中
            if '_process' in line and any(keyword in line for keyword in ['move_and_slide', 'velocity', 'gravity']):
                self.add_issue(
                    filename, i, line,
                    "PHYSICS",
                    "物理相关代码应该放在_physics_process中而不是_process中"
                )
    
    def check_memory_management(self, filename: str, lines: List[str]):
        """检查内存管理问题"""
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # 检查资源加载
            if 'load(' in line and '_process' not in line and 'preload(' not in line:
                self.add_issue(
                    filename, i, line,
                    "MEMORY",
                    "发现动态资源加载，考虑实现资源缓存机制"
                )
    
    def check_error_handling(self, filename: str, lines: List[str]):
        """检查错误处理"""
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # 检查直接节点访问
            if re.search(r'\$[A-Za-z_][A-Za-z0-9_/]*', line) and 'get_node_or_null' not in line:
                self.add_issue(
                    filename, i, line,
                    "ERROR_HANDLING",
                    "直接使用路径访问节点，建议使用get_node_or_null并进行null检查"
                )
    
    def check_scene_file(self, file_path: Path):
        """检查场景文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = str(file_path.relative_to(self.project_path))
            
            # 检查场景复杂度
            node_count = content.count('<node')
            if node_count > 50:
                self.add_issue(
                    filename, 0, "",
                    "COMPLEXITY",
                    f"场景包含{node_count}个节点，考虑拆分为更小的子场景以提高性能"
                )
        
        except Exception as e:
            print(f"Error checking scene file {file_path}: {e}")
    
    def add_issue(self, filename: str, line_number: int, line_content: str, 
                  issue_type: str, message: str):
        """添加一个问题到列表"""
        issue = {
            'file': filename,
            'line': line_number,
            'content': line_content,
            'type': issue_type,
            'message': message,
            'severity': self._get_severity(issue_type)
        }
        self.issues.append(issue)
    
    def _get_severity(self, issue_type: str) -> str:
        """获取问题严重程度"""
        severity_map = {
            'PERFORMANCE': 'MEDIUM',
            'MEMORY': 'HIGH',
            'ERROR_HANDLING': 'HIGH',
            'PHYSICS': 'MEDIUM',
            'BEST_PRACTICE': 'LOW',
            'COMPLEXITY': 'MEDIUM'
        }
        return severity_map.get(issue_type, 'LOW')
    
    def generate_report(self) -> str:
        """生成检查报告"""
        if not self.issues:
            return "🎉 没有发现明显问题！"
        
        # 按严重程度分组
        issues_by_severity = {'HIGH': [], 'MEDIUM': [], 'LOW': []}
        for issue in self.issues:
            issues_by_severity[issue['severity']].append(issue)
        
        report = []
        report.append("# Godot代码检查报告\n")
        
        # 严重问题
        if issues_by_severity['HIGH']:
            report.append("## 🚨 严重问题\n")
            for issue in issues_by_severity['HIGH']:
                report.append(f"**{issue['file']}:{issue['line']}** ({issue['type']})")
                report.append(f"- 问题：{issue['message']}")
                if issue['content']:
                    report.append(f"- 代码：`{issue['content']}`")
                report.append("")
        
        # 中等问题
        if issues_by_severity['MEDIUM']:
            report.append("## ⚠️ 中等问题\n")
            for issue in issues_by_severity['MEDIUM']:
                report.append(f"**{issue['file']}:{issue['line']}** ({issue['type']})")
                report.append(f"- 问题：{issue['message']}")
                if issue['content']:
                    report.append(f"- 代码：`{issue['content']}`")
                report.append("")
        
        # 轻微问题
        if issues_by_severity['LOW']:
            report.append("## 💡 改进建议\n")
            for issue in issues_by_severity['LOW']:
                report.append(f"**{issue['file']}:{issue['line']}** ({issue['type']})")
                report.append(f"- 建议：{issue['message']}")
                if issue['content']:
                    report.append(f"- 代码：`{issue['content']}`")
                report.append("")
        
        # 统计信息
        report.append("## 📊 统计信息\n")
        report.append(f"- 总问题数：{len(self.issues)}")
        report.append(f"- 严重问题：{len(issues_by_severity['HIGH'])}")
        report.append(f"- 中等问题：{len(issues_by_severity['MEDIUM'])}")
        report.append(f"- 改进建议：{len(issues_by_severity['LOW'])}")
        
        return "\n".join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: python godot_linter.py <godot_project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    if not os.path.exists(project_path):
        print(f"Error: Path '{project_path}' does not exist")
        sys.exit(1)
    
    linter = GodotLinter(project_path)
    issues = linter.scan_project()
    report = linter.generate_report()
    
    print(report)
    
    # 保存报告到文件
    report_path = os.path.join(project_path, "godot_lint_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📝 报告已保存到：{report_path}")

if __name__ == "__main__":
    main()