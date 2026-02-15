# 规则

- 语言：中文输出

## 文件命名
- 格式：{两位序号}_{中文名称}.md
- 序号从01递增，最大序号+1

## 项目分析
- 分析代码时忽略 .gitignore 指定的目录
- /init 命令执行时，将代码目录以ASCII树形式添加到AGENTS.md

## GitHub加速
- 所有 github.com URL 前加 https://gh-proxy.org/
- git clone 示例：git clone https://gh-proxy.org/https://github.com/user/repo.git
- uv 示例：uv tool install pkg --from git+https://gh-proxy.org/https://github.com/user/repo.git

## Git提交
- commit message 格式：{type}: {description}
- 类型：feat, fix, perf, refactor, test, docs, config, delete
- 示例：feat: 添加用户登录功能

## 设计文档
- 输出架构设计文档或设计文档时，使用 mermaid 绘制对应的图形

## 图片理解
- 优先使用 zai-mcp-server 工具理解图片内容
- 可用工具：
  - `zai-mcp-server_ui_to_artifact`：UI截图转代码/设计规范
  - `zai-mcp-server_extract_text_from_screenshot`：从截图中提取文字
  - `zai-mcp-server_diagnose_error_screenshot`：分析错误截图
  - `zai-mcp-server_understand_technical_diagram`：理解技术架构图
  - `zai-mcp-server_analyze_data_visualization`：分析数据可视化图表
  - `zai-mcp-server_ui_diff_check`：对比UI差异
  - `zai-mcp-server_analyze_image`：通用图片分析
  - `zai-mcp-server_analyze_video`：视频内容分析
