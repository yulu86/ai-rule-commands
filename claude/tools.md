# MCP服务器工具配置表

本文档列出了当前配置的MCP（Model Context Protocol）服务器工具及其功能描述。

## 工具概览

| MCP服务器 | 主要功能 | 工具数量 | 状态 |
|-----------|----------|----------|------|
| filesystem | 文件系统操作 | 12 | ✅ 已启用 |
| sequential-thinking | 序列化思考和复杂问题分析 | 1 | ✅ 已启用 |
| memory | 知识图谱和记忆管理 | 8 | ✅ 已启用 |
| tavily-mcp | 网络搜索、内容提取和网站分析 | 3 | ✅ 已启用 |
| godot | Godot游戏引擎开发工具 | 11 | ✅ 已启用 |
| context7 | 库文档查询和代码示例获取 | 2 | ✅ 已启用 |
| chrome-devtools | Chrome开发者工具 | 3 | ✅ 已启用 |
| multi-model-advisor | 多模型顾问 | 1 | ✅ 已启用 |

## 详细工具列表

### filesystem - 文件系统操作工具

| 工具名称 | 功能描述 | 参数 |
|----------|----------|------|
| `read_file` | 读取文件完整内容（已弃用） | path, tail, head |
| `read_text_file` | 读取文本文件内容 | path, tail, head |
| `read_media_file` | 读取图片或音频文件 | path |
| `read_multiple_files` | 同时读取多个文件 | paths |
| `write_file` | 创建或覆盖文件 | path, content |
| `edit_file` | 基于行的文本文件编辑 | path, edits, dryRun |
| `create_directory` | 创建目录 | path |
| `list_directory` | 获取目录详细列表 | path |
| `list_directory_with_sizes` | 获取目录列表（包含大小） | path, sortBy |
| `directory_tree` | 获取递归目录树结构 | path |
| `search_files` | 递归搜索文件和目录 | path, pattern, excludePatterns |
| `list_allowed_directories` | 获取允许访问的目录列表 | - |

### sequential-thinking - 序列化思考和复杂问题分析

| 工具名称 | 功能描述 | 参数 |
|----------|----------|------|
| `sequentialthinking` | 动态反思性问题解决工具 | thought, nextThoughtNeeded, thoughtNumber, totalThoughts, isRevision, revisesThought, branchFromThought, branchId, needsMoreThoughts |

### memory - 知识图谱和记忆管理

| 工具名称 | 功能描述 | 参数 |
|----------|----------|------|
| `create_entities` | 创建多个新实体 | entities |
| `create_relations` | 创建实体间关系 | relations |
| `add_observations` | 添加观察记录到现有实体 | observations |
| `delete_entities` | 删除实体及相关关系 | entityNames |
| `delete_observations` | 删除特定观察记录 | deletions |
| `delete_relations` | 删除关系 | relations |
| `read_graph` | 读取整个知识图谱 | - |
| `search_nodes` | 基于查询搜索节点 | query |
| `open_nodes` | 通过名称打开特定节点 | names |

### tavily-mcp - 网络搜索、内容提取和网站分析

| 工具名称 | 功能描述 | 参数 |
|----------|----------|------|
| `tavily-search` | 强大的网络搜索工具 | query, search_depth, topic, days, time_range, start_date, end_date, max_results, include_images, include_image_descriptions, include_raw_content, include_domains, exclude_domains, country, include_favicon |
| `tavily-extract` | 网页内容提取工具 | urls, extract_depth, include_images, format, include_favicon |
| `tavily-crawl` | 结构化网站爬虫 | url, max_depth, max_breadth, limit, instructions, select_paths, select_domains, allow_external, extract_depth, format, include_favicon |
| `tavily-map` | 网站结构映射工具 | url, max_depth, max_breadth, limit, instructions, select_paths, select_domains, allow_external |

### godot - Godot游戏引擎开发工具

| 工具名称 | 功能描述 | 参数 |
|----------|----------|------|
| `launch_editor` | 启动Godot编辑器 | projectPath |
| `run_project` | 运行Godot项目并捕获输出 | projectPath, scene |
| `get_debug_output` | 获取当前调试输出和错误 | - |
| `stop_project` | 停止当前运行的Godot项目 | - |
| `get_godot_version` | 获取已安装的Godot版本 | - |
| `list_projects` | 列出目录中的Godot项目 | directory, recursive |
| `get_project_info` | 获取Godot项目元数据 | projectPath |
| `create_scene` | 创建新的Godot场景文件 | projectPath, scenePath, rootNodeType |
| `add_node` | 向现有场景添加节点 | projectPath, scenePath, parentNodePath, nodeType, nodeName, properties |
| `load_sprite` | 向Sprite2D节点加载精灵 | projectPath, scenePath, nodePath, texturePath |
| `export_mesh_library` | 将场景导出为MeshLibrary资源 | projectPath, scenePath, outputPath, meshItemNames |
| `save_scene` | 保存场景文件更改 | projectPath, scenePath, newPath |

### context7 - 库文档查询和代码示例获取

| 工具名称 | 功能描述 | 参数 |
|----------|----------|------|
| `resolve-library-id` | 解析库名称为Context7兼容的库ID | libraryName |
| `get-library-docs` | 获取库的最新文档 | context7CompatibleLibraryID, topic, tokens |

### chrome-devtools - Chrome开发者工具

| 工具名称 | 功能描述 | 参数 |
|----------|----------|------|
| `performance_start_trace` | 开始性能追踪 | - |
| `performance_analyze_insight` | 性能分析和洞察 | - |
| `take_screenshot` | 截图 | - |

### multi-model-advisor - 多模型顾问

| 工具名称 | 功能描述 | 参数 |
|----------|----------|------|
| `list-available-models` | 列出可用模型 | - |

## 权限配置

当前启用的工具权限包括：

### Bash权限
- `Bash(claude mcp:*)` - MCP相关命令
- `WebSearch` - 网络搜索
- `WebFetch(domain:github.com)` - GitHub内容获取
- `Bash(npm search:*)` - NPM包搜索
- `Bash(npm install:*)` - NPM包安装
- `Bash(ollama-mcp)` - Ollama MCP命令
- `Bash(where:*)` - 路径查找命令
- `Bash(echo $env:APPDATA:*)` - 环境变量输出

### MCP工具权限
- **filesystem**: 所有文件系统操作工具
- **chrome-devtools**: 性能分析和截图工具
- **multi-model-advisor**: 模型列表工具
- **memory**: 实体和关系管理工具
- **tavily-mcp**: 网络搜索工具
- **sequential-thinking**: 序列化思考工具

## 配置文件位置

- **主配置**: `.claude/settings.local.json`
- **全局指令**: `.claude/CLAUDE.md`
- **路由配置**: `claude-code-router/config.json`

## 使用指南

### 优先级排序
1. **memory工具** - 优先查询记忆中的知识
2. **context7工具** - 查询最新的库文档
3. **tavily-mcp工具** - 搜索最新技术资讯
4. **sequential-thinking工具** - 处理复杂架构设计
5. **filesystem工具** - 进行项目文件操作
6. **godot工具** - Godot项目特定开发操作

### 特定场景使用规范
- **代码审查**: sequential-thinking + memory
- **文档生成**: context7 + tavily-mcp
- **架构设计**: sequential-thinking + memory
- **问题诊断**: tavily-mcp + sequential-thinking
- **Godot开发**: godot + filesystem

---
*最后更新时间: 2025-11-18*