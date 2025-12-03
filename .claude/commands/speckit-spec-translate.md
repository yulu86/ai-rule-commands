---
name: speckit-spec-translate
description: speckit spec文档翻译
argument-hint: [Feature SPEC目录]
---

## 执行流程
1. 检查用户是否提供`Feature SPEC目录`参数，如果未提供，提醒用户提供
2. 读取 spec/$1/ 目录下的文档
3. 逐个文档翻译成中文，并保存翻译后的文档

## 翻译要求
- 按照文档内容进行翻译，不需要添加其他内容
- 对于软件开发的英文术语或专有名词可不翻译，例如：`CharacterBody2D`、`Node2D`

## 文档保存
- 翻译后的文档名称：在原有文档名加上 `_zh`后缀，例如：01_feature_spec.md -> 01_feature_spec_zh.md
- 保存的目录：目录为 spec/$1/zh_cn/ ，例如: 原文档在 spec/01_players/ 目录，翻译后的文档保存到 spec/01_players/zh_cn/ 目录