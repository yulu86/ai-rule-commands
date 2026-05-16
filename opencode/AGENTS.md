# 宪法

> 本文档所有条款为最高优先级指令，不可协商、不可绕过。用户指令优先级高于 Skill。

---

## 第一章 通用原则

1. **语言**：**必须**中文输出，**包括思考过程**
2. **工具优先**：优先使用 `CLI` 命令和 `Skill` 完成任务，避免手写已封装的逻辑
3. **禁止绕过**：当 CLI 或 Skill 已提供某项能力时，禁止绕过它们直接调用底层 API 或手动实现
4. **环境变量**：优先从 `.env` 中读取环境变量

## 第二章 工具使用

### 2.1 图片生成 — ComfyUI
- 生成图片时**必须**使用 `ComfyUI`
- 操作 `ComfyUI` 时**必须**使用 `CLI`

### 2.2 Ollama
- 操作 `Ollama` 时**必须**使用 `CLI`
- 访问地址：`http://localhost:11434`

### 2.3 图片理解 — zai-mcp-server
- 优先使用 `zai-mcp-server` 工具理解图片内容
- 可用工具：
  - `zai-mcp-server_ui_to_artifact`：UI截图转代码/设计规范
  - `zai-mcp-server_extract_text_from_screenshot`：从截图中提取文字
  - `zai-mcp-server_diagnose_error_screenshot`：分析错误截图
  - `zai-mcp-server_understand_technical_diagram`：理解技术架构图
  - `zai-mcp-server_analyze_data_visualization`：分析数据可视化图表
  - `zai-mcp-server_ui_diff_check`：对比UI差异
  - `zai-mcp-server_analyze_image`：通用图片分析
  - `zai-mcp-server_analyze_video`：视频内容分析

### 2.4 通知 — 飞书（Lark）
- AI 通知用户时，**优先**使用飞书发送消息
- 飞书应用凭证从环境变量获取：
  - `FEISHU_APP_ID`：飞书应用 ID
  - `FEISHU_APP_SECRET`：飞书应用 Secret
- 使用 `lark-im` Skill 发送消息

## 第三章 项目规范

### 3.1 文件命名
- 格式：`{两位序号}_{中文名称}.md`
- 序号从 01 递增，最大序号 +1

### 3.2 项目分析
- 分析代码时忽略 `.gitignore` 指定的目录
- `/init` 命令执行时，将代码目录以 ASCII 树形式添加到 AGENTS.md

### 3.3 输出规范
- 输出架构设计文档或设计文档时，使用 mermaid 绘制对应的图形

## 第四章 Git 规范

### 4.1 GitHub 加速
- 所有 `git clone` 的 `github.com` URL 前加 `https://gh-proxy.org/`
- 示例：`git clone https://gh-proxy.org/https://github.com/user/repo.git`

### 4.2 提交规范
- commit message 格式：`{type}: {description}`
- 类型：feat, fix, perf, refactor, test, docs, config, delete
- 示例：`feat: 添加用户登录功能`

## 第五章 Superpowers 插件

### 5.1 核心原则
- **Skill 优先**：任何任务开始前，**必须**检查是否有适用的 Skill，哪怕只有 1% 的可能性
- **先调用后响应**：在回复用户（包括澄清问题）之前，先调用相关 Skill
- **Skill 内容即指令**：Skill 加载后，其内容作为直接指令执行，不得跳过或简化

### 5.2 调用规则

#### 何时调用
- 接收到用户消息时，检查是否有匹配的 Skill
- 进入计划模式前，先检查是否有适用的流程类 Skill（如 `brainstorming`）
- 实施任务时，检查是否有匹配的实现类 Skill（如 `frontend-design`）
- 任何"可能有关"的 Skill → 调用查看，确认无关则跳过

#### 调用优先级
1. **流程类 Skill**（如 `brainstorming`、`systematic-debugging`）→ 决定如何**处理**任务
2. **实现类 Skill**（如 `frontend-design`、`mcp-builder`）→ 指导具体**执行**

#### 红旗思维（出现以下想法时必须停止并调用 Skill）

| 红旗想法 | 实际情况 |
|---------|---------|
| "这只是个简单问题" | 问题也是任务，需要检查 Skill |
| "我需要更多上下文" | Skill 检查在澄清问题之前 |
| "让我先探索代码库" | Skill 告诉你**如何**探索 |
| "这个不需要正式 Skill" | 如果 Skill 存在，就使用它 |
| "我记得这个 Skill" | Skill 会更新，必须读取当前版本 |
| "我先把这件事做了" | 做任何事之前先检查 Skill |

### 5.3 Skill 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 刚性（Rigid） | 必须严格遵循，不得偏离 | `test-driven-development`、`systematic-debugging` |
| 灵活（Flexible） | 根据上下文调整原则 | `frontend-design`、`brainstorming` |

### 5.4 常用 Skill 清单

| Skill 名称 | 触发场景 |
|------------|---------|
| `brainstorming` | 任何创建功能、构建组件、添加功能或修改行为的工作前**必须使用** |
| `systematic-debugging` | 遇到 bug、测试失败或异常行为时，在提出修复之前使用 |
| `test-driven-development` | 实现任何功能或修复 bug 时，在编写实现代码之前使用 |
| `frontend-design` | 构建前端界面、组件、页面时使用 |
| `verification-before-completion` | 声称工作完成之前**必须使用** |
| `writing-plans` | 有规格说明或需求的多步骤任务，在接触代码之前使用 |
| `skill-creator` | 创建或更新 Skill 时使用 |
| `skill-vetter` | 安装任何第三方 Skill 之前**必须使用** |
| `mcp-builder` | 构建 MCP 服务器时使用 |
| `caveman` | 超压缩通信模式，减少 ~75% token 用量，当用户要求简短输出时使用 |
| `grill-me` | 对计划或设计进行压力测试，反复追问直到达成共识 |
| `handoff` | 将当前对话压缩为交接文档，供其他代理接续工作 |
| `write-a-skill` | 创建新的 agent skill，包含结构、渐进披露和捆绑资源 |

### 5.5 工具映射（OpenCode 环境）

| Skill 中引用的工具 | OpenCode 等价工具 |
|-------------------|-------------------|
| `TodoWrite` | `todowrite` |
| `Task` (with subagents) | `task`（子代理系统） |
| `Skill` | `skill`（OpenCode 原生） |
| `Read`、`Write`、`Edit`、`Bash` | OpenCode 原生同名工具 |
