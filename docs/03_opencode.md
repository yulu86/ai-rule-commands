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

#### godot-mcp
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

#### context7-mcp
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

#### chrome-devtools-mcp
```bash
npm -g install chrome-devtools-mcp
```

```json
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
```

#### excalidraw:
```bash
docker pull excalidraw/excalidraw:latest
docker run -d -p 8090:80 --restart=always --name excalidraw excalidraw/excalidraw:latest

npm -g install excalidraw-mcp
```

```json
    "excalidraw": {
      "command": "npx",
      "args": ["-y", "excalidraw-mcp"]
    }
```

#### ~~[multi-ai-advisor-mcp](https://github.com/YuChenSSR/multi-ai-advisor-mcp)~~

```bash
git clone https://gh-proxy.com/https://github.com/YuChenSSR/multi-ai-advisor-mcp.git 
cd multi-ai-advisor-mcp

npm install
npm run build
```

```json
    "multi-model-advisor": {
      "command": "node",
      "args": [
        // "D:/workspace/code/01_AI/multi-ai-advisor-mcp/build/index.js"
        "/Users/xuyulu/workspace/code/01_AI/multi-ai-advisor-mcp/build/index.js"
      ]
    }
```

### GLM工具(视觉工具、联网搜索、网页读取)

```json
    "web-search-prime": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp",
      "headers": {
        "Authorization": "Bearer <API KEY>"
      }
    },
    "web-reader": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/web_reader/mcp",
      "headers": {
        "Authorization": "Bearer <API KEY>"
      }
    },
    "zai-mcp-server": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "@z_ai/mcp-server"
      ],
      "env": {
        "Z_AI_API_KEY": "<API KEY>"
      }
    }
```


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
                "TAVILY_API_KEY": "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"
            }
        },
        "web-search-prime": {
            "type": "remote",
            "url": "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp",
            "headers": {
                "Authorization": "Bearer <API KEY>"
            }
        },
        "web-reader": {
            "type": "remote",
            "url": "https://open.bigmodel.cn/api/mcp/web_reader/mcp",
            "headers": {
                "Authorization": "Bearer <API KEY>"
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
                "Z_AI_API_KEY": "<API KEY>"
            }
        }
    }
}
```