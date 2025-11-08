---
name: design-feature
description: 根据feature进行设计
argument-hint: "[feature]"
---

1. 检查用户是否提供参数，如果没有提供，请求用户提供参数
2. 如果用户提供了参数，继续执行
3. @godot-architect 读取项目代码信息 CLAUDE.md，掌握项目基本信息
4. @godot-architect 读取必须的代码，根据主题 $ARGUMENTS 进行分析
5. @godot-architect 根据上面的分析，输出2个备选方案，并请求用户选择最终方案
6. @design-doc-writer 按照用户选择的最终方案输出特性设计文档

## 文档输出路径
- /docs/02_特性设计/{two-digit-number}_{feature}.md
- 文档所在的目录和文件名称请使用中文

## 约束
- 仅需要输出特性设计文档，不需要输出代码
