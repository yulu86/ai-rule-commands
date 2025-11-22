---
name: godot-code-explainer
description: Godot游戏引擎专用代码解释分析技能，当用户在Godot项目中输入"解释代码"、"explain code"时触发，专门分析GDScript、C#游戏代码的功能、实现逻辑和游戏设计意图。使用文本、表格和ASCII图等多种形式，结合MCP工具和Godot专业知识进行游戏代码理解和可视化展示。
---

# Godot 代码解释分析技能

## 技能概述

专门为 Godot 游戏引擎设计的智能代码分析技能，深度分析 GDScript 和 C# 游戏代码的功能、实现逻辑和游戏设计意图。理解 Godot 的节点系统、信号机制、场景管理等核心概念，为游戏开发人员提供专业、准确的代码理解服务。

## 触发条件

当用户在 Godot 项目中输入以下任一指令时触发技能：
- "解释代码"
- "explain code"
- "代码分析"
- "代码解读"
- "这段代码是做什么的"
- "这个脚本怎么工作的"

## Godot 环境检测

### 项目识别
自动检测当前是否为 Godot 项目：
- 检查是否存在 `project.godot` 文件
- 检查是否有 `.gd`、`.cs`、`.tscn`、`.tres` 等 Godot 文件
- 验证项目结构和 Godot 特定目录

### 语言支持
- **GDScript**：Godot 的主要脚本语言
- **C#**：用于 Godot 的 .NET 支持
- **场景文件**：`.tscn` 场景结构分析
- **资源文件**：`.tres` 资源配置分析

## 执行流程

使用agent`godot-code-reviewer`执行：

### 1. 代码获取与上下文分析
使用 MCP Godot 工具获取目标代码和项目信息：

**项目信息获取**：
- 调用 `mcp__godot__get_project_info` 获取项目基本信息
- 识别项目结构、场景组织、脚本分布

**代码文件读取**：
- 支持文件路径指定（如："解释 scripts/Player.gd"）
- 支持场景相关的脚本分析
- 支持附加脚本（attached scripts）的自动识别

### 2. Godot 专用代码分析
使用 `scripts/godot_code_analyzer.py` 进行 Godot 特定的深度分析：

**Godot 概念识别**：
- 节点类型和继承关系（Node、Node2D、Node3D、Control等）
- 信号连接和回调函数
- 场景树结构和父子关系
- 资源加载和管理
- 输入处理和事件系统
- 物理引擎集成
- 动画系统使用

**游戏逻辑分析**：
- 游戏状态管理
- 玩家控制逻辑
- AI 行为模式
- 碰撞检测和响应
- UI 交互逻辑
- 关卡和进度管理

### 3. 多维度游戏代码解释

#### 3.1 功能概述
- **游戏机制**：代码在游戏中的作用和玩法影响
- **节点职责**：在场景树中的角色和责任
- **交互设计**：与玩家和其他游戏元素的交互方式
- **性能考虑**：对游戏性能的影响

#### 3.2 实现逻辑
- **Godot API 使用**：内置函数和属性的使用
- **信号流程**：信号的发送、连接和响应
- **场景管理**：场景切换、实例化、销毁等操作
- **生命周期**：`_ready()`, `_process()`, `_physics_process()` 等生命周期方法

#### 3.3 游戏设计意图
- **玩法实现**：如何支持特定的游戏玩法
- **架构设计**：代码结构对游戏可扩展性的影响
- **用户体验**：代码对玩家体验的贡献
- **开发维护**：代码的可维护性和团队协作考虑

#### 3.4 特殊处理说明
- **帧率依赖**：`_delta` 参数的使用和帧率独立性
- **性能优化**：批量处理、对象池、延迟加载等优化技术
- **平台适配**：不同平台的特殊处理
- **调试辅助**：调试信息的输出和测试支持

### 4. 可视化展示

#### 4.1 文本说明
```markdown
## 游戏机制概述
[代码在游戏中的作用和玩法影响]

## 节点与场景分析
[在场景树中的位置和职责]

## 核心实现逻辑
[Godot API 使用和游戏流程]

## 设计意图分析
[游戏设计思路和架构考虑]

## 性能与优化
[性能影响和优化建议]

## 注意事项
[Godot 特殊处理和最佳实践]
```

#### 4.2 表格展示（可选）

| 方法/函数 | 游戏作用 | Godot特性 | 性能影响 | 注意事项 |
|-----------|----------|-----------|----------|----------|
| _ready | 初始化玩家状态 | 节点生命周期 | 一次性 | 获取节点引用 |
| _process | 处理玩家输入 | 每帧调用 | 关键影响 | 需要优化 |
| _on_area_entered | 处理碰撞 | 信号回调 | 事件驱动 | 物理层设置 |

#### 4.3 场景树 ASCII 图（可选）
```
Main Scene (Main.tscn)
├── World (Node2D)
│   ├── Player (CharacterBody2D) ← 当前脚本
│   │   ├── Sprite2D
│   │   ├── CollisionShape2D
│   │   └── Camera2D
│   ├── Enemies (Node2D)
│   └── Environment (TileMap)
├── UI (CanvasLayer)
│   ├── HealthBar (ProgressBar)
│   └── ScoreLabel (Label)
└── Audio (AudioStreamPlayer)
```

#### 4.4 信号流程图（可选）
```
玩家移动输入
    ↓
_process(delta)
    ↓
velocity 计算和 apply_gravity()
    ↓
move_and_slide() ← 物理引擎
    ↓
碰撞检测
    ↓
发射信号信号（如有）
    ↓
_on_area_entered() → 处理碰撞逻辑
```

## 核心脚本使用

### 基本 Godot 代码分析
```bash
python scripts/godot_code_analyzer.py --file <文件路径> --godot-project <项目路径>
```

### 场景关联分析
```bash
python scripts/godot_code_analyzer.py --scene <场景文件> --analyze-attached-scripts
```

### 性能分析模式
```bash
python scripts/godot_code_analyzer.py --file <文件路径> --performance-analysis
```

### 脚本特性
- **Godot API 识别**：内置函数、属性、信号的智能识别
- **场景树分析**：理解节点关系和场景结构
- **性能检测**：识别潜在的性能瓶颈
- **模式识别**：Godot 最佳实践和设计模式
- **版本适配**：支持 Godot 3.x 和 4.x 的差异

## 分析模板参考

### 节点脚本分析模板
参考 [references/node-script-template.md](references/node-script-template.md)：

#### 节点基本信息
- 节点类型和继承链
- 在场景树中的位置
- 附加的资源组件

#### 游戏行为
- 游戏循环中的作用
- 与其他节点的交互
- 玩家输入处理

### 场景分析模板
参考 [references/scene-analysis-template.md](references/scene-analysis-template.md)：

#### 场景结构
- 节点层次关系
- 脚本分布和职责
- 资源依赖关系

#### 场景功能
- 场景的主要用途
- 状态管理和数据流
- 与其他场景的交互

## Godot 工具集成

### MCP Godot 服务器工具
- **mcp__godot__get_project_info**：获取项目基本信息
- **mcp__godot__get_project_info**：分析项目结构
- **mcp__godot__launch_editor**：启动编辑器进行可视化检查
- **mcp__godot__run_project**：运行项目进行动态分析

### 代码读取工具
- **Read**：读取 GDScript、C# 脚本文件
- **Glob**：批量查找 Godot 文件（`*.gd`, `*.cs`, `*.tscn`）
- **Grep**：搜索 Godot 特定的代码模式

### 专业分析工具
- **sequential-thinking**：逐步分析游戏逻辑流程
- **memory**：存储 Godot 设计模式和最佳实践
- **tavily-mcp**：查找 Godot 文档和教程资源

### Agents 协作
- **godot-code-reviewer**：进行 Godot 专业的代码审查
- **godot-architect**：分析游戏架构和场景设计
- **godot-game-developer**：提供游戏开发的专业建议
- **Explore**：快速理解大型 Godot 项目的组织结构

## Godot 特殊代码处理

### 生命周期方法
- **_ready()**：节点准备就绪时的初始化
- **_process(delta)**：每帧执行的逻辑
- **_physics_process(delta)**：物理相关的每帧处理
- **_input(event)**：输入事件处理
- **_enter_tree() / _exit_tree()**：场景树进入/退出

### 信号系统
- 自定义信号的定义和使用
- 内置信号的连接方式
- 信号参数传递和类型安全
- 信号的连接时机和断开

### 物理引擎集成
- CharacterBody2D/3D 的移动和碰撞
- Area2D/3D 的重叠检测
- RigidBody2D/3D 的物理模拟
- 物理层的设置和碰撞矩阵

### 资源管理
- `preload()` 和 `load()` 的使用区别
- 资源的引用计数和内存管理
- `@export` 变量的设计和使用
- 自定义资源的创建和使用

## 解释质量标准

### Godot 专业知识准确性
- ✅ 正确理解 Godot 的 API 和概念
- ✅ 准确分析场景树和节点关系
- ✅ 精确识别信号机制和事件流程
- ✅ 深入理解游戏开发模式

### 游戏设计洞察
- ✅ 分析代码对游戏玩法的影响
- ✅ 识别游戏状态管理策略
- ✅ 理解用户体验设计考虑
- ✅ 评估代码的可扩展性

### 实用开发指导
- ✅ 提供 Godot 最佳实践建议
- ✅ 指出性能优化机会
- ✅ 给出调试和测试建议
- ✅ 推荐代码重构方案

## 特殊游戏模式处理

### 平台跳跃游戏
- 角色控制器物理参数
- 平台碰撞检测和响应
- 相机跟随和视口管理

### RPG 游戏
- 角色属性和状态系统
- 战斗逻辑和伤害计算
- 物品系统和背包管理

### 策略游戏
- AI 决策和行为树
- 单位管理和路径规划
- 游戏状态同步和保存

## 错误处理

### Godot 环境问题
- Godot 项目文件损坏或缺失
- 脚本附加节点丢失
- 资源文件路径错误

### 代码解析错误
- GDScript 语法错误
- C# 编译问题
- API 版本兼容性

### 分析失败处理
- 复杂场景结构超出分析能力
- 缺少必要的游戏上下文
- 特定游戏领域的专业知识不足

## 技能限制

- 需要有效的 Godot 项目环境
- 依赖 Python 环境运行分析脚本
- 对于大型项目可能需要分层分析
- 某些游戏类型可能需要领域专业知识补充
- Godot 3.x 和 4.x 之间的 API 差异需要明确区分