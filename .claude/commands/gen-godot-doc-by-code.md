---
name: gen-godot-doc-by-code
description: 根据Godot代码反推生成Godot游戏设计文档
argument-hint: "[设计文档主题]"
---

1. 检查用户是否提供参数，如果没有提供，请求用户提供参数
2. 如果用户提供了参数，继续执行
3. @godot-architect 读取项目代码信息 CLAUDE.md，掌握项目基本信息
4. @godot-architect 读取必须的代码，根据主题 $ARGUMENTS 进行分析
5. @design-doc-writer 接收`步骤4`的分析结果，根据 $ARGUMENTS 生成主题或对应的子主题名称，按照`文档输出路径`的要求创建文档所在的目录和文件
6. @design-doc-writer 根据`步骤4`的分析结果，输出设计文档


## 文档输出路径
- /docs/{two-digit-number}_{topic}/{two-digit-number}_{subtopic}.md
- 文档所在的目录和文件名称请使用中文
