# Architecture Designer Skill - 内部参考文档

## 技能概述
这是一个高质量的架构设计文档编写技能，能够使用文本、表格和mermaid图的合理组合来输出架构设计文档。

## 技能结构
- `SKILL.md` - 技能主文件，包含使用说明和指导
- `assets/` - 模板文件和资产
  - `architecture-template.md` - 标准架构设计文档模板
  - `microservices-template.md` - 微服务架构模板  
  - `adr-template.md` - 架构决策记录模板
- `references/` - 参考资源
  - `patterns.md` - 架构模式参考
  - `best-practices.md` - 最佳实践指南
  - `tech-stack.md` - 技术栈选型参考
- `scripts/` - 自动化脚本
  - `arch_diagram_generator.py` - 架构图生成器
  - `example_config.yml` - 示例配置文件

## 主要功能
1. 深度思考分析 - 使用Sequential Thinking工具全面分析需求
2. 信息收集验证 - 使用context7查询相关API和SDK文档
3. 架构设计决策 - 基于分析结果做出架构决策
4. 文档结构设计 - 选择合适的模板和图表类型
5. 内容生成输出 - 使用文本、表格、mermaid图组合输出

## 集成工具
- Sequential Thinking Server: 深度思考和分析
- context7: API和SDK文档查询
- mermaid: 图表生成

## 技能状态
✅ 目录结构创建完成
✅ SKILL.md核心内容编写完成
✅ 架构设计模板和参考资源创建完成
✅ Sequential Thinking工具集成指南完成
✅ context7 API查询指南集成完成

## 下一步
技能已完成开发，可以进行打包发布。