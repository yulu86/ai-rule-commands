---
name: godot-debug
description: Godot 代码问题诊断与修复
argument-hint: "[问题描述]"
---

## 功能说明

专门用于诊断和修复 Godot 项目中的代码问题，采用系统化的调试流程，确保问题得到准确分析和有效解决。

## 执行步骤

1. **问题验证**：
   - 检查用户是否提供了问题描述参数
   - 如未提供参数，提示用户详细描述遇到的问题

2. **项目信息收集**：
   - 使用Explore工具快速扫描项目结构，了解问题可能影响的相关模块
   - 使用memory工具查询项目历史问题和已知解决方案
   - 使用filesystem工具读取项目配置文件 CLAUDE.md，掌握项目基本信息
   - 通过godot工具分析项目运行状态和错误日志
   - 分析项目结构和技术栈，为问题诊断提供上下文

3. **问题分析与定位**：
   - 使用Task工具启动senior-code-reviewer代理进行专业代码分析
   - 使用sequential-thinking工具深入分析问题描述 $ARGUMENTS，推断可能的原因和影响范围
   - 使用Explore工具定位可能存在问题的代码模块和具体位置
   - 使用context7获取相关的Godot API文档和最佳实践
   - 系统性地检查相关代码，分析是否存在问题的根本原因
   - 使用tavily-mcp搜索类似问题的解决方案
   - 如初步分析未找到根因，扩大搜索范围，持续深入分析

4. **根因确认**：
   - 输出详细的问题根因分析报告
   - 使用AskUserQuestion向用户确认诊断结果，如用户不认可则返回步骤3重新分析

5. **解决方案设计**：
   - 使用Task工具启动godot-game-developer代理进行专业修复方案设计
   - 基于确认的问题根因，设计具体的修复方案
   - 使用memory工具查询相关的修复模式和最佳实践
   - 评估方案的影响范围和潜在风险
   - 向用户展示修复方案并请求确认，如用户不认可则重新设计

6. **代码实施与验证**：
   - 使用Task工具启动godot-game-developer代理进行代码实施
   - 按照确认的修复方案实施代码修改
   - 使用godot工具测试修改后的功能
   - 使用Bash命令运行相关的测试和验证
   - 确保所有修改严格遵循 `gdscript编码规范`
   - 进行必要的测试验证，确保问题得到解决且未引入新问题

## GDScript 编码规范

### 基础规范

#### 文件格式
- **编码**：使用不带 BOM 的 UTF-8 编码
- **换行符**：统一使用 LF（\n）换行，避免使用 CRLF 或 CR
- **文件结尾**：每个文件末尾必须包含一个换行符
- **缩进**：使用制表符（Tab）而非空格进行缩进

#### 代码结构
- **函数与类定义**：用两个空行包围函数和类定义
- **续行缩进**：使用 2 个额外的缩进级别区分续行代码块
- **数组/字典/枚举**：作为例外，仅使用单个缩进级别

#### 命名约定
- **未使用参数**：函数签名中未使用的参数以 `_` 开头
- **自注释代码**：优先使用清晰的命名替代注释
- **日志输出**：避免使用 `print()` 打印日志

### 代码示例

#### 正确的缩进示例
```gdscript
# 基本缩进
for i in range(10):
	pass

# 续行缩进
effect.interpolate_property(sprite, "transform/scale",
		sprite.get_scale(), Vector2(2.0, 2.0), 0.3,
		Tween.TRANS_QUAD, Tween.EASE_OUT)

# 数组/字典续行
var positions = [
	Vector2(0, 0),
	Vector2(100, 50),
	Vector2(-50, 75)
]
```

#### 错误的缩进示例
```gdscript
# 缩进不足
for i in range(10):
print("hello")

# 缩进过度
for i in range(10):
		print("hello")

# 续行缩进不足
effect.interpolate_property(sprite, "transform/scale",
	sprite.get_scale(), Vector2(2.0, 2.0), 0.3,
	Tween.TRANS_QUAD, Tween.EASE_OUT)
```