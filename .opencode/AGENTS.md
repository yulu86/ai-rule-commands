# 基本设置
- 语言：中文输出
- session名称：使用中文作为session名称

# 规范

## 文件规范
- 标准化路径和命名
- 命名：{两位序号}_{中文名称}.md（序号从01自增）
- 序号规则：目录下已存在文件时从最大序号递增

## 项目分析
- 分析项目代码目录时忽略 .gitignore中指定的目录和文件
- 在执行 /init 命令时，同时把项目代码目录用ASCII树形式添加到 AGENTS.md 文件中

## github加速
在clone或下载`https://github.com`的资源时，使用代理(`https://gh-proxy.org`)以提高下载速度，例如:
1. ```curl -JLO https://github.com/tillberg/gut/archive/refs/tags/v1.0.3.tar.gz``` 转换成 ```curl -JLO https://gh-proxy.org/https://github.com/tillberg/gut/archive/refs/tags/v1.0.3.tar.gz```
2. ```uv tool install specify-cli --from git+https://github.com/github/spec-kit.git``` 转换成 ```uv tool install specify-cli --from git+https://gh-proxy.org/https://github.com/github/spec-kit.git```

## git提交
1. git commit的message内容请使用中文