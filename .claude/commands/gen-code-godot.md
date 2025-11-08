---
name: gen-code-godot
description: 与我合作编写Godot代码
argument-hint: "[编码任务]"
---

## 执行步骤

- 检查用户是否提供参数，如果没有提供，请求用户提供参数
- 如果用户提供了参数，继续执行
- 与我`分工合作`完成编码任务 $ARGUMENTS，按照以下步骤编写代码：    
    1. 查找当前项目中 /docs 目录下的文档(如果存在)，寻找跟编码任务 $ARGUMENTS 相关的设计
    2. 如果没有找到对应的设计，@godot-architect 请按照编码任务 $ARGUMENTS 输出设计，用一句话总结方案，并请求用户确认，如果用户不认可，请回到步骤2开始执行
	3. @godot-architect 按照设计方案分解任务，并按照依赖关系编排好任务的顺序。
	4. @godot-architect 按照任务是否涉及可视化划分责任人，可视化相关的任务交给我，非可视化的任务交给 @godot-game-developer
	5. 按照任务划分，生成todo-list，并按顺序开始执行
	6. 如果执行到是我负责的任务，请给出任务的详细说明、操作步骤和完成标准，@design-doc-writer 输出到 docs/tasks/ 目录下。并暂停执行，询问我是否已完成工作，待我回答完成后，刷新todo-list状态，继续执行。
	7. 如果执行到 @godot-game-developer 负责的任务，@godot-game-developer 根据设计编写代码。编写的代码需要符合`gdscript编码规范`的要求
	8. @senior-code-reviewer 检视刚编写的代码，查找是否存在警告或代码坏味道，重构解决坏味道
    9. 重复执行步骤6~8，直到实现编码任务 $ARGUMENTS

## 分工合作
1. 你的职责：
  - 使用gdscript编写游戏逻辑
  - tscn文件框架搭建
2. 我的职责：
  - tscn文件细化调整
  - 使用资产完成动画创建
  - 创建Sprite、
  - 创建碰撞
  - 配置字体、颜色等  
  - 配置项目设置

## 原则
1. 遵守小步前进原则
2. 遵守SOLID原则
3. 遵守DRY原则

### gdscript编码规范

#### 编码与特殊字符

- 使用换行符（LF）换行，而非 CRLF 或 CR。
- 在每个文件的末尾使用一个换行符。
- 使用不带字节顺序标记的 UTF-8 编码。
- 使用制表符代替空格进行缩进。

#### 缩进

- 每个缩进的缩进级别必须大于包含该缩进的代码块的缩进级别。
  规范示例:
  ```gdscript
  for i in range(10):
	print("hello")
  ```

  不规范示例:
  ```gdscript
  for i in range(10):
  print("hello")

  for i in range(10):
		print("hello")
  ```
- 使用2个缩进级别来区分续行代码块与常规代码块。
  规范示例:
  ```gdscript
  effect.interpolate_property(sprite, "transform/scale",
		sprite.get_scale(), Vector2(2.0, 2.0), 0.3,
		Tween.TRANS_QUAD, Tween.EASE_OUT)
  ```

  不规范示例:
  ```gdscript
  effect.interpolate_property(sprite, "transform/scale",
	sprite.get_scale(), Vector2(2.0, 2.0), 0.3,
	Tween.TRANS_QUAD, Tween.EASE_OUT)
  ```
  此规则的例外：数组、字典和枚举。使用单个缩进级别来区分续行代码块。

- 用两个空行来包围函数和类定义

### 编码

- gdscript的func签名里的参数如果没有在func的实现中使用，请用`_`作为参数名的开头
- 请不要使用`print`打印日志
- 请尽量减少代码注释，而是使用代码的名称自注释