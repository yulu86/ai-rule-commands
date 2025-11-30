---
name: tool-filler
description: 填充MCP工具和SKILL到settings.local.json文件中
---

MCP工具和SKILL权限放开工具

自动填充MCP工具和SKILL到settings.local.json文件中

## 执行流程

1. 获取当前环境中可使用的MCP Server tools
2. 获取当前环境中可使用的Claude Code SKILL
3. 如果 .claude/settings.local.json 不存在，则按照`模版`创建
4. 把MCP Server tools和Claude Code SKILL添加到 .claude/settings.local.json 文件中，参考`填充MCP Server tool和SKILL示例`

## MCP Server tools名称构建
- 规则：
  
## 模版
```json
{
  "permissions": {
    "allow": [],
    "deny": [],
    "ask": []
  }
}
```

## MCP Server tool和SKILL命名规则
- MCP Server tool命名规则：`mcp__{mcp server名称}__{工具名称}`，例如: `filesystem` MCP Server的`directory_tree`工具，名称为`mcp__filesystem__directory_tree`
- SKILL命名规则：`Skill({技能名称})`，例如：技能`excalidraw-creator`，名称为`Skill(excalidraw-creator)`

## 填充MCP Server tool和SKILL示例
填充后的示例如下：
```json
{
  "permissions": {
    "allow": [
      "mcp__filesystem__directory_tree",
      "mcp__memory__create_entities",
      "mcp__memory__create_relations",
      "Skill(excalidraw-creator)",
      "mcp__excalidraw__create_element",
      "mcp__excalidraw__get_resource"
    ],
    "deny": [],
    "ask": []
  }
}
```