---
description: 生成项目目录结构的ASCII树并添加到AGENTS.md中 [目录树最大深度]
agent: build
---

智能项目目录结构生成工具

自动分析项目结构，生成美观的ASCII目录树，并将其添加到项目根目录的AGENTS.md文件中。

## 功能特点

- **智能目录扫描**：递归扫描项目目录，识别文件和文件夹
- **ASCII树形结构**：生成清晰的树形目录结构图
- **文件类型标识**：使用不同符号标识文件类型
- **深度控制**：可配置显示深度，避免过深的目录结构
- **排除规则**：自动排除不必要的文件和目录（如.git、node_modules等）
- **AGENTS.md集成**：自动将目录树添加到AGENTS.md文件中

## 执行流程

1. **项目分析**：检测当前目录和项目类型
2. **目录扫描**：递归扫描所有文件和文件夹
3. **过滤处理**：排除不需要的文件和目录
4. **树形结构生成**：构建ASCII树形结构
5. **AGENTS.md更新**：将生成的目录树添加到AGENTS.md文件中

## 使用示例

```bash
/project-tree
```

## 目录树格式

### 基本结构
```
项目名称/
├── 目录名/
│   ├── 子目录/
│   │   └── 文件.ext
│   └── 文件.ext
├── 文件.md
└── 配置文件.json
```

### 文件类型标识符号
- 📁 目录文件夹
- 📄 普通文件
- 📝 文档文件 (.md, .txt, .rst)
- 💻 代码文件 (.py, .js, .ts, .java, .cpp, .c)
- 🎨 样式文件 (.css, .scss, .less)
- 📱 前端文件 (.html, .jsx, .tsx, .vue)
- ⚙️ 配置文件 (.json, .yml, .yaml, .toml, .ini)
- 🗄️ 数据文件 (.sql, .db, .sqlite)
- 📦 包管理文件 (package.json, requirements.txt, Cargo.toml)
- 🚀 构建文件 (Makefile, Dockerfile, webpack.config.js)
- 📊 测试文件 (.test.js, _test.py, tests/)

## 默认排除规则

以下文件和目录不会被包含在目录树中：
- Git相关：`.git/`, `.gitignore`, `.gitmodules`
- 依赖目录：`node_modules/`, `vendor/`, `target/`, `dist/`, `build/`
- IDE文件：`.vscode/`, `.idea/`, `*.swp`, `*.swo`
- 系统文件：`.DS_Store`, `Thumbs.db`
- 临时文件：`*.tmp`, `*.temp`, `*.log`
- 缓存文件：`__pycache__/`, `.pytest_cache/`

## AGENTS.md集成

### 添加位置
在AGENTS.md文件中添加以下部分：

```markdown
## 项目目录结构

```
[生成的ASCII目录树]
```
```

### 更新策略
- 如果AGENTS.md中已存在目录结构部分，则替换更新
- 如果不存在，则在文件末尾添加新的部分
- 保持文件其他内容不变

## 配置选项

可以通过环境变量或命令参数自定义行为：

- `TREE_DEPTH`：目录树最大深度（默认：5）

### 示例配置
```bash
/project-tree 3 # 限制深度为3层
```

## 项目类型识别

工具会自动识别项目类型并调整显示策略：

- **Node.js项目**：突出package.json、src/、dist/等
- **Python项目**：突出requirements.txt、setup.py、src/等
- **Java项目**：突出pom.xml、src/main/、target/等
- **Go项目**：突出go.mod、pkg/、cmd/等
- **Rust项目**：突出Cargo.toml、src/、target/等

## 特殊文件处理

### README文件
- 优先显示README文件（README.md, README.txt等）
- 在目录树中用特殊符号标识

### 配置文件
- 识别各种配置文件格式
- 按重要性排序显示

### 文档目录
- 识别docs/、doc/、documentation/等文档目录
- 优先显示文档结构

## 输出示例

```
my-awesome-project/
├── 📁 src/
│   ├── 📁 components/
│   │   ├── 📱 Header.jsx
│   │   └── 📱 Footer.jsx
│   ├── 📁 utils/
│   │   └── 💻 helpers.js
│   └── 💻 index.js
├── 📁 public/
│   └── 📄 index.html
├── 📝 README.md
├── 📦 package.json
├── 🎨 styles.css
├── ⚙️ .env.example
└── 🚀 webpack.config.js
```

## 错误处理

- **非项目目录**：提示用户在有效的项目目录中使用
- **权限问题**：处理文件权限不足的情况
- **AGENTS.md缺失**AGENTS.md不存在，询问是否创建
- **文件锁定**AGENTS.md被其他程序占用的情况

## 最佳实践

1. **定期更新**：项目结构变化后及时更新目录树
2. **适当深度**：避免过深的目录结构影响可读性
3. **保持整洁**：确保项目结构清晰，便于生成有意义的目录树
4. **版本控制**：将更新后的AGENTS.md纳入版本控制

## 限制说明

- 最大扫描深度限制（默认5层）
- 不支持符号链接跟踪
- 大型项目可能需要较长的扫描时间
- 某些特殊字符文件名可能显示异常