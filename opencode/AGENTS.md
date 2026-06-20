# 宪法

> 本文档所有条款为最高优先级指令，不可协商、不可绕过。用户指令优先级高于 Skill。

---

## 第一章 通用原则

1. **语言**：**必须**中文输出，**包括思考过程**
2. **工具优先**：优先使用 `CLI` 命令和 `Skill` 完成任务，避免手写已封装的逻辑
3. **禁止绕过**：当 CLI 或 Skill 已提供某项能力时，禁止绕过它们直接调用底层 API 或手动实现
4. **环境变量**：优先从 `.env` 中读取环境变量
5. **交互选项化**：与用户交互时（澄清需求、确认方案、做选择等），**必须**优先使用 `question` 工具以选项形式呈现，让用户用鼠标点击选择，而非纯文字问答；仅当选项无法覆盖时才使用自由输入
6. **暂停等待反馈**：当任务需要用户确认方案、做出选择、或提供关键信息才能继续时，**必须**暂停执行，不要自行假设或替用户决定；发出 `question` 工具请求后**停止后续动作**，直到收到用户反馈再继续

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

### 3.4 图形输出格式
- **TUI（终端界面）**：**必须**使用 ASCII 字符绘制图形，确保在纯文本环境下可读
- **Markdown 文件**：**必须**使用 Mermaid 语法绘制图形，确保标准化渲染

## 第四章 Git 规范

### 4.1 GitHub 加速
- 所有 `git clone` 的 `github.com` URL 前加 `https://gh-proxy.org/`
- 示例：`git clone https://gh-proxy.org/https://github.com/user/repo.git`

### 4.2 提交规范
- commit message 格式：`{type}: {description}`
- 类型：feat, fix, perf, refactor, test, docs, config, delete
- 示例：`feat: 添加用户登录功能`
