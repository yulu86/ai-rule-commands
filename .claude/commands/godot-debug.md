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

2. **并行信息收集**（并行执行，最大化效率）：
   - **项目扫描组**（并行执行）:
     * 使用Explore工具快速扫描项目结构，了解问题可能影响的相关模块
     * 使用filesystem工具读取项目配置文件 CLAUDE.md，掌握项目基本信息
     * 通过godot工具分析项目运行状态和错误日志
   - **知识查询组**（并行执行）:
     * 使用memory工具查询项目历史问题和已知解决方案
     * 使用context7获取相关的Godot API文档和最佳实践
     * 使用tavily-mcp搜索类似问题的解决方案和社区经验
   - **实时分析组**（并行执行）:
     * 使用ide工具获取实时代码诊断和语法检查信息
     * 分析项目结构和技术栈，为问题诊断提供上下文

3. **智能问题评估与并行Agent部署**：
   - **问题复杂度评估**: 根据问题描述 $ARGUMENTS 智能选择分析策略
     * **简单问题**（语法错误、基础逻辑bug）: local-developer + ide工具组合
     * **中等复杂问题**（功能异常、性能问题）: local-developer + senior-code-reviewer
     * **复杂问题**（架构缺陷、系统性故障）: 全专家agent协作
     * **Godot特定问题**: 优先使用godot专业agents

   - **并行分析执行**（根据复杂度同时启动多个agent）:
     * **基础分析组**（并行执行）:
       - Task工具启动local-developer(qwen3-coder:30b)进行快速问题分析
       - Explore工具进一步定位相关代码和依赖关系
       - sequential-thinking工具进行初步逻辑推理
     * **专业分析组**（复杂问题时并行启动）:
       - Task工具启动senior-code-reviewer代理进行深度代码分析
       - Task工具启动godot-architect分析架构层面问题
       - Task工具启动godot-game-developer分析具体实现问题
     * **辅助分析组**（需要时并行启动）:
       - Task工具启动godot-game-designer分析游戏机制问题
       - multi-model-advisor进行多模型验证（特别复杂问题）

4. **智能根因诊断与确认**：
   - 使用sequential-thinking工具整合所有agent的并行分析结果
   - 形成综合的问题根因报告，按照问题严重程度和修复难度进行优先级排序
   - 使用AskUserQuestion向用户确认诊断结果，提供详细的解释和建议
   - 如用户不认可分析结果，返回步骤3进行更深入的并行分析
   - 将问题分析结果和诊断过程记录到memory中供后续参考

5. **并行解决方案设计与审查**：
   - **并行方案设计组**（同时启动多个agent进行方案设计）:
     * **主导方案设计**: Task工具启动godot-game-developer代理主导修复方案设计
       - 基于确认的问题根因，设计具体的代码修复方案
       - 考虑性能影响、兼容性和可维护性
       - 提供详细的实施步骤和测试方案
     * **架构方案设计**: Task工具启动godot-architect设计架构级修复方案
     * **质量方案设计**: Task工具启动senior-code-reviewer设计代码质量保证方案
     * **游戏机制方案**: Task工具启动godot-game-designer设计游戏逻辑修复方案（如适用）
   - **并行方案审查组**（同时进行多角度审查）:
     * **架构一致性审查**: godot-architect确保所有修复方案符合整体架构
     * **代码质量审查**: senior-code-reviewer验证修复方案的质量和可行性
     * **游戏逻辑审查**: godot-game-designer确保游戏机制的正确性（如适用）
     * **实现可行性审查**: local-developer验证技术实现难度
   - **方案整合优化**: sequential-thinking工具整合所有方案和审查意见
   - 使用memory工具查询相关的修复模式和最佳实践
   - 向用户展示最终综合修复方案并请求确认

6. **并行代码实施与质量保证**：
   - **修复方案复杂度评估**: 根据修复复杂度智能选择实施agent
     * **简单修复**（<50行代码，基础逻辑修正）: 使用local-developer高效实施
     * **中等复杂修复**（50-200行，多个函数修改）: local-developer + godot-game-developer协作
     * **复杂修复**（>200行，架构级修改）: godot-game-developer主导 + 多专家协作
     * **性能关键修复**: godot-game-developer + senior-code-reviewer双重验证

   - **并行代码实施组**（根据修复复杂度同时启动多个agent）:
     * **主要实施**: Task工具启动主导agent（local-developer或godot-game-developer）
       - 按照确认的修复方案精确实施代码修改
       - 确保所有修改严格遵循 `gdscript编码规范`
       - 处理复杂的游戏逻辑和架构级修改（复杂修复时）
       - 添加必要的注释和文档说明
     * **并行质量检查**: Task工具启动senior-code-reviewer进行实时质量监控
       - 在实施过程中提供质量建议和预警
       - 监控代码质量和架构一致性
       - 识别潜在的副作用和风险
   - **并行验证测试组**（代码完成后立即启动）:
     * **代码质量验证**: senior-code-reviewer进行修改后代码的全面质量审查
       - 验证修复的完整性和正确性
       - 检查是否引入了新的问题或副作用
       - 确保代码质量符合项目标准
     * **功能测试**: 使用godot工具和bash命令进行全面测试
       - 测试修复后的功能是否正常工作
       - 运行相关的单元测试和集成测试
       - 验证性能是否达到预期标准
     * **架构验证**: godot-architect验证架构完整性
     * **游戏逻辑验证**: godot-game-designer验证游戏机制（如适用）
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