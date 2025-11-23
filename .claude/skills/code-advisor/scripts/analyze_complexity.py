#!/usr/bin/env python3
"""
代码复杂度分析工具
分析代码文件的圈复杂度、认知复杂度等指标
"""

import ast
import os
import sys
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ComplexityMetrics:
    """复杂度指标数据类"""
    file_path: str
    function_name: str
    line_number: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    lines_of_code: int
    parameters_count: int

class ComplexityAnalyzer(ast.NodeVisitor):
    """AST访问器，用于计算复杂度"""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.split('\n')
        self.complexity_metrics: List[ComplexityMetrics] = []
        self.current_function = None
        self.current_line = 0
        self.cyclomatic = 1  # 基础复杂度为1
        self.cognitive = 0
        self.nesting_level = 0
        
    def visit_FunctionDef(self, node):
        """访问函数定义"""
        old_function = self.current_function
        old_line = self.current_line
        old_cyclomatic = self.cyclomatic
        old_cognitive = self.cognitive
        old_nesting = self.nesting_level
        
        self.current_function = node.name
        self.current_line = node.lineno
        self.cyclomatic = 1
        self.cognitive = 0
        self.nesting_level = 0
        
        # 计算参数数量
        param_count = len(node.args.args) + len(node.args.kwonlyargs)
        if node.args.vararg:
            param_count += 1
        if node.args.kwarg:
            param_count += 1
        
        # 递归访问函数体
        self.generic_visit(node)
        
        # 计算代码行数
        lines_of_code = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
        
        # 记录复杂度指标
        self.complexity_metrics.append(ComplexityMetrics(
            file_path="",
            function_name=node.name,
            line_number=node.lineno,
            cyclomatic_complexity=self.cyclomatic,
            cognitive_complexity=self.cognitive,
            lines_of_code=lines_of_code,
            parameters_count=param_count
        ))
        
        # 恢复状态
        self.current_function = old_function
        self.current_line = old_line
        self.cyclomatic = old_cyclomatic
        self.cognitive = old_cognitive
        self.nesting_level = old_nesting
    
    def visit_If(self, node):
        """访问if语句"""
        self.cyclomatic += 1
        self.cognitive += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1
    
    def visit_While(self, node):
        """访问while循环"""
        self.cyclomatic += 1
        self.cognitive += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1
    
    def visit_For(self, node):
        """访问for循环"""
        self.cyclomatic += 1
        self.cognitive += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1
    
    def visit_With(self, node):
        """访问with语句"""
        self.cognitive += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1
    
    def visit_Try(self, node):
        """访问try-except语句"""
        self.cyclomatic += len(node.handlers) + (1 if node.finalbody else 0)
        self.cognitive += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1
    
    def visit_ExceptHandler(self, node):
        """访问except处理器"""
        self.cognitive += 1
        self.generic_visit(node)
    
    def visit_ListComp(self, node):
        """访问列表推导式"""
        self.cognitive += 1
        self.generic_visit(node)
    
    def visit_DictComp(self, node):
        """访问字典推导式"""
        self.cognitive += 1
        self.generic_visit(node)
    
    def visit_SetComp(self, node):
        """访问集合推导式"""
        self.cognitive += 1
        self.generic_visit(node)
    
    def visit_GeneratorExp(self, node):
        """访问生成器表达式"""
        self.cognitive += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        """访问布尔运算"""
        self.cognitive += len(node.values) - 1
        self.generic_visit(node)

class JavaScriptAnalyzer:
    """JavaScript代码复杂度分析器"""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.complexity_metrics: List[ComplexityMetrics] = []
    
    def analyze(self) -> List[ComplexityMetrics]:
        """分析JavaScript代码复杂度"""
        # 简化的JavaScript解析逻辑
        # 实际项目中建议使用esprima等专业解析器
        lines = self.source_code.split('\n')
        
        # 查找函数定义
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('function ') or 'function' in stripped:
                # 提取函数名
                func_name = self._extract_function_name(stripped)
                if func_name:
                    # 计算复杂度（简化版本）
                    cyclomatic = self._count_control_structures(lines, i)
                    cognitive = self._calculate_cognitive_complexity(lines, i)
                    
                    self.complexity_metrics.append(ComplexityMetrics(
                        file_path="",
                        function_name=func_name,
                        line_number=i + 1,
                        cyclomatic_complexity=cyclomatic,
                        cognitive_complexity=cognitive,
                        lines_of_code=0,  # 需要进一步分析
                        parameters_count=self._count_parameters(stripped)
                    ))
        
        return self.complexity_metrics
    
    def _extract_function_name(self, line: str) -> str:
        """提取函数名"""
        if 'function ' in line:
            parts = line.split('function ')
            if len(parts) > 1:
                name_part = parts[1].split('(')[0].strip()
                return name_part if name_part else 'anonymous'
        return ""
    
    def _count_control_structures(self, lines: List[str], start_line: int) -> int:
        """计算控制结构数量"""
        complexity = 1  # 基础复杂度
        for i in range(start_line, min(start_line + 50, len(lines))):
            line = lines[i].strip()
            if any(keyword in line for keyword in ['if', 'for', 'while', 'case', 'catch']):
                complexity += 1
        return complexity
    
    def _calculate_cognitive_complexity(self, lines: List[str], start_line: int) -> int:
        """计算认知复杂度（简化版本）"""
        complexity = 0
        nesting = 0
        
        for i in range(start_line, min(start_line + 50, len(lines))):
            line = lines[i].strip()
            
            if any(keyword in line for keyword in ['if', 'for', 'while', 'try', 'with']):
                complexity += 1 + nesting
                nesting += 1
            elif '}' in line and nesting > 0:
                nesting -= 1
        
        return complexity
    
    def _count_parameters(self, line: str) -> int:
        """计算函数参数数量"""
        if '(' in line and ')' in line:
            params_str = line.split('(')[1].split(')')[0]
            if not params_str.strip():
                return 0
            return len([p.strip() for p in params_str.split(',') if p.strip()])
        return 0

def analyze_file(file_path: str) -> List[ComplexityMetrics]:
    """分析单个文件的复杂度"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.py':
            tree = ast.parse(source_code)
            analyzer = ComplexityAnalyzer(source_code)
            analyzer.visit(tree)
            metrics = analyzer.complexity_metrics
            
        elif file_ext in ['.js', '.jsx', '.ts', '.tsx']:
            js_analyzer = JavaScriptAnalyzer(source_code)
            metrics = js_analyzer.analyze()
            
        else:
            return []
        
        # 设置文件路径
        for metric in metrics:
            metric.file_path = file_path
        
        return metrics
    
    except Exception as e:
        print(f"Error analyzing file {file_path}: {e}")
        return []

def generate_report(metrics: List[ComplexityMetrics]) -> Dict[str, Any]:
    """生成复杂度分析报告"""
    if not metrics:
        return {"error": "No metrics to analyze"}
    
    # 按复杂度排序
    sorted_metrics = sorted(metrics, key=lambda x: x.cyclomatic_complexity, reverse=True)
    
    # 计算统计信息
    total_functions = len(metrics)
    high_complexity = [m for m in metrics if m.cyclomatic_complexity > 10]
    medium_complexity = [m for m in metrics if 5 <= m.cyclomatic_complexity <= 10]
    low_complexity = [m for m in metrics if m.cyclomatic_complexity < 5]
    
    avg_cyclomatic = sum(m.cylomatic_complexity for m in metrics) / total_functions
    avg_cognitive = sum(m.cognitive_complexity for m in metrics) / total_functions
    
    report = {
        "summary": {
            "total_functions": total_functions,
            "high_complexity_count": len(high_complexity),
            "medium_complexity_count": len(medium_complexity),
            "low_complexity_count": len(low_complexity),
            "average_cyclomatic_complexity": round(avg_cyclomatic, 2),
            "average_cognitive_complexity": round(avg_cognitive, 2)
        },
        "complex_functions": [
            {
                "file": m.file_path,
                "function": m.function_name,
                "line": m.line_number,
                "cyclomatic_complexity": m.cyclomatic_complexity,
                "cognitive_complexity": m.cognitive_complexity,
                "parameters": m.parameters_count,
                "lines": m.lines_of_code
            }
            for m in high_complexity
        ],
        "recommendations": []
    }
    
    # 生成建议
    if high_complexity:
        report["recommendations"].append(
            f"发现 {len(high_complexity)} 个高复杂度函数，建议重构以提高可维护性"
        )
    
    if avg_cyclomatic > 5:
        report["recommendations"].append(
            "平均圈复杂度过高，建议简化控制逻辑和函数设计"
        )
    
    return report

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("Usage: python analyze_complexity.py <file_or_directory>")
        sys.exit(1)
    
    path = sys.argv[1]
    all_metrics = []
    
    if os.path.isfile(path):
        # 分析单个文件
        all_metrics = analyze_file(path)
    
    elif os.path.isdir(path):
        # 分析目录中的所有代码文件
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx')):
                    file_path = os.path.join(root, file)
                    metrics = analyze_file(file_path)
                    all_metrics.extend(metrics)
    
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)
    
    # 生成并输出报告
    report = generate_report(all_metrics)
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()