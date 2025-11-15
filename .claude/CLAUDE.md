# 语言偏好
- 使用中文输出回答和文档

# 记忆偏好
- 优先使用记忆，减少文件读取
- 如果刷新了文档或代码，请同步刷新到记忆中
- 执行`/init`命令时，同时刷新到记忆中

# 知识偏好
- 对于你不确定的知识，优先使用搜索工具搜索并归纳信息，以补充到知识库

# MCP工具使用指南

## 已配置的MCP服务器
- **filesystem**: 文件系统操作工具
- **sequential-thinking**: 序列化思考和复杂问题分析
- **memory**: 知识图谱和记忆管理
- **tavily-mcp**: 网络搜索、内容提取和网站分析
- **godot**: Godot游戏引擎开发工具
- **context7**: 库文档查询和代码示例获取

## 工具使用优先级
1. **memory工具**: 优先查询记忆中的知识，避免重复搜索
2. **context7工具**: 查询最新的库文档和API参考
3. **tavily-mcp工具**: 搜索最新技术资讯和解决方案
4. **sequential-thinking工具**: 处理复杂架构设计和问题分析
5. **filesystem工具**: 进行项目文件操作和代码管理
6. **godot工具**: Godot项目特定的开发操作

## 特定场景工具使用规范
- **代码审查**: 使用sequential-thinking进行深度分析，结合memory记录最佳实践
- **文档生成**: 使用context7获取最新的API文档，用tavily-mcp补充最新趋势
- **架构设计**: 使用sequential-thinking分解复杂问题，用memory记录设计决策
- **问题诊断**: 使用tavily-mcp搜索相似问题，用sequential-thinking系统性分析
- **Godot开发**: 优先使用godot专用工具，配合filesystem进行项目管理

## 文件操作规范
- 使用filesystem工具进行所有文件读写操作
- 重要配置变更后同步更新到memory中
- 使用标准化的文件路径和命名规范


