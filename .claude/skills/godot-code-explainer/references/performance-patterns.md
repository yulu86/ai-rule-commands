# Godot 性能优化模式

## 帧率独立性

### Delta 时间使用
```gdsharp
func _process(delta):
    # 正确：使用 delta 时间
    position.x += speed * delta
    rotation_degrees += rotation_speed * delta
    
    # 错误：不考虑帧率
    position.x += speed  # 会在不同帧率下表现不同
```

### 物理更新分离
```gdsharp
func _process(delta):
    # 游戏逻辑（每帧更新）
    update_animation()
    handle_input()

func _physics_process(delta):
    # 物理计算（固定时间步长）
    move_player()
    check_collisions()
```

## 对象池化

### 项目对象池
```gdsharp
class_name BulletPool
extends Node

const MAX_BULLETS = 50
var available_bullets: Array[Node] = []
var active_bullets: Array[Node] = []

func _ready():
    _create_pool()

func _create_pool():
    var bullet_scene = preload("res://scenes/bullet.tscn")
    for i in MAX_BULLETS:
        var bullet = bullet_scene.instantiate()
        bullet.visible = false
        bullet.set_process(false)
        add_child(bullet)
        available_bullets.append(bullet)

func get_bullet() -> Node:
    var bullet: Node
    if available_bullets.size() > 0:
        bullet = available_bullets.pop_back()
    else:
        # 复用最早的子弹
        bullet = active_bullets.pop_front()
        _recycle_bullet(bullet)
    
    active_bullets.append(bullet)
    bullet.visible = true
    bullet.set_process(true)
    return bullet

func return_bullet(bullet: Node):
    if bullet in active_bullets:
        active_bullets.erase(bullet)
        available_bullets.append(bullet)
        _recycle_bullet(bullet)

func _recycle_bullet(bullet: Node):
    bullet.visible = false
    bullet.set_process(false)
    bullet.position = Vector2.ZERO
    bullet.velocity = Vector2.ZERO
```

## 节点引用缓存

### 延迟初始化
```gdsharp
extends CharacterBody2D

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var health_bar: ProgressBar = $HealthBar

# 避免在 _process 中重复查找节点
func _process(delta):
    # 缓存后的节点访问（高效）
    sprite.rotation = velocity.angle()
    
    # 错误：每次都查找节点（低效）
    # $Sprite2D.rotation = velocity.angle()
```

### 动态节点缓存
```gdsharp
class_name GameManager
extends Node

var player: CharacterBody2D
var ui_root: CanvasLayer
var camera: Camera2D

func _ready():
    # 缓存重要节点引用
    player = get_tree().get_first_node_in_group("player")
    ui_root = get_tree().get_first_node_in_group("ui")
    camera = get_tree().get_first_node_in_group("camera")

func update_ui():
    if player and ui_root:
        var health_label = ui_root.get_node("HealthLabel")
        health_label.text = "Health: %d" % player.health
```

## 碰撞优化

### 空间分区
```gdsharp
# 使用 Area2D 作为碰撞检测区域
class_name EnemyDetectionZone
extends Area2D

signal enemy_entered(enemy: Enemy)
signal enemy_exited(enemy: Enemy)

func _ready():
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node):
    if body.is_in_group("enemies"):
        enemy_entered.emit(body)

func _on_body_exited(body: Node):
    if body.is_in_group("enemies"):
        enemy_exited.emit(body)
```

### 碰撞层优化
```gdsharp
# 在 _ready 中设置碰撞层
func _ready():
    collision_layer = 0
    collision_mask = 0
    
    # 设置为第2层（0-based）
    set_collision_layer_value(2, true)
    
    # 只检测第1层和第3层
    set_collision_mask_value(1, true)  # 玩家层
    set_collision_mask_value(3, true)  # 环境层
```

## 渲染优化

### 视口剔除
```gdsharp
extends Node2D

func _process(delta):
    var camera = get_tree().get_first_node_in_group("camera")
    var viewport = camera.get_viewport().get_visible_rect()
    var camera_pos = camera.global_position
    
    # 只处理视口内的对象
    for enemy in get_tree().get_nodes_in_group("enemies"):
        var screen_pos = camera.to_screen(enemy.global_position)
        if viewport.has_point(screen_pos):
            enemy.set_process(true)
        else:
            enemy.set_process(false)
```

### 批量渲染
```gdsharp
class_name ParticleSystem
extends Node2D

var particles: Array[Dictionary] = []
var max_particles = 100
var particle_texture: Texture2D

func _ready():
    particle_texture = preload("res://assets/particle.png")

func _process(delta):
    _update_particles(delta)
    _render_particles()

func _render_particles():
    # 使用 MultiMeshInstance 进行批量渲染
    var multimesh = $MultiMeshInstance.multimesh
    multimesh.instance_count = particles.size()
    
    for i in range(particles.size()):
        var particle = particles[i]
        multimesh.set_instance_transform_2d(i, Transform2D(particle.rotation, particle.position))
```

## 内存管理

### 资源清理
```gdsharp
class_name ResourceManager
extends Node

var loaded_resources: Dictionary = {}

func load_resource(path: String, cache: bool = true) -> Resource:
    if cache and path in loaded_resources:
        return loaded_resources[path]
    
    var resource = load(path)
    if cache:
        loaded_resources[path] = resource
    return resource

func unload_resource(path: String):
    if path in loaded_resources:
        loaded_resources.erase(path)
        # 手动触发垃圾回收（仅在必要时）
        # call_deferred("force_gc")

func force_gc():
    # 强制垃圾回收
    for i in range(3):
        await get_tree().process_frame
```

### 节点回收
```gdsharp
func _exit_tree():
    # 清理连接的信号
    player.health_changed.disconnect(_on_health_changed)
    
    # 清理定时器
    if is_instance_valid(spawn_timer):
        spawn_timer.queue_free()
    
    # 清理动态创建的节点
    for child in dynamic_children:
        if is_instance_valid(child):
            child.queue_free()
```

## 异步操作

### 异步加载
```gdsharp
func load_level_async(level_path: String):
    # 显示加载界面
    show_loading_screen()
    
    # 异步加载场景
    var packed_scene = ResourceLoader.load_threaded_request(level_path)
    
    while true:
        var status = ResourceLoader.load_threaded_get_status(level_path)
        if status == ResourceLoader.THREAD_LOAD_LOADED:
            var scene = ResourceLoader.load_threaded_get(level_path)
            get_tree().change_scene_to_packed(scene)
            break
        elif status == ResourceLoader.THREAD_LOAD_FAILED:
            print("Failed to load level: ", level_path)
            break
        
        # 更新加载进度
        update_loading_progress(status)
        await get_tree().process_frame
```

### 并行处理
```gdsharp
func process_large_dataset(data: Array):
    var chunk_size = 100
    var tasks = []
    
    for i in range(0, data.size(), chunk_size):
        var chunk = data.slice(i, i + chunk_size)
        tasks.append(_process_chunk_async(chunk))
    
    # 等待所有任务完成
    await Promise.all(tasks).then(_on_processing_complete)

func _process_chunk_async(chunk: Array):
    return await Promise.new(func(resolve):
        # 处理数据块
        var result = []
        for item in chunk:
            result.append(_process_item(item))
        resolve.call(result)
    )
```

## 性能监控

### 性能调试器
```gdsharp
class_name PerformanceProfiler
extends Node

var profile_data: Dictionary = {}
var enabled = false

func start_profile(name: String):
    if not enabled:
        return
    
    if name not in profile_data:
        profile_data[name] = {"calls": 0, "total_time": 0.0}
    
    profile_data[name]["start_time"] = Time.get_ticks_usec()

func end_profile(name: String):
    if not enabled or name not in profile_data or "start_time" not in profile_data[name]:
        return
    
    var elapsed = (Time.get_ticks_usec() - profile_data[name]["start_time"]) / 1000.0
    profile_data[name]["calls"] += 1
    profile_data[name]["total_time"] += elapsed
    profile_data[name].erase("start_time")

func get_report() -> String:
    var report = "Performance Profile:\n"
    for name in profile_data:
        var data = profile_data[name]
        var avg_time = data["total_time"] / data["calls"] if data["calls"] > 0 else 0
        report += "%s: %d calls, %.2fms total, %.2fms avg\n" % [name, data["calls"], data["total_time"], avg_time]
    
    return report

# 使用示例
func _process(delta):
    PerformanceProfiler.start_profile("player_movement")
    handle_player_movement(delta)
    PerformanceProfiler.end_profile("player_movement")
    
    PerformanceProfiler.start_profile("enemy_ai")
    update_enemy_ai(delta)
    PerformanceProfiler.end_profile("enemy_ai")
```

## 常见性能陷阱

### 避免的操作
```gdsharp
func _process(delta):
    # ❌ 在 _process 中查找节点
    var player = get_tree().get_first_node_in_group("player")
    
    # ❌ 在 _process 中加载资源
    var texture = load("res://textures/player.png")
    
    # ❌ 在 _process 中创建新对象
    var new_bullet = preload("res://scenes/bullet.tscn").instantiate()
    
    # ❌ 在 _process 中调用 expensive 函数
    var expensive_result = calculate_expensive_computation()
    
    # ✅ 正确做法：缓存和预加载
    # 在 _ready 中初始化，在 _process 中使用
    if player:
        sprite.texture = cached_player_texture
        update_player_animation()
```

### 优化检查清单
- [ ] 所有频繁访问的节点都已缓存
- [ ] 所有常用资源都已预加载
- [ ] 没有在 _process 中进行文件 I/O
- [ ] 没有在 _process 中创建临时对象
- [ ] 使用对象池管理频繁创建销毁的对象
- [ ] 碰撞检测层设置合理
- [ ] 视口剔除已实现（大型场景）
- [ ] 异步加载用于大资源
- [ ] 内存泄漏检查已完成