---
name: quick-commit
description: 快速智能分析项目代码变更，自动生成符合规范的commit消息并执行提交。
argument-hint: [简单描述]
---

# 参数说明

- **简单描述** (可选): 提供commit提示，包含：
  - **快速类型**: f/feat(新功能)、x/fix(修复bug)、d/docs(文档)、r/refactor(重构)等
  - **功能描述**: 如"登录"、"动画"、"崩溃"、"性能"等关键词
  - **自定义**: 任何描述变更性质的关键词

# 执行步骤

**当前提交目标**: $ARGUMENTS

## 快速分析阶段
工具：Bash + sequential-thinking

1. Git状态快速检查
2. 变更内容快速扫描
3. 意图快速推断

## 消息生成阶段
工具：sequential-thinking

1. 类型自动确定
2. 标题快速生成
3. 描述优化

## 输出执行阶段
工具：Bash

1. 命令生成和执行

# 工具使用

## Bash 工具
- `git status`: 查看工作区状态
- `git diff --name-only`: 获取变更文件列表
- `git add .`: 暂存所有变更
- `git commit`: 提交变更

## 消息格式
```git
<type>: <subject>

# 示例
feat: 添加用户登录功能
fix: 修复按钮点击无响应问题
refactor: 重构用户管理模块
docs: 更新API文档
```

# 约束条件

## 分析约束
- **深度限制**: 快速分析可能遗漏某些细节
- **上下文**: 无法深入理解复杂的业务逻辑
- **消息简洁**: 为保证简洁，可能省略某些细节

## 使用约束
- **变更复杂度**: 适合简单到中等复杂度的变更
- **团队规范**: 可能与特定团队的详细规范存在差异
- **历史一致性**: 与历史commit的一致性需要人工确认

# 禁止内容

- **禁止出现**: 🤖 Generated with Claude Code (https://claude.com/claude-code)
- **禁止出现**: Co-Authored-By: Claude <noreply@anthropic.com>

# 使用场景

## 适用场景
- **日常开发**: 日常功能开发、bug修复、文档更新
- **团队协作**: 统一commit格式、提高协作效率
- **版本管理**: 快速记录代码变更、维护版本历史

## 不适用场景
- **复杂重构**: 大型架构重构需要详细的commit说明
- **发布准备**: 重要版本发布需要规范的release notes
- **法律合规**: 需要法律审查的变更内容