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

3. **智能问题分析与Agent选择**：
   - **问题复杂度评估**: 根据问题描述 $ARGUMENTS 智能选择分析策略
     * **简单问题**（语法错误、基础逻辑bug）: local-developer + ide工具组合
     * **中等复杂问题**（功能异常、性能问题）: local-developer + senior-code-reviewer
     * **复杂问题**（架构缺陷、系统性故障）: 全专家agent协作
     * **Godot特定问题**: 优先使用godot专业agents

   - **分层分析执行**:
     * **基础分析**: 使用Task工具启动local-developer(qwen3-coder:30b)进行快速问题分析
       - 分析问题描述，识别常见的问题模式
       - 定位可能存在问题的代码模块
       - 提供初步的诊断和解决方案建议
       - 进行基础的代码检查和语法验证
     * **专业代码分析**: 对于复杂问题，启动senior-code-reviewer代理进行深度分析
       - 深度分析问题描述 $ARGUMENTS，识别问题类型和严重程度
       - 定位可能存在问题的代码模块和具体位置
       - 分析问题的根本原因和影响范围
       - 输出详细的代码审查报告和问题诊断
     * **领域专业分析**: 根据问题类型，启动相应的专业领域agent进行深度分析
       - **架构问题**: 启动godot-architect分析架构层面的设计缺陷
       - **实现问题**: 启动godot-game-developer分析具体的代码实现问题
       - **游戏机制问题**: 启动godot-game-designer分析游戏逻辑和机制问题
     * **补充分析**: 使用ide工具获取实时代码诊断和语法检查信息
       使用sequential-thinking工具整合所有agent的分析结果
       使用Explore工具进一步定位相关代码和依赖关系
       使用context7获取相关的Godot API文档和最佳实践
       使用tavily-mcp搜索类似问题的解决方案和社区经验
       对于特别复杂的问题，使用multi-model-advisor进行多模型验证

4. **智能根因诊断与确认**：
   - 整合所有agent的分析结果，形成综合的问题根因报告
   - 按照问题严重程度和修复难度进行优先级排序
   - 使用AskUserQuestion向用户确认诊断结果，提供详细的解释和建议
   - 如用户不认可分析结果，返回步骤3进行更深入的分析
   - 将问题分析结果和诊断过程记录到memory中供后续参考

5. **Agent协作解决方案设计**：
   - **主导方案设计**: 使用Task工具启动godot-game-developer代理主导修复方案设计
     - 基于确认的问题根因，设计具体的代码修复方案
     - 考虑性能影响、兼容性和可维护性
     - 提供详细的实施步骤和测试方案
   - **方案审查**: 启动相关agent对修复方案进行专业审查
     - **架构一致性审查**: godot-architect确保修复符合整体架构
     - **代码质量审查**: senior-code-reviewer验证修复方案的质量
     - **游戏机制审查**: godot-game-designer确保游戏逻辑的正确性（如适用）
   - **方案优化**: 根据多方专业意见优化修复方案
   - 使用memory工具查询相关的修复模式和最佳实践
   - 向用户展示最终修复方案并请求确认

6. **智能代码实施与质量保证**：
   - **修复方案复杂度评估**: 根据修复复杂度智能选择实施agent
     * **简单修复**（<50行代码，基础逻辑修正）: 使用local-developer高效实施
     * **中等复杂修复**（50-200行，多个函数修改）: local-developer + godot-game-developer协作
     * **复杂修复**（>200行，架构级修改）: godot-game-developer主导 + 多专家协作
     * **性能关键修复**: godot-game-developer + senior-code-reviewer双重验证

   - **分层代码实施**:
     * **简单修复实施**: 使用Task工具启动local-developer(qwen3-coder:30b)进行代码修改
       - 按照确认的修复方案精确实施代码修改
       - 确保所有修改严格遵循 `gdscript编码规范`
       - 添加必要的注释和文档说明
       - 进行基础的代码质量检查
     * **复杂修复实施**: 使用Task工具启动godot-game-developer代理进行代码修改
       - 处理复杂的游戏逻辑和架构级修改
       - 确保符合Godot引擎最佳实践
       - 与现有系统架构保持一致
   - **质量验证**: 启动senior-code-reviewer进行修改后代码的质量审查
     - 验证修复的完整性和正确性
     - 检查是否引入了新的问题或副作用
     - 确保代码质量符合项目标准
   - **功能测试**: 使用godot工具和bash命令进行全面测试
     - 测试修复后的功能是否正常工作
     - 运行相关的单元测试和集成测试
     - 验证性能是否达到预期标准
   - **文档更新**: 更新相关文档和注释，记录修复过程和经验

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