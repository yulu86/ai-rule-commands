# Agent协作流程指南

## 概述

本文档定义了Claude Code中各个专业agent之间的协作机制、调用策略和数据传递规范，确保多agent协同工作时的高效性和专业性。

## Agent专业分工

### 核心Agent
- **godot-architect**: 架构设计、SOLID原则、项目结构规划
- **design-doc-writer**: 文档撰写、标准化格式、内容组织
- **senior-code-reviewer**: 代码审查、问题诊断、质量保证
- **godot-game-developer**: GDScript编程、功能实现、性能优化
- **godot-game-designer**: 游戏设计、创意构思、机制设计

## 协作流程矩阵

### 完整游戏开发流程

```
用户需求 → godot-game-designer → godot-architect → godot-game-developer → senior-code-reviewer → design-doc-writer
    ↓              ↓                    ↓                      ↓                     ↓                     ↓
游戏概念设计    架构可行性评估      技术架构设计           功能实现              代码质量审查          文档化输出
```

### 常见协作场景

#### 1. 新功能开发流程
```
需求分析 → godot-architect(架构设计) → godot-game-developer(实现) → senior-code-reviewer(审查) → design-doc-writer(文档)
```

#### 2. 游戏设计开发流程
```
创意设计 → godot-game-designer(概念) → godot-architect(架构适配) → godot-game-developer(实现) → senior-code-reviewer(质量)
```

#### 3. 代码优化流程
```
问题发现 → senior-code-reviewer(分析) → godot-architect(架构建议) → godot-game-developer(修复) → design-doc-writer(记录)
```

## 标准协作模式

### 模式1: 设计→开发→审查→文档
**适用场景**: 完整功能开发

**协作流程**:
1. **设计阶段**: godot-architect或godot-game-designer进行专业设计
2. **开发阶段**: godot-game-developer按照设计方案实现功能
3. **审查阶段**: senior-code-reviewer进行代码质量和架构审查
4. **文档阶段**: design-doc-writer生成标准化文档

**数据传递**:
- 设计→开发: 架构规范、接口定义、实现指南
- 开发→审查: 实现代码、测试结果、性能数据
- 审查→文档: 审查报告、改进建议、最佳实践

### 模式2: 审查→咨询→修复
**适用场景**: 代码问题修复

**协作流程**:
1. **问题发现**: senior-code-reviewer识别代码问题
2. **专业咨询**: 根据问题类型咨询相关专家agent
3. **方案制定**: 结合多方意见制定修复方案
4. **实施修复**: godot-game-developer实施修复

**专家分配**:
- 架构问题: godot-architect
- 实现问题: godot-game-developer
- 设计问题: godot-game-designer

### 模式3: 多agent协作文档生成
**适用场景**: 复杂系统文档

**协作流程**:
1. **信息收集**: 从相关专业agent收集设计输入
2. **内容整合**: design-doc-writer整合多方专业知识
3. **专业审查**: 各领域专家审查专业内容
4. **文档优化**: 根据反馈进行文档完善

## 协作调用规范

### Task工具使用标准

```typescript
// 标准调用格式
Task({
  subagent_type: "target-agent",
  description: "简短描述",
  prompt: "详细的任务描述，包含上下文和具体要求"
})
```

### 数据传递格式

#### 架构设计传递
```json
{
  "architecture_decisions": "架构决策说明",
  "component_specifications": "组件规范定义",
  "interface_definitions": "接口定义文档",
  "implementation_guidelines": "实现指导原则",
  "quality_standards": "质量标准和约束"
}
```

#### 游戏设计传递
```json
{
  "game_concept": "游戏概念描述",
  "mechanics_design": "机制设计详情",
  "user_experience": "用户体验规范",
  "technical_requirements": "技术需求说明",
  "art_audio_specs": "美术音效规范"
}
```

#### 代码审查传递
```json
{
  "review_focus": "审查重点领域",
  "identified_issues": "识别的问题列表",
  "severity_levels": "问题严重程度分级",
  "recommendations": "改进建议",
  "best_practices": "最佳实践推荐"
}
```

## 协作质量控制

### 质量检查点
1. **输入验证**: 确保接收的协作数据完整且格式正确
2. **专业边界**: 明确各agent的专业职责范围
3. **输出标准**: 确保协作输出符合专业标准
4. **反馈机制**: 建立有效的协作反馈循环

### 知识管理
- **决策记录**: 将重要的协作决策记录到memory中
- **最佳实践**: 总结协作过程中的最佳实践
- **模式沉淀**: 将成功的协作模式进行标准化
- **经验共享**: 在不同agent间共享专业经验

## 冲突解决机制

### 专业分歧处理
1. **技术分歧**: 以senior-code-reviewer的分析为最终依据
2. **设计分歧**: 以godot-architect的架构建议为优先
3. **实现分歧**: 以godot-game-developer的技术评估为准

### 协作失败处理
1. **重新评估**: 重新评估协作需求和agent分配
2. ** mediator介入**: 使用上级agent进行调解
3. **方案调整**: 根据实际情况调整协作方案
4. **经验总结**: 分析失败原因并记录经验

## 性能优化

### 协作效率提升
- **并行处理**: 在可能的情况下进行并行协作
- **缓存机制**: 缓存常用的协作数据和结果
- **模板化**: 将常见的协作流程模板化
- **智能路由**: 根据任务特点智能选择协作路径

### 资源管理
- **Agent调度**: 合理调度agent的使用，避免过载
- **内存管理**: 有效管理协作过程中的内存使用
- **网络优化**: 优化agent间的数据传输效率

## 最佳实践

### 协作启动前
1. **需求明确**: 确保协作需求和目标明确
2. **角色清晰**: 明确各agent的角色和职责
3. **沟通计划**: 制定协作过程中的沟通计划
4. **质量标准**: 统一协作输出的质量标准

### 协作过程中
1. **及时反馈**: 建立及时的反馈机制
2. **进度跟踪**: 跟踪协作进度和里程碑
3. **问题处理**: 及时处理协作中出现的问题
4. **知识共享**: 促进agent间的知识共享

### 协作完成后
1. **结果验证**: 验证协作结果的完整性和正确性
2. **经验总结**: 总结协作经验和教训
3. **文档更新**: 更新相关文档和知识库
4. **改进计划**: 制定持续改进计划

## 总结

通过建立标准化的agent协作机制，可以充分发挥各专业agent的优势，提高工作效率和输出质量。关键在于明确分工、规范流程、建立有效的沟通和质量控制机制。