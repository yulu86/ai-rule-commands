#!/usr/bin/env python3
"""
设计文档生成脚本
基于分析结果生成标准化的设计文档
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class DesignDocGenerator:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.docs_path = self.root_path / "docs"
        self.templates_path = Path(__file__).parent.parent / "assets"

    def generate(self, analysis_results: Dict) -> str:
        """生成设计文档"""
        # 确保docs目录存在
        self.docs_path.mkdir(exist_ok=True)

        # 分析结果
        project_type = analysis_results.get("project_type", {})
        structure = analysis_results.get("structure", {})
        patterns = analysis_results.get("patterns", {})

        # 生成文档
        doc_content = self._generate_document_content(analysis_results)

        # 创建目录结构
        doc_dir = self._create_doc_directory(project_type.get("type", "unknown"))
        doc_file = doc_dir / f"01_{self._get_doc_title(project_type.get('type', 'unknown'))}.md"

        # 写入文档
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)

        return str(doc_file)

    def _generate_document_content(self, analysis_results: Dict) -> str:
        """生成文档内容"""
        project_type = analysis_results.get("project_type", {})
        structure = analysis_results.get("structure", {})
        patterns = analysis_results.get("patterns", {})

        # 加载模板
        template = self._load_template()

        # 替换模板变量
        content = template.format(
            project_name=self._get_project_name(),
            project_type=project_type.get("type", "unknown"),
            framework=project_type.get("framework", "未识别"),
            language=project_type.get("language", "未识别"),
            generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            project_overview=self._generate_project_overview(analysis_results),
            architecture_analysis=self._generate_architecture_analysis(structure, patterns),
            design_patterns=self._generate_design_patterns_section(patterns),
            structure_analysis=self._generate_structure_analysis(structure),
            recommendations=self._generate_recommendations(analysis_results)
        )

        return content

    def _create_doc_directory(self, project_type: str) -> Path:
        """创建文档目录"""
        # 根据项目类型确定目录
        type_mapping = {
            "web_frontend": "01_前端应用",
            "web_backend": "02_后端服务",
            "mobile": "03_移动应用",
            "desktop": "04_桌面应用",
            "data_science": "05_数据科学",
            "unknown": "99_未知类型"
        }

        dir_name = type_mapping.get(project_type, "99_未知类型")
        doc_dir = self.docs_path / dir_name
        doc_dir.mkdir(parents=True, exist_ok=True)

        return doc_dir

    def _get_doc_title(self, project_type: str) -> str:
        """获取文档标题"""
        title_mapping = {
            "web_frontend": "前端应用设计文档",
            "web_backend": "后端服务设计文档",
            "mobile": "移动应用设计文档",
            "desktop": "桌面应用设计文档",
            "data_science": "数据科学项目设计文档",
            "unknown": "项目设计文档"
        }
        return title_mapping.get(project_type, "项目设计文档")

    def _load_template(self) -> str:
        """加载文档模板"""
        template_path = self.templates_path / "design_doc_template.md"
        if template_path.exists():
            return template_path.read_text(encoding='utf-8')
        else:
            return self._get_default_template()

    def _get_default_template(self) -> str:
        """获取默认模板"""
        return """# {project_name} - {project_type}设计文档

## 项目概述

**项目名称**: {project_name}
**项目类型**: {project_type}
**主要框架**: {framework}
**开发语言**: {language}
**生成时间**: {generation_time}

{project_overview}

## 架构分析

{architecture_analysis}

## 设计模式

{design_patterns}

## 项目结构分析

{structure_analysis}

## 建议和改进

{recommendations}

---

*本文档由项目分析器自动生成，请人工审查和补充完善*
"""

    def _get_project_name(self) -> str:
        """获取项目名称"""
        # 尝试从package.json或pyproject.toml等文件中获取
        for config_file in ["package.json", "pyproject.toml", "Cargo.toml", "pom.xml"]:
            config_path = self.root_path / config_file
            if config_path.exists():
                try:
                    if config_file == "package.json":
                        import json
                        data = json.loads(config_path.read_text(encoding='utf-8'))
                        return data.get("name", self.root_path.name)
                except:
                    pass

        return self.root_path.name

    def _generate_project_overview(self, analysis_results: Dict) -> str:
        """生成项目概述"""
        project_type = analysis_results.get("project_type", {})
        details = project_type.get("details", {})

        overview_parts = []

        # 基本信息
        overview_parts.append("### 基本信息")
        overview_parts.append(f"- 项目类型: {project_type.get('type', '未识别')}")
        overview_parts.append(f"- 技术框架: {project_type.get('framework', '未识别')}")
        overview_parts.append(f"- 编程语言: {project_type.get('language', '未识别')}")
        overview_parts.append(f"- 分析置信度: {project_type.get('confidence', 0)}%")

        # 项目统计
        if details:
            overview_parts.append("\n### 项目统计")
            overview_parts.append(f"- 总文件数: {details.get('total_files', 0)}")
            overview_parts.append(f"- 主要目录: {', '.join(details.get('main_directories', []))}")
            overview_parts.append(f"- 包含文档: {'是' if details.get('has_docs') else '否'}")
            overview_parts.append(f"- 包含测试: {'是' if details.get('has_tests') else '否'}")

        return "\n".join(overview_parts)

    def _generate_architecture_analysis(self, structure: Dict, patterns: Dict) -> str:
        """生成架构分析"""
        analysis_parts = []

        # 代码组织模式
        code_org = structure.get("code_organization", {})
        if code_org:
            analysis_parts.append("### 代码组织模式")
            for pattern, detected in code_org.items():
                status = "✓ 检测到" if detected else "✗ 未检测到"
                analysis_parts.append(f"- {pattern.replace('_', ' ').title()}: {status}")

        # 架构模式
        arch_patterns = patterns.get("architecture_patterns", [])
        if arch_patterns:
            analysis_parts.append("\n### 架构模式")
            for pattern in arch_patterns:
                analysis_parts.append(f"- {pattern}")

        # 依赖分析
        dependencies = structure.get("dependencies", {})
        if dependencies:
            analysis_parts.append("\n### 依赖管理")
            for dep_type, deps in dependencies.items():
                analysis_parts.append(f"- {dep_type}: {len(deps)} 个依赖")

        return "\n".join(analysis_parts) if analysis_parts else "暂无架构分析结果"

    def _generate_design_patterns_section(self, patterns: Dict) -> str:
        """生成设计模式部分"""
        design_patterns = patterns.get("design_patterns", {})
        if not design_patterns:
            return "未检测到明确的设计模式"

        sections = []

        for category, patterns_dict in design_patterns.items():
            if patterns_dict:
                sections.append(f"### {category.title()} Patterns")
                for pattern, instances in patterns_dict.items():
                    sections.append(f"#### {pattern.title()}")
                    sections.append(f"- 检测到 {len(instances)} 个实例")

                    # 显示前几个实例
                    for instance in instances[:3]:
                        if "class" in instance:
                            sections.append(f"  - 类: {instance['class']} (文件: {instance.get('file', 'unknown')})")
                        elif "content" in instance:
                            sections.append(f"  - 位置: {instance.get('file', 'unknown')}:{instance.get('line', 'unknown')}")

                    if len(instances) > 3:
                        sections.append(f"  - ... 还有 {len(instances) - 3} 个实例")

        return "\n".join(sections)

    def _generate_structure_analysis(self, structure: Dict) -> str:
        """生成结构分析"""
        file_patterns = structure.get("file_patterns", {})
        dir_structure = structure.get("directory_structure", {})

        sections = []

        # 目录结构
        if dir_structure:
            sections.append("### 目录层次")
            sections.append(f"- 最大深度: {dir_structure.get('max_depth', 0)}")
            sections.append(f"- 目录总数: {dir_structure.get('total_directories', 0)}")

        # 文件分布
        if file_patterns:
            sections.append("\n### 文件分布")
            extensions = file_patterns.get("file_extensions", {})
            if extensions:
                sections.append("**文件类型分布:**")
                for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]:
                    sections.append(f"- {ext}: {count} 个文件")

            config_files = file_patterns.get("config_files", [])
            if config_files:
                sections.append(f"\n**配置文件 ({len(config_files)}):**")
                for config in config_files[:5]:
                    sections.append(f"- {config}")
                if len(config_files) > 5:
                    sections.append(f"- ... 还有 {len(config_files) - 5} 个配置文件")

            test_files = file_patterns.get("test_files", [])
            if test_files:
                sections.append(f"\n**测试文件 ({len(test_files)}):**")
                sections.append(f"- 发现 {len(test_files)} 个测试文件，测试覆盖率良好")

        return "\n".join(sections) if sections else "暂无结构分析结果"

    def _generate_recommendations(self, analysis_results: Dict) -> str:
        """生成建议"""
        recommendations = []

        # 基于设计模式的建议
        patterns = analysis_results.get("patterns", {})
        summary = patterns.get("summary", {})

        if summary.get("recommendations"):
            recommendations.extend(summary["recommendations"])

        # 基于项目结构的建议
        project_type = analysis_results.get("project_type", {})
        details = project_type.get("details", {})

        if not details.get("has_docs"):
            recommendations.append("建议添加项目文档，提高代码可维护性")

        if not details.get("has_tests"):
            recommendations.append("建议添加单元测试，提高代码质量")

        # 基于文件分布的建议
        structure = analysis_results.get("structure", {})
        file_patterns = structure.get("file_patterns", {})

        if file_patterns.get("config_files") and len(file_patterns["config_files"]) > 10:
            recommendations.append("配置文件较多，建议统一管理配置")

        # 通用建议
        if not recommendations:
            recommendations.append("项目结构良好，建议继续保持当前的代码组织方式")

        recommendations.append("定期更新依赖包，确保安全性")
        recommendations.append("建议建立代码审查流程")

        sections = ["### 改进建议"]
        for i, rec in enumerate(recommendations, 1):
            sections.append(f"{i}. {rec}")

        return "\n".join(sections)

def main():
    """主函数 - 用于测试"""
    # 模拟分析结果
    sample_results = {
        "project_type": {
            "type": "web_frontend",
            "framework": "React",
            "language": "TypeScript",
            "confidence": 85,
            "details": {
                "total_files": 150,
                "main_directories": ["src", "public", "build"],
                "has_docs": True,
                "has_tests": True
            }
        },
        "structure": {
            "code_organization": {
                "mvc": False,
                "layered": True,
                "modular": True
            },
            "file_patterns": {
                "file_extensions": {".tsx": 45, ".ts": 30, ".json": 10, ".md": 5},
                "config_files": ["package.json", "tsconfig.json", "webpack.config.js"],
                "test_files": ["App.test.tsx", "utils.test.ts"]
            }
        },
        "patterns": {
            "design_patterns": {
                "creational": {
                    "singleton": [{"class": "ConfigManager", "file": "src/config.ts"}],
                    "factory": [{"class": "ComponentFactory", "file": "src/factory.ts"}]
                }
            },
            "architecture_patterns": ["Component-Based Architecture"],
            "summary": {
                "recommendations": ["考虑使用Redux进行状态管理"]
            }
        }
    }

    generator = DesignDocGenerator()
    doc_path = generator.generate(sample_results)
    print(f"设计文档已生成: {doc_path}")

if __name__ == "__main__":
    main()