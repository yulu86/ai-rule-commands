---
name: godot-project-init
description: godot项目初始化
---

godot项目初始化工具

## 执行流程
1. 如果当前操作系统为mac，执行
```bash
cp -r ~/workspace/code/07_games/GodotScaffolding/.claude ./
cp -r ~/workspace/code/07_games/GodotScaffolding/assets ./
cp -r ~/workspace/code/07_games/GodotScaffolding/scenes ./
cp -r ~/workspace/code/07_games/GodotScaffolding/scripts ./
cp -r ~/workspace/code/07_games/GodotScaffolding/addons ./
cp -r ~/workspace/code/07_games/GodotScaffolding/test ./
cp ~/workspace/code/07_games/GodotScaffolding/.gitignore ./
cp ~/workspace/code/07_games/GodotScaffolding/CLAUDE.md ./
cp ~/workspace/code/07_games/GodotScaffolding/README.md ./
```

2. 如果当前操作系统为windows，执行
```powershell
robocopy "~\workspace\code\07_games\GodotScaffolding\.claude" ".claude" /E /NFL /NDL
robocopy "~\workspace\code\07_games\GodotScaffolding\assets" "assets" /E /NFL /NDL
robocopy "~\workspace\code\07_games\GodotScaffolding\scenes" "scenes" /E /NFL /NDL
robocopy "~\workspace\code\07_games\GodotScaffolding\scripts" "scripts" /E /NFL /NDL
robocopy "~\workspace\code\07_games\GodotScaffolding\addons" "addons" /E /NFL /NDL
robocopy "~\workspace\code\07_games\GodotScaffolding\test" "test" /E /NFL /NDL
copy "~\workspace\code\07_games\GodotScaffolding\.gitignore" ".gitignore"
copy "~\workspace\code\07_games\GodotScaffolding\CLAUDE.md" "CLAUDE.md"
copy "~\workspace\code\07_games\GodotScaffolding\README.md" "README.md"
```

注意：
- robocopy 的 `/E` 参数表示复制子目录，包括空的子目录
- `/NFL` 和 `/NDL` 参数用于减少输出，只显示错误和失败的文件
- copy 命令用于复制单个文件