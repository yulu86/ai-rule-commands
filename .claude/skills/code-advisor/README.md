# Code Advisor 技能 - 智能代码助手

## 概述

Code Advisor 是一个智能代码助手技能，专门处理代码编写、实现、检视和解释任务。该技能已经过优化，能够智能检测 Godot 项目并提供针对性的 Godot 4.5+ 特性优化。

## 主要特性

### 🧠 智能项目检测
- **自动项目类型识别**：检测当前项目是否为 Godot 项目
- **多语言支持**：支持 Python、JavaScript、Java、C++、C#、Go、Rust、TypeScript 等主流编程语言
- **框架识别**：识别 React、Vue、Django、Flask、Express 等流行框架

### 🎮 Godot 项目专门优化
- **Godot 4.5+ 特性**：充分利用最新的 Godot 功能和最佳实践
- **GDScript 专业支持**：提供针对 GDScript 的专业代码建议
- **游戏开发模式**：从游戏开发角度进行代码审查和优化
- **MCP 工具集成**：智能建议使用 Godot MCP server 工具

### 🚀 多模型智能咨询
- **专用模型**：使用 `qwen3-coder:30b` 模型进行代码生成和审查
- **上下文优化**：根据项目类型和任务动态调整系统提示词
- **Token 效率**：优化查询以减少不必要的 token 消耗

## 触发条件

当用户输入以下任一关键词时触发此技能：
- "实现代码"
- "编写代码" 
- "输出代码"
- "检视代码"
- "解释代码"

## 工作流程

### 1. 项目类型检测
自动检测项目类型：
- **Godot 项目**：存在 `project.godot` 文件或 `.gd`、`.tscn`、`.tres` 文件
- **通用项目**：其他所有类型的软件开发项目

### 2. 任务类型识别
- **实现任务**：代码生成、功能实现
- **检视任务**：代码审查、性能分析
- **解释任务**：代码说明、概念解释

### 3. 智能系统提示词生成
根据项目类型和任务类型生成专门的系统提示词：
- **通用项目**：使用对应编程语言的专业提示词
- **Godot 项目**：使用 Godot 4.5+ 专门的提示词，关注游戏开发最佳实践

### 4. 工具建议（仅 Godot 项目）
根据用户需求智能建议 Godot MCP server 工具：
- 场景创建：`mcp__godot__create_scene`
- 节点操作：`mcp__godot__add_node`
- 资源加载：`mcp__godot__load_sprite`
- 项目信息：`mcp__godot__get_project_info`
- 项目运行：`mcp__godot__run_project`

## 使用示例

### 通用项目示例
```bash
用户: "实现代码 - 写一个Python函数来排序数组"
AI: 生成高质量的 Python 排序代码，包含错误处理和最佳实践
```

### Godot 项目示例
```bash
用户: "实现代码 - 创建一个玩家控制器脚本，支持8方向移动和动画"
AI: 生成符合 Godot 4.5+ 最佳实践的 GDScript 代码，包含：
- 使用 @onready 优化性能
- 正确的信号处理
- 高效的动画状态管理
- 移动和摩擦力物理处理
```

## 技术实现

### 文件结构
```
code-advisor/
├── skill.md              # 技能配置和文档
├── scripts/
│   └── code_helper.py    # 核心实现逻辑
├── assets/              # 资源文件
├── references/          # 参考资料
└── package.json         # 技能元数据
```

### 核心算法
1. **正则表达式模式匹配**：用于检测任务类型、编程语言、框架
2. **文件系统扫描**：检测 Godot 项目特征文件
3. **动态提示词生成**：根据上下文生成最优的系统提示词
4. **MCP 工具映射**：根据用户需求映射到相应的 Godot 工具

### 性能优化
- **缓存机制**：避免重复的文件系统扫描
- **精准匹配**：使用高效的正则表达式进行模式匹配
- **Token 优化**：精简系统提示词，减少不必要的 token 消耗

## 扩展性

### 添加新的编程语言支持
在 `code_helper.py` 的 `_detect_language` 方法中添加新的语言模式：

```python
languages = {
    # 现有语言...
    'new_language': r'\bnewlanguage|nl\b'
}
```

### 添加新的框架支持
在 `_detect_framework` 方法中添加新的框架模式：

```python
frameworks = {
    # 现有框架...
    'new_framework': r'\bnewframework\b'
}
```

### 添加新的 MCP 工具建议
在 `get_godot_tools_suggestions` 方法中添加新的工具映射：

```python
if any(keyword in input_lower for keyword in ['新关键词', 'new_keyword']):
    suggestions.append('mcp__tool_name - 工具描述')
```

## 版本历史

### v2.0.0 (当前版本)
- ✅ 添加 Godot 项目智能检测
- ✅ 集成 Godot 4.5+ 最佳实践
- ✅ 实现 MCP 工具智能建议
- ✅ 优化项目类型识别算法
- ✅ 增强系统提示词生成逻辑

### v1.0.0
- ✅ 基础代码生成功能
- ✅ 多语言支持
- ✅ 任务类型识别
- ✅ Multi-model advisor 集成

## 许可证

MIT License - 详见项目根目录的 LICENSE 文件

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进此技能。请确保：

1. 遵循现有的代码风格
2. 添加适当的测试用例
3. 更新相关文档
4. 确保向后兼容性