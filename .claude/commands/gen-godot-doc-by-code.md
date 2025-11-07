---
name: gen-godot-doc-by-code
description: 根据Godot代码反推生成Godot游戏设计文档
argument-hint: "[设计文档主题]"
steps:
  - agent: godot-architect
  - agent: design-doc-writer
---

1. @godot-architect 读取项目代码信息 CLAUDE.md，掌握项目基本信息
2. @godot-architect 读取必须的代码，根据主题 $ARGUMENTS 进行分析
3. @design-doc-writer 接收上一步的分析结果，根据主题 $ARGUMENTS 输出设计文档文件
