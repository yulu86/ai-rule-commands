#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

def detect_language(code):
    """简单的语言检测"""
    if 'def ' in code and ('import ' in code or ':' in code):
        return 'python'
    elif 'function ' in code or 'const ' in code or 'let ' in code:
        return 'javascript'
    elif 'public class ' in code:
        return 'java'
    else:
        return 'unknown'

def analyze_python(code):
    """分析Python代码"""
    functions = re.findall(r'def\s+(\w+)\s*\([^)]*\)', code)
    classes = re.findall(r'class\s+(\w+)', code)
    imports = re.findall(r'import\s+(\w+)', code)
    
    return {
        'language': 'python',
        'functions': functions,
        'classes': classes,
        'imports': imports,
        'lines': len(code.split('\n'))
    }

def analyze_javascript(code):
    """分析JavaScript代码"""
    functions = re.findall(r'function\s+(\w+)|const\s+(\w+)\s*=', code)
    classes = re.findall(r'class\s+(\w+)', code)
    
    # 提取函数名
    func_names = []
    for f1, f2 in functions:
        func_names.append(f1 or f2)
    
    return {
        'language': 'javascript',
        'functions': func_names,
        'classes': classes,
        'imports': [],
        'lines': len(code.split('\n'))
    }

def generate_report(analysis):
    """生成分析报告"""
    report = []
    report.append("# 代码分析报告\n")
    report.append(f"**编程语言**: {analysis['language']}")
    report.append(f"**代码行数**: {analysis['lines']}")
    report.append("")
    
    if analysis['functions']:
        report.append("## 函数分析")
        for func in analysis['functions']:
            report.append(f"- `{func}()`")
        report.append("")
    
    if analysis['classes']:
        report.append("## 类分析")
        for cls in analysis['classes']:
            report.append(f"- `{cls}`")
        report.append("")
    
    if analysis['imports']:
        report.append("## 导入模块")
        for imp in analysis['imports']:
            report.append(f"- `{imp}`")
        report.append("")
    
    return '\n'.join(report)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python simple_analyzer.py \"<code>\"")
        sys.exit(1)
    
    code = sys.argv[1]
    language = detect_language(code)
    
    if language == 'python':
        analysis = analyze_python(code)
    elif language == 'javascript':
        analysis = analyze_javascript(code)
    else:
        analysis = {'language': 'unknown', 'functions': [], 'classes': [], 'imports': [], 'lines': len(code.split('\n'))}
    
    report = generate_report(analysis)
    print(report)