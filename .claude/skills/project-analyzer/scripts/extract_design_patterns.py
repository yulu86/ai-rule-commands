#!/usr/bin/env python3
"""
设计模式提取脚本
从代码中提取识别的设计模式和架构模式
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class DesignPatternExtractor:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.patterns = {
            "creational": {
                "singleton": self._detect_singleton,
                "factory": self._detect_factory,
                "builder": self._detect_builder,
                "prototype": self._detect_prototype
            },
            "structural": {
                "adapter": self._detect_adapter,
                "decorator": self._detect_decorator,
                "facade": self._detect_facade,
                "proxy": self._detect_proxy,
                "composite": self._detect_composite
            },
            "behavioral": {
                "observer": self._detect_observer,
                "strategy": self._detect_strategy,
                "command": self._detect_command,
                "state": self._detect_state,
                "template": self._detect_template_method
            }
        }

    def extract(self) -> Dict:
        """提取设计模式"""
        patterns_found = defaultdict(list)
        architecture_patterns = []

        # 扫描代码文件
        code_files = self._find_code_files()

        for file_path in code_files:
            file_patterns = self._analyze_file(file_path)
            for category, patterns in file_patterns.items():
                for pattern, instances in patterns.items():
                    patterns_found[f"{category}.{pattern}"].extend(instances)

        # 检测架构模式
        architecture_patterns = self._detect_architecture_patterns()

        return {
            "design_patterns": dict(patterns_found),
            "architecture_patterns": architecture_patterns,
            "summary": self._generate_summary(patterns_found, architecture_patterns)
        }

    def _find_code_files(self) -> List[Path]:
        """查找代码文件"""
        code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.rb', '.go'}
        files = []

        for file_path in self.root_path.rglob("*"):
            if (file_path.is_file() and
                file_path.suffix in code_extensions and
                not self._should_ignore(file_path)):
                files.append(file_path)

        return files

    def _analyze_file(self, file_path: Path) -> Dict:
        """分析单个文件的模式"""
        patterns_found = defaultdict(lambda: defaultdict(list))

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # 根据文件类型选择分析方法
            if file_path.suffix == '.py':
                patterns_found = self._analyze_python(content, file_path)
            elif file_path.suffix in {'.js', '.ts'}:
                patterns_found = self._analyze_javascript(content, file_path)
            else:
                patterns_found = self._analyze_generic(content, file_path)

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

        return patterns_found

    def _analyze_python(self, content: str, file_path: Path) -> Dict:
        """分析Python代码"""
        patterns_found = defaultdict(lambda: defaultdict(list))

        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # 检测各种模式
                    for pattern_name, detector in self.patterns["creational"].items():
                        if detector(node, content):
                            patterns_found["creational"][pattern_name].append({
                                "class": node.name,
                                "file": str(file_path),
                                "line": node.lineno
                            })

                    for pattern_name, detector in self.patterns["structural"].items():
                        if detector(node, content):
                            patterns_found["structural"][pattern_name].append({
                                "class": node.name,
                                "file": str(file_path),
                                "line": node.lineno
                            })

                    for pattern_name, detector in self.patterns["behavioral"].items():
                        if detector(node, content):
                            patterns_found["behavioral"][pattern_name].append({
                                "class": node.name,
                                "file": str(file_path),
                                "line": node.lineno
                            })

        except SyntaxError:
            pass

        return patterns_found

    def _analyze_javascript(self, content: str, file_path: Path) -> Dict:
        """分析JavaScript/TypeScript代码"""
        patterns_found = defaultdict(lambda: defaultdict(list))

        # 使用正则表达式检测模式
        lines = content.split('\n')

        for i, line in enumerate(lines):
            # 检测Singleton模式
            if re.search(r'(class|function)\s+\w+.*(?:getInstance|instance)', line):
                patterns_found["creational"]["singleton"].append({
                    "line": i + 1,
                    "file": str(file_path),
                    "content": line.strip()
                })

            # 检测Factory模式
            if re.search(r'(create|build|make|factory)\s*\w*\s*\(', line):
                patterns_found["creational"]["factory"].append({
                    "line": i + 1,
                    "file": str(file_path),
                    "content": line.strip()
                })

            # 检测Observer模式
            if re.search(r'(subscribe|on|addEventListener|watch)', line):
                patterns_found["behavioral"]["observer"].append({
                    "line": i + 1,
                    "file": str(file_path),
                    "content": line.strip()
                })

        return patterns_found

    def _analyze_generic(self, content: str, file_path: Path) -> Dict:
        """通用代码分析"""
        patterns_found = defaultdict(lambda: defaultdict(list))
        lines = content.split('\n')

        # 通用模式检测
        singleton_keywords = ["getInstance", "instance", "singleton"]
        factory_keywords = ["create", "build", "make", "factory"]
        observer_keywords = ["subscribe", "notify", "observer", "listener"]

        for i, line in enumerate(lines):
            line_lower = line.lower()

            if any(keyword in line_lower for keyword in singleton_keywords):
                patterns_found["creational"]["singleton"].append({
                    "line": i + 1,
                    "file": str(file_path),
                    "content": line.strip()
                })

            if any(keyword in line_lower for keyword in factory_keywords):
                patterns_found["creational"]["factory"].append({
                    "line": i + 1,
                    "file": str(file_path),
                    "content": line.strip()
                })

            if any(keyword in line_lower for keyword in observer_keywords):
                patterns_found["behavioral"]["observer"].append({
                    "line": i + 1,
                    "file": str(file_path),
                    "content": line.strip()
                })

        return patterns_found

    def _detect_singleton(self, node, content: str) -> bool:
        """检测Singleton模式"""
        singleton_indicators = ["_instance", "instance", "getInstance"]

        # 检查类名和属性
        if any(indicator in node.name for indicator in singleton_indicators):
            return True

        # 检查类内容
        class_content = content[node.lineno-1:node.end_lineno] if hasattr(node, 'end_lineno') else ""
        return any(indicator in class_content for indicator in singleton_indicators)

    def _detect_factory(self, node, content: str) -> bool:
        """检测Factory模式"""
        factory_indicators = ["create", "build", "make", "factory"]
        return any(indicator in node.name.lower() for indicator in factory_indicators)

    def _detect_builder(self, node, content: str) -> bool:
        """检测Builder模式"""
        builder_indicators = ["builder", "build", "with_", "set_", "add_"]
        return any(indicator in node.name.lower() for indicator in builder_indicators)

    def _detect_prototype(self, node, content: str) -> bool:
        """检测Prototype模式"""
        prototype_indicators = ["clone", "copy", "prototype"]
        return any(indicator in node.name.lower() for indicator in prototype_indicators)

    def _detect_adapter(self, node, content: str) -> bool:
        """检测Adapter模式"""
        adapter_indicators = ["adapter", "wrapper", "convert"]
        return any(indicator in node.name.lower() for indicator in adapter_indicators)

    def _detect_decorator(self, node, content: str) -> bool:
        """检测Decorator模式"""
        decorator_indicators = ["decorator", "wrapper"]
        return (any(indicator in node.name.lower() for indicator in decorator_indicators) or
                "@" in content and "decorator" in content.lower())

    def _detect_facade(self, node, content: str) -> bool:
        """检测Facade模式"""
        facade_indicators = ["facade", "manager", "controller"]
        return any(indicator in node.name.lower() for indicator in facade_indicators)

    def _detect_proxy(self, node, content: str) -> bool:
        """检测Proxy模式"""
        proxy_indicators = ["proxy", "surrogate"]
        return any(indicator in node.name.lower() for indicator in proxy_indicators)

    def _detect_composite(self, node, content: str) -> bool:
        """检测Composite模式"""
        composite_indicators = ["composite", "component", "leaf", "node"]
        return any(indicator in node.name.lower() for indicator in composite_indicators)

    def _detect_observer(self, node, content: str) -> bool:
        """检测Observer模式"""
        observer_indicators = ["observer", "subject", "notify", "subscribe"]
        return any(indicator in node.name.lower() for indicator in observer_indicators)

    def _detect_strategy(self, node, content: str) -> bool:
        """检测Strategy模式"""
        strategy_indicators = ["strategy", "algorithm"]
        return any(indicator in node.name.lower() for indicator in strategy_indicators)

    def _detect_command(self, node, content: str) -> bool:
        """检测Command模式"""
        command_indicators = ["command", "execute", "invoke"]
        return any(indicator in node.name.lower() for indicator in command_indicators)

    def _detect_state(self, node, content: str) -> bool:
        """检测State模式"""
        state_indicators = ["state", "context"]
        return any(indicator in node.name.lower() for indicator in state_indicators)

    def _detect_template_method(self, node, content: str) -> bool:
        """检测Template Method模式"""
        template_indicators = ["template", "abstract"]
        return any(indicator in node.name.lower() for indicator in template_indicators)

    def _detect_architecture_patterns(self) -> List[str]:
        """检测架构模式"""
        patterns = []

        # 检查目录结构
        directories = [d.name for d in self.root_path.iterdir() if d.is_dir()]

        # MVC模式
        if all(indicator in directories for indicator in ["models", "views", "controllers"]):
            patterns.append("MVC")

        # MVVM模式
        if all(indicator in directories for indicator in ["models", "views", "viewmodels"]):
            patterns.append("MVVM")

        # 分层架构
        layer_indicators = ["presentation", "business", "data", "domain"]
        if len([ind for ind in layer_indicators if ind in " ".join(directories).lower()]) >= 3:
            patterns.append("Layered Architecture")

        # 微服务
        if any("service" in d.lower() for d in directories):
            patterns.append("Microservices")

        # 事件驱动
        if any("event" in d.lower() for d in directories):
            patterns.append("Event-Driven Architecture")

        return patterns

    def _generate_summary(self, patterns_found: Dict, architecture_patterns: List[str]) -> Dict:
        """生成模式摘要"""
        summary = {
            "total_patterns": sum(len(instances) for instances in patterns_found.values()),
            "pattern_types": len(patterns_found),
            "architecture_patterns": len(architecture_patterns),
            "most_common": None,
            "recommendations": []
        }

        # 找出最常见的模式
        if patterns_found:
            most_common = max(patterns_found.items(), key=lambda x: len(x[1]))
            summary["most_common"] = {
                "pattern": most_common[0],
                "instances": len(most_common[1])
            }

        # 生成建议
        if len(architecture_patterns) == 0:
            summary["recommendations"].append("考虑建立清晰的架构模式以提高代码组织性")

        if summary["total_patterns"] < 3:
            summary["recommendations"].append("项目设计模式使用较少，可以考虑引入适当的设计模式")

        return summary

    def _should_ignore(self, file_path: Path) -> bool:
        """检查是否应该忽略文件"""
        ignore_patterns = {".git", "__pycache__", "node_modules", ".vscode", ".idea"}
        return any(pattern in str(file_path) for pattern in ignore_patterns)

def main():
    extractor = DesignPatternExtractor()
    result = extractor.extract()

    print("设计模式提取结果:")
    print(f"发现的设计模式: {result['design_patterns']}")
    print(f"架构模式: {result['architecture_patterns']}")
    print(f"摘要: {result['summary']}")

    return result

if __name__ == "__main__":
    main()