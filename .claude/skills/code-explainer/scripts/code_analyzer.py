#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码分析器 - 智能代码解释和可视化工具
支持多种编程语言的语法分析、结构解析和意图识别
"""

import argparse
import re
import ast
import json
import sys
import os
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# 设置控制台编码
if sys.platform == 'win32':
    try:
        os.system('chcp 65001 >nul')
    except:
        pass

class AnalysisDepth(Enum):
    """分析深度枚举"""
    BASIC = "basic"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"

class LanguageType(Enum):
    """支持的编程语言"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    UNKNOWN = "unknown"

@dataclass
class FunctionInfo:
    """函数信息结构"""
    name: str
    params: List[str]
    return_type: str
    docstring: str
    complexity: str
    line_number: int

@dataclass
class ClassInfo:
    """类信息结构"""
    name: str
    methods: List[FunctionInfo]
    attributes: List[str]
    inheritance: List[str]
    line_number: int

@dataclass
class AnalysisResult:
    """分析结果结构"""
    language: LanguageType
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    imports: List[str]
    complexity: str
    patterns: List[str]
    summary: str

class CodeAnalyzer:
    """代码分析器主类"""
    
    def __init__(self):
        self.patterns = {
            'design_patterns': {
                'singleton': r'class\s+\w+.*\ndef\s+__new__',
                'observer': r'notify|update|subscribe|unsubscribe',
                'factory': r'def\s+create_\w+|def\s+factory',
                'decorator': r'@\w+|def\s+decorator',
                'adapter': r'Adapter|Wrapper',
            },
            'async_patterns': {
                'async': r'async\s+def|await|asyncio',
                'promise': r'Promise|\.then\(|\.catch\(',
                'callback': r'callback|cb\s*=|function\s*\([^)]*\)\s*{',
            }
        }
    
    def detect_language(self, file_path: str, code: str = None) -> LanguageType:
        """检测编程语言"""
        if file_path:
            ext = Path(file_path).suffix.lower()
            lang_map = {
                '.py': LanguageType.PYTHON,
                '.js': LanguageType.JAVASCRIPT,
                '.jsx': LanguageType.JAVASCRIPT,
                '.ts': LanguageType.TYPESCRIPT,
                '.tsx': LanguageType.TYPESCRIPT,
                '.java': LanguageType.JAVA,
                '.cpp': LanguageType.CPP,
                '.cc': LanguageType.CPP,
                '.cxx': LanguageType.CPP,
                '.go': LanguageType.GO,
                '.rs': LanguageType.RUST,
            }
            return lang_map.get(ext, LanguageType.UNKNOWN)
        
        if code:
            # 基于代码特征识别语言
            if 'def ' in code and 'import ' in code:
                return LanguageType.PYTHON
            elif 'function ' in code or 'const ' in code:
                if 'interface ' in code or 'type ' in code:
                    return LanguageType.TYPESCRIPT
                return LanguageType.JAVASCRIPT
            elif 'public class ' in code:
                return LanguageType.JAVA
            elif '#include' in code:
                return LanguageType.CPP
            elif 'package ' in code and 'func ' in code:
                return LanguageType.GO
            elif 'fn ' in code and '->' in code:
                return LanguageType.RUST
        
        return LanguageType.UNKNOWN

    def analyze_python(self, code: str, depth: AnalysisDepth) -> AnalysisResult:
        """分析Python代码"""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return AnalysisResult(
                language=LanguageType.PYTHON,
                functions=[],
                classes=[],
                imports=[],
                complexity="语法错误",
                patterns=[],
                summary=f"代码解析失败: {e}"
            )
        
        functions = []
        classes = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                params = [arg.arg for arg in node.args.args]
                return_type = ast.unparse(node.returns) if node.returns else "None"
                docstring = ast.get_docstring(node) or ""
                
                functions.append(FunctionInfo(
                    name=node.name,
                    params=params,
                    return_type=return_type,
                    docstring=docstring,
                    complexity=self._calculate_function_complexity(node),
                    line_number=node.lineno
                ))
            
            elif isinstance(node, ast.ClassDef):
                methods = []
                attributes = []
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        params = [arg.arg for arg in item.args.args]
                        methods.append(FunctionInfo(
                            name=item.name,
                            params=params,
                            return_type="None",
                            docstring=ast.get_docstring(item) or "",
                            complexity="简单",
                            line_number=item.lineno
                        ))
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                attributes.append(target.id)
                
                base_classes = [base.id for base in node.bases if isinstance(base, ast.Name)]
                
                classes.append(ClassInfo(
                    name=node.name,
                    methods=methods,
                    attributes=attributes,
                    inheritance=base_classes,
                    line_number=node.lineno
                ))
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        patterns = self._detect_patterns(code)
        summary = self._generate_summary(functions, classes, len(code.split('\n')))
        complexity = self._calculate_overall_complexity(functions, classes)
        
        return AnalysisResult(
            language=LanguageType.PYTHON,
            functions=functions,
            classes=classes,
            imports=imports,
            complexity=complexity,
            patterns=patterns,
            summary=summary
        )
    
    def analyze_javascript(self, code: str, depth: AnalysisDepth) -> AnalysisResult:
        """分析JavaScript/TypeScript代码"""
        functions = []
        classes = []
        imports = []
        
        # 函数检测
        func_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>',
            r'(\w+)\s*:\s*\([^)]*\)\s*=>',
            r'async\s+function\s+(\w+)',
        ]
        
        for pattern in func_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                functions.append(FunctionInfo(
                    name=match.group(1),
                    params=[],
                    return_type="unknown",
                    docstring="",
                    complexity="中等",
                    line_number=code[:match.start()].count('\n') + 1
                ))
        
        # 类检测
        class_matches = re.finditer(r'class\s+(\w+)(?:\s+extends\s+(\w+))?', code)
        for match in class_matches:
            class_name = match.group(1)
            parent = match.group(2) if match.group(2) else None
            classes.append(ClassInfo(
                name=class_name,
                methods=[],
                attributes=[],
                inheritance=[parent] if parent else [],
                line_number=code[:match.start()].count('\n') + 1
            ))
        
        # 导入检测
        import_patterns = [
            r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\([\'"]([^\'"]+)[\'"]\)',
            r'import\s+\{[^}]*\}\s+from\s+[\'"]([^\'"]+)[\'"]'
        ]
        
        for pattern in import_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                imports.append(match.group(1))
        
        patterns = self._detect_patterns(code)
        summary = self._generate_summary(functions, classes, len(code.split('\n')))
        complexity = self._calculate_overall_complexity(functions, classes)
        
        lang_type = LanguageType.TYPESCRIPT if 'interface ' in code or 'type ' in code else LanguageType.JAVASCRIPT
        return AnalysisResult(
            language=lang_type,
            functions=functions,
            classes=classes,
            imports=imports,
            complexity=complexity,
            patterns=patterns,
            summary=summary
        )

    def _calculate_function_complexity(self, node) -> str:
        """计算函数复杂度"""
        complexity_score = 1
        
        # 统计控制结构
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                complexity_score += 1
            elif isinstance(child, ast.Try):
                complexity_score += 2
        
        if complexity_score <= 3:
            return "简单"
        elif complexity_score <= 7:
            return "中等"
        else:
            return "复杂"
    
    def _detect_patterns(self, code: str) -> List[str]:
        """检测代码模式"""
        detected_patterns = []
        
        for category, patterns in self.patterns.items():
            for pattern_name, pattern in patterns.items():
                if re.search(pattern, code, re.IGNORECASE):
                    detected_patterns.append(pattern_name)
        
        return detected_patterns
    
    def _generate_summary(self, functions: List[FunctionInfo], classes: List[ClassInfo], lines: int) -> str:
        """生成代码摘要"""
        parts = []
        if classes:
            parts.append(f"包含{len(classes)}个类")
        if functions:
            parts.append(f"包含{len(functions)}个函数")
        parts.append(f"共{lines}行代码")
        
        return "，".join(parts)
    
    def _calculate_overall_complexity(self, functions: List[FunctionInfo], classes: List[ClassInfo]) -> str:
        """计算整体复杂度"""
        if not functions and not classes:
            return "简单"
        
        complex_count = sum(1 for f in functions if f.complexity == "复杂")
        medium_count = sum(1 for f in functions if f.complexity == "中等")
        
        if complex_count > 0:
            return "高复杂度"
        elif medium_count > len(functions) // 2:
            return "中等复杂度"
        else:
            return "低复杂度"

def format_analysis_report(result: AnalysisResult, depth: AnalysisDepth = AnalysisDepth.DETAILED) -> str:
    """格式化分析报告"""
    report = []
    
    # 代码概览
    report.append("# 代码分析报告\n")
    report.append(f"**编程语言**: {result.language.value}")
    report.append(f"**复杂度**: {result.complexity}")
    report.append(f"**代码摘要**: {result.summary}")
    
    if result.patterns:
        report.append(f"**设计模式**: {', '.join(result.patterns)}")
    
    report.append("")
    
    # 函数分析
    if result.functions:
        report.append("## 函数分析\n")
        if depth == AnalysisDepth.BASIC:
            for func in result.functions:
                report.append(f"### `{func.name}`")
                report.append(f"- **参数**: {', '.join(func.params) if func.params else '无'}")
                report.append(f"- **返回类型**: {func.return_type}")
                report.append(f"- **复杂度**: {func.complexity}")
                report.append("")
        else:
            # 详细表格
            report.append("| 函数名 | 参数 | 返回类型 | 复杂度 | 行号 |")
            report.append("|--------|------|----------|--------|------|")
            for func in result.functions:
                params = ', '.join(func.params[:3]) + ('...' if len(func.params) > 3 else '')
                report.append(f"| `{func.name}` | {params or '无'} | {func.return_type} | {func.complexity} | {func.line_number} |")
            report.append("")
    
    # 类分析
    if result.classes:
        report.append("## 类分析\n")
        for cls in result.classes:
            report.append(f"### `{cls.name}`")
            if cls.inheritance:
                report.append(f"**继承**: {', '.join(cls.inheritance)}")
            if cls.methods:
                report.append(f"**方法**: {len(cls.methods)}个")
            if cls.attributes:
                report.append(f"**属性**: {', '.join(cls.attributes)}")
            report.append("")
    
    # 导入依赖
    if result.imports and depth != AnalysisDepth.BASIC:
        report.append("## 依赖项\n")
        for imp in result.imports[:10]:  # 限制显示数量
            report.append(f"- `{imp}`")
        if len(result.imports) > 10:
            report.append(f"- ... 还有{len(result.imports) - 10}个导入")
        report.append("")
    
    return '\n'.join(report)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='智能代码分析器')
    parser.add_argument('--file', type=str, help='要分析的文件路径')
    parser.add_argument('--code', type=str, help='要分析的代码字符串')
    parser.add_argument('--depth', type=str, default='detailed', 
                       choices=['basic', 'detailed', 'comprehensive'],
                       help='分析深度')
    
    args = parser.parse_args()
    
    if not args.file and not args.code:
        print("错误: 必须指定 --file 或 --code 参数")
        return
    
    analyzer = CodeAnalyzer()
    depth = AnalysisDepth(args.depth)
    
    try:
        if args.file:
            file_path = Path(args.file)
            if not file_path.exists():
                print(f"错误: 文件不存在 - {args.file}")
                return
            
            code = file_path.read_text(encoding='utf-8')
            language = analyzer.detect_language(args.file)
        else:
            code = args.code
            language = analyzer.detect_language("", code)
        
        # 根据语言选择分析方法
        if language == LanguageType.PYTHON:
            result = analyzer.analyze_python(code, depth)
        elif language in [LanguageType.JAVASCRIPT, LanguageType.TYPESCRIPT]:
            result = analyzer.analyze_javascript(code, depth)
        else:
            # 通用分析
            result = AnalysisResult(
                language=language,
                functions=[],
                classes=[],
                imports=[],
                complexity="未知",
                patterns=[],
                summary="不支持的语言类型"
            )
        
        # 输出分析报告
        report = format_analysis_report(result, depth)
        print(report)
        
        # 可选: 输出JSON格式结果
        if args.depth == 'comprehensive':
            json_data = {
                'language': result.language.value,
                'complexity': result.complexity,
                'summary': result.summary,
                'patterns': result.patterns,
                'functions': [{'name': f.name, 'params': f.params, 'complexity': f.complexity} for f in result.functions],
                'classes': [{'name': c.name, 'methods': len(c.methods), 'inheritance': c.inheritance} for c in result.classes],
                'imports': result.imports
            }
            print(f"\n```json\n{json.dumps(json_data, ensure_ascii=False, indent=2)}\n```")
    
    except Exception as e:
        print(f"分析失败: {e}")

if __name__ == '__main__':
    main()