# Godot Code Explainer 技能

## 技能概述

这是一个专门为 Godot 游戏引擎设计的代码解释分析技能。当用户在 Godot 项目中输入"解释代码"、"explain code"等指令时，该技能会自动触发，提供对 GDScript 和 C# 游戏代码的专业分析。

## 功能特性

### 🔍 智能代码分析
- **Godot 概念识别**: 自动识别 Godot 特定的节点、信号、生命周期方法
- **项目上下文**: 理解 Godot 项目结构和场景关系
- **游戏设计意图**: 分析代码背后的游戏设计思路

### 📊 多维度解释
- **文本说明**: 清晰的代码功能描述
- **表格展示**: 结构化的变量和函数信息
- **ASCII 图表**: 场景树和信号流程可视化
- **性能分析**: 识别性能瓶颈和优化建议

### 🎮 Godot 专业化
- **节点系统**: 深度理解 Godot 节点层次和继承
- **信号机制**: 分析信号连接和事件处理
- **物理引擎**: CharacterBody、RigidBody、Area 等
- **资源管理**: preload、load、资源生命周期
- **动画系统**: AnimationPlayer、Tween 等

## 触发条件

该技能会在以下情况下自动触发：

1. **环境检测**: 当前目录是有效的 Godot 项目（包含 `project.godot` 文件）
2. **用户输入**: 以下任一指令
   - "解释代码"
   - "explain code"  
   - "代码分析"
   - "代码解读"
   - "这段代码是做什么的"
   - "这个脚本怎么工作的"

## 使用示例

### 基础代码解释
```
用户: 解释代码 scripts/Player.gd
```

**输出示例**:
```
## 游戏机制概述
这是一个 2D 平台跳跃游戏的玩家控制脚本，处理玩家移动、跳跃、攻击和生命值管理。

## 节点与场景分析
- **继承类型**: CharacterBody2D (物理角色体)
- **职责**: 玩家角色控制、状态管理、输入处理
- **场景位置**: 通常是主场景的根节点

## 核心实现逻辑
- **物理更新**: _physics_process(delta) 处理重力和移动
- **输入处理**: handle_input() 捕获玩家输入
- **状态机**: State 枚举管理玩家状态 (IDLE, WALKING, JUMPING, ATTACKING, HURT)
- **信号系统**: health_changed, player_died, coin_collected

## 设计意图分析
采用状态机模式管理玩家行为，提供流畅的游戏体验。通过信号系统解耦模块，便于 UI 更新和音效处理。

## 性能提示
- [警告] 在 _process() 中调用 get_node() 可能影响性能，建议使用 @onready 缓存节点引用
- [信息] 使用了 4 个 onready 变量，是良好的性能优化实践
```

### 场景分析
```
用户: 解释代码 scenes/Main.tscn
```

**输出示例**:
```
## 场景结构分析
```
Main Scene (Main.tscn)
├── World (Node2D)
│   ├── Player (CharacterBody2D) ← Player.gd
│   │   ├── Sprite2D
│   │   ├── CollisionShape2D
│   │   ├── AttackArea (Area2D)
│   │   ├── Camera2D
│   │   └── AudioStreamPlayer
│   ├── Enemies (Node2D)
│   └── Environment (TileMap)
├── UI (CanvasLayer)
│   ├── HealthBar (ProgressBar)
│   └── CoinLabel (Label)
└── GameManager (Node) ← GameManager.gd
```

## 工具集成

### MCP 服务器工具
- **mcp__godot**: 项目信息获取、场景管理
- **mcp__sequential-thinking**: 逐步逻辑推理
- **mcp__memory**: 存储设计模式和最佳实践

### 专业 Agents
- **godot-code-reviewer**: Godot 专业代码审查
- **godot-architect**: 游戏架构分析
- **godot-game-developer**: 游戏开发建议

## 分析模板

### 节点脚本分析模板
- 节点基本信息和职责
- 游戏行为分析
- Godot 特性使用
- 性能分析
- 游戏设计意图
- 常见模式识别
- 调试和测试
- 扩展建议

### 场景分析模板
- 场景基本信息
- 节点层次结构
- 脚本分布和职责
- 资源依赖关系
- 信号连接分析
- 性能影响分析

## 性能优化指导

### 自动检测
- **对象创建**: _process() 中的临时对象创建
- **节点查找**: 重复的 get_node() 调用
- **资源加载**: 动态资源加载的性能影响
- **内存泄漏**: 未正确释放的资源引用

### 优化建议
- 使用 @onready 缓存节点引用
- 对象池化频繁创建销毁的对象
- 视口剔除大型场景中的非可见对象
- 批量渲染减少 Draw Call

## 支持的 Godot 版本

- **Godot 4.x**: 完整支持
- **Godot 3.x**: 基础支持（API 差异会特别说明）

## 技能结构

```
godot-code-explainer/
├── SKILL.md                    # 技能核心配置和指令
├── scripts/
│   └── godot_code_analyzer.py  # Python 分析脚本
├── references/
│   ├── node-script-template.md # 节点脚本分析模板
│   ├── scene-analysis-template.md # 场景分析模板
│   ├── godot-api-reference.md  # Godot API 参考手册
│   └── performance-patterns.md # 性能优化模式
├── assets/
│   └── test_player.gd          # 测试用例
└── README.md                   # 使用说明
```

## 测试技能

### 分析脚本测试
```bash
cd .claude/skills/godot-code-explainer
python scripts/godot_code_analyzer_fixed.py --file assets/test_player.gd
```

### 项目分析测试
```bash
python scripts/godot_code_analyzer_fixed.py --file scripts/player.gd --godot-project /path/to/godot/project --performance-analysis
```

## 扩展开发

### 添加新的分析功能
1. 在 `scripts/godot_code_analyzer.py` 中添加新的分析方法
2. 在 `references/` 中添加新的参考文档
3. 更新 `SKILL.md` 中的使用说明

### 支持新的 Godot 特性
1. 更新 `godot_builtin_types` 和 `godot_lifecycle_methods`
2. 添加新的特性检测逻辑
3. 创建专门的分析模板

## 贡献指南

欢迎提交改进建议和 bug 报告：

1. **分析准确性**: 改进代码分析的准确性
2. **模板完善**: 完善分析模板和示例
3. **性能优化**: 改进分析脚本的性能
4. **文档更新**: 更新 Godot API 参考和最佳实践

## 许可证

本技能遵循开源许可证，可自由使用和修改。