# AI工具rule

## 1. 启动`qdrant`

```bash
docker compose -f qdrant-docker-compose.yaml down

docker compose -f qdrant-docker-compose.yaml up -d
```

## 2. 配置`continue`


## 3. 配置`kilo code`

### mac

```bash
ln -s /Users/xuyulu/workspace/code/01_AI/ai-rule-commands/.kilocode  /Users/xuyulu/.kilocode
```

### windows

#### cmd
```cmd
mklink /D "%USERPROFILE%\.kilocode" "C:\Users\xuyulu\workspace\code\01_AI\ai-rule-commands\.kilocode"
```

#### powershell
```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.kilocode" -Target "C:\Users\xuyulu\workspace\code\01_AI\ai-rule-commands\.kilocode"
```