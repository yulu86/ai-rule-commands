# Godot API使用模式指南

## 节点操作模式

### 安全的节点引用
```gdscript
# 好的模式：使用类型提示和null检查
var _player: CharacterBody2D = null

func _ready():
    _player = get_node("../Player") as CharacterBody2D
    if not _player:
        push_error("Player node not found!")

func use_player():
    if _player and is_instance_valid(_player):
        _player.take_damage(10)

# 避免的模式：不安全的节点操作
func use_player():
    get_node("../Player").take_damage(10)  # 可能崩溃
```

### 节点查找优化
```gdscript
# 好的模式：使用相对路径和类型转换
@onready var _sprite: Sprite2D = $Sprite2D
@onready var _collision: CollisionShape2D = $CollisionShape2D
@onready var _health_bar: ProgressBar = $UI/HealthBar

# 好的模式：使用组查找
func _ready():
    var enemies = get_tree().get_nodes_in_group("enemies")
    for enemy in enemies:
        if enemy is Enemy:
            enemy.connect("died", _on_enemy_died)

# 避免的模式：深度嵌套的get_node调用
func get_component():
    return get_node("Sprite2D/CollisionShape2D/SomeNode").get_node("Component")
```

## 信号系统模式

### 信号连接的最佳实践
```gdscript
# 好的模式：使用函数引用连接
func _ready():
    button.pressed.connect(_on_button_pressed)
    timer.timeout.connect(_on_timer_timeout)
    custom_signal.connect(_handler_method)

func _on_button_pressed():
    # 处理按钮点击
    pass

# 好的模式：使用lambda连接（简单情况）
func _ready():
    button.pressed.connect(func(): print("Button clicked!"))

# 避免的模式：字符串方法名连接（容易出错）
func _ready():
    button.pressed.connect("on_button_pressed")  # 方法名拼写错误不会报错
```

### 自定义信号设计
```gdscript
# 好的模式：提供完整上下文的信号
signal health_changed(current: float, maximum: float, change_amount: float)
signal item_collected(item: ItemData, collector: Node)
signal level_completed(level_index: int, time_taken: float, score: int)

# 信号发射的最佳实践
func take_damage(amount: float):
    var old_health = current_health
    current_health = max(0, current_health - amount)
    
    health_changed.emit(current_health, max_health, old_health - current_health)
    
    if current_health <= 0:
        died.emit()
```

## 输入处理模式

### 输入映射使用
```gdscript
# 好的模式：使用输入映射
extends CharacterBody2D

@export var speed: float = 300.0

func _physics_process(delta):
    var direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    velocity = direction * speed
    move_and_slide()

func _unhandled_input(event):
    if event.is_action_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

# 好的模式：自定义输入处理
func _input(event):
    if not event.is_action_type():
        return
    
    if event.is_action("attack"):
        _handle_attack()
    elif event.is_action("interact"):
        _handle_interaction()
```

## 资源管理模式

### 资源加载和缓存
```gdscript
# 好的模式：预加载和缓存资源
extends Node

# 预加载常用资源
@onready var _bullet_scene = preload("res://scenes/Bullet.tscn")
@onready var _explosion_scene = preload("res://scenes/Explosion.tscn")

# 动态加载资源
var _loaded_resources: Dictionary = {}

func load_texture(path: String) -> Texture2D:
    if _loaded_resources.has(path):
        return _loaded_resources[path]
    
    var texture = load(path) as Texture2D
    if texture:
        _loaded_resources[path] = texture
    else:
        push_error("Failed to load texture: " + path)
    
    return texture

# 资源清理
func cleanup_resources():
    for resource in _loaded_resources.values():
        if resource and resource is Resource:
            resource = null
    _loaded_resources.clear()
```

### 场景实例化模式
```gdscript
# 好的模式：场景实例化工厂
class_name SceneFactory
extends Node

static func create_player(position: Vector2) -> Player:
    var player_scene = preload("res://scenes/Player.tscn")
    var player = player_scene.instantiate() as Player
    player.global_position = position
    return player

static func create_enemy(enemy_type: String, position: Vector2) -> Enemy:
    var scene_path = "res://scenes/enemies/" + enemy_type + ".tscn"
    var enemy_scene = load(scene_path)
    if enemy_scene:
        var enemy = enemy_scene.instantiate() as Enemy
        enemy.global_position = position
        return enemy
    return null

# 使用示例
func spawn_enemy():
    var enemy = SceneFactory.create_enemy("goblin", spawn_position)
    if enemy:
        add_child(enemy)
        enemies.append(enemy)
```

## 动画和状态机模式

### 动画控制
```gdscript
# 好的模式：结构化的动画控制
extends CharacterBody2D

@onready var _animation_player = $AnimationPlayer
@onready var _sprite = $Sprite2D

enum State { IDLE, RUNNING, JUMPING, FALLING, ATTACKING }

var current_state: State = State.IDLE

func _physics_process(delta):
    var new_state = _determine_state()
    if new_state != current_state:
        _change_state(new_state)

func _change_state(new_state: State):
    current_state = new_state
    match current_state:
        State.IDLE:
            _animation_player.play("idle")
        State.RUNNING:
            _animation_player.play("run")
        State.JUMPING:
            _animation_player.play("jump")
        State.FALLING:
            _animation_player.play("fall")
        State.ATTACKING:
            _animation_player.play("attack")

func _determine_state() -> State:
    if not is_on_floor():
        return State.JUMPING if velocity.y < 0 else State.FALLING
    elif abs(velocity.x) > 10:
        return State.RUNNING
    else:
        return State.IDLE
```

## 数据管理模式

### 游戏状态管理
```gdscript
# 好的模式：单例游戏状态管理器
extends Node

signal game_state_changed(old_state: GameState, new_state: GameState)

enum GameState { MENU, PLAYING, PAUSED, GAME_OVER }

var current_state: GameState = GameState.MENU:
    set = _set_game_state

var player_data: Dictionary = {}
var level_data: Dictionary = {}
var game_settings: Dictionary = {}

func _set_game_state(new_state: GameState):
    var old_state = current_state
    current_state = new_state
    game_state_changed.emit(old_state, new_state)
    
    match new_state:
        GameState.MENU:
            _handle_menu_state()
        GameState.PLAYING:
            _handle_playing_state()
        GameState.PAUSED:
            _handle_paused_state()
        GameState.GAME_OVER:
            _handle_game_over_state()

# 数据持久化
func save_game():
    var save_data = {
        "player_data": player_data,
        "level_data": level_data,
        "current_level": current_level_index
    }
    
    var file = FileAccess.open("user://savegame.dat", FileAccess.WRITE)
    if file:
        file.store_var(save_data)
        file.close()

func load_game():
    var file = FileAccess.open("user://savegame.dat", FileAccess.READ)
    if file:
        var save_data = file.get_var()
        file.close()
        
        player_data = save_data.get("player_data", {})
        level_data = save_data.get("level_data", {})
        current_level_index = save_data.get("current_level", 0)
```

## 调试和日志模式

### 结构化日志
```gdscript
# 好的模式：结构化的日志系统
class_name GameLogger
extends Node

enum LogLevel { DEBUG, INFO, WARNING, ERROR }

var log_level: LogLevel = LogLevel.INFO

func _ready():
    # 可以从设置中读取日志级别
    if OS.has_feature("debug"):
        log_level = LogLevel.DEBUG

func debug(message: String):
    if log_level <= LogLevel.DEBUG:
        print("[DEBUG] [%s] %s" % [Time.get_datetime_string_from_system(), message])

func info(message: String):
    if log_level <= LogLevel.INFO:
        print("[INFO] [%s] %s" % [Time.get_datetime_string_from_system(), message])

func warning(message: String):
    if log_level <= LogLevel.WARNING:
        print("[WARNING] [%s] %s" % [Time.get_datetime_string_from_system(), message])

func error(message: String):
    if log_level <= LogLevel.ERROR:
        print("[ERROR] [%s] %s" % [Time.get_datetime_string_from_system(), message])
        push_error(message)

# 使用示例
func take_damage(amount: float):
    GameLogger.debug("Taking damage: " + str(amount))
    
    current_health -= amount
    if current_health <= 0:
        GameLogger.info("Player died")
        died.emit()
    else:
        GameLogger.warning("Player health low: " + str(current_health))
```

## 错误处理模式

### 防御性编程
```gdscript
# 好的模式：安全的API调用
func get_node_safe(path: String, parent: Node = self) -> Node:
    var node = parent.get_node_or_null(path)
    if not node:
        push_error("Node not found at path: " + str(path))
    return node

func call_method_safe(object: Object, method_name: String, args: Array = []):
    if not object:
        push_error("Object is null, cannot call method: " + method_name)
        return null
    
    if not object.has_method(method_name):
        push_error("Method not found: " + method_name)
        return null
    
    return object.callv(method_name, args)

# 使用示例
func setup_enemy():
    var enemy_node = get_node_safe("Enemy")
    if enemy_node:
        call_method_safe(enemy_node, "set_difficulty", [current_difficulty])
```

### 类型安全模式
```gdscript
# 好的模式：类型安全的转换
func get_player_character() -> Player:
    var player_node = get_node_or_null("../Player")
    if not player_node:
        return null
    
    var player = player_node as Player
    if not player:
        push_error("Player node is not of type Player")
        return null
    
    return player

# 好的模式：使用类型检查
func process_collision(collision: KinematicCollision2D):
    var collider = collision.get_collider()
    if collider:
        if collider is Enemy:
            _handle_enemy_collision(collider as Enemy)
        elif collider is Item:
            _handle_item_collection(collider as Item)
        elif collider is StaticBody2D:
            _handle_wall_collision(collider as StaticBody2D)
```