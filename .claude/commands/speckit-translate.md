---
name: speckit-translate
description: speckit spec文档翻译
argument-hint: [Feature SPEC目录]
---

## 执行流程
1. 检查用户是否提供`Feature SPEC目录`参数，如果未提供，提醒用户提供
2. 读取 specs/$1/ 目录和子目录下的文档
3. 逐个文档翻译成中文，并保存翻译后的文档

## 翻译要求
- 按照文档内容进行翻译，不需要添加其他内容
- 对于软件开发的英文术语或专有名词可不翻译，例如：`CharacterBody2D`、`Node2D`

## 文档保存
- 翻译后的文档名称：与原文档名称保持一致，例如：01_feature_spec.md -> 01_feature_spec.md
- 保存的目录：目录为 specs_zh/$1/ ，相对路径与原文档保持一致，例如: 
  specs/01_players/01_feature_spec.md -> specs_zh/01_players/01_feature_spec.md 
  specs/01_players/checklist/01_abc.md -> specs_zh/01_players/checklist/01_abc.md