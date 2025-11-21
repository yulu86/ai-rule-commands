---
name: project-analyzer
description: 通用项目逆向分析专家，专门通过分析现有项目代码来推导系统设计意图和架构，并生成完整的设计文档。当用户输入"分析项目"、"逆向分析"等关键词且当前目录包含非Godot项目文件时触发。适用于项目交接、文档补全、代码重构、学习研究等场景，能够深度分析项目结构、代码组织、依赖管理，并输出标准化的系统设计文档和技术架构文档。
---

# 项目逆向分析技能

## 技能概述

本技能专门用于通过分析现有项目代码来反推系统设计，生成完整的设计文档。支持多种编程语言和技术栈的分析。

## 触发条件

- 用户输入"分析项目"、"逆向分析"、"代码反推设计"等关键词
- 当前目录包含项目文件但非Godot项目（避免与godot-project-analyzer冲突）

## 分析流程

### 1. 项目类型检测
使用 `scripts/detect_project_type.py` 自动识别项目类型和技术栈

### 2. 结构分析
使用 `scripts/analyze_structure.py` 分析项目目录结构和文件组织

### 3. 代码模式识别
使用 `scripts/extract_design_patterns.py` 识别设计模式和架构模式

### 4. 文档生成
使用 `scripts/generate_design_doc.py` 生成标准化设计文档

## 资源使用指南

### Scripts
- **项目检测**: `detect_project_type.py` - 识别技术栈和框架
- **结构分析**: `analyze_structure.py` - 分析目录结构
- **模式提取**: `extract_design_patterns.py` - 提取设计模式
- **文档生成**: `generate_design_doc.py` - 生成最终文档

### References
- **设计模式**: `design_patterns.md` - 常见设计模式参考
- **架构模式**: `architecture_patterns.md` - 架构模式识别指南
- **项目指标**: `project_indicators.md` - 各技术栈识别指标
- **文档模板**: `template_document.md` - 文档结构和内容指南

### Assets
- **设计文档模板**: `design_doc_template.md` - 标准设计文档模板
- **分析报告模板**: `analysis_report_template.md` - 分析报告格式

## 使用方法

1. **自动触发**: 在项目目录下输入"分析项目"或"逆向分析"
2. **智能分析**: 技能会自动检测项目类型并选择合适的分析策略
3. **文档输出**: 在docs目录下生成标准化设计文档

## 输出文档结构

生成的文档将按照用户的文档规范进行组织：
- 文档路径: `docs/{目录序号}_{主题}/`
- 文档命名: `{序号}_{中文文档名称}.md`

## 支持的项目类型

- Web应用 (前端/后端/全栈)
- 移动应用 (React Native, Flutter)
- 桌面应用 (Electron, Qt)
- 微服务架构
- 数据分析项目
- API服务
- 库和框架

## MCP集成

技能会结合已配置的MCP server tools：
- filesystem工具用于文件系统操作
- sequential-thinking工具用于复杂分析推理
- 记忆工具用于存储分析结果和模式

## 注意事项

- 确保在项目根目录下使用
- 大型项目可能需要较长分析时间
- 生成的文档需要人工review和调整
- 敏感代码内容会被自动过滤