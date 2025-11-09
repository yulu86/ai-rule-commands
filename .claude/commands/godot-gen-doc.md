---
name: godot-gen-doc
description: 根据主题或feature进行Godot设计并输出设计文档
argument-hint: "[topic|feature][概要|详细]"
---

1. 检查用户是否提供参数，如果没有提供，请求用户提供参数
2. 如果用户提供了参数，继续执行
3. @godot-architect 读取项目代码信息 CLAUDE.md，掌握项目基本信息
4. @godot-architect 读取必须的代码(如果存在代码)，根据主题 $1 进行分析
5. @godot-architect 根据上面的分析，输出2个备选方案
6. @godot-architect 各自用一句话简要描述备选方案，用选项的方式提供给用户，并请求用户选择最终方案
7. @design-doc-writer 按照用户选择的最终方案输出 $2 设计文档

## 文档输出路径
- /docs/02_特性设计/{two-digit-number}_{feature}.md
- 文档所在的目录和文件名称请使用中文

## 约束
- 如果 $2 是概要，输出概要设计文档，不需要输出详细的代码设计
- 如果 $2 是详细，输出详细设计文档，包含代码的设计，但不需要输出详细的代码
