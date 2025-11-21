#!/usr/bin/env python3
"""
项目结构分析脚本
分析项目的目录结构、文件组织和代码组织模式
"""

import os
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

class StructureAnalyzer:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.ignore_patterns = {
            ".git", "__pycache__", "node_modules", ".vscode",
            ".idea", "dist", "build", "target", ".DS_Store"
        }

    def analyze(self) -> Dict:
        """分析项目结构"""
        return {
            "directory_structure": self._analyze_directories(),
            "file_patterns": self._analyze_file_patterns(),
            "code_organization": self._analyze_code_organization(),
            "architecture_hints": self._extract_architecture_hints(),
            "dependencies": self._analyze_dependencies()
        }

    def _analyze_directories(self) -> Dict:
        """分析目录结构"""
        directories = []
        max_depth = 0

        for root, dirs, files in os.walk(self.root_path):
            # 过滤忽略的目录
            dirs[:] = [d for d in dirs if d not in self.ignore_patterns]

            current_depth = root.count(os.sep) - str(self.root_path).count(os.sep)
            max_depth = max(max_depth, current_depth)

            rel_path = Path(root).relative_to(self.root_path)
            if rel_path != Path("."):
                directories.append({
                    "path": str(rel_path),
                    "depth": current_depth,
                    "file_count": len([f for f in files if not f.startswith('.')]),
                    "subdirs": len(dirs)
                })

        return {
            "directories": sorted(directories, key=lambda x: x["depth"]),
            "max_depth": max_depth,
            "total_directories": len(directories)
        }

    def _analyze_file_patterns(self) -> Dict:
        """分析文件分布模式"""
        file_extensions = defaultdict(int)
        file_sizes = defaultdict(list)
        config_files = []
        test_files = []

        for file_path in self.root_path.rglob("*"):
            if file_path.is_file() and not self._should_ignore(file_path):
                # 统计文件扩展名
                ext = file_path.suffix.lower()
                if ext:
                    file_extensions[ext] += 1

                # 统计文件大小
                try:
                    size = file_path.stat().st_size
                    file_sizes[ext].append(size)
                except:
                    pass

                # 识别配置文件
                if self._is_config_file(file_path):
                    config_files.append(str(file_path.relative_to(self.root_path)))

                # 识别测试文件
                if self._is_test_file(file_path):
                    test_files.append(str(file_path.relative_to(self.root_path)))

        # 计算统计信息
        size_stats = {}
        for ext, sizes in file_sizes.items():
            if sizes:
                size_stats[ext] = {
                    "avg_size": sum(sizes) / len(sizes),
                    "max_size": max(sizes),
                    "min_size": min(sizes),
                    "total_size": sum(sizes)
                }

        return {
            "file_extensions": dict(file_extensions),
            "file_size_stats": size_stats,
            "config_files": config_files,
            "test_files": test_files,
            "total_files": sum(file_extensions.values())
        }

    def _analyze_code_organization(self) -> Dict:
        """分析代码组织模式"""
        patterns = {
            "mvc": False,
            "layered": False,
            "modular": False,
            "service_oriented": False,
            "feature_based": False
        }

        # 检查MVC模式
        mvc_indicators = ["models", "views", "controllers", "components"]
        if any(indicator in str(self.root_path).lower() for indicator in mvc_indicators):
            patterns["mvc"] = True

        # 检查分层架构
        layer_indicators = ["src", "lib", "app", "services", "repositories", "domain"]
        found_layers = sum(1 for indicator in layer_indicators
                          if any(indicator in str(p).lower() for p in self.root_path.rglob("*") if p.is_dir()))
        if found_layers >= 3:
            patterns["layered"] = True

        # 检查模块化
        if any(p.is_dir() for p in self.root_path.glob("modules/*")):
            patterns["modular"] = True

        # 检查服务导向
        service_indicators = ["services", "api", "handlers", "controllers"]
        if any(indicator in str(self.root_path).lower() for indicator in service_indicators):
            patterns["service_oriented"] = True

        # 检查功能导向
        feature_indicators = ["features", "pages", "screens"]
        if any(indicator in str(self.root_path).lower() for indicator in feature_indicators):
            patterns["feature_based"] = True

        return patterns

    def _extract_architecture_hints(self) -> List[str]:
        """提取架构提示"""
        hints = []

        # 检查微服务
        if any(p.name in ["docker-compose.yml", "Dockerfile"] for p in self.root_path.glob("*")):
            hints.append("容器化部署")

        # 检查API
        if any("api" in str(p).lower() for p in self.root_path.rglob("*")):
            hints.append("API服务")

        # 检查数据库配置
        db_files = ["database.yml", "db.py", "models.py", "schema.sql"]
        if any(any(db_file in f.name.lower() for db_file in db_files)
               for f in self.root_path.rglob("*")):
            hints.append("数据库集成")

        # 检查前端框架
        frontend_files = ["package.json", "webpack.config.js", "vite.config.js"]
        if any(f.name in frontend_files for f in self.root_path.glob("*")):
            hints.append("前端应用")

        # 检查测试覆盖率
        if len(list(self.root_path.rglob("*test*"))) > 2:
            hints.append("重视测试")

        return hints

    def _analyze_dependencies(self) -> Dict:
        """分析项目依赖"""
        dependencies = {}

        # 检查package.json
        package_json = self.root_path / "package.json"
        if package_json.exists():
            try:
                import json
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    dependencies["npm"] = {
                        "dependencies": list(data.get("dependencies", {}).keys()),
                        "devDependencies": list(data.get("devDependencies", {}).keys())
                    }
            except:
                pass

        # 检查requirements.txt
        requirements_txt = self.root_path / "requirements.txt"
        if requirements_txt.exists():
            try:
                with open(requirements_txt, 'r', encoding='utf-8') as f:
                    deps = [line.strip().split('==')[0].split('>=')[0]
                           for line in f if line.strip() and not line.startswith('#')]
                    dependencies["pip"] = deps
            except:
                pass

        return dependencies

    def _should_ignore(self, file_path: Path) -> bool:
        """检查是否应该忽略文件"""
        return any(pattern in str(file_path) for pattern in self.ignore_patterns)

    def _is_config_file(self, file_path: Path) -> bool:
        """检查是否为配置文件"""
        config_patterns = [
            ".json", ".yaml", ".yml", ".toml", ".ini", ".conf", ".config",
            "Dockerfile", "docker-compose", ".env"
        ]
        return any(file_path.name.endswith(pattern) or pattern in file_path.name
                  for pattern in config_patterns)

    def _is_test_file(self, file_path: Path) -> bool:
        """检查是否为测试文件"""
        test_patterns = ["test", "spec", "__test__"]
        return any(pattern in file_path.name.lower() or pattern in str(file_path).lower()
                  for pattern in test_patterns)

def main():
    analyzer = StructureAnalyzer()
    result = analyzer.analyze()

    print("项目结构分析结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    return result

if __name__ == "__main__":
    import json
    main()