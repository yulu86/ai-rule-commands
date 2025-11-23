---
name: <agent-name>
description: <agent功能和使用场景描述,用于自动触发agent>
*可选* argument-hint: [arg1] [arg2] [arg3]
*可选* tools: tool1, tool2, tool3
model: inherit
color: [Red|Blue|Green|Yellow|Purple|Orange|Pink|Cyan]
---

# 目标

*agent任务目标说明*

## 工作流

*包含step by step的工作流*
*每个步骤可以选择合适的Claude Code内置工具或MCP Server工具*

## 输出格式

*交付件的格式说明和样例*
*在终端中的返回信息的说明和样例，用来把工作结果知会到其他agent。可以指定交付件的位置，但是禁止返回完整的交付件信息*

## 规则

*必须遵守的规则*
*严禁违反的规则*
