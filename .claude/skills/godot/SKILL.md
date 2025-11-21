---
name: godot
description: 在处理 Godot 引擎项目时应使用此技能。它提供关于 Godot 文件格式（.gd、.tscn、.tres）、架构模式（基于组件、信号驱动、基于资源）、常见陷阱、验证工具、代码模板和 CLI 工作流的专业知识。`godot` 命令可用于运行游戏、验证脚本、导入资源和导出构建。在涉及 Godot 游戏开发、调试场景/资源文件、实现游戏系统或创建新的 Godot 组件的任务时使用此技能。
---

# Godot 引擎开发技能

使用 Godot 引擎开发游戏和应用程序的专业指导，强调 LLM 编程助手与 Godot 独特文件结构之间的有效协作。

## 概述

Godot 项目混合使用 GDScript 代码文件（.gd）和基于文本的资源文件（.tscn 用于场景，.tres 用于资源）。虽然 GDScript 很简单，但资源文件有着严格的格式要求，与 GDScript 语法有显著差异。此技能提供文件格式专业知识、经过验证的架构模式、验证工具、代码模板和调试工作流，以实现 Godot 项目的有效开发。

## 何时使用此技能

在以下情况下调用此技能：

- 处理任何 Godot 引擎项目时
- 创建或修改 .tscn（场景）或 .tres（资源）文件时
- 实现游戏系统（交互、属性、法术、物品栏等）时
- 调试"文件加载失败"或类似的资源错误时
- 设置基于组件的架构时
- 创建信号驱动的系统时
- 实现基于资源的数据（物品、法术、能力）时

## 核心原则

### 1. 理解文件格式差异

**GDScript (.gd) - 完整的编程语言：**
```gdscript
extends Node
class_name MyClass

var speed: float = 5.0
const MAX_HEALTH = 100

func _ready():
    print("Ready")
```

**场景文件 (.tscn) - 严格的序列化格式：**
```
[ext_resource type="Script" path="res://script.gd" id="1"]

[node name="Player" type="CharacterBody3D"]
script = ExtResource("1")  # 不要用 preload()!
```

**资源文件 (.tres) - 不包含 GDScript 语法：**
```
[ext_resource type="Script" path="res://item.gd" id="1"]

[resource]
script = ExtResource("1")  # 不要用 preload()!
item_name = "Sword"        # 不要用 var item_name = "Sword"!
```

### 2. .tres 和 .tscn 文件的关键规则

**在 .tres/.tscn 文件中绝不要使用：**
- `preload()` - 改用 `ExtResource("id")`
- `var`, `const`, `func` - 这些是 GDScript 关键字
- 无类型数组 - 使用 `Array[Type]([...])` 语法

**在 .tres/.tscn 文件中总是使用：**
- `ExtResource("id")` 用于外部资源
- `SubResource("id")` 用于内联资源
- 类型化数组：`Array[Resource]([...])`
- 在使用前正确声明 ExtResource

### 3. 关注点分离

**将逻辑放在 .gd 文件中，数据放在 .tres 文件中：**
```
src/
  spells/
    spell_resource.gd      # 类定义 + 逻辑
    spell_effect.gd        # 效果逻辑
resources/
  spells/
    fireball.tres          # 仅数据，引用脚本
    ice_spike.tres         # 仅数据
```

这使得 LLM 编辑更安全、更清晰。

### 4. 基于组件的架构

将功能分解为小的、专注的组件：
```
Player (CharacterBody3D)
├─ HealthAttribute (Node)     # 组件
├─ ManaAttribute (Node)        # 组件
├─ Inventory (Node)            # 组件
└─ StateMachine (Node)         # 组件
    ├─ IdleState (Node)
    ├─ MoveState (Node)
    └─ AttackState (Node)
```

**优点：**
- 每个组件都是小的、专注的文件
- 易于理解和修改
- 责任清晰
- 可在不同实体间重用

### 5. 信号驱动通信

使用信号实现松耦合：
```gdscript
# 组件发出信号
signal health_changed(current, max)
signal death()

# 父节点连接到信号
func _ready():
    $HealthAttribute.health_changed.connect(_on_health_changed)
    $HealthAttribute.death.connect(_on_death)
```

**优点：**
- 系统间没有紧密耦合
- 易于添加新的监听器
- 自文档化（信号显示可用事件）
- UI 可以在不修改游戏逻辑的情况下连接

## 使用捆绑资源

### 验证脚本

在 Godot 中测试之前验证 .tres 和 .tscn 文件，以尽早发现语法错误。

**验证 .tres 文件：**
```bash
python3 scripts/validate_tres.py resources/spells/fireball.tres
```

**验证 .tscn 文件：**
```bash
python3 scripts/validate_tscn.py scenes/player/player.tscn
```

在以下情况下使用这些脚本：
- 在以编程方式创建或编辑 .tres/.tscn 文件后
- 调试"加载失败"错误时
- 在提交场景/资源更改前
- 当用户报告自定义资源问题时

### 参考文档

在需要详细信息时加载参考文件：

**`references/file-formats.md`** - 深入了解 .gd、.tscn、.tres 语法：
- 每种文件类型的完整语法规则
- 常见错误及示例
- 安全与风险编辑模式
- ExtResource 和 SubResource 的使用

**`references/architecture-patterns.md`** - 经过验证的架构模式：
- 基于组件的交互系统
- 属性系统（生命值、魔力等）
- 基于资源的效果系统（法术、物品）
- 物品栏系统
- 状态机模式
- 模式组合示例

在以下情况下阅读这些参考：
- 实现新的游戏系统时
- 对 .tres/.tscn 语法不确定时
- 调试文件格式错误时
- 为新功能规划架构时

### 代码模板

使用模板作为常见模式的起点。模板位于 `assets/templates/`：

**`component_template.gd`** - 带有信号、导出、激活的基础组件：
```gdscript
# 复制并自定义为新组件
cp assets/templates/component_template.gd src/components/my_component.gd
```

**`attribute_template.gd`** - 数值属性（生命值、魔力、体力）：
```gdscript
# 用于任何有最小/最大值的数值属性
cp assets/templates/attribute_template.gd src/attributes/stamina_attribute.gd
```

**`interaction_template.gd`** - 交互组件基类：
```gdscript
# 扩展为自定义交互（拾取、门、开关等）
cp assets/templates/interaction_template.gd src/interactions/lever_interaction.gd
```

**`spell_resource.tres`** - 带有效果的法术示例：
```bash
# 用作创建新法术数据的参考
cat assets/templates/spell_resource.tres
```

**`item_resource.tres`** - 物品资源示例：
```bash
# 用作创建新物品数据的参考
cat assets/templates/item_resource.tres
```

## 工作流

### 工作流 1：创建新的组件系统

示例：为敌人添加生命值系统。

**步骤：**

1. **阅读架构模式参考：**
   ```bash
   # 检查类似模式
   Read references/architecture-patterns.md
   # 查找"属性系统"部分
   ```

2. **使用模板创建基类：**
   ```bash
   cp assets/templates/attribute_template.gd src/attributes/attribute.gd
   # 自定义基类
   ```

3. **创建专门的子类：**
   ```bash
   # 创建扩展 attribute.gd 的 health_attribute.gd
   # 添加生命值特定的信号（damage_taken、death）
   ```

4. **通过 .tscn 编辑添加到场景：**
   ```
   [ext_resource type="Script" path="res://src/attributes/health_attribute.gd" id="4_health"]

   [node name="HealthAttribute" type="Node" parent="Enemy"]
   script = ExtResource("4_health")
   value_max = 50.0
   value_start = 50.0
   ```

5. **在 Godot 编辑器中立即测试**

6. **如果有问题，验证场景文件：**
   ```bash
   python3 scripts/validate_tscn.py scenes/enemies/base_enemy.tscn
   ```

### 工作流 2：创建资源数据文件（.tres）

示例：创建新法术。

**步骤：**

1. **参考模板：**
   ```bash
   cat assets/templates/spell_resource.tres
   ```

2. **使用正确结构创建新的 .tres 文件：**
   ```tres
   [gd_resource type="Resource" script_class="SpellResource" load_steps=3 format=3]

   [ext_resource type="Script" path="res://src/spells/spell_resource.gd" id="1"]
   [ext_resource type="Script" path="res://src/spells/spell_effect.gd" id="2"]

   [sub_resource type="Resource" id="Effect_1"]
   script = ExtResource("2")
   effect_type = 0
   magnitude_min = 15.0
   magnitude_max = 25.0

   [resource]
   script = ExtResource("1")
   spell_name = "Fireball"
   spell_id = "fireball"
   mana_cost = 25.0
   effects = Array[ExtResource("2")]([SubResource("Effect_1")])
   ```

3. **测试前验证：**
   ```bash
   python3 scripts/validate_tres.py resources/spells/fireball.tres
   ```

4. **修复验证器报告的任何错误**

5. **在 Godot 编辑器中测试**

### 工作流 3：调试资源加载问题

当用户报告"资源加载失败"或类似错误时。

**步骤：**

1. **读取报告错误的文件：**
   ```bash
   # 检查文件语法
   Read resources/spells/problem_spell.tres
   ```

2. **运行验证脚本：**
   ```bash
   python3 scripts/validate_tres.py resources/spells/problem_spell.tres
   ```

3. **检查常见错误：**
   - 使用 `preload()` 而不是 `ExtResource()`
   - 使用 `var`、`const`、`func` 关键字
   - 缺少 ExtResource 声明
   - 不正确的数组语法（未类型化）

4. **如需要，阅读文件格式参考：**
   ```bash
   Read references/file-formats.md
   # 关注"资源文件（.tres）"部分
   # 查看"常见错误参考"
   ```

5. **修复错误并重新验证**

### 工作流 4：从架构模式实现

当实现已知模式（交互系统、状态机等）时。

**步骤：**

1. **阅读相关模式：**
   ```bash
   Read references/architecture-patterns.md
   # 查找特定模式（例如，"基于组件的交互系统"）
   ```

2. **复制相关模板：**
   ```bash
   cp assets/templates/interaction_template.gd src/interactions/door_interaction.gd
   ```

3. **自定义模板：**
   - 重写 `_perform_interaction()`
   - 添加配置的自定义导出
   - 如需要，添加自定义信号

4. **按照模式创建场景结构：**
   ```
   [node name="Door" type="StaticBody3D"]
   script = ExtResource("base_interactable.gd")

   [node name="DoorInteraction" type="Node" parent="."]
   script = ExtResource("door_interaction.gd")
   interaction_text = "Open Door"
   ```

5. **增量测试**

## 常见陷阱和解决方案

### 陷阱 1：在 .tres 文件中使用 GDScript 语法

**问题：**
```tres
# ❌ 错误
script = preload("res://script.gd")
var items = [1, 2, 3]
```

**解决方案：**
```tres
# ✅ 正确
[ext_resource type="Script" path="res://script.gd" id="1"]
script = ExtResource("1")
items = Array[int]([1, 2, 3])
```

**预防：** 在测试前运行验证脚本。

### 陷阱 2：缺少 ExtResource 声明

**问题：**
```tres
[resource]
script = ExtResource("1_script")  # 未声明！
```

**解决方案：**
```tres
[ext_resource type="Script" path="res://script.gd" id="1_script"]

[resource]
script = ExtResource("1_script")
```

**检测：** 验证脚本会捕获此问题。

### 陷阱 3：编辑复杂的 .tscn 层次结构

**问题：** 修改实例化场景的子节点可能在编辑器重新保存时破坏。

**解决方案：**
- 在 .tscn 文件中只做简单的属性编辑
- 对于复杂更改，使用 Godot 编辑器
- 文本编辑后立即测试
- 使用 git 跟踪更改并在需要时回滚

### 陷阱 4：在 .tres 文件中使用无类型数组

**问题：**
```tres
effects = [SubResource("Effect_1")]  # 缺少类型
```

**解决方案：**
```tres
effects = Array[Resource]([SubResource("Effect_1")])
```

**预防：** 验证脚本会警告此问题。

### 陷阱 5：忘记实例属性覆盖

**问题：** 实例化场景时，忘记覆盖子节点属性。实例使用默认值（通常是 `null`），导致静默错误。

```
# level.tscn
[node name="KeyPickup" parent="." instance=ExtResource("6_pickup")]
# 糟糕！PickupInteraction.item_resource 为 null - 拾取不起作用！
```

**解决方案：** 总是使用 `index` 语法配置实例化场景属性：

```
[node name="KeyPickup" parent="." instance=ExtResource("6_pickup")]

[node name="PickupInteraction" parent="KeyPickup" index="0"]
item_resource = ExtResource("7_key")
```

**检测：**
- 立即在游戏中测试实例
- 阅读 `references/file-formats.md` "实例属性覆盖" 部分了解详情
- 创建场景实例时，问："这个场景是否有需要设置属性的可配置组件？"

**预防：** 实例化任何具有可配置子节点的场景（PickupInteraction、DoorInteraction 等）后，总是验证关键属性已被覆盖。

### 陷阱 6：CPUParticles3D color_ramp 不显示颜色

**问题：** 在 CPUParticles3D 上设置 `color_ramp`，但粒子仍然显示白色或不显示渐变颜色。

```tres
[node name="CPUParticles3D" type="CPUParticles3D" parent="."]
mesh = SubResource("SphereMesh_1")
color_ramp = SubResource("Gradient_1")  # 渐变已设置但不工作！
```

**根本原因：** 网格需要带有 `vertex_color_use_as_albedo = true` 的材质，才能将粒子颜色应用到网格表面。

**解决方案：** 为网格添加启用顶点颜色的 StandardMaterial3D：

```tres
[sub_resource type="StandardMaterial3D" id="StandardMaterial3D_1"]
vertex_color_use_as_albedo = true

[sub_resource type="SphereMesh" id="SphereMesh_1"]
material = SubResource("StandardMaterial3D_1")
radius = 0.12
height = 0.24

[node name="CPUParticles3D" type="CPUParticles3D" parent="."]
mesh = SubResource("SphereMesh_1")
color_ramp = SubResource("Gradient_1")  # 现在有效了！
```

**预防：** 创建带有 `color` 或 `color_ramp` 的 CPUParticles3D 时，总是为网格添加带有 `vertex_color_use_as_albedo = true` 的材质。

## 最佳实践

### 1. 查阅参考资料解决常见问题

遇到问题时，查阅参考文档：

**`use context7`** - 使用MCP Server context7查询godot API

**`references/common-pitfalls.md`** - 常见 Godot 陷阱和解决方案：
- 初始化和 @onready 时序问题
- 节点引用和 get_node() 问题
- 信号连接问题
- 资源加载和修改
- CharacterBody3D 移动
- 变换和基向量混淆
- 输入处理
- 类型安全问题
- 场景实例化陷阱
- 补间问题

**`references/godot4-physics-api.md`** - 物理API快速参考：
- 正确的光线投射API（`PhysicsRayQueryParameters3D`）
- 形状查询和碰撞检测
- 碰撞层和掩码
- Area3D vs RigidBody3D vs CharacterBody3D
- 常见物理模式
- 性能技巧

在以下情况下加载这些参考资料：
- 遇到空引用错误
- 实现物理/碰撞系统
- 调试 @onready 时序问题
- 处理 CharacterBody3D 移动
- 设置光线投射或形状查询

### 2. 编辑 .tres/.tscn 后总是验证

```bash
python3 scripts/validate_tres.py path/to/file.tres
python3 scripts/validate_tscn.py path/to/file.tscn
```

### 3. 使用模板作为起点

不要从头开始编写组件 - 适配模板：
```bash
cp assets/templates/component_template.gd src/my_component.gd
```

### 4. 阅读参考资料了解详细语法

对语法不确定时，加载参考资料：
```bash
Read references/file-formats.md
```

### 5. 遵循关注点分离

- 逻辑 → .gd 文件
- 数据 → .tres 文件
- 场景结构 → .tscn 文件（复杂更改优先使用编辑器）

### 6. 使用信号进行通信

优先使用信号而不是直接方法调用：
```gdscript
# ✅ 好的 - 松耦合
signal item_picked_up(item)
item_picked_up.emit(item)

# ❌ 避免 - 紧耦合
get_parent().get_parent().add_to_inventory(item)
```

### 7. 增量测试

每次更改后：
1. 使用脚本验证
2. 在 Godot 编辑器中测试
3. 验证功能
4. 提交到 git

### 8. 充分使用导出变量

使配置可见和可编辑：
```gdscript
@export_group("移动")
@export var speed: float = 5.0
@export var jump_force: float = 10.0

@export_group("战斗")
@export var damage: int = 10
```

## 使用 Godot CLI

`godot` 命令行工具可用于运行游戏和执行各种操作，而无需打开编辑器。

### 运行游戏

**运行当前项目：**
```bash
godot --path . --headless
```

**运行特定场景：**
```bash
godot --path . --scene scenes/main_menu.tscn
```

**使用调试标志运行：**
```bash
# 显示碰撞形状
godot --path . --debug-collisions

# 显示导航调试可视化
godot --path . --debug-navigation

# 显示路径线条
godot --path . --debug-paths
```

### 检查/验证代码

**检查 GDScript 语法而不运行：**
```bash
godot --path . --check-only --script path/to/script.gd
```

**运行无头测试（用于自动化测试）：**
```bash
godot --path . --headless --quit --script path/to/test_script.gd
```

### 从 CLI 执行编辑器操作

**导入资源而不打开编辑器：**
```bash
godot --path . --import --headless --quit
```

**导出项目：**
```bash
# 导出发布构建
godot --path . --export-release "预设名称" builds/game.exe

# 导出调试构建
godot --path . --export-debug "预设名称" builds/game_debug.exe
```

### 常见的 CLI 工作流

**工作流：快速测试运行**
```bash
# 运行项目并在测试后退出
godot --path . --quit-after 300  # 运行300帧然后退出
```

**工作流：自动化资源导入**
```bash
# 导入所有资源并退出（在 CI/CD 中有用）
godot --path . --import --headless --quit
```

**工作流：脚本验证**
```bash
# 在提交前验证 GDScript 文件
godot --path . --check-only --script src/player/player.gd
```

**工作流：无头服务器**
```bash
# 作为专用服务器运行（无渲染）
godot --path . --headless --scene scenes/multiplayer_server.tscn
```

### CLI 使用技巧

1. **从项目目录运行时总是指定 `--path .`** 以确保 Godot 找到 `project.godot`
2. **使用 `--headless`** 进行 CI/CD 和自动化测试（无窗口、无渲染）
3. **使用 `--quit` 或 `--quit-after N`** 在任务完成后自动退出
4. **结合 `--check-only` 和 `--script`** 快速验证 GDScript 语法
5. **使用调试标志**（`--debug-collisions`、`--debug-navigation`）在开发期间可视化系统
6. **检查退出代码** - 非零表示错误（对 CI/CD 脚本有用）

### 示例：GDScript 验证的预提交钩子

```bash
#!/bin/bash
# 在提交前验证所有更改的 .gd 文件

for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.gd$'); do
    if ! godot --path . --check-only --script "$file" --headless --quit; then
        echo "GDScript validation failed for $file"
        exit 1
    fi
done
```

## 快速参考

### 文件类型决策树

**编写游戏逻辑？** → 使用 .gd 文件

**存储数据（物品属性、法术配置）？** → 使用 .tres 文件

**创建场景结构？** → 使用 .tscn 文件（复杂结构优先使用 Godot 编辑器）

### 语法快速检查

**在 .gd 文件中：** 完整的 GDScript - `var`、`func`、`preload()` 等 ✅

**在 .tres/.tscn 文件中：**
- `preload()` ❌ → 使用 `ExtResource("id")` ✅
- `var`, `const`, `func` ❌ → 仅使用属性值 ✅
- `[1, 2, 3]` ❌ → `Array[int]([1, 2, 3])` ✅

### 何时使用每个验证脚本

**`validate_tres.py`** - 用于资源文件：
- 物品、法术、能力
- 自定义资源数据
- 创建 .tres 文件后

**`validate_tscn.py`** - 用于场景文件：
- 玩家、敌人、关卡
- UI 场景
- 编辑 .tscn 文件后

### 何时阅读每个参考

**`file-formats.md`** - 在以下情况下：
- 创建/编辑 .tres/.tscn 文件
- 遇到"加载失败"错误
- 对语法规则不确定

**`architecture-patterns.md`** - 在以下情况下：
- 实现新的游戏系统
- 规划组件结构
- 寻找经过验证的模式

## 总结

通过以下方式有效地处理 Godot 项目：

1. **理解文件格式** - .gd 是代码，.tres/.tscn 是具有严格语法的数据
2. **使用验证工具** - 在测试前捕获错误
3. **遵循模式** - 使用参考中的经过验证的架构
4. **从模板开始** - 适配而不是从头开始创建
5. **增量测试** - 频繁验证、测试、提交

关键见解：当您尊重 GDScript 和资源序列化格式之间的语法差异时，Godot 的基于文本的文件对 LLM 友好。
