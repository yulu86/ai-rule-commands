# MCP Server Tools 配置清单

本文档记录了当前已安装配置的MCP Server tools，按功能类别分类展示。

## MCP Server Tools 总览

| 服务器名称 | 工具类别 | 工具数量 | 主要功能 | 用途描述 |
|-----------|----------|----------|----------|----------|
| Memory | 知识图谱管理 | 10 | 实体关系管理、知识存储 | 提供持久化知识图谱功能，支持实体、关系和观察的增删改查 |
| Godot | 游戏开发 | 15 | 项目操作、场景编辑、调试 | 集成Godot游戏引擎，支持项目运行、场景创建和调试 |
| Context7 | 文档检索 | 2 | 库文档查询、代码示例 | 提供最新库文档和代码示例的检索功能 |
| Tavily | 网络搜索 | 4 | 网页搜索、内容提取、站点爬取 | 强大的网络搜索和内容提取工具 |
| IDE | 开发环境 | 2 | 代码诊断、执行 | VS Code集成，提供代码诊断和执行功能 |
| Multi-Model Advisor | 模型咨询 | 2 | 多模型查询、比较 | 支持同时查询多个AI模型并比较结果 |
| Sequential Thinking | 问题分析 | 1 | 顺序思考、问题分解 | 提供结构化的问题分析和解决流程 |

## 详细工具清单

### 1. Memory Server (知识图谱管理)

| 工具名称 | 功能描述 |
|----------|----------|
| create_entities | 创建多个新实体到知识图谱 |
| create_relations | 在实体间创建关系 |
| add_observations | 向现有实体添加观察内容 |
| delete_entities | 删除实体及其关联关系 |
| delete_observations | 删除特定观察内容 |
| delete_relations | 删除实体间的关系 |
| read_graph | 读取整个知识图谱 |
| search_nodes | 基于查询搜索节点 |
| open_nodes | 按名称打开特定节点 |

### 2. Godot Server (游戏开发)

| 工具名称 | 功能描述 |
|----------|----------|
| launch_editor | 启动Godot编辑器 |
| run_project | 运行Godot项目并捕获输出 |
| get_debug_output | 获取当前调试输出和错误 |
| stop_project | 停止当前运行的Godot项目 |
| get_godot_version | 获取安装的Godot版本 |
| list_projects | 列出目录中的Godot项目 |
| get_project_info | 检索Godot项目元数据 |
| create_scene | 创建新的Godot场景文件 |
| add_node | 向现有场景添加节点 |
| load_sprite | 将精灵加载到Sprite2D节点 |
| export_mesh_library | 将场景导出为MeshLibrary资源 |
| save_scene | 保存对场景文件的更改 |
| get_uid | 获取Godot项目中特定文件的UID |
| update_project_uids | 通过重新保存资源更新UID引用 |

### 3. Context7 Server (文档检索)

| 工具名称 | 功能描述 |
|----------|----------|
| resolve-library-id | 解析包名到Context7兼容的库ID |
| get-library-docs | 获取库的最新文档 |

### 4. Tavily Server (网络搜索)

| 工具名称 | 功能描述 |
|----------|----------|
| tavily-search | 强大的网络搜索工具 |
| tavily-extract | 网页内容提取工具 |
| tavily-crawl | 结构化网页爬虫 |
| tavily-map | 网站结构映射工具 |

### 5. IDE Server (开发环境)

| 工具名称 | 功能描述 |
|----------|----------|
| getDiagnostics | 从VS Code获取语言诊断 |
| executeCode | 在Jupyter内核中执行Python代码 |

### 6. Multi-Model Advisor Server (模型咨询)

| 工具名称 | 功能描述 |
|----------|----------|
| list-available-models | 列出Ollama中可用的模型 |
| query-models | 查询多个AI模型并比较响应 |

### 7. Sequential Thinking Server (问题分析)

| 工具名称 | 功能描述 |
|----------|----------|
| sequentialthinking | 通过思考过程进行动态和反思性解决问题 |

## 使用说明

- **Memory Server**: 适用于需要持久化知识和关系管理的场景
- **Godot Server**: 专门用于Godot游戏开发项目
- **Context7 Server**: 需要最新库文档和代码示例时使用
- **Tavily Server**: 需要网络搜索、内容提取或站点分析时使用
- **IDE Server**: 与VS Code和Jupyter集成时使用
- **Multi-Model Advisor**: 需要比较多个AI模型响应时使用
- **Sequential Thinking**: 复杂问题需要结构化分析时使用

## 更新记录

- **创建时间**: 2025-11-22
- **工具总数**: 36个MCP工具
- **覆盖领域**: 知识管理、游戏开发、文档检索、网络搜索、开发环境、模型咨询、问题分析

---

*本文档自动生成，反映当前MCP Server tools配置状态*