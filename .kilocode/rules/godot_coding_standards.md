# godot_coding_standards.md

Godot开发编码规范

## 指导原则

### 编程语言

- 使用gdscript代码编程

### 格式

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
