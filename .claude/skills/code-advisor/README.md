# Code Advisor 技能

## 概述

Code Advisor 是一个智能代码助手技能，专门处理代码编写、实现、检视和解释任务。该技能使用 Multi-Model Advisor 工具调用 qwen3-coder:30b 模型，有效减少 token 消耗。

## 触发关键词

当用户输入以下任一关键词时，此技能会自动触发：

- "实现代码"
- "编写代码"
- "输出代码"
- "检视代码"
- "解释代码"

## 核心功能

### 1. 代码生成
- 根据需求生成高质量代码
- 支持多种编程语言
- 遵循最佳实践和编码规范

### 2. 代码审查
- 分析代码质量和结构
- 识别性能问题和安全漏洞
- 提供具体的改进建议

### 3. 代码解释
- 解释复杂代码的功能和逻辑
- 分析设计模式和架构思路
- 提供学习价值指导

## 使用示例

```
用户: 实现代码 - 写一个Python函数来计算斐波那契数列
系统: [自动调用Code Advisor技能，使用qwen3-coder:30b生成代码]

用户: 检视代码 - 请审查这段JavaScript代码的性能
系统: [自动调用Code Advisor技能，进行专业代码审查]

用户: 解释代码 - 这段React组件是如何工作的？
系统: [自动调用Code Advisor技能，详细解释代码逻辑]
```

## 技术特点

### Token优化
- 精准提问，避免模糊描述
- 分步处理复杂任务
- 控制上下文长度
- 输出简洁高效

### 多模型集成
- 优先使用 qwen3-coder:30b 模型
- 集成 context7 工具获取最新文档
- 支持多种编程语言和框架

## 目录结构

```
code-advisor/
├── SKILL.md              # 技能主文件
├── README.md             # 使用说明
├── package.json          # 技能配置
├── scripts/              # 辅助脚本
│   └── code_helper.py   # 代码助手工具
└── references/           # 参考资料
    └── patterns.md       # 代码模式和最佳实践
```

## 安装和使用

1. 将技能文件放置在 `.claude/skills/` 目录下
2. Claude Code 会自动识别并加载该技能
3. 使用触发关键词即可激活技能

## 依赖工具

- `mcp__multi-model-advisor__query-models`: 多模型查询
- `mcp__context7__resolve-library-id`: 库文档解析
- `mcp__context7__get-library-docs`: 获取库文档