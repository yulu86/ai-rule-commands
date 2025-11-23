# Godot最佳实践指南

## 节点和场景管理

### 节点引用最佳实践
```gdscript
# 好的做法：使用@onready缓存节点引用
@onready var player_sprite = $Player/Sprite2D
@onready var collision_shape = $CollisionShape2D

# 避免的做法：在_process中重复获取节点
func _process(delta):
    var sprite = get_node("Player/Sprite2D")  # 每帧都查询
```

### 场景切换最佳实践
```gdscript
# 好的做法：使用场景切换的加载管理
func change_scene_to_level():
    get_tree().call_deferred("change_scene_to_file", "res://levels/level_1.tscn")

# 避免的做法：在关键函数中直接切换场景
func on_game_over():
    change_scene_to_file("res://menu/game_over.tscn")  # 可能导致问题
```

## 信号系统

### 信号连接最佳实践
```gdscript
# 好的做法：在_ready中连接，在_exit_tree中断开
func _ready():
    health_component.health_changed.connect(_on_health_changed)
    game_manager.game_state_changed.connect(_on_game_state_changed)

func _exit_tree():
    health_component.health_changed.disconnect(_on_health_changed)
    game_manager.game_state_changed.disconnect(_on_game_state_changed)
```

### 自定义信号设计
```gdscript
# 好的做法：提供必要信息的信号
signal health_changed(new_health: float, max_health: float)
signal item_picked_up(item: ItemData, amount: int)

# 避免的做法：信息不足或过多的信号
signal health_changed()  # 缺少具体信息
signal everything_changed(data: Dictionary)  # 信息过于宽泛
```

## 性能优化

### 物理和帧处理
```gdscript
# 好的做法：区分物理处理和帧处理
func _physics_process(delta):
    # 处理物理相关的逻辑
    move_and_slide()
    handle_collisions()

func _process(delta):
    # 处理渲染和UI更新
    update_animations(delta)
    update_ui()

# 避免的做法：在_process中进行物理计算
func _process(delta):
    velocity += gravity * delta  # 应该在_physics_process中
```

### 循环和计算优化
```gdscript
# 好的做法：缓存重复计算结果
var _expensive_calculation_result = null

func get_expensive_result():
    if _expensive_calculation_result == null:
        _expensive_calculation_result = calculate_complex_math()
    return _expensive_calculation_result

# 避免的做法：重复进行昂贵计算
func _process(delta):
    var result = calculate_complex_math()  # 每帧都计算
    use_result(result)
```

## 内存管理

### 资源管理
```gdscript
# 好的做法：适当管理资源生命周期
class ResourceManager:
    var loaded_resources = {}
    
    func get_resource(path: String):
        if not loaded_resources.has(path):
            loaded_resources[path] = load(path)
        return loaded_resources[path]
    
    func cleanup():
        for resource in loaded_resources.values():
            if resource and resource is Texture:
                resource = null
        loaded_resources.clear()
```

### 对象池模式
```gdscript
# 好的做法：使用对象池管理频繁创建销毁的对象
class BulletPool:
    var available_bullets = []
    var active_bullets = []
    var bullet_scene = preload("res://scenes/bullet.tscn")
    
    func get_bullet():
        var bullet
        if available_bullets.size() > 0:
            bullet = available_bullets.pop_back()
        else:
            bullet = bullet_scene.instantiate()
        active_bullets.append(bullet)
        return bullet
    
    func return_bullet(bullet):
        active_bullets.erase(bullet)
        bullet.reset()
        available_bullets.append(bullet)
```

## 输入处理

### 输入映射最佳实践
```gdscript
# 好的做法：使用输入映射而不是硬编码按键
func _process(delta):
    var movement = Vector2.ZERO
    if Input.is_action_pressed("move_left"):
        movement.x -= 1
    if Input.is_action_pressed("move_right"):
        movement.x += 1
    if Input.is_action_just_pressed("jump"):
        jump()

# 避免的做法：硬编码按键
func _process(delta):
    if Input.is_key_pressed(KEY_A):
        move_left()
    if Input.is_key_pressed(KEY_D):
        move_right()
```

## 代码组织

### 脚本结构最佳实践
```gdscript
# 好的做法：清晰的脚本结构
extends CharacterBody2D

# 信号
signal health_changed
signal died

# 导出的变量
@export var max_health: float = 100.0
@export var speed: float = 300.0

# 私有变量
var _current_health: float
@onready var _sprite = $Sprite2D
@onready var _collision_shape = $CollisionShape2D

# 生命周期函数
func _ready():
    _current_health = max_health

# 公共方法
func take_damage(amount: float):
    _current_health -= amount
    _current_health = max(0, _current_health)
    health_changed.emit(_current_health)
    if _current_health <= 0:
        died.emit()

# 私有方法
func _handle_death():
    # 死亡处理逻辑
    pass
```

## 调试和错误处理

### 防御性编程
```gdscript
# 好的做法：添加必要的检查
func set_target(target_node: Node):
    if not target_node:
        push_error("Target node is null")
        return
    
    if not is_instance_valid(target_node):
        push_error("Target node is not valid")
        return
    
    _current_target = target_node

# 避免的做法：假设外部输入总是有效
func set_target(target_node: Node):
    _current_target = target_node  # 可能为null或无效
```

### 调试信息输出
```gdscript
# 好的做法：有意义的调试信息
func _on_health_changed(new_health):
    if DEBUG_MODE:
        print("[%s] Health changed to: %.1f" % [name, new_health])

# 避免的做法：无意义的调试信息
func _on_health_changed(new_health):
    print("health")  # 缺少上下文信息
```