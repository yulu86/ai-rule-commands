extends CharacterBody2D

class_name Player

signal health_changed(new_health: int)
signal player_died
signal coin_collected(amount: int)

@export var speed: float = 300.0
@export var jump_velocity: float = -400.0
@export var max_health: int = 100

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var camera: Camera2D = $Camera2D

var health: int = 100
var is_jumping: bool = false
var is_attacking: bool = false
var coins: int = 0

enum State { IDLE, WALKING, JUMPING, ATTACKING, HURT }
var current_state: State = State.IDLE

const GRAVITY: float = 980.0
const COIN_SCENE = preload("res://scenes/coin.tscn")
const PLAYER_SOUNDS = preload("res://assets/player_sounds.tres")

func _ready():
    health = max_health
    add_to_group("player")
    setup_camera_limits()
    connect("health_changed", _on_health_changed)

func _physics_process(delta):
    handle_input()
    apply_gravity(delta)
    handle_movement(delta)
    handle_jump()
    handle_attack()
    move_and_slide()
    update_animation_state()
    check_boundaries()

func handle_input():
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity
        is_jumping = true
        play_jump_sound()
    
    if Input.is_action_just_pressed("attack") and not is_attacking:
        start_attack()
    
    var direction = Input.get_axis("move_left", "move_right")
    velocity.x = direction * speed

func apply_gravity(delta):
    if not is_on_floor():
        velocity.y += GRAVITY * delta
    else:
        is_jumping = false

func handle_movement(delta):
    if velocity.x != 0:
        sprite.flip_h = velocity.x < 0
        current_state = State.WALKING
    elif is_on_floor():
        current_state = State.IDLE

func handle_jump():
    if is_jumping:
        current_state = State.JUMPING

func handle_attack():
    if is_attacking:
        current_state = State.ATTACKING
        check_attack_hitbox()

func start_attack():
    is_attacking = true
    animation_player.play("attack")
    $AttackArea/CollisionShape2D.disabled = false
    await animation_player.animation_finished
    is_attacking = false
    $AttackArea/CollisionShape2D.disabled = true

func check_attack_hitbox():
    var bodies = $AttackArea.get_overlapping_bodies()
    for body in bodies:
        if body.is_in_group("enemies"):
            body.take_damage(25)
            create_hit_effect(body.global_position)

func take_damage(amount: int):
    if current_state == State.HURT:
        return
    
    health -= amount
    current_state = State.HURT
    health_changed.emit(health)
    
    if health <= 0:
        die()
    else:
        play_hurt_animation()
        await get_tree().create_timer(0.5).timeout
        if current_state == State.HURT:
            current_state = State.IDLE

func die():
    player_died.emit()
    set_process(false)
    set_physics_process(false)
    collision_shape.disabled = true
    animation_player.play("death")
    await animation_player.animation_finished
    queue_free()

func collect_coin():
    coins += 1
    coin_collected.emit(1)
    play_coin_sound()
    update_coin_ui()

func update_animation_state():
    match current_state:
        State.IDLE:
            animation_player.play("idle")
        State.WALKING:
            animation_player.play("walk")
        State.JUMPING:
            if is_jumping:
                animation_player.play("jump")
            else:
                animation_player.play("fall")
        State.ATTACKING:
            if not animation_player.is_playing():
                animation_player.play("attack")
        State.HURT:
            if not animation_player.is_playing():
                animation_player.play("hurt")

func play_jump_sound():
    $AudioStreamPlayer.stream = PLAYER_SOUNDS.jump_sound
    $AudioStreamPlayer.play()

func play_hurt_sound():
    $AudioStreamPlayer.stream = PLAYER_SOUNDS.hurt_sound
    $AudioStreamPlayer.play()

func play_coin_sound():
    $AudioStreamPlayer.stream = PLAYER_SOUNDS.coin_sound
    $AudioStreamPlayer.play()

func create_hit_effect(position: Vector2):
    var hit_effect = preload("res://effects/hit_effect.tscn").instantiate()
    get_tree().current_scene.add_child(hit_effect)
    hit_effect.global_position = position

func setup_camera_limits():
    if camera:
        camera.limit_left = -1000
        camera.limit_right = 1000
        camera.limit_top = -1000
        camera.limit_bottom = 1000

func check_boundaries():
    if global_position.y < get_viewport_rect().size.y + 100:
        take_damage(health)  # 掉出地图直接死亡

func update_coin_ui():
    var coin_label = get_tree().get_first_node_in_group("coin_ui")
    if coin_label:
        coin_label.text = "Coins: %d" % coins

func _on_health_changed(new_health: int):
    print("Player health: ", new_health)
    
    if new_health < max_health * 0.3:
        sprite.modulate = Color.RED
    else:
        sprite.modulate = Color.WHITE

func _on_coin_area_entered(area):
    if area.is_in_group("coin"):
        area.queue_free()
        collect_coin()