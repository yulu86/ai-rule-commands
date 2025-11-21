# Godot API 参考手册

## 核心节点类型

### Node (基类)
所有节点的基类，提供基础功能：
- **生命周期**: `_ready()`, `_process(delta)`, `_physics_process(delta)`
- **树操作**: `get_node()`, `find_child()`, `get_children()`
- **信号系统**: `connect()`, `disconnect()`, `emit_signal()`
- **组系统**: `add_to_group()`, `is_in_group()`, `get_tree().get_nodes_in_group()`

### Node2D (2D 节点基类)
2D 空间中的基础节点：
- **变换**: `position`, `rotation`, `scale`
- **层级**: `z_index`, `y_sort_enabled`
- **可见性**: `visible`, `modulate`
- **全局变换**: `global_position`, `global_rotation`, `global_scale`

### Node3D (3D 节点基类)
3D 空间中的基础节点：
- **变换**: `position`, `rotation_degrees`, `scale`
- **可见性**: `visible`
- **全局变换**: `global_position`, `global_rotation`, `global_transform`
- **层次管理**: `rotate_x()`, `rotate_y()`, `rotate_z()`

### Control (UI 节点基类)
UI 系统的基础节点：
- **布局**: `anchor_left`, `anchor_right`, `anchor_top`, `anchor_bottom`
- **尺寸**: `size`, `custom_minimum_size`
- **定位**: `position`, `global_position`
- **主题**: `theme`, `add_theme_color_override()`
- **焦点**: `grab_focus()`, `has_focus()`
- **鼠标**: `mouse_filter`, `gui_input`

## 物理节点

### CharacterBody2D/3D
角色控制专用物理体：
- **移动**: `move_and_slide()`, `move_and_collide()`
- **速度**: `velocity`, `linear_velocity`
- **物理属性**: `floor_snap_length`, `wall_min_slide_angle`
- **碰撞**: `get_last_slide_collision()`, `is_on_floor()`, `is_on_wall()`
- **平台**: `platform_on_leave`, `platform_floor_layers`

### RigidBody2D/3D
物理模拟实体：
- **力应用**: `apply_central_impulse()`, `apply_force()`
- **物理属性**: `mass`, `gravity_scale`, `friction`
- **运动状态**: `linear_velocity`, `angular_velocity`
- **休眠**: `sleeping`, `can_sleep`
- **接触**: `get_colliding_bodies()`

### Area2D/3D
区域检测节点：
- **重叠检测**: `get_overlapping_bodies()`, `get_overlapping_areas()`
- **监控**: `monitoring`, `monitorable`
- **碰撞层**: `collision_layer`, `collision_mask`
- **空间覆盖**: `space_override`

## 渲染节点

### Sprite2D/3D
精灵渲染节点：
- **纹理**: `texture`
- **区域**: `region_enabled`, `region_rect`
- **动画**: `frame`, `hframes`, `vframes`
- **材质**: `material`, `texture_filter`
- **居中**: `centered`, `offset`

### Label
文本显示节点：
- **文本**: `text`, `text_direction`
- **字体**: `theme_override_font_sizes`, `add_theme_font_size_override()`
- **对齐**: `horizontal_alignment`, `vertical_alignment`
- **自动换行**: `autowrap_mode`, `text_overrun_behavior`
- **效果**: `uppercase`, `add_color_override()`

### AnimatedSprite2D/3D
动画精灵节点：
- **精灵帧**: `sprite_frames`
- **动画**: `animation`, `frame`
- **播放**: `play()`, `stop()`, `is_playing()`
- **速度**: `speed_scale`
- **方向**: `flip_h`, `flip_v`

## 音频节点

### AudioStreamPlayer
基础音频播放器：
- **音频流**: `stream`
- **播放控制**: `play()`, `stop()`, `pause()`
- **音量**: `volume_db`
- **音调**: `pitch_scale`
- **循环**: `autoplay`, `loop`

### AudioStreamPlayer2D/3D
空间音频播放器：
- **位置音频**: `position`, `attenuation`
- **最大距离**: `max_distance`
- **范围**: `unit_db`, `unit_size`

## 动画节点

### AnimationPlayer
动画播放器：
- **动画库**: `animation_library`
- **播放控制**: `play()`, `stop()`, `pause()`
- **动画队列**: `queue()`
- **动画信息**: `current_animation`, `is_playing()`
- **动画方法**: `get_animation_list()`, `has_animation()`
- **方法调用**: `call_deferred()` for animation methods

### Tween
补间动画：
- **属性动画**: `tween_property()`, `tween_method()`
- **回调**: `tween_callback()`, `tween_interval()`
- **缓动**: `set_ease()`, `set_trans()`
- **并行/串行**: `parallel()`, `chain()`
- **循环**: `set_loops()`

## 相机节点

### Camera2D
2D 相机：
- **跟随**: `follow_smoothing`, `position_smoothing_enabled`
- **边界**: `limit_left`, `limit_right`, `limit_top`, `limit_bottom`
- **缩放**: `zoom`
- **视口**: `anchor_mode`

### Camera3D
3D 相机：
- **投影**: `projection`, `fov`, `size`
- **变换**: `global_transform`
- **裁剪**: `near`, `far`
- **效果**: `h_offset`, `v_offset`

## 输入系统

### 输入映射
```gdscript
# 检查按键状态
Input.is_action_pressed("ui_right")
Input.is_action_just_pressed("jump")
Input.is_action_just_released("fire")

# 获取输入强度
Input.get_action_strength("move_forward")
Input.get_axis("move_left", "move_right")
```

### 输入事件处理
```gdsharp
func _input(event):
    if event is InputEventKey:
        if event.pressed and event.keycode == KEY_SPACE:
            _jump()
    
    elif event is InputEventMouseButton:
        if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
            _handle_click(event.position)
```

## 常用工具方法

### 节点查找
```gdsharp
# 按路径查找
get_node("Player/Sprite")
$Player/Sprite  # 语法糖

# 按名称查找
find_child("Player")  # 递归查找
get_node_or_null("OptionalNode")  # 安全查找

# 按组查找
get_tree().get_nodes_in_group("enemies")
```

### 延迟执行
```gdsharp
# 下一帧执行
call_deferred("_delayed_method")

# 延迟执行
await get_tree().create_timer(2.0).timeout
# 或者
get_tree().create_timer(2.0).timeout.connect(_on_timeout)

# 帧结束等待
await get_tree().process_frame
```

### 场景管理
```gdsharp
# 场景切换
get_tree().change_scene_to_file("res://scenes/level_2.tscn")
get_tree().change_scene_to_packed(preload("res://scenes/menu.tscn"))

# 场景实例化
var enemy_scene = preload("res://scenes/enemy.tscn")
var enemy = enemy_scene.instantiate()
add_child(enemy)

# 场景树操作
get_tree().current_scene
get_tree().get_first_node_in_group("player")
```

## 信号系统

### 定义信号
```gdsharp
signal player_died
signal health_changed(new_health: int)
signal item_collected(item: Item, amount: int)
```

### 连接信号
```gdsharp
# 在编辑器连接（推荐）
# 或者在代码中连接
player.health_changed.connect(_on_player_health_changed)
button.pressed.connect(_on_button_pressed)

# 带参数的信号连接
item_collected.connect(_on_item_collected.bind("coins"))

# 一次性信号连接
some_signal.connect(_callback, CONNECT_ONE_SHOT)
```

### 发射信号
```gdsharp
# 发射信号
health_changed.emit(50)
player_died.emit()

# 带多个参数
item_collected.emit(power_up_item, 100)
```

## 资源系统

### 预加载 vs 动态加载
```gdsharp
# 预加载（推荐用于常用资源）
const PLAYER_SCENE = preload("res://scenes/player.tscn")
const BULLET_TEXTURE = preload("res://assets/bullet.png")

# 动态加载
var resource = load("res://data/player_stats.tres")
var scene = load("res://scenes/" + scene_name + ".tscn")
```

### 资源类型
- **PackedScene**: 场景资源
- **Texture**: 纹理资源
- **AudioStream**: 音频资源
- **Script**: 脚本资源
- **Font**: 字体资源
- **Theme**: UI主题资源

## 全局访问

### 单例节点
```gdsharp
# 访问内置单例
get_tree().root
get_tree().current_scene
get_tree().get_first_node_in_group("player")

# 自定义单例
GameManager.instance
AudioManager.play_sound("jump")
```

### 场景树全局操作
```gdsharp
# 查找根节点
get_tree().root.get_child(0)

# 递归查找节点
get_tree().get_nodes_in_group("enemies")
get_tree().get_first_node_in_group("player")
```