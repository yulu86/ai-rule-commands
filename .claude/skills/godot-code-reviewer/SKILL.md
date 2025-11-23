---
name: godot-code-reviewer
description: 专业的Godot代码检视和质量分析技能。检视Godot项目中的GDScript、C#代码，发现潜在问题，提供符合Godot开发范式和规范的修改建议。涵盖性能优化、内存管理、信号使用、场景结构、节点操作、动画控制等各个方面。使用context7获取API和SDK的详细信息。
---

# Godot代码检视技能

## 快速开始

当用户要求检视Godot代码时，使用此技能进行全面的代码审查：

1. **读取并分析代码** - 理解代码结构和功能，可以使用`Godot Server` MCP Server的工具
2. **识别问题** - 根据Godot最佳实践识别潜在问题
3. **提供解决方案** - 给出具体的修改建议和代码示例
4. **API查询** - 对不确定的API使用context7获取详细信息

## 检视原则

### 核心范式检查
- **节点生命周期**：检查`_ready()`、`_process()`、`_physics_process()`的正确使用
- **信号连接**：验证信号的定义、连接和断开是否正确
- **场景树操作**：检查节点引用、添加/移除节点是否安全
- **资源管理**：验证资源的加载、释放和内存管理

### 性能优化检查
- **循环优化**：检查for/while循环的性能问题
- **重复计算**：识别可缓存的重复计算
- **节点查询**：检查`get_node()`、`find_child()`等调用是否优化
- **渲染优化**：检查draw call、texture usage等渲染相关问题

### 代码质量检查
- **变量命名**：检查是否符合GDScript命名规范
- **函数职责**：确保函数单一职责原则
- **错误处理**：检查是否有适当的错误处理机制
- **类型安全**：检查类型注解和类型转换

## 常见问题检查点

### 1. 节点操作问题
```gdscript
# 问题：重复获取节点引用
func _process(delta):
    var player = get_node("Player")
    player.move(delta)

# 建议：缓存节点引用
@onready var player = $Player
func _process(delta):
    player.move(delta)
```

### 2. 信号处理问题
```gdscript
# 问题：忘记断开信号连接
func _ready():
    some_button.pressed.connect(_on_button_pressed)

# 建议：在适当时机断开信号
func _exit_tree():
    some_button.pressed.disconnect(_on_button_pressed)
```

### 3. 内存管理问题
```gdscript
# 问题：资源未释放
func load_texture():
    var texture = load("res://texture.png")
    return texture

# 建议：适当管理资源引用
var cached_texture = null
func get_texture():
    if not cached_texture:
        cached_texture = load("res://texture.png")
    return cached_texture
```

### 4. 性能问题
```gdscript
# 问题：在_process中重复计算
func _process(delta):
    var expensive_result = calculate_something_complex()
    update_ui(expensive_result)

# 建议：缓存计算结果或使用条件更新
var cached_result = null
func _process(delta):
    if not cached_result:
        cached_result = calculate_something_complex()
    update_ui(cached_result)
```

## 代码分析流程

### 第一步：代码结构分析
1. **文件组织** - 检查脚本与场景的对应关系
2. **类结构** - 分析类的继承关系和职责
3. **依赖关系** - 检查外部依赖和耦合度

### 第二步：功能逻辑分析
1. **核心功能** - 识别主要功能和实现方式
2. **数据流** - 跟踪数据的创建、传递和销毁
3. **状态管理** - 检查状态的变化和管理方式

### 第三步：问题识别
1. **潜在bug** - 识别可能导致错误的问题
2. **性能瓶颈** - 找出影响性能的代码段
3. **安全问题** - 检查内存泄漏、空引用等

### 第四步：建议提供
1. **具体修改** - 提供可直接使用的代码
2. **最佳实践** - 解释为什么这样修改更好
3. **替代方案** - 提供多种实现选择

## 使用Context7查询API

对不确定的API或功能，使用context7获取最新信息：

```
查询示例：
- Godot 4.x Node类的所有方法
- GDScript信号系统的最佳实践
- Godot性能优化技巧
- CollisionShape2D的正确使用方法
```

## 检视报告格式

### 问题分级
- **严重**：会导致崩溃或严重性能问题
- **重要**：影响功能或性能的重要问题
- **建议**：代码改进建议和最佳实践

### 报告模板
```
## 代码检视报告

### 文件：[文件名]

#### 严重问题
1. **问题描述** - 具体问题说明
   - **位置**：行号
   - **问题**：详细解释
   - **建议**：解决方案和代码示例

#### 重要问题
[同上格式]

#### 改进建议
[同上格式]

### 总结
- 总体评价
- 优先修复建议
- 最佳实践建议
```

## Godot版本兼容性

- **Godot 4.x** - 重点支持的新版本特性
- **跨版本** - 版本间的差异和注意事项

## 特殊场景处理

### 网络游戏代码
- **同步机制** - 检查客户端-服务器同步
- **延迟补偿** - 网络延迟处理
- **安全性** - 作弊防护和数据验证

### 移动平台优化
- **性能优化** - 针对移动设备的优化
- **内存管理** - 移动设备内存限制
- **输入处理** - 触摸输入和传感器

### 大型项目管理
- **模块化** - 代码组织和模块划分
- **资源管理** - 大型资源加载和释放
- **性能监控** - 性能分析和调试

## 参考资源

### 内部参考
- [GODOT_BEST_PRACTICES.md](references/GODOT_BEST_PRACTICES.md) - Godot最佳实践
- [PERFORMANCE_GUIDE.md](references/PERFORMANCE_GUIDE.md) - 性能优化指南
- [API_PATTERNS.md](references/API_PATTERNS.md) - 常用API使用模式

### 外部资源
- Godot官方文档
- Godot社区最佳实践
- 性能分析工具使用指南

## 使用建议

1. **优先级排序** - 先修复严重和重要问题
2. **渐进式改进** - 逐步实施改进建议
3. **测试验证** - 每次修改后进行功能测试
4. **性能测试** - 使用Godot性能工具验证优化效果