# Godot架构模式详解

## 1. 单例模式 (Singleton Pattern)

### 使用场景
- 全局游戏状态管理
- 资源管理器
- 输入管理器
- 音频管理器

### 实现示例

```gdscript
# GameManager.gd
extends Node

signal game_state_changed(old_state: GameState, new_state: GameState)
signal score_changed(new_score: int)
signal level_completed(level_number: int)

enum GameState {
    MENU,
    PLAYING,
    PAUSED,
    GAME_OVER,
    LEVEL_COMPLETE
}

@export var current_state: GameState = GameState.MENU
@export var current_score: int = 0
@export var current_level: int = 1

# 自动加载为单例
func _ready():
    process_mode = Node.PROCESS_MODE_ALWAYS
    InputMap.action_pressed("pause").connect(_toggle_pause)

func _toggle_pause():
    if current_state == GameState.PLAYING:
        change_state(GameState.PAUSED)
    elif current_state == GameState.PAUSED:
        change_state(GameState.PLAYING)

func change_state(new_state: GameState):
    var old_state = current_state
    current_state = new_state
    game_state_changed.emit(old_state, new_state)
    
    # 状态改变时的处理逻辑
    match new_state:
        GameState.PLAYING:
            get_tree().paused = false
        GameState.PAUSED:
            get_tree().paused = true
        GameState.GAME_OVER:
            _handle_game_over()

func add_score(points: int):
    current_score += points
    score_changed.emit(current_score)
```

### 优缺点
- **优点**: 全局访问，状态集中管理
- **缺点**: 全局状态可能导致耦合，测试困难

## 2. 组件实体模式 (Component Entity Pattern)

### 使用场景
- 玩家角色
- 敌人实体
- 可交互对象

### 实现示例

```gdscript
# Entity.gd - 基础实体类
extends Node2D

signal component_added(component_name: String)
signal component_removed(component_name: String)

var components: Dictionary = {}

func _ready():
    # 自动注册子节点为组件
    for child in get_children():
        if child.has_method("initialize"):
            add_component(child.name, child)

func add_component(name: String, component: Node):
    components[name] = component
    component_added.emit(name)

func get_component(name: String) -> Node:
    return components.get(name)

func has_component(name: String) -> bool:
    return components.has(name)

# HealthComponent.gd
extends Node

signal health_changed(current_health: int, max_health: int)
signal health_depleted
signal damage_taken(amount: int)
signal healing_received(amount: int)

@export var max_health: int = 100
@export var current_health: int = 100

func initialize():
    current_health = max_health

func take_damage(amount: int):
    amount = min(amount, current_health)
    current_health -= amount
    damage_taken.emit(amount)
    health_changed.emit(current_health, max_health)
    
    if current_health <= 0:
        health_depleted.emit()

func heal(amount: int):
    var old_health = current_health
    current_health = min(current_health + amount, max_health)
    var actual_healing = current_health - old_health
    healing_received.emit(actual_healing)
    health_changed.emit(current_health, max_health)

# MovementComponent.gd
extends Node

signal position_changed(new_position: Vector2)
signal movement_started()
signal movement_stopped()

@export var speed: float = 200.0
@export var acceleration: float = 1000.0
@export var friction: float = 900.0

var velocity: Vector2 = Vector2.ZERO
var is_moving: bool = false

func initialize():
    pass

func move_direction(direction: Vector2, delta: float):
    direction = direction.normalized()
    
    if direction.length() > 0.1:
        velocity = velocity.move_toward(direction * speed, acceleration * delta)
        if not is_moving:
            is_moving = true
            movement_started.emit()
    else:
        velocity = velocity.move_toward(Vector2.ZERO, friction * delta)
        if is_moving and velocity.length() < 10.0:
            is_moving = false
            movement_stopped.emit()
    
    if velocity.length() > 0.1:
        owner.global_position += velocity * delta
        position_changed.emit(owner.global_position)
```

### 优缺点
- **优点**: 模块化，可重用，易于扩展
- **缺点**: 组件间通信复杂，需要额外协调

## 3. 命令模式 (Command Pattern)

### 使用场景
- 输入处理
- 撤销/重做功能
- AI行为队列

### 实现示例

```gdscript
# Command.gd - 命令基类
extends Resource

class_name Command

func execute(context: Node) -> void:
    push_error("Command.execute() must be implemented by subclass")

func undo(context: Node) -> void:
    pass

# MoveCommand.gd
extends Resource
class_name MoveCommand

var direction: Vector2
var previous_position: Vector2

func _init(dir: Vector2):
    direction = dir

func execute(context: Node) -> void:
    previous_position = context.global_position
    context.global_position += direction * 32  # 假设网格移动

func undo(context: Node) -> void:
    context.global_position = previous_position

# InputHandler.gd
extends Node

var command_history: Array[Command] = []
@export var max_history_size: int = 100

func _input(event):
    if not event.is_pressed():
        return
        
    var command: Command = null
    
    match event.as_text():
        "W", "Up":
            command = MoveCommand.new(Vector2.UP)
        "S", "Down":
            command = MoveCommand.new(Vector2.DOWN)
        "A", "Left":
            command = MoveCommand.new(Vector2.LEFT)
        "D", "Right":
            command = MoveCommand.new(Vector2.RIGHT)
        "Z":
            _undo_last_command()
            return
    
    if command and get_player():
        execute_command(command, get_player())

func execute_command(command: Command, context: Node):
    command.execute(context)
    _add_to_history(command)

func _add_to_history(command: Command):
    command_history.append(command)
    if command_history.size() > max_history_size:
        command_history.pop_front()

func _undo_last_command():
    if command_history.is_empty():
        return
    
    var command = command_history.pop_back()
    if get_player():
        command.undo(get_player())

func get_player() -> Node:
    return get_tree().get_first_node_in_group("player")
```

## 4. 状态机模式 (State Machine Pattern)

### 使用场景
- AI行为控制
- 游戏流程管理
- UI状态管理

### 实现示例

```gdscript
# State.gd - 状态基类
extends Resource

class_name State

signal state_entered()
signal state_exited()

func enter(host: Node) -> void:
    state_entered.emit()

func exit(host: Node) -> void:
    state_exited.emit()

func update(host: Node, delta: float) -> void:
    pass

func handle_input(host: Node, event: InputEvent) -> void:
    pass

# StateMachine.gd
extends Node

signal state_changed(previous_state: State, current_state: State)

@export var initial_state: State
var current_state: State
var states: Dictionary = {}

func _ready():
    # 注册所有子节点状态
    for child in get_children():
        if child is State:
            states[child.name] = child
    
    if initial_state:
        change_state(initial_state)

func change_state(new_state: State):
    if current_state:
        current_state.exit(self)
    
    var previous_state = current_state
    current_state = new_state
    current_state.enter(self)
    
    state_changed.emit(previous_state, current_state)

func add_state(name: String, state: State):
    states[name] = state

func get_state(name: String) -> State:
    return states.get(name)

func _process(delta):
    if current_state:
        current_state.update(self, delta)

func _input(event):
    if current_state:
        current_state.handle_input(self, event)

# PlayerIdleState.gd
extends State
class_name PlayerIdleState

func enter(host: Node) -> void:
    super.enter(host)
    # 播放空闲动画
    if host.has_node("AnimationPlayer"):
        host.get_node("AnimationPlayer").play("idle")

func handle_input(host: Node, event: InputEvent) -> void:
    super.handle_input(host, event)
    
    if event.is_action_pressed("move_left") or event.is_action_pressed("move_right"):
        host.change_state(host.get_state("Move"))

# PlayerMoveState.gd
extends State
class_name PlayerMoveState

var direction: int = 0

func enter(host: Node) -> void:
    super.enter(host)
    # 播放移动动画
    if host.has_node("AnimationPlayer"):
        host.get_node("AnimationPlayer").play("run")

func update(host: Node, delta: float) -> void:
    super.update(host, delta)
    
    # 处理移动逻辑
    host.velocity.x = direction * host.speed
    host.velocity.y += host.gravity * delta
    
    host.move_and_slide()
    
    # 检查是否停止移动
    if direction == 0 and abs(host.velocity.x) < 10:
        host.change_state(host.get_state("Idle"))

func handle_input(host: Node, event: InputEvent) -> void:
    super.handle_input(host, event)
    
    if event.is_action_pressed("move_left"):
        direction = -1
    elif event.is_action_pressed("move_right"):
        direction = 1
    elif event.is_action_released("move_left") and direction == -1:
        direction = 0
    elif event.is_action_released("move_right") and direction == 1:
        direction = 0
```

## 5. 工厂模式 (Factory Pattern)

### 使用场景
- 敌人生成
- 道具创建
- 场景实例化

### 实现示例

```gdscript
# EnemyFactory.gd
extends Node

class_name EnemyFactory

@export var enemy_scenes: Dictionary = {}
@export var spawn_points: Array[Node2D] = []

func _ready():
    # 注册敌人类型
    enemy_scenes["goblin"] = preload("res://scenes/enemies/Goblin.tscn")
    enemy_scenes["orc"] = preload("res://scenes/enemies/Orc.tscn")
    enemy_scenes["dragon"] = preload("res://scenes/enemies/Dragon.tscn")

func create_enemy(enemy_type: String, level: int = 1) -> Node:
    if not enemy_scenes.has(enemy_type):
        push_error("Unknown enemy type: " + enemy_type)
        return null
    
    var enemy_scene = enemy_scenes[enemy_type]
    var enemy = enemy_scene.instantiate()
    
    # 根据等级调整属性
    _configure_enemy(enemy, level)
    
    return enemy

func _configure_enemy(enemy: Node, level: int):
    if enemy.has_method("set_level"):
        enemy.set_level(level)
    
    # 调整血量、攻击力等属性
    if enemy.has_node("HealthComponent"):
        var health = enemy.get_node("HealthComponent")
        health.max_health *= (1.0 + level * 0.1)
        health.current_health = health.max_health

func spawn_enemy(enemy_type: String, spawn_point_index: int = -1, level: int = 1):
    var enemy = create_enemy(enemy_type, level)
    if not enemy:
        return null
    
    var spawn_point: Node2D
    
    if spawn_point_index >= 0 and spawn_point_index < spawn_points.size():
        spawn_point = spawn_points[spawn_point_index]
    else:
        # 随机选择生成点
        spawn_point = spawn_points.pick_random()
    
    enemy.global_position = spawn_point.global_position
    get_tree().current_scene.add_child(enemy)
    
    return enemy
```

## 架构组合策略

### 多模式组合

```gdscript
# Player.gd - 组合多种架构模式
extends CharacterBody2D

# 组件实体模式
@onready var health_component = $HealthComponent
@onready var movement_component = $MovementComponent
@onready var combat_component = $CombatComponent

# 状态机模式
@onready var state_machine = $StateMachine

# 命令模式 - 通过输入处理器
var input_handler: InputHandler

func _ready():
    # 初始化组件
    health_component.health_depleted.connect(_on_death)
    
    # 设置状态机初始状态
    state_machine.initial_state = state_machine.get_state("Idle")
    
    # 设置命令处理器
    input_handler = InputHandler.new()
    add_child(input_handler)
```

### 层次化架构

```
Presentation Layer (UI, Effects)
    ↓
Application Layer (Game Logic, State)
    ↓
Domain Layer (Entities, Components)
    ↓
Infrastructure Layer (Input, Audio, Network)
```