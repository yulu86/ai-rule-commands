---
name: godot-project-init
description: godot项目初始化
---

godot项目初始化工具

## 执行流程
1. 如果当前操作系统为mac，执行
```bash
cp -r /Users/xuyulu/workspace/code/07_games/GodotScaffolding/.claude ./
cp -r /Users/xuyulu/workspace/code/07_games/GodotScaffolding/assets ./
cp -r /Users/xuyulu/workspace/code/07_games/GodotScaffolding/scenes ./
cp -r /Users/xuyulu/workspace/code/07_games/GodotScaffolding/scripts ./
cp -r /Users/xuyulu/workspace/code/07_games/GodotScaffolding/addons ./
cp -r /Users/xuyulu/workspace/code/07_games/GodotScaffolding/test ./
cp /Users/xuyulu/workspace/code/07_games/GodotScaffolding/.gitignore ./
cp /Users/xuyulu/workspace/code/07_games/GodotScaffolding/CLAUDE.md ./
cp /Users/xuyulu/workspace/code/07_games/GodotScaffolding/README.md ./
```

2. 安装`GUT`插件
- 使用`curl`从`https://github.com/bitwes/gut/releases`下载最新的zip包
- 解压zip包后，将`gut`目录放入项目的`addons`文件夹中