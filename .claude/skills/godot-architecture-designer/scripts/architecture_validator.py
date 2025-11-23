#!/usr/bin/env python3
"""
Godot架构设计验证工具
用于检查架构设计文档的完整性和规范性
"""

import os
import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]

class GodotArchitectureValidator:
    def __init__(self):
        self.required_sections = [
            "项目概述",
            "架构设计总览", 
            "核心系统设计",
            "实体系统架构",
            "界面系统架构",
            "数据架构设计",
            "性能优化策略",
            "开发规范"
        ]
        
        self.mermaid_patterns = [
            r"```mermaid",
            r"graph",
            r"stateDiagram",
            r"sequenceDiagram",
            r"classDiagram",
            r"erDiagram",
            r"gantt"
        ]
        
        self.table_patterns = [
            r"\|.*\|.*\|",
            r"\|.*\|.*\|.*\|"
        ]
        
        self.architecture_components = [
            "游戏管理器",
            "场景管理系统", 
            "输入系统",
            "玩家系统",
            "敌人系统",
            "UI系统",
            "音频系统",
            "物理系统",
            "存档系统"
        ]
    
    def validate_document(self, file_path: str) -> ValidationResult:
        """验证架构设计文档"""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return ValidationResult(False, [f"无法读取文件: {e}"], [], [])
        
        # 检查必需章节
        self._check_required_sections(content, errors, warnings)
        
        # 检查Mermaid图表
        self._check_mermaid_diagrams(content, warnings, suggestions)
        
        # 检查表格
        self._check_tables(content, warnings, suggestions)
        
        # 检查架构组件
        self._check_architecture_components(content, errors, warnings)
        
        # 检查命名规范
        self._check_naming_conventions(content, warnings)
        
        # 检查性能考虑
        self._check_performance_considerations(content, warnings, suggestions)
        
        # 检查可测试性
        self._check_testability(content, warnings, suggestions)
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, suggestions)
    
    def _check_required_sections(self, content: str, errors: List[str], warnings: List[str]):
        """检查必需章节"""
        missing_sections = []
        
        for section in self.required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            errors.append(f"缺少必需章节: {', '.join(missing_sections)}")
    
    def _check_mermaid_diagrams(self, content: str, warnings: List[str], suggestions: List[str]):
        """检查Mermaid图表"""
        mermaid_count = 0
        
        for pattern in self.mermaid_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            mermaid_count += len(matches)
        
        if mermaid_count == 0:
            warnings.append("文档中缺少Mermaid图表")
            suggestions.append("建议添加架构图、流程图或状态图来增强可视化")
        elif mermaid_count < 3:
            suggestions.append("建议添加更多类型的图表（如序列图、类图等）")
    
    def _check_tables(self, content: str, warnings: List[str], suggestions: List[str]):
        """检查表格"""
        table_count = 0
        
        for pattern in self.table_patterns:
            matches = re.findall(pattern, content)
            table_count += len(matches)
        
        if table_count == 0:
            warnings.append("文档中缺少表格")
            suggestions.append("建议使用表格来展示组件职责、接口定义等")
    
    def _check_architecture_components(self, content: str, errors: List[str], warnings: List[str]):
        """检查架构组件"""
        missing_components = []
        
        for component in self.architecture_components:
            if component not in content:
                missing_components.append(component)
        
        if missing_components:
            warnings.append(f"可能缺少架构组件描述: {', '.join(missing_components)}")
    
    def _check_naming_conventions(self, content: str, warnings: List[str]):
        """检查命名规范"""
        # 检查是否有命名规范相关内容
        naming_keywords = ["命名规范", "命名约定", "naming convention", "命名标准"]
        
        has_naming_section = any(keyword in content.lower() for keyword in naming_keywords)
        
        if not has_naming_section:
            warnings.append("缺少命名规范说明")
    
    def _check_performance_considerations(self, content: str, warnings: List[str], suggestions: List[str]):
        """检查性能考虑"""
        performance_keywords = ["性能", "优化", "performance", "optimization"]
        
        has_performance_section = any(keyword in content.lower() for keyword in performance_keywords)
        
        if not has_performance_section:
            warnings.append("缺少性能优化相关内容")
            suggestions.append("建议添加性能优化策略和考虑因素")
    
    def _check_testability(self, content: str, warnings: List[str], suggestions: List[str]):
        """检查可测试性"""
        test_keywords = ["测试", "test", "测试策略", "testing"]
        
        has_test_section = any(keyword in content.lower() for keyword in test_keywords)
        
        if not has_test_section:
            warnings.append("缺少测试策略相关内容")
            suggestions.append("建议添加单元测试、集成测试等测试策略")

class GodotProjectStructureValidator:
    """Godot项目结构验证器"""
    
    def __init__(self):
        self.required_directories = [
            "scenes",
            "scripts", 
            "assets",
            "resources"
        ]
        
        self.recommended_subdirectories = {
            "scenes": ["player", "enemies", "ui", "levels", "effects"],
            "scripts": ["managers", "components", "entities", "ui", "utilities"],
            "assets": ["textures", "sounds", "fonts", "materials"],
            "resources": ["items", "enemies", "levels", "animations"]
        }
    
    def validate_project_structure(self, project_path: str) -> ValidationResult:
        """验证Godot项目结构"""
        errors = []
        warnings = []
        suggestions = []
        
        if not os.path.exists(project_path):
            return ValidationResult(False, [f"项目路径不存在: {project_path}"], [], [])
        
        # 检查project.godot文件
        project_file = os.path.join(project_path, "project.godot")
        if not os.path.exists(project_file):
            errors.append("缺少project.godot文件")
        
        # 检查必需目录
        for directory in self.required_directories:
            dir_path = os.path.join(project_path, directory)
            if not os.path.exists(dir_path):
                warnings.append(f"缺少推荐目录: {directory}")
                suggestions.append(f"建议创建 {directory} 目录")
        
        # 检查推荐的子目录结构
        for parent_dir, subdirs in self.recommended_subdirectories.items():
            parent_path = os.path.join(project_path, parent_dir)
            if os.path.exists(parent_path):
                existing_subdirs = [d for d in os.listdir(parent_path) 
                                 if os.path.isdir(os.path.join(parent_path, d))]
                
                missing_subdirs = set(subdirs) - set(existing_subdirs)
                if missing_subdirs:
                    suggestions.append(f"建议在 {parent_dir}/ 中创建: {', '.join(missing_subdirs)}")
        
        # 检查文件命名规范
        self._check_file_naming(project_path, warnings, suggestions)
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, suggestions)
    
    def _check_file_naming(self, project_path: str, warnings: List[str], suggestions: List[str]):
        """检查文件命名规范"""
        naming_issues = []
        
        for root, dirs, files in os.walk(project_path):
            # 跳过.git等隐藏目录
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.endswith('.gd'):
                    # 检查GDScript文件命名 (应该是PascalCase)
                    if not self._is_pascal_case(file.replace('.gd', '')):
                        naming_issues.append(f"脚本文件命名建议使用PascalCase: {file}")
                
                elif file.endswith('.tscn'):
                    # 检查场景文件命名 (应该是PascalCase)
                    if not self._is_pascal_case(file.replace('.tscn', '')):
                        naming_issues.append(f"场景文件命名建议使用PascalCase: {file}")
                
                elif file.endswith('.gdshader'):
                    # 着色器文件命名
                    if not self._is_snake_case(file.replace('.gdshader', '')):
                        naming_issues.append(f"着色器文件命名建议使用snake_case: {file}")
        
        if naming_issues:
            suggestions.extend(naming_issues[:5])  # 限制建议数量
            if len(naming_issues) > 5:
                suggestions.append(f"还有 {len(naming_issues) - 5} 个命名规范问题")
    
    def _is_pascal_case(self, name: str) -> bool:
        """检查是否为PascalCase"""
        return re.match(r'^[A-Z][a-zA-Z0-9]*$', name) is not None
    
    def _is_snake_case(self, name: str) -> bool:
        """检查是否为snake_case"""
        return re.match(r'^[a-z][a-z0-9_]*$', name) is not None

def generate_architecture_report(project_path: str, output_path: str = "architecture_report.md"):
    """生成架构分析报告"""
    
    # 初始化验证器
    arch_validator = GodotArchitectureValidator()
    struct_validator = GodotProjectStructureValidator()
    
    # 查找架构文档
    doc_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.md') and ('architecture' in file.lower() or '架构' in file):
                doc_files.append(os.path.join(root, file))
    
    report_lines = [
        "# Godot游戏架构分析报告",
        f"生成时间: {os.popen('date').read().strip()}",
        f"项目路径: {project_path}",
        "",
        "## 📋 执行摘要",
        ""
    ]
    
    # 分析文档
    if doc_files:
        report_lines.append(f"✅ 找到 {len(doc_files)} 个架构文档")
        
        for doc_file in doc_files:
            report_lines.append(f"\n### 分析文档: {os.path.basename(doc_file)}")
            result = arch_validator.validate_document(doc_file)
            
            if result.is_valid:
                report_lines.append("✅ 文档验证通过")
            else:
                report_lines.append("❌ 文档验证失败")
            
            if result.errors:
                report_lines.append("\n**错误:**")
                for error in result.errors:
                    report_lines.append(f"- ❌ {error}")
            
            if result.warnings:
                report_lines.append("\n**警告:**")
                for warning in result.warnings:
                    report_lines.append(f"- ⚠️ {warning}")
            
            if result.suggestions:
                report_lines.append("\n**建议:**")
                for suggestion in result.suggestions:
                    report_lines.append(f"- 💡 {suggestion}")
    else:
        report_lines.append("❌ 未找到架构文档")
        report_lines.append("💡 建议创建架构设计文档")
    
    # 分析项目结构
    report_lines.append("\n## 🏗️ 项目结构分析")
    struct_result = struct_validator.validate_project_structure(project_path)
    
    if struct_result.is_valid:
        report_lines.append("✅ 项目结构基本符合规范")
    else:
        report_lines.append("❌ 项目结构存在问题")
    
    if struct_result.errors:
        report_lines.append("\n**结构错误:**")
        for error in struct_result.errors:
            report_lines.append(f"- ❌ {error}")
    
    if struct_result.warnings:
        report_lines.append("\n**结构警告:**")
        for warning in struct_result.warnings:
            report_lines.append(f"- ⚠️ {warning}")
    
    if struct_result.suggestions:
        report_lines.append("\n**结构建议:**")
        for suggestion in struct_result.suggestions:
            report_lines.append(f"- 💡 {suggestion}")
    
    # 添加改进建议
    report_lines.extend([
        "\n## 🚀 改进建议",
        "",
        "### 立即行动项",
        "1. 如果缺少架构文档，请立即创建",
        "2. 修复文档验证中的错误项",
        "3. 完善项目目录结构",
        "",
        "### 短期目标 (1-2周)",
        "1. 添加更多Mermaid图表来可视化架构",
        "2. 完善组件职责表格",
        "3. 建立命名规范文档",
        "",
        "### 长期目标 (1-2月)",
        "1. 建立自动化验证流程",
        "2. 添加性能测试基准",
        "3. 完善测试覆盖率",
        ""
    ])
    
    # 写入报告
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✅ 架构分析报告已生成: {output_path}")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python architecture_validator.py <项目路径> [输出路径]")
        return
    
    project_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "architecture_report.md"
    
    generate_architecture_report(project_path, output_path)

if __name__ == "__main__":
    main()