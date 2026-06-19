---
description: godot项目初始化
agent: build
---

1. 如果 $1 为空，则默认为 `init`
2. 如果 $1 为 `init`，则执行:

   1. 如果当前操作系统为mac，执行
   ```bash
   # 拷贝函数：目标已存在则跳过
   copy_dir()  { [ -d "$2" ] || cp -r "$1" "$2"; }
   copy_file() { [ -f "$2" ] || cp "$1" "$2"; }

   copy_dir  ~/workspace/code/07_games/GodotScaffolding/.opencode ./.opencode
   copy_dir  ~/workspace/code/07_games/GodotScaffolding/assets ./assets
   copy_dir  ~/workspace/code/07_games/GodotScaffolding/scenes ./scenes
   copy_dir  ~/workspace/code/07_games/GodotScaffolding/scripts ./scripts
   copy_dir  ~/workspace/code/07_games/GodotScaffolding/docs ./docs
   copy_dir  ~/workspace/code/07_games/GodotScaffolding/addons ./addons
   copy_dir  ~/workspace/code/07_games/GodotScaffolding/test ./test
   copy_file ~/workspace/code/07_games/GodotScaffolding/.gitignore ./.gitignore
   copy_file ~/workspace/code/07_games/GodotScaffolding/opencode.json ./opencode.json
   copy_file ~/workspace/code/07_games/GodotScaffolding/AGETNS.md ./AGETNS.md
   copy_file ~/workspace/code/07_games/GodotScaffolding/README.md ./README.md

   copy_dir  ~/workspace/code/07_games/GodotScaffolding/.zcode ./.zcode
   copy_dir  ~/workspace/code/07_games/GodotScaffolding/.opencode/skills ./.zcode/skills
   sed -i '' "s/brave-legend/$(basename $(pwd))/g" ./opencode.json
   sed -i '' "s/brave-legend/$(basename $(pwd))/g" ./zcode/config.json
   copy_file ~/workspace/code/07_games/GodotScaffolding/.env.example ./.env

   # 替换 {env:VAR} 占位符为对应环境变量的值（环境变量未设置则保留原占位符）
   perl -i -pe 's/\{env:(\w+)\}/defined $ENV{$1} ? $ENV{$1} : "{env:$1}"/ge' ./.zcode/config.json
   ```

   2. 拷贝完成后，提醒用户：
   > ⚠️ 已自动从 `.env.example` 生成 `.env` 文件，请根据项目需要填写其中的配置项。

   2. 如果当前操作系统为windows，执行
   ```powershell
   # 拷贝函数：目标已存在则跳过
   function Copy-DirIfNotExists($src, $dest)  { if (-not (Test-Path $dest)) { xcopy $src $dest /E /I /H /Y } }
   function Copy-FileIfNotExists($src, $dest) { if (-not (Test-Path $dest)) { copy $src $dest } }

   Copy-DirIfNotExists  "~\workspace\code\07_games\GodotScaffolding\.opencode" ".opencode"
   Copy-DirIfNotExists  "~\workspace\code\07_games\GodotScaffolding\assets" "assets"
   Copy-DirIfNotExists  "~\workspace\code\07_games\GodotScaffolding\scenes" "scenes"
   Copy-DirIfNotExists  "~\workspace\code\07_games\GodotScaffolding\scripts" "scripts"
   Copy-DirIfNotExists  "~\workspace\code\07_games\GodotScaffolding\docs" "docs"
   Copy-DirIfNotExists  "~\workspace\code\07_games\GodotScaffolding\addons" "addons"
   Copy-DirIfNotExists  "~\workspace\code\07_games\GodotScaffolding\test" "test"
   Copy-FileIfNotExists "~\workspace\code\07_games\GodotScaffolding\.gitignore" ".gitignore"
   Copy-FileIfNotExists "~\workspace\code\07_games\GodotScaffolding\opencode.json" "opencode.json"
   Copy-FileIfNotExists "~\workspace\code\07_games\GodotScaffolding\AGETNS.md" "AGETNS.md"
   Copy-FileIfNotExists "~\workspace\code\07_games\GodotScaffolding\README.md" "README.md"

   Copy-DirIfNotExists  "~\workspace\code\07_games\GodotScaffolding\.zcode" ".zcode"
   Copy-DirIfNotExists  "~\workspace\code\07_games\GodotScaffolding\.opencode\skills" ".zcode\skills"

   $projectName = Split-Path -Leaf (Get-Location)
   (Get-Content "opencode.json" -Raw) -replace 'brave-legend', $projectName | Set-Content "opencode.json" -NoNewline

   $projectName = Split-Path -Leaf (Get-Location)
   (Get-Content ".zcode/config.json" -Raw) -replace 'brave-legend', $projectName | Set-Content ".zcode/config.json" -NoNewline

   Copy-FileIfNotExists "~\workspace\code\07_games\GodotScaffolding\.env.example" ".env"

   # 替换 {env:VAR} 占位符为对应环境变量的值（环境变量未设置则保留原占位符）
   $replaceEnv = { param($m); $v = [Environment]::GetEnvironmentVariable($m.Groups[1].Value); if ($v) { $v } else { $m.Groups[0].Value } }
   $__cfg = Get-Content ".zcode/config.json" -Raw
   $__cfg = [regex]::Replace($__cfg, '\{env:(\w+)\}', $replaceEnv)
   Set-Content ".zcode/config.json" $__cfg -NoNewline
   ```

   3. 拷贝完成后，提醒用户：
   > ⚠️ 已自动从 `.env.example` 生成 `.env` 文件，请根据项目需要填写其中的配置项。

注意：
- 拷贝前会判断目标是否已存在，已存在则跳过，避免覆盖用户已有文件
- `.zcode/config.json` 中的 `{env:VAR}` 占位符会读取同名环境变量替换；环境变量未设置时保留占位符
- xcopy 的 `/E` 参数表示复制子目录，包括空的子目录
- `/I` 参数表示如果目标不存在，则创建目录
- `/H` 参数表示复制隐藏文件和系统文件
- `/Y` 参数表示覆盖已存在文件时不提示
- copy 命令用于复制单个文件
