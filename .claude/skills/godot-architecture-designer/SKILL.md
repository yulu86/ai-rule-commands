---
name: godot-architecture-designer
description: 专业的Godot 2D游戏架构设计技能，提供系统化的游戏架构规划、场景结构设计、节点组织模式、信号通信架构、资源管理策略和状态机设计。遵循Godot最佳实践，输出包含文字说明、架构表格和Mermaid图表的综合架构设计文档。当用户需要设计Godot 2D游戏的整体架构、规划项目结构、设计系统间通信方式或制定技术规范时使用此技能。
---

# Godot 2D游戏架构设计

## 快速开始

### 架构设计流程

1. **需求分析** - 明确游戏类型、核心玩法和技术需求
2. **系统划分** - 识别核心系统（输入、渲染、物理、音频、UI等）
3. **架构模式选择** - 选择合适的架构模式
4. **场景层次设计** - 规划场景树结构
5. **通信机制设计** - 设计信号和数据流
6. **资源管理策略** - 规划资源加载和生命周期
7. **状态管理设计** - 设计游戏状态机

### 输出格式要求

架构设计文档必须包含：
- **文字说明** - 详细的设计思路和技术选型理由
- **架构表格** - 系统组件、职责、依赖关系
- **Mermaid图表** - 架构图、数据流图、状态图

## 架构模式

### 单例模式 (Singleton)

适用于全局管理器：
```gdscript
# GameManager.gd
extends Node

signal game_state_changed(new_state)

@export var current_level: int = 1
@export var player_score: int = 0

func _ready():
    process_mode = Node.PROCESS_MODE_ALWAYS

func change_level(level_id: int):
    current_level = level_id
    game_state_changed.emit(current_level)
```

### 组件模式 (Component Entity)

适用于复杂的游戏对象：
```gdscript
# Player.gd - 主控节点
extends CharacterBody2D

@onready var health_component = $HealthComponent
@onready var movement_component = $MovementComponent  
@onready var combat_component = $CombatComponent

func _ready():
    health_component.health_depleted.connect(_on_health_depleted)
```

### 观察者模式 (Observer)

使用信号系统实现松耦合通信。

### 状态机模式 (State Machine)

管理复杂的状态转换逻辑。

## 核心系统架构

### 1. 输入系统 (Input System)

```gdscript
# InputManager.gd - 单例管理器
extends Node

signal input_action_activated(action: String, strength: float)
signal input_action_deactivated(action: String)

func _input(event):
    # 处理输入事件
    pass
```

### 2. 场景管理系统 (Scene Management)

```gdscript
# SceneManager.gd - 场景切换管理
extends Node

signal scene_loading_started(scene_name: String)
signal scene_loading_finished(scene_name: String)

func load_scene(scene_path: String):
    # 场景加载逻辑
    pass
```

### 3. 音频系统 (Audio System)

### 4. UI系统 (UI System)

### 5. 资源管理系统 (Resource Management)

## 通信架构

### 信号连接模式

- **单向通信**: 使用简单的信号连接
- **双向通信**: 需要回执的信号通信
- **多播通信**: 一个发射者，多个接收者
- **中介者模式**: 通过中央管理器协调

### 数据流设计

```
Input → GameManager → Systems → Rendering
                ↓
            StateManager
```

## 项目结构规范

### 目录结构

```
project/
├── scenes/           # 场景文件
│   ├── ui/
│   ├── levels/
│   └── entities/
├── scripts/          # 脚本文件
│   ├── managers/     # 管理器脚本
│   ├── components/   # 组件脚本
│   ├── entities/     # 实体脚本
│   └── ui/          # UI脚本
├── assets/          # 资源文件
│   ├── textures/
│   ├── sounds/
│   └── fonts/
└── resources/       # 资源文件
```

### 命名规范

- **场景**: PascalCase (Player.tscn, MainMenu.tscn)
- **脚本**: PascalCase (Player.gd, GameManager.gd)
- **变量**: snake_case (player_health, max_speed)
- **常量**: UPPER_CASE (MAX_HEALTH, GRAVITY)
- **信号**: snake_case (health_changed, level_completed)
- **函数**: snake_case (take_damage, initialize_player)

## 设计模式和最佳实践

### 节点组织原则

1. **单一职责** - 每个节点只负责一个功能
2. **层次清晰** - 父子关系明确，避免过深的嵌套
3. **解耦合** - 使用信号而不是直接引用
4. **可重用性** - 设计可复用的组件

### 性能优化

1. **对象池** - 重用频繁创建销毁的对象
2. **批处理** - 合并相似的渲染调用
3. **LOD系统** - 距离相关的细节层次
4. **异步加载** - 避免主线程阻塞

### 内存管理

1. **资源引用** - 明确资源的生命周期
2. **弱引用** - 避免循环引用
3. **及时释放** - 不再使用时调用queue_free()

## 高级架构

### 网络游戏架构

```
Client → NetworkManager → Server
        ↑               ↓
  GameState ← SyncData
```

### 模组化架构

- 插件系统
- 热重载
- 配置驱动

## 设计文档模板

### 架构设计检查清单

- [ ] 系统边界清晰
- [ ] 接口设计合理
- [ ] 依赖关系明确
- [ ] 错误处理完善
- [ ] 性能考虑充分
- [ ] 可扩展性良好
- [ ] 可测试性高

### 技术选型记录

记录重要技术决策的理由和考虑因素。

## 常见问题解决

### 循环依赖

使用信号或中介者模式解决。

### 状态同步

使用权威状态机或快照同步。

### 性能瓶颈

使用Godot性能分析工具识别和优化。

## 参考资料

详细的设计模式和实现示例请参考：

- **架构模式**: [ARCHITECTURE_PATTERNS.md](ARCHITECTURE_PATTERNS.md)
- **组件设计**: [COMPONENT_DESIGN.md](COMPONENT_DESIGN.md)
- **状态机实现**: [STATE_MACHINE.md](STATE_MACHINE.md)
- **性能优化**: [PERFORMANCE.md](PERFORMANCE.md)
- **网络架构**: [NETWORKING.md](NETWORKING.md)