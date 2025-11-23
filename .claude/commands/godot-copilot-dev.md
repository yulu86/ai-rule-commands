---
name: godot-copilot-dev
description: 根据Story生成开发指导，协同用户完成Godot游戏开发
argument-hint: [story|story文档]
---

## 执行流程

必须严格按照以下流程执行

### 1. Story检查与确认
首先检查是否提供了待开发的Story文档：
- 如果未提供Story，提醒用户提供待开发的Story文档
- 如果已提供Story，进入下一步详细设计

### 2. 理解架构设计
- 查找并读取架构设计文档，理解架构设计，以支撑后续开发

### 3. Story协同开发
- 强制使用SKILL godot-copilot进行协同开发
