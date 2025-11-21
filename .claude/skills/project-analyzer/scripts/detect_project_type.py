#!/usr/bin/env python3
"""
项目类型检测脚本
用于自动识别项目的技术栈和框架类型
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple

class ProjectDetector:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.indicators = self._load_indicators()

    def _load_indicators(self) -> Dict:
        """加载项目识别指标"""
        return {
            "web_frontend": {
                "files": ["package.json", "webpack.config.js", "vite.config.js", "next.config.js"],
                "directories": ["src", "public", "dist", "build"],
                "dependencies": ["react", "vue", "angular", "svelte"],
                "extensions": [".jsx", ".tsx", ".vue", ".svelte"]
            },
            "web_backend": {
                "files": ["requirements.txt", "Pipfile", "Gemfile", "pom.xml", "build.gradle"],
                "directories": ["app", "lib", "config", "migrations"],
                "dependencies": ["django", "flask", "express", "spring", "rails"],
                "extensions": [".py", ".java", ".rb", ".go"]
            },
            "mobile": {
                "files": ["pubspec.yaml", "Podfile", "build.gradle", "package.json"],
                "directories": ["android", "ios", "lib"],
                "dependencies": ["react-native", "flutter", "cordova"],
                "extensions": [".dart", ".swift", ".kt"]
            },
            "desktop": {
                "files": ["CMakeLists.txt", "Cargo.toml", "package.json"],
                "directories": ["src", "build", "target"],
                "dependencies": ["electron", "qt", "gtk"],
                "extensions": [".cpp", ".c", ".rs"]
            },
            "data_science": {
                "files": ["requirements.txt", "environment.yml", "Dockerfile"],
                "directories": ["notebooks", "data", "models"],
                "dependencies": ["pandas", "numpy", "tensorflow", "pytorch", "scikit-learn"],
                "extensions": [".ipynb", ".py", ".r"]
            }
        }

    def detect(self) -> Dict:
        """检测项目类型"""
        project_type = "unknown"
        framework = None
        language = None
        confidence = 0

        for type_name, indicators in self.indicators.items():
            score = self._calculate_score(indicators)
            if score > confidence:
                confidence = score
                project_type = type_name
                framework, language = self._detect_framework_and_language(indicators)

        return {
            "type": project_type,
            "framework": framework,
            "language": language,
            "confidence": confidence,
            "details": self._get_project_details()
        }

    def _calculate_score(self, indicators: Dict) -> float:
        """计算项目类型匹配分数"""
        score = 0

        # 检查文件存在
        for file_name in indicators.get("files", []):
            if (self.root_path / file_name).exists():
                score += 20

        # 检查目录存在
        for dir_name in indicators.get("directories", []):
            if (self.root_path / dir_name).exists():
                score += 15

        # 检查文件扩展名
        for ext in indicators.get("extensions", []):
            if any(file.suffix == ext for file in self.root_path.rglob("*")):
                score += 10

        return score

    def _detect_framework_and_language(self, indicators: Dict) -> Tuple[str, str]:
        """检测具体的框架和语言"""
        framework = None
        language = None

        # 检查package.json中的依赖
        package_json = self.root_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

                    for dep in indicators.get("dependencies", []):
                        if dep in deps:
                            framework = dep
                            break
            except:
                pass

        # 基于扩展名检测语言
        ext_lang_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".cpp": "C++",
            ".c": "C",
            ".go": "Go",
            ".rs": "Rust",
            ".rb": "Ruby",
            ".dart": "Dart"
        }

        for file in self.root_path.rglob("*"):
            if file.suffix in ext_lang_map:
                language = ext_lang_map[file.suffix]
                break

        return framework, language

    def _get_project_details(self) -> Dict:
        """获取项目详细信息"""
        details = {
            "total_files": 0,
            "main_directories": [],
            "config_files": [],
            "has_docs": False,
            "has_tests": False
        }

        # 统计文件和目录
        for item in self.root_path.iterdir():
            if item.is_file():
                details["total_files"] += 1
                if item.name.endswith((".json", ".yaml", ".yml", ".toml", ".ini", ".conf")):
                    details["config_files"].append(item.name)
            elif item.is_dir() and not item.name.startswith('.'):
                details["main_directories"].append(item.name)

        # 检查文档和测试
        docs_patterns = ["docs", "doc", "documentation", "README", "readme"]
        tests_patterns = ["tests", "test", "spec", "__tests__", "test_"]

        for dir_name in details["main_directories"]:
            if any(pattern in dir_name.lower() for pattern in docs_patterns):
                details["has_docs"] = True
            if any(pattern in dir_name.lower() for pattern in tests_patterns):
                details["has_tests"] = True

        return details

def main():
    detector = ProjectDetector()
    result = detector.detect()

    print("项目类型检测结果:")
    print(f"类型: {result['type']}")
    print(f"框架: {result['framework'] or '未识别'}")
    print(f"语言: {result['language'] or '未识别'}")
    print(f"置信度: {result['confidence']}")
    print(f"详细信息: {result['details']}")

    return result

if __name__ == "__main__":
    main()