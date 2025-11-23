---
name: godot-scaffolding-creator
description: 创建Godot游戏工程脚手架，自动配置项目结构和基础文件。支持Godot 4.5+版本，可配置渲染器类型。当用户输入"创建godot项目"、"创建godot脚手架"、"创建godot项目脚手架"时触发此技能。
---

# Godot脚手架生成器

## 快速开始

在目标目录执行脚手架创建：

1. 确定项目目录名称作为项目名
2. 拷贝模板文件到目标目录
3. 更新项目配置文件

## 模板文件结构

```
templates/
├── .claude/settings.local.json    # Claude本地配置
├── .godot/                        # Godot项目缓存目录
├── assets/                        # 游戏资源目录
│   ├── fonts/                     # 字体资源
│   ├── music/                     # 音乐资源
│   ├── resources/                 # 资源子目录
│   │   ├── sound_bus/            # 音频总线
│   │   ├── texture/              # 纹理资源
│   │   ├── theme/                # 主题资源
│   │   └── tileset/              # 瓦片集
│   ├── sounds/                    # 音效资源
│   └── sprites/                   # 精灵资源
├── scenes/                        # 场景文件目录
├── scripts/                       # 脚本文件目录
├── project.godot                  # Godot项目配置
├── README.md                      # 项目说明
└── CLAUDE.md                      # Claude开发配置
```

## 执行流程

### 1. 创建项目目录
以用户输入的项目名称创建目录

### 2. 拷贝模板文件
从 `templates/` 目录拷贝所有文件到项目目录

### 3. 更新项目配置
修改 `project.godot` 中的项目名称：
```ini
[application]
config/name="项目名称"
```

### 4. 设置引擎版本
要求用户输入Godot引擎版本（最低4.5），更新配置：
```ini
[application]
config/features=PackedStringArray("用户输入版本", "GL Compatibility")
```

### 5. 配置渲染器类型
提供渲染器选项：
- Forward+（默认）
- 移动
- 兼容

根据用户选择更新渲染器配置：
```ini
[rendering]
renderer/rendering_method="用户选择"
renderer/rendering_method.mobile="用户选择"
```

## 注意事项

- 所有目录都包含 `.gitkeeper` 文件以保持目录结构
- `.godot` 目录包含编辑器缓存和配置
- 模板文件中的占位符需要替换为实际项目名称
- 确保版本号格式正确（如 "4.5", "4.6"）
- 渲染器类型使用Godot标准命名