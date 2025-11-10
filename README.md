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

#### openmemory-mcp
```bash
docker run -d --restart=always -p 8080:8080 mem0ai/openmemory-mcp
```



```plaintext
请在claude code中全局配置`mcp-server-memory`，对接到QDRANT，以保存记忆。QDRANT的访问地址 http://localhost:6333
```

### 3.3 安装配置`claude-code-router`

```bash
npm i -g @musistudio/claude-code-router
```

配置
```json
{
  "API_TIMEOUT_MS": 600000,
  "Providers": [
    {
      "name": "deepseek",
      "api_base_url": "https://api.deepseek.com/chat/completions",
      "api_key": "<key>",
      "models": ["deepseek-chat", "deepseek-reasoner"],
      "transformer": {
        "use": ["deepseek"],
        "deepseek-chat": {
          "use": ["tooluse"]
        }
      }
    },
    {
      "name": "moonshot",
      "api_base_url": "https://api.moonshot.cn/v1/chat/completions",
      "api_key": "<key>",
      "models": ["kimi-k2-0905-preview", "kimi-k2-thinking", "moonshot-v1-8k-vision-preview"],
      "transformer": {
        "use": ["moonshot"],
        "kimi-k2-0905-preview": {
          "use": ["tooluse"]
        }
      }
    },
    {
      "name": "ollama",
      "api_base_url": "http://localhost:11434/v1/chat/completions",
      "api_key": "ollama",
      "models": ["qwen3-coder:30b"]
    }
  ],
  "Router": {
    "default": "deepseek,deepseek-chat",
    "background": "ollama,qwen3-coder:30b",
    "think": "deepseek,deepseek-reasoner",
    "webSearch": "deepseek,deepseek-chat",
	"image": "moonshot,moonshot-v1-8k-vision-preview"
  },
  "CUSTOM_ROUTER_PATH": "D:/workspace/code/01_AI/ai-rule-commands/.claude/router.js"
}
```

```plaintext
请帮我写router.js。规则：
1. 当提示词包含中英文的写代码或输出编码，或者agent角色包含developer，使用 ollama,qwen3-coder:30b 
2. 当提示词包含中英文的检视代码或修复bug或修复issue，reviewer，使用 ollama,qwen3-coder:30b 
3. 当提示词需要识别图片内容时，使用moonshot,moonshot-v1-8k-vision-preview
4. 当提示词需要深度思考时，当前agent为godot-architect，使用deepseek,deepseek-reasoner
5. 默认使用 deepseek,deepseek-chat
```

`router.js`
```typescript
/**
 * A custom router function to determine which model to use based on the request.
 *
 * @param {object} req - The request object from Claude Code, containing the request body.
 * @param {object} config - The application's config object.
 * @returns {Promise<string|null>} - A promise that resolves to the "provider,model_name" string, or null to use the default router.
 */
module.exports = async function router(req, config) {
  const userMessage = req.body.messages.find((m) => m.role === "user")?.content;
  if (!userMessage) return null;

  const text = userMessage.toLowerCase();
  const role = (req.body.agent?.role || '').toLowerCase();

  // 1. 写代码 / 输出编码 / developer 角色
  const codeKeys = [
    '写代码', '编码', '代码', 'code', 'coding', 'write code', 'generate code', '输出编码'
  ];
  if (codeKeys.some(k => text.includes(k)) || role.includes('developer')) {
    return 'ollama,qwen3-coder:30b';
  }

  // 2. 检视代码 / 修复 bug / 修复 issue / reviewer 角色
  const reviewKeys = [
    '检视代码', 'review code', '修复bug', 'fix bug', '修复issue', 'fix issue', 'debug'
  ];
  if (reviewKeys.some(k => text.includes(k)) || role.includes('reviewer')) {
    return 'ollama,qwen3-coder:30b';
  }

  // 3. 需要识别图片内容
  const visionKeys = ['看图', '图片', '图像', '识别图', 'vision', 'image', 'picture', 'photo'];
  if (visionKeys.some(k => text.includes(k)) || text.includes('<image>') || text.includes('data:image')) {
    return 'moonshot,moonshot-v1-8k-vision-preview';
  }

  // 4. 需要深度思考 + godot-architect
  const reasoningKeys = [
    '深度思考', '推理', 'reason', 'deep think', '逐步思考', 'step by step',
    '逻辑', 'logic', '证明', 'prove', '分析', 'analyze'
  ];
  if (reasoningKeys.some(k => text.includes(k)) && role.includes('godot-architect')) {
    return 'deepseek,deepseek-reasoner';
  }

  // 5. 默认使用 deepseek-chat
  return 'deepseek,deepseek-chat';
};
```

启动
```bash
ccr restart
ccr code
```
