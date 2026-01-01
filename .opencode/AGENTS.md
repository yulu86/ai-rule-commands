# 基本设置
- 语言：中文输出

# 工作原则
1. First think through the problem, read the codebase for relevant files, and write a plan to tasks/todo.md.
2. The plan should have a list of todo items that you can check off as you complete them.
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high-level explanation of what changes you made.
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes.
Every change should impact as little code as possible. Everything is about simplicity.
7. Finally, add a review section to the todo.md file with a summary of the changes you made and any other relevant
information.
8. DO NOT BE LAZY. NEVER BE LAZY. IF THERE IS A BUG, FIND THE ROOT CAUSE AND FIX IT. NO TEMPORARY FIXES. YOU ARE A SENIOR
DEVELOPER. NEVER BE LAZY.
9. MAKE ALL FIXES AND CODE CHANGES AS SIMPLE AS HUMANLY POSSIBLE. THEY SHOULD ONLY IMPACT NECESSARY CODE RELEVANT TO THE
TASK AND NOTHING ELSE. IT SHOULD IMPACT AS LITTLE CODE AS POSSIBLE. YOUR GOAL IS TO NOT INTRODUCE ANY BUGS. IT'S ALL ABOUT
SIMPLICITY. use context7

# 细节规范

## 文档规范
- 命名：{两位序号}_{中文名称}.md（序号从01自增）
- 序号规则：目录下已存在文件时从最大序号递增

## 文件操作
- 使用filesystem工具
- 重要配置变更同步到memory
- 标准化路径和命名

## 项目分析
- 分析项目代码目录时忽略 .gitignore中指定的目录和文件
- 在执行 /init 命令时，同时把项目代码目录用ASCII树形式添加到 AGENTS.md 文件中

## github加速
在clone或下载`https://github.com`的资源时，使用代理(`https://gh-proxy.org`)以提高下载速度，例如:
1. ```curl -JLO https://github.com/tillberg/gut/archive/refs/tags/v1.0.3.tar.gz``` 转换成 ```curl -JLO https://gh-proxy.org/https://github.com/tillberg/gut/archive/refs/tags/v1.0.3.tar.gz```
2. ```uv tool install specify-cli --from git+https://github.com/github/spec-kit.git``` 转换成 ```uv tool install specify-cli --from git+https://gh-proxy.org/https://github.com/github/spec-kit.git```

## git提交
1. git commit的message内容请使用中文