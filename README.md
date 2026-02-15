# AI工具rule

## 0. 安装 `oh-my-opencode`

```bash
npx oh-my-opencode install
```

## 1. 配置连接

### windows cmd (管理员模式)
```bash
mklink "C:\Users\Yulu Xu\.config\opencode\AGENTS.md" "D:\workspace\code\01_AI\ai-rule-commands\opencode\AGENTS.md"
mklink "C:\Users\Yulu Xu\.config\opencode\oh-my-opencode.json" "D:\workspace\code\01_AI\ai-rule-commands\opencode\oh-my-opencode.jsonc"
mklink "C:\Users\Yulu Xu\.config\opencode\opencode.jsonc" "D:\workspace\code\01_AI\ai-rule-commands\opencode\opencode.jsonc"
mklink /d "C:\Users\Yulu Xu\.config\opencode\agents" "D:\workspace\code\01_AI\ai-rule-commands\opencode\agents"
mklink /d "C:\Users\Yulu Xu\.config\opencode\command" "D:\workspace\code\01_AI\ai-rule-commands\opencode\command"
mklink /d "C:\Users\Yulu Xu\.config\opencode\skills" "D:\workspace\code\01_AI\ai-rule-commands\opencode\skills"
```

### mac
```bash
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/opencode/AGENTS.md" "/Users/xuyulu/.config/opencode/AGENTS.md"
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/opencode/oh-my-opencode.jsonc" "/Users/xuyulu/.config/opencode/oh-my-opencode.jsonc"
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/opencode/opencode.jsonc" "/Users/xuyulu/.config/opencode/opencode.jsonc"
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/opencode/agents" "/Users/xuyulu/.config/opencode/agents"
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/opencode/command" "/Users/xuyulu/.config/opencode/command"
ln -s "/Users/xuyulu/workspace/code/01_AI/ai-rule-commands/opencode/skills" "/Users/xuyulu/.config/opencode/skills"
