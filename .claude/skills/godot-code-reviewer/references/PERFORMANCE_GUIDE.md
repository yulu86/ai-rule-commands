# Godot性能优化指南

## 渲染性能优化

### Draw Call优化
```gdscript
# 问题：过多的单独绘制调用
func create_individual_sprites():
    for i in 100:
        var sprite = Sprite2D.new()
        sprite.texture = load("res://textures/unit.png")
        add_child(sprite)

# 优化：使用MultiMesh或合并纹理
func create_optimized_sprites():
    var multimesh = MultiMeshInstance2D.new()
    var multimesh_resource = MultiMesh.new()
    multimesh_resource.mesh = QuadMesh.new()
    multimesh_resource.mesh.size = Vector2(32, 32)
    multimesh_resource.transform_format = MultiMesh.TRANSFORM_2D
    multimesh_resource.instance_count = 100
    
    multimesh.multimesh = multimesh_resource
    add_child(multimesh)
```

### 纹理优化
```gdscript
# 好的做法：纹理压缩和合理尺寸
func optimize_textures():
    # 使用适当的纹理大小
    var texture = load("res://textures/character.png")
    
    # 确保纹理是2的幂次大小
    if not _is_power_of_two(texture.get_width()) or not _is_power_of_two(texture.get_height()):
        push_warning("Texture size should be power of 2 for better performance")

func _is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0
```

## 脚本性能优化

### 变量访问优化
```gdscript
# 问题：重复的节点查找
func _process(delta):
    var player = get_node("../Player")  # 每帧都查找
    var health = player.get_node("HealthComponent")
    health.update_health_bar()

# 优化：缓存节点引用
@onready var _player = get_node("../Player")
@onready var _health_component = _player.get_node("HealthComponent")

func _process(delta):
    _health_component.update_health_bar()
```

### 数学运算优化
```gdscript
# 问题：重复的昂贵的数学运算
func _process(delta):
    var direction = (target_position - global_position).normalized()
    var distance = (target_position - global_position).length()
    
    if distance > 0:
        move_and_collide(direction * speed * delta)

# 优化：减少重复计算
var _last_target_position: Vector2
var _cached_direction: Vector2
var _cached_distance: float

func _process(delta):
    if target_position != _last_target_position:
        var to_target = target_position - global_position
        _cached_distance = to_target.length()
        if _cached_distance > 0:
            _cached_direction = to_target / _cached_distance
        _last_target_position = target_position
    
    if _cached_distance > 0:
        move_and_collide(_cached_direction * speed * delta)
```

## 内存优化

### 对象池实现
```gdscript
# 高效的对象池实现
class_name GameObjectPool
extends Node

var available_objects: Array = []
var active_objects: Array = []
var object_scene: PackedScene

func _init(scene: PackedScene):
    object_scene = scene

func get_object():
    var obj: Node
    if available_objects.size() > 0:
        obj = available_objects.pop_back()
    else:
        obj = object_scene.instantiate()
    
    active_objects.append(obj)
    return obj

func return_object(obj: Node):
    if obj in active_objects:
        active_objects.erase(obj)
        obj.get_parent()?.remove_child(obj)
        available_objects.append(obj)
        obj.reset_if_exists()  # 如果对象有reset方法

func cleanup():
    for obj in active_objects:
        obj.queue_free()
    active_objects.clear()
    
    for obj in available_objects:
        obj.queue_free()
    available_objects.clear()
```

### 资源缓存策略
```gdscript
# 智能资源缓存系统
class_name ResourceCache
extends Node

var cache: Dictionary = {}
var max_cache_size: int = 100
var access_count: Dictionary = {}

func get_resource(path: String) -> Resource:
    if cache.has(path):
        access_count[path] += 1
        return cache[path]
    
    var resource = load(path)
    if resource:
        cache[path] = resource
        access_count[path] = 1
        
        # 检查缓存大小并清理最少使用的资源
        if cache.size() > max_cache_size:
            _cleanup_least_used()
    
    return resource

func _cleanup_least_used():
    var least_used_path = ""
    var min_access_count = INF
    
    for path in access_count:
        if access_count[path] < min_access_count:
            min_access_count = access_count[path]
            least_used_path = path
    
    if least_used_path != "":
        cache.erase(least_used_path)
        access_count.erase(least_used_path)
```

## 物理性能优化

### 碰撞优化
```gdscript
# 问题：过多的碰撞检测
func _physics_process(delta):
    for enemy in get_tree().get_nodes_in_group("enemies"):
        if global_position.distance_to(enemy.global_position) < 100:
            check_collision_with(enemy)

# 优化：使用Area2D或空间分区
func _ready():
    var detection_area = Area2D.new()
    var collision_shape = CollisionShape2D.new()
    collision_shape.shape = CircleShape2D.new()
    collision_shape.shape.radius = 100
    
    detection_area.add_child(collision_shape)
    add_child(detection_area)
    detection_area.monitoring = true
    detection_area.body_entered.connect(_on_enemy_in_range)

func _on_enemy_in_range(enemy):
    check_collision_with(enemy)
```

### 移动计算优化
```gdscript
# 问题：不必要的复杂物理计算
func _physics_process(delta):
    velocity = Vector2.ZERO
    if Input.is_action_pressed("ui_left"):
        velocity.x -= speed
    if Input.is_action_pressed("ui_right"):
        velocity.x += speed
    if Input.is_action_pressed("ui_up"):
        velocity.y -= speed
    if Input.is_action_pressed("ui_down"):
        velocity.y += speed
    velocity = velocity.normalized() * speed  # 不必要的重复计算

# 优化：简化计算
func _physics_process(delta):
    var input_vector = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = input_vector * speed
    move_and_slide()
```

## 音频性能优化

### 音频流管理
```gdscript
# 问题：频繁的音频文件加载
func play_sound():
    var sound_player = AudioStreamPlayer.new()
    sound_player.stream = load("res://sounds/shot.wav")  # 每次都加载
    add_child(sound_player)
    sound_player.play()

# 优化：音频预加载和池化
class_name AudioManager
extends Node

var sound_pool: Dictionary = {}
var max_players_per_sound = 5

func _ready():
    _preload_sounds()

func _preload_sounds():
    var sound_files = ["shot.wav", "explosion.wav", "pickup.wav"]
    for file in sound_files:
        var stream = load("res://sounds/" + file)
        if stream:
            sound_pool[file] = []
            for i in max_players_per_sound:
                var player = AudioStreamPlayer.new()
                player.stream = stream
                add_child(player)
                sound_pool[file].append(player)

func play_sound(file_name: String):
    if sound_pool.has(file_name):
        for player in sound_pool[file_name]:
            if not player.playing:
                player.play()
                return
```

## UI性能优化

### UI更新优化
```gdscript
# 问题：不必要的UI更新
func _process(delta):
    health_bar.value = current_health  # 每帧都更新
    score_label.text = "Score: " + str(score)

# 优化：条件更新
var _last_health = -1
var _last_score = -1

func _process(delta):
    if current_health != _last_health:
        health_bar.value = current_health
        _last_health = current_health
    
    if score != _last_score:
        score_label.text = "Score: " + str(score)
        _last_score = score
```

## 性能监控

### 性能分析工具
```gdscript
# 简单的性能监控系统
class_name PerformanceProfiler
extends Node

var frame_times: Array = []
var max_samples = 60

func _process(delta):
    frame_times.append(delta)
    if frame_times.size() > max_samples:
        frame_times.pop_front()

func get_average_frame_time() -> float:
    if frame_times.size() == 0:
        return 0.0
    
    var total = 0.0
    for time in frame_times:
        total += time
    return total / frame_times.size()

func get_fps() -> float:
    return 1.0 / get_average_frame_time() if get_average_frame_time() > 0 else 0.0

func print_performance_stats():
    if Engine.get_frames_drawn() % 60 == 0:  # 每秒打印一次
        print("FPS: %.1f, Frame Time: %.3f ms" % [get_fps(), get_average_frame_time() * 1000])
```