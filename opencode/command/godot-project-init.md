---
description: godot项目初始化
agent: build
---

1. 如果 $1 为空，则默认为 `init`
2. 如果 $1 为 `init`，则执行:

   1. 如果当前操作系统为mac，执行
   ```bash
   cp -r ~/workspace/code/07_games/GodotScaffolding/.opencode ./
   cp -r ~/workspace/code/07_games/GodotScaffolding/assets ./
   cp -r ~/workspace/code/07_games/GodotScaffolding/scenes ./
   cp -r ~/workspace/code/07_games/GodotScaffolding/scripts ./
   cp -r ~/workspace/code/07_games/GodotScaffolding/docs ./
   cp -r ~/workspace/code/07_games/GodotScaffolding/addons ./
   cp -r ~/workspace/code/07_games/GodotScaffolding/test ./
   cp ~/workspace/code/07_games/GodotScaffolding/.gitignore ./
   cp ~/workspace/code/07_games/GodotScaffolding/opencode.json.template ./
   cp ~/workspace/code/07_games/GodotScaffolding/opencode.json.template ./opencode.json
   cp ~/workspace/code/07_games/GodotScaffolding/CONTRIBUTING.md ./
   cp ~/workspace/code/07_games/GodotScaffolding/README.md ./
   ```

   2. 如果当前操作系统为windows，执行
   ```powershell
   xcopy "~\workspace\code\07_games\GodotScaffolding\.opencode" ".opencode" /E /I /H /Y
   xcopy "~\workspace\code\07_games\GodotScaffolding\assets" "assets" /E /I /H /Y
   xcopy "~\workspace\code\07_games\GodotScaffolding\scenes" "scenes" /E /I /H /Y
   xcopy "~\workspace\code\07_games\GodotScaffolding\scripts" "scripts" /E /I /H /Y
   xcopy "~\workspace\code\07_games\GodotScaffolding\docs" "docs" /E /I /H /Y
   xcopy "~\workspace\code\07_games\GodotScaffolding\addons" "addons" /E /I /H /Y
   xcopy "~\workspace\code\07_games\GodotScaffolding\test" "test" /E /I /H /Y
   copy "~\workspace\code\07_games\GodotScaffolding\.gitignore" ".gitignore"
   copy "~\workspace\code\07_games\GodotScaffolding\opencode.json.template" "opencode.json.template"
   copy "~\workspace\code\07_games\GodotScaffolding\opencode.json.template" "opencode.json"
   copy "~\workspace\code\07_games\GodotScaffolding\CONTRIBUTING.md" "CONTRIBUTING.md"
   copy "~\workspace\code\07_games\GodotScaffolding\README.md" "README.md"
   ```

注意：
- xcopy 的 `/E` 参数表示复制子目录，包括空的子目录
- `/I` 参数表示如果目标不存在，则创建目录
- `/H` 参数表示复制隐藏文件和系统文件
- `/Y` 参数表示覆盖已存在文件时不提示
- copy 命令用于复制单个文件