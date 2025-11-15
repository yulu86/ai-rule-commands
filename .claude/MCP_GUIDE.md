# MCP服务器配置和使用指南

## 已安装的MCP服务器

### 1. Filesystem Server
- **功能**: 文件系统操作工具
- **主要工具**:
  - `read_text_file`: 读取文本文件内容
  - `write_file`: 写入文件内容
  - `edit_file`: 编辑文件（支持git diff格式）
  - `list_directory`: 列出目录内容
  - `create_directory`: 创建目录
  - `search_files`: 搜索文件
  - `get_file_info`: 获取文件元数据

### 2. Sequential-thinking Server
- **功能**: 序列化思考和复杂问题分析
- **主要工具**:
  - `sequentialthinking`: 动态问题解决和思考过程

### 3. Memory Server
- **功能**: 知识图谱和记忆管理
- **主要工具**:
  - `create_entities`: 创建知识实体
  - `create_relations`: 创建实体关系
  - `add_observations`: 添加观察内容
  - `read_graph`: 读取整个知识图谱
  - `search_nodes`: 搜索知识节点
  - `open_nodes`: 打开特定节点

### 4. Tavily MCP Server
- **功能**: 网络搜索、内容提取和网站分析
- **主要工具**:
  - `tavily-search`: 强大的网络搜索
  - `tavily-extract`: 网页内容提取
  - `tavily-crawl`: 网站爬取
  - `tavily-map`: 网站结构映射

### 5. Godot Server
- **功能**: Godot游戏引擎开发工具
- **主要工具**:
  - `launch_editor`: 启动Godot编辑器
  - `run_project`: 运行Godot项目
  - `create_scene`: 创建新场景
  - `add_node`: 添加节点到场景
  - `load_sprite`: 加载精灵资源
  - `save_scene`: 保存场景文件

### 6. Context7 Server
- **功能**: 库文档查询和代码示例获取
- **主要工具**:
  - `resolve-library-id`: 解析库名称到ID
  - `get-library-docs`: 获取库文档

## 最佳实践

### 工具使用优先级
1. **Memory**: 优先查询已有知识
2. **Context7**: 获取最新API文档
3. **Tavily**: 搜索网络信息
4. **Sequential-thinking**: 复杂问题分析
5. **Filesystem**: 文件操作
6. **Godot**: Godot特定操作

### 常见工作流

#### 架构设计工作流
```
Memory查询 → Sequential-thinking分析 → Context7查文档 → Tavily搜索趋势 → Filesystem操作 → Memory记录
```

#### 代码审查工作流
```
Filesystem读取 → Sequential-thinking分析 → Memory对比标准 → Context7验证API → 生成建议
```

#### 文档生成工作流
```
Memory查询项目信息 → Filesystem分析结构 → Sequential-thinking设计 → Context7获取文档 → 生成文档 → Memory记录
```

## 配置文件说明

### `.claude/CLAUDE.md`
全局配置文件，包含语言偏好、MCP工具使用指南等。

### `.claude/agents/`
专门代理配置，如godot-architect、design-doc-writer等。

### `.claude/commands/`
自定义命令配置，如godot-gen-doc、explain-code等。

## 注意事项

1. **权限管理**: 确保MCP服务器只能访问授权的目录
2. **性能考虑**: 合理使用搜索工具，避免过度请求
3. **知识维护**: 定期更新memory中的知识图谱
4. **版本兼容**: 关注MCP服务器版本更新和兼容性