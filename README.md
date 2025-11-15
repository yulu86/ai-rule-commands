# AI工具rule

## 1. 启动`qdrant`

```bash
docker compose -f qdrant-docker-compose.yaml down

docker compose -f qdrant-docker-compose.yaml up -d
```

## 2. 配置`continue`


# windows cmd (管理员模式)
```bash
mklink "C:\Users\Yulu Xu\.continue\config.yaml" "D:\workspace\code\01_AI\ai-rule-commands\.continue\config.yaml"
```

# mac
```bash
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/.continue/config.yaml" "/Users/xuyulu/.continue/config.yaml"
```

## 3. 配置`claude code`

### 3.1 安装`claude code`，对接`deepseek`
```bash
# 设置npm源
npm config set registry https://registry.npmmirror.com/
```

参考`[https://api-docs.deepseek.com/zh-cn/guides/anthropic_api](https://api-docs.deepseek.com/zh-cn/guides/anthropic_api)`配置deepseek，环境变量
```
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=${DEEPSEEK_API_KEY}
export API_TIMEOUT_MS=600000
export ANTHROPIC_MODEL=deepseek-chat
export ANTHROPIC_SMALL_FAST_MODEL=deepseek-chat
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
```

启动`claude code`
```bash
claude
```

### 3.2 配置`claude code`

#### 配置代理

```bash
mkdir -p ~/.claude
vim ~/.claude/settings.json
```

增加
```json
  "env": {
    "HTTP_PROXY": "http://127.0.0.1:7890",
    "HTTPS_PROXY": "http://127.0.0.1:7890"
  },
```



#### windows cmd (管理员模式)
```bash
mklink "C:\Users\Yulu Xu\.claude\CLAUDE.md" "D:\workspace\code\01_AI\ai-rule-commands\.claude\CLAUDE.md"
mklink /d "C:\Users\Yulu Xu\.claude\agents" "D:\workspace\code\01_AI\ai-rule-commands\.claude\agents"
mklink /d "C:\Users\Yulu Xu\.claude\commands" "D:\workspace\code\01_AI\ai-rule-commands\.claude\commands"
```

#### mac
```bash
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/.claude/CLAUDE.md" "/Users/xuyulu/.claude/CLAUDE.md"
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/.claude/agents" "/Users/xuyulu/.claude/agents"
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/.claude/commands" "/Users/xuyulu/.claude/commands"
```

---
以下内容为可选

---

### 3.3 安装`mcp-server`

> mcp server可查找：
> [https://github.com/punkpeye/awesome-mcp-servers?tab=readme-ov-file](https://github.com/punkpeye/awesome-mcp-servers?tab=readme-ov-file)
> [https://code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp)


#### filesystem
```bash
npm i -g @modelcontextprotocol/server-filesystem
```

```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/Users/xuyulu/workspace/code"
  ]
}
```

#### thinking
```bash
npm i -g @modelcontextprotocol/server-sequential-thinking
claude mcp add thinking -s user -- server-sequential-thinking
```

```json
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    }
```

#### server-memory
```bash
npm i -g @modelcontextprotocol/server-memory
```

```json
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
```

#### tavily-mcp
```bash
npm i -g tavily-mcp@latest
```

```json
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "your-api-key-here"
      }
    }
```


### godot-mcp
[godot-mcp](https://github.com/Coding-Solo/godot-mcp)

```json
    "godot": {
      "command": "node",
      "args": ["D:/workspace/code/01_AI/godot-mcp/build/index.js"],
      "env": {
        "DEBUG": "false"
      }
    }
```

### context7-mcp
```bash
npm -g install @upstash/context7-mcp
```

```json
    "context7": {
      "command": "npx",
      "args": [
        "-y",
        "@upstash/context7-mcp"
      ],
      "env": {
        "api-key": "<api-key>"
      }
    }
```

> 提示词中增加 `use context7`

```

### 3.3 安装配置`claude-code-router`

```bash
npm i -g @musistudio/claude-code-router
```

配置参考 [claude-code-router/config.json](claude-code-router/config.json)
