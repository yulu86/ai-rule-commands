# Godot组件设计指南

## 组件设计原则

### 1. 单一职责原则
每个组件只负责一个明确的功能。

### 2. 松耦合设计
组件间通过信号通信，避免直接引用。

### 3. 可重用性
设计通用的组件，可在不同实体间共享。

### 4. 可配置性
使用导出变量让组件可配置。

## 基础组件模板

### 组件基类

```gdscript
# Component.gd - 所有组件的基类
extends Node

class_name Component

signal component_initialized
signal component_activated
signal component_deactivated

var is_active: bool = true
var owner_entity: Node

func _ready():
    owner_entity = get_parent()
    initialize()

func initialize():
    """子类重写此方法进行初始化"""
    component_initialized.emit()

func activate():
    is_active = true
    component_activated.emit()

func deactivate():
    is_active = false
    component_deactivated.emit()

func get_component(component_name: String) -> Component:
    """获取兄弟组件"""
    if owner_entity:
        return owner_entity.get_node_or_null(component_name) as Component
    return null

func send_signal(signal_name: String, args: Array = []):
    """向所有兄弟组件发送信号"""
    if owner_entity:
        owner_entity.emit_signal(signal_name, args)
```

## 核心组件类型

### 1. 生命值组件 (Health Component)

```gdscript
# HealthComponent.gd
extends Component
class_name HealthComponent

signal health_changed(current: int, maximum: int)
signal health_depleted
signal damage_received(amount: int, damage_type: String)
signal healing_received(amount: int)

@export var max_health: int = 100
@export var current_health: int = 100
@export var damage_resistance: float = 0.0  # 伤害抗性 0-1
@export var regeneration_rate: float = 0.0  # 每秒回复量

var is_invulnerable: bool = false
var damage_over_time: Array = []  # 持续伤害效果

enum DamageType {
    PHYSICAL,
    MAGICAL,
    FIRE,
    ICE,
    POISON
}

func initialize():
    super.initialize()
    current_health = max_health
    _setup_regeneration()

func take_damage(amount: int, damage_type: DamageType = DamageType.PHYSICAL, source: Node = null):
    if is_invulnerable or not is_active:
        return
    
    # 应用抗性
    var actual_damage = int(amount * (1.0 - damage_resistance))
    actual_damage = max(0, actual_damage)
    
    current_health -= actual_damage
    current_health = max(0, current_health)
    
    damage_received.emit(actual_damage, DamageType.keys()[damage_type])
    health_changed.emit(current_health, max_health)
    
    if current_health <= 0:
        health_depleted.emit()

func heal(amount: int):
    if not is_active:
        return
    
    var old_health = current_health
    current_health = min(current_health + amount, max_health)
    var actual_healing = current_health - old_health
    
    healing_received.emit(actual_healing)
    health_changed.emit(current_health, max_health)

func add_damage_over_time(amount_per_second: float, duration: float, damage_type: DamageType):
    var dot = {
        "amount": amount_per_second,
        "duration": duration,
        "type": damage_type,
        "time_left": duration
    }
    damage_over_time.append(dot)

func remove_damage_over_time(damage_type: DamageType):
    damage_over_time = damage_over_time.filter(func(dot): return dot.type != damage_type)

func set_invulnerable(invulnerable: bool):
    is_invulnerable = invulnerable

func _setup_regeneration():
    if regeneration_rate > 0:
        var timer = Timer.new()
        timer.wait_time = 1.0
        timer.timeout.connect(_regenerate)
        timer.autostart = true
        add_child(timer)

func _regenerate():
    if is_active and current_health < max_health:
        heal(int(regeneration_rate))

func _process(delta):
    # 处理持续伤害
    for i in range(damage_over_time.size() - 1, -1, -1):
        var dot = damage_over_time[i]
        dot.time_left -= delta
        
        if dot.time_left <= 0:
            damage_over_time.remove_at(i)
        else:
            take_damage(int(dot.amount * delta), dot.type)
```

### 2. 移动组件 (Movement Component)

```gdscript
# MovementComponent.gd
extends Component
class_name MovementComponent

signal movement_started(direction: Vector2)
signal movement_stopped()
signal position_changed(new_position: Vector2)
signal speed_changed(new_speed: float)

@export var base_speed: float = 200.0
@export var acceleration: float = 1000.0
@export var friction: float = 900.0
@export var max_fall_speed: float = 1000.0
@export var jump_impulse: float = 400.0

@export var can_jump: bool = true
@export var can_double_jump: bool = false
@export var can_dash: bool = false
@export var can_wall_slide: bool = false

var current_speed: float
var velocity: Vector2 = Vector2.ZERO
var is_moving: bool = false
var is_jumping: bool = false
var jumps_remaining: int = 0
var last_move_direction: Vector2 = Vector2.ZERO

# 修饰符
var speed_multipliers: Array[float] = [1.0]
var movement_modifiers: Dictionary = {}

func initialize():
    super.initialize()
    current_speed = base_speed
    jumps_remaining = 1 if can_jump else 0

func move(direction: Vector2, delta: float):
    if not is_active:
        return
    
    direction = direction.normalized()
    
    # 应用移动修饰符
    for modifier in movement_modifiers.values():
        direction = modifier.apply(direction, delta)
    
    # 计算目标速度
    var target_velocity = direction * get_effective_speed()
    
    # 应用加速/减速
    if direction.length() > 0.1:
        velocity = velocity.move_toward(target_velocity, acceleration * delta)
        last_move_direction = direction
        
        if not is_moving:
            is_moving = true
            movement_started.emit(direction)
    else:
        velocity = velocity.move_toward(Vector2.ZERO, friction * delta)
        
        if is_moving and velocity.length() < 10.0:
            is_moving = false
            movement_stopped.emit()
    
    # 应用移动
    if owner_entity and owner_entity is CharacterBody2D:
        _apply_physics_movement(delta)
    elif owner_entity:
        _apply_simple_movement(delta)
    
    position_changed.emit(owner_entity.global_position)

func jump():
    if not is_active or not can_jump:
        return
    
    if jumps_remaining > 0:
        velocity.y = -jump_impulse
        jumps_remaining -= 1
        is_jumping = true

func double_jump():
    if not is_active or not can_double_jump:
        return
    
    if jumps_remaining > 0:
        velocity.y = -jump_impulse * 0.8  # 二段跳稍弱
        jumps_remaining -= 1

func dash(direction: Vector2, dash_speed: float, dash_duration: float):
    if not is_active or not can_dash:
        return
    
    var dash_modifier = DashModifier.new(direction, dash_speed, dash_duration)
    add_movement_modifier("dash", dash_modifier)

func wall_slide():
    if not is_active or not can_wall_slide:
        return
    
    velocity.y = min(velocity.y, 100.0)  # 限制下落速度

func get_effective_speed() -> float:
    var speed = current_speed
    for multiplier in speed_multipliers:
        speed *= multiplier
    return speed

func add_speed_modifier(multiplier: float):
    speed_multipliers.append(multiplier)
    speed_changed.emit(get_effective_speed())

func remove_speed_modifier(multiplier: float):
    speed_multipliers.erase(multiplier)
    speed_changed.emit(get_effective_speed())

func add_movement_modifier(name: String, modifier: MovementModifier):
    movement_modifiers[name] = modifier

func remove_movement_modifier(name: String):
    movement_modifiers.erase(name)

func reset_jumps():
    jumps_remaining = (1 if can_jump else 0) + (1 if can_double_jump else 0)

func _apply_physics_movement(delta: float):
    var character_body = owner_entity as CharacterBody2D
    
    # 应用重力
    if not character_body.is_on_floor():
        velocity.y += character_body.gravity * delta
        velocity.y = min(velocity.y, max_fall_speed)
    else:
        reset_jumps()
        is_jumping = false
    
    character_body.velocity = velocity
    character_body.move_and_slide()
    velocity = character_body.velocity

func _apply_simple_movement(delta: float):
    owner_entity.global_position += velocity * delta

# 移动修饰符基类
class MovementModifier:
    func apply(direction: Vector2, delta: float) -> Vector2:
        return direction

# 冲刺修饰符
class DashModifier extends MovementModifier:
    var dash_direction: Vector2
    var dash_speed: float
    var duration: float
    var time_left: float
    
    func _init(dir: Vector2, speed: float, dur: float):
        dash_direction = dir.normalized()
        dash_speed = speed
        duration = dur
        time_left = dur
    
    func apply(direction: Vector2, delta: float) -> Vector2:
        if time_left > 0:
            time_left -= delta
            return dash_direction
        return direction
```

### 3. 动画组件 (Animation Component)

```gdscript
# AnimationComponent.gd
extends Component
class_name AnimationComponent

signal animation_started(name: String)
signal animation_finished(name: String)
signal animation_changed(from: String, to: String)

@export var animation_player_path: NodePath = "AnimationPlayer"
@export var auto_play: bool = true

var animation_player: AnimationPlayer
var current_animation: String = ""
var animation_states: Dictionary = {}
var animation_queue: Array[String] = []

# 动画状态映射
var state_animations: Dictionary = {
    "idle": "idle",
    "walk": "walk",
    "run": "run",
    "jump": "jump",
    "fall": "fall",
    "attack": "attack",
    "hurt": "hurt",
    "death": "death"
}

func initialize():
    super.initialize()
    animation_player = get_node(animation_player_path)
    
    if not animation_player:
        push_error("AnimationComponent: AnimationPlayer not found at " + animation_player_path)
        return
    
    animation_player.animation_finished.connect(_on_animation_finished)
    
    if auto_play:
        play("idle")

func play(animation_name: String, blend_time: float = -1):
    if not animation_player or not is_active:
        return
    
    if not animation_player.has_animation(animation_name):
        push_warning("AnimationComponent: Animation '" + animation_name + "' not found")
        return
    
    var previous_animation = current_animation
    
    if blend_time >= 0:
        animation_player.play(animation_name, blend_time)
    else:
        animation_player.play(animation_name)
    
    current_animation = animation_name
    animation_started.emit(animation_name)
    
    if previous_animation != animation_name:
        animation_changed.emit(previous_animation, animation_name)

func play_with_queue(animation_name: String, priority: int = 0):
    """播放动画，如果有更高优先级动画则排队"""
    if not animation_player or not is_active:
        return
    
    if current_animation == animation_name:
        return
    
    # 简单优先级系统
    if priority > _get_current_priority():
        animation_queue.append(animation_name)
        if animation_queue.size() == 1:
            _play_next_queued_animation()
    else:
        play(animation_name)

func play_by_state(state_name: String):
    """根据状态播放对应动画"""
    var animation_name = state_animations.get(state_name, "idle")
    play(animation_name)

func set_speed(speed_scale: float):
    if animation_player:
        animation_player.speed_scale = speed_scale

func is_playing() -> bool:
    if animation_player:
        return animation_player.is_playing()
    return false

func get_current_animation() -> String:
    return current_animation

func get_current_animation_length() -> float:
    if animation_player and current_animation != "":
        return animation_player.get_animation(current_animation).length
    return 0.0

func get_current_animation_position() -> float:
    if animation_player:
        return animation_player.current_animation_position
    return 0.0

func add_animation_state(state_name: String, animation_name: String):
    """添加状态到动画的映射"""
    state_animations[state_name] = animation_name

func create_transition(from_anim: String, to_anim: String, duration: float = 0.2):
    """创建动画过渡"""
    if animation_player:
        animation_player.play(to_anim, -1.0, from_anim, duration)

func _play_next_queued_animation():
    if not animation_queue.is_empty():
        var next_animation = animation_queue.pop_front()
        play(next_animation)

func _on_animation_finished(anim_name: String):
    animation_finished.emit(anim_name)
    
    if not animation_queue.is_empty():
        _play_next_queued_animation()
    elif current_animation == anim_name:
        # 动画结束后回到默认状态
        play("idle")

func _get_current_priority() -> int:
    """获取当前动画的优先级"""
    match current_animation:
        "attack", "skill":
            return 2
        "hurt":
            return 1
        _:
            return 0
```

### 4. 战斗组件 (Combat Component)

```gdscript
# CombatComponent.gd
extends Component
class_name CombatComponent

signal attack_started(attack_data: Dictionary)
signal attack_hit(target: Node, damage: int)
signal attack_completed
signal ability_used(ability_name: String)

@export var base_attack_damage: int = 10
@export var attack_speed: float = 1.0  # 攻击速度倍率
@export var attack_range: float = 50.0
@export var critical_chance: float = 0.1
@export var critical_multiplier: float = 2.0

var is_attacking: bool = false
var attack_cooldown: float = 0.0
var current_target: Node

# 技能系统
var abilities: Dictionary = {}
var ability_cooldowns: Dictionary = {}

func initialize():
    super.initialize()
    _setup_default_abilities()

func attack(target: Node = null) -> bool:
    if not is_active or is_attacking or attack_cooldown > 0:
        return false
    
    current_target = target or _find_nearest_enemy()
    if not current_target:
        return false
    
    # 检查攻击范围
    if owner_entity.global_position.distance_to(current_target.global_position) > attack_range:
        return false
    
    _perform_attack(current_target)
    return true

func use_ability(ability_name: String, target: Node = null) -> bool:
    if not is_active or not abilities.has(ability_name):
        return false
    
    if ability_cooldowns.has(ability_name) and ability_cooldowns[ability_name] > 0:
        return false
    
    var ability = abilities[ability_name]
    _execute_ability(ability, target)
    return true

func add_attack_modifier(modifier: float, duration: float = -1):
    """添加攻击力修饰符"""
    if duration > 0:
        var timer = Timer.new()
        timer.wait_time = duration
        timer.timeout.connect(_remove_attack_modifier.bind(modifier))
        timer.autostart = true
        add_child(timer)
    
    base_attack_damage = int(base_attack_damage * modifier)

func _setup_default_abilities():
    # 添加基础技能
    abilities["power_attack"] = {
        "name": "Power Attack",
        "damage_multiplier": 1.5,
        "cooldown": 3.0,
        "range_multiplier": 1.2,
        "cost": 10
    }
    
    abilities["whirlwind"] = {
        "name": "Whirlwind",
        "damage_multiplier": 0.8,
        "cooldown": 5.0,
        "area_radius": 100.0,
        "cost": 20
    }

func _perform_attack(target: Node):
    is_attacking = true
    attack_cooldown = 1.0 / attack_speed
    
    var damage = _calculate_damage()
    var attack_data = {
        "damage": damage,
        "target": target,
        "is_critical": damage > base_attack_damage,
        "attack_type": "melee"
    }
    
    attack_started.emit(attack_data)
    
    # 应用伤害
    if target.has_node("HealthComponent"):
        var health = target.get_node("HealthComponent")
        health.take_damage(damage, HealthComponent.DamageType.PHYSICAL, owner_entity)
        attack_hit.emit(target, damage)
    
    # 播放攻击动画
    if owner_entity.has_node("AnimationComponent"):
        var anim = owner_entity.get_node("AnimationComponent")
        anim.play("attack")
    
    await get_tree().create_timer(0.5).timeout
    
    is_attacking = false
    attack_completed.emit()

func _execute_ability(ability: Dictionary, target: Node = null):
    ability_used.emit(ability.name)
    ability_cooldowns[ability.name] = ability.cooldown
    
    match ability.name:
        "Power Attack":
            _execute_power_attack(ability, target)
        "Whirlwind":
            _execute_whirlwind(ability)
        # 其他技能...

func _execute_power_attack(ability: Dictionary, target: Node):
    var damage = int(base_attack_damage * ability.damage_multiplier)
    
    if target and target.has_node("HealthComponent"):
        var health = target.get_node("HealthComponent")
        health.take_damage(damage, HealthComponent.DamageType.PHYSICAL, owner_entity)

func _execute_whirlwind(ability: Dictionary):
    var damage = int(base_attack_damage * ability.damage_multiplier)
    var enemies = _get_enemies_in_radius(ability.area_radius)
    
    for enemy in enemies:
        if enemy.has_node("HealthComponent"):
            var health = enemy.get_node("HealthComponent")
            health.take_damage(damage, HealthComponent.DamageType.PHYSICAL, owner_entity)

func _calculate_damage() -> int:
    var damage = base_attack_damage
    
    # 暴击判定
    if randf() < critical_chance:
        damage = int(damage * critical_multiplier)
    
    # 随机浮动
    damage = int(damage * randf_range(0.9, 1.1))
    
    return damage

func _find_nearest_enemy() -> Node:
    var enemies = get_tree().get_nodes_in_group("enemy")
    var nearest_enemy = null
    var nearest_distance = INF
    
    for enemy in enemies:
        var distance = owner_entity.global_position.distance_to(enemy.global_position)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_enemy = enemy
    
    return nearest_enemy

func _get_enemies_in_radius(radius: float) -> Array:
    var enemies = []
    var all_enemies = get_tree().get_nodes_in_group("enemy")
    
    for enemy in all_enemies:
        var distance = owner_entity.global_position.distance_to(enemy.global_position)
        if distance <= radius:
            enemies.append(enemy)
    
    return enemies

func _process(delta):
    if attack_cooldown > 0:
        attack_cooldown -= delta
    
    # 更新技能冷却
    for ability_name in ability_cooldowns:
        if ability_cooldowns[ability_name] > 0:
            ability_cooldowns[ability_name] -= delta

func _remove_attack_modifier(modifier: float):
    base_attack_damage = int(base_attack_damage / modifier)
```

## 组件通信模式

### 1. 信号通信

```gdscript
# 组件间通过信号通信
health_component.health_changed.connect(_on_health_changed)

func _on_health_changed(current: int, maximum: int):
    # 更新UI显示
    if owner_entity.has_node("UIComponent"):
        var ui = owner_entity.get_node("UIComponent")
        ui.update_health_bar(current, maximum)
```

### 2. 事件总线

```gdscript
# EventBus.gd - 全局事件总线
extends Node

signal player_died
signal level_completed
signal enemy_spawned(enemy: Node)
signal item_collected(item: Node)

# 组件发送事件
EventBus.player_died.emit()

# 组件监听事件
EventBus.enemy_spawned.connect(_on_enemy_spawned)
```

### 3. 组件容器

```gdscript
# Entity.gd - 实体基类，管理所有组件
extends Node2D

var components: Dictionary = {}

func _ready():
    _register_components()

func _register_components():
    for child in get_children():
        if child is Component:
            components[child.name] = child

func get_component(component_name: String) -> Component:
    return components.get(component_name)

func broadcast_event(event_name: String, data: Dictionary = {}):
    for component in components.values():
        if component.has_method(event_name):
            component.call(event_name, data)
```

## 组件性能优化

### 1. 组件池化

```gdscript
# ComponentPool.gd
extends Node

var component_pools: Dictionary = {}

func get_component(component_scene: PackedScene) -> Component:
    var component_type = component_scene.resource_path.get_basename()
    
    if not component_pools.has(component_type):
        component_pools[component_type] = []
    
    var pool = component_pools[component_type]
    
    if pool.is_empty():
        return component_scene.instantiate()
    else:
        return pool.pop_back()

func return_component(component: Component):
    var component_type = component.scene_file_path.get_basename()
    
    if not component_pools.has(component_type):
        component_pools[component_type] = []
    
    component_pools[component_type].append(component)
    component.get_parent().remove_child(component)
```

### 2. 条件更新

```gdscript
# 只在需要时更新组件
func _process(delta):
    if not is_active:
        return
    
    if owner_entity and _should_update():
        _update_component(delta)

func _should_update() -> bool:
    # 距离玩家很远时不更新
    var player = get_tree().get_first_node_in_group("player")
    if player:
        var distance = owner_entity.global_position.distance_to(player.global_position)
        return distance < 500.0
    
    return true
```

## 组件测试策略

### 1. 单元测试

```gdscript
# 测试生命值组件
func test_health_component():
    var entity = Node2D.new()
    var health = HealthComponent.new()
    entity.add_child(health)
    
    health.initialize()
    assert(health.current_health == health.max_health)
    
    health.take_damage(50)
    assert(health.current_health == 50)
```

### 2. 集成测试

```gdscript
# 测试组件协作
func test_combat_flow():
    var player = _create_test_player()
    var enemy = _create_test_enemy()
    
    # 攻击流程测试
    var success = player.get_component("CombatComponent").attack(enemy)
    assert(success)
    
    var enemy_health = enemy.get_component("HealthComponent").current_health
    assert(enemy_health < enemy.get_component("HealthComponent").max_health)
```

## 组件文档化

### 组件接口文档

```gdscript
# HealthComponent.gd 文档注释
##
## 管理实体的生命值系统
##
## 功能：
## - 处理伤害和治疗效果
## - 支持不同伤害类型和抗性
## - 持续伤害效果
## - 生命值回复机制
##
## 信号：
## - health_changed(current, maximum): 生命值改变时触发
## - health_depleted: 生命值耗尽时触发
## - damage_received(amount, type): 受到伤害时触发
## - healing_received(amount): 接受治疗时触发
##
class_name HealthComponent
extends Component
```