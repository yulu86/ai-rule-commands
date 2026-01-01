# OpenCode

## 1. 配置连接

#### windows cmd (管理员模式)
```bash
```

#### mac
```bash
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/.opencode/AGENTS.md" "//Users/xuyulu/.config/opencode/AGENTS.md"
```

## 2. MCP 

### 安装
```bash
npm i -g @modelcontextprotocol/server-sequential-thinking
npm i -g tavily-mcp@latest
npm -g install @upstash/context7-mcp
npm -g install chrome-devtools-mcp
```


### 配置 ~/.config/opencode/opencode.json
```json
{
    "$schema": "https://opencode.ai/config.json",
    "mcp": {
        "sequential-thinking": {
            "type": "local",
            "command": [
                "npx",
                "-y",
                "@modelcontextprotocol/server-sequential-thinking"
            ]
        },
        "tavily-mcp": {
            "type": "local",
            "command": [
                "npx",
                "-y",
                "tavily-mcp@latest"
            ],
            "environment": {
                "TAVILY_API_KEY": "{env:TAVILY_API_KEY}"
            }
        },
        "context7": {
            "type": "local",
            "command": [
                "npx",
                "-y",
                "@upstash/context7-mcp"
            ],
            "environment": {
                "api-key": "{env:CONTEXT7_API_KEY}"
            }
        },
        "chrome-devtools": {
            "type": "local",
            "command": [
                "npx",
                "-y",
                "chrome-devtools-mcp@latest"
            ]
        },
        "web-search-prime": {
            "type": "remote",
            "url": "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp",
            "headers": {
                "Authorization": "Bearer {env:ANTHROPIC_AUTH_TOKEN}"
            }
        },
        "web-reader": {
            "type": "remote",
            "url": "https://open.bigmodel.cn/api/mcp/web_reader/mcp",
            "headers": {
                "Authorization": "Bearer {env:ANTHROPIC_AUTH_TOKEN}"
            }
        },
        "zai-mcp-server": {
            "type": "local",
            "command": [
                "npx",
                "-y",
                "@z_ai/mcp-server"
            ],
            "environment": {
                "Z_AI_API_KEY": "{env:ANTHROPIC_AUTH_TOKEN}"
            }
        }
    }
}
```