# AI工具rule

## 1. 启动`qdrant`

```bash
docker compose -f qdrant-docker-compose.yaml down

docker compose -f qdrant-docker-compose.yaml up -d
```

## 2. 配置`continue`



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

#### windows cmd (管理员模式)
```bash
mklink "C:\Users\Yulu Xu\.claude\CLAUDE.md" "D:\workspace\code\01_AI\ai-rule-commands\.claude\CLAUDE.md"
mklink /d "C:\Users\Yulu Xu\.claude\agents" "D:\workspace\code\01_AI\ai-rule-commands\.claude\agents"
```

#### mac
```bash
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/.claude/CLAUDE.md" "/Users/xuyulu/.claude/CLAUDE.md"
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/.claude/agents" "/Users/xuyulu/.claude/agents"
```

### 3.3 安装`mcp-server`

> mcp server可查找：
> [https://github.com/punkpeye/awesome-mcp-servers?tab=readme-ov-file](https://github.com/punkpeye/awesome-mcp-servers?tab=readme-ov-file)
> [https://code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp)


- [godot-mcp](https://github.com/Coding-Solo/godot-mcp)
- [mcp-client-for-ollama](https://github.com/jonigl/mcp-client-for-ollama)

```plaintext
请帮我全局安装并配置MCPServer: godot-mcp，参考 https://github.com/Coding-Solo/godot-mcp
```