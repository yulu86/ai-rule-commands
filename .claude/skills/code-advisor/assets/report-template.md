# 代码审查报告

## 📊 审查概要

**项目名称**: {{PROJECT_NAME}}  
**审查时间**: {{REVIEW_DATE}}  
**审查范围**: {{REVIEW_SCOPE}}  
**审查者**: Code Advisor  

### 整体评估
- **代码质量等级**: {{QUALITY_GRADE}} (优秀/良好/一般/需要改进)
- **发现总问题数**: {{TOTAL_ISSUES}}
- **高优先级问题**: {{HIGH_PRIORITY_COUNT}}
- **中优先级问题**: {{MEDIUM_PRIORITY_COUNT}}  
- **低优先级问题**: {{LOW_PRIORITY_COUNT}}

---

## 🔴 高优先级问题

### 1. [安全漏洞] {{SECURITY_ISSUE_TITLE}}
**位置**: `{{FILE_PATH}}:{{LINE_NUMBER}}`  
**严重程度**: 高  
**问题描述**:  
{{SECURITY_ISSUE_DESCRIPTION}}

**风险评估**:  
- 影响: {{SECURITY_IMPACT}}
- 利用难度: {{SECURITY_DIFFICULTY}}
- 建议修复时间: {{SECURITY_TIMELINE}}

**修改建议**:  
{{SECURITY_SUGGESTION}}

**代码示例**:
```diff
- // 问题代码
{{BAD_CODE}}

+ // 建议修改
{{GOOD_CODE}}
```

**相关文档**: {{SECURITY_REFERENCES}}

---

## 🟡 中优先级问题

### 1. [性能问题] {{PERFORMANCE_ISSUE_TITLE}}
**位置**: `{{FILE_PATH}}:{{LINE_NUMBER}}`  
**严重程度**: 中  
**问题描述**:  
{{PERFORMANCE_ISSUE_DESCRIPTION}}

**性能影响**:  
- 时间复杂度: {{TIME_COMPLEXITY}}
- 空间复杂度: {{SPACE_COMPLEXITY}}
- 预期性能提升: {{PERFORMANCE_GAIN}}

**修改建议**:  
{{PERFORMANCE_SUGGESTION}}

**代码示例**:
```diff
- // 当前实现
{{CURRENT_CODE}}

+ // 优化建议
{{OPTIMIZED_CODE}}
```

### 2. [可维护性] {{MAINTAINABILITY_ISSUE_TITLE}}
**位置**: `{{FILE_PATH}}:{{LINE_NUMBER}}`  
**严重程度**: 中  
**问题描述**:  
{{MAINTAINABILITY_ISSUE_DESCRIPTION}}

**维护成本**: {{MAINTENANCE_COST}}

**修改建议**:  
{{MAINTAINABILITY_SUGGESTION}}

---

## 🟢 低优先级问题

### 1. [代码风格] {{STYLE_ISSUE_TITLE}}
**位置**: `{{FILE_PATH}}:{{LINE_NUMBER}}`  
**严重程度**: 低  
**问题描述**:  
{{STYLE_ISSUE_DESCRIPTION}}

**修改建议**:  
{{STYLE_SUGGESTION}}

---

## 📈 代码质量指标

| 指标 | 当前值 | 目标值 | 状态 |
|------|--------|--------|------|
| 代码覆盖率 | {{COVERAGE_PERCENT}}% | >80% | {{COVERAGE_STATUS}} |
| 圈复杂度 | {{CYCLOMATIC_COMPLEXITY}} | <10 | {{COMPLEXITY_STATUS}} |
| 重复代码率 | {{DUPLICATION_PERCENT}}% | <5% | {{DUPLICATION_STATUS}} |
| 技术债务 | {{TECHNICAL_DEBT}}小时 | <40小时 | {{DEBT_STATUS}} |

### 文件分析
```
{{FILE_ANALYSIS_CHART}}
```

---

## 🔧 具体修改建议

### 立即处理 (高优先级)
1. [ ] 修复安全漏洞：{{SECURITY_FIX_1}}
2. [ ] 解决稳定性问题：{{STABILITY_FIX_1}}
3. [ ] 优化关键性能瓶颈：{{PERFORMANCE_FIX_1}}

### 近期处理 (中优先级)
1. [ ] 重构复杂函数：{{REFACTOR_1}}
2. [ ] 改进错误处理：{{ERROR_HANDLING_1}}
3. [ ] 优化算法效率：{{ALGORITHM_OPTIMIZATION_1}}

### 长期改进 (低优先级)
1. [ ] 统一代码风格：{{STYLE_IMPROVEMENT_1}}
2. [ ] 完善文档注释：{{DOCUMENTATION_IMPROVEMENT_1}}
3. [ ] 增加单元测试：{{TEST_IMPROVEMENT_1}}

---

## 📚 推荐学习资源

### 安全最佳实践
- [OWASP Top 10]({{OWASP_LINK}})
- [安全编码规范]({{SECURITY_GUIDE_LINK}})

### 性能优化
- [JavaScript性能指南]({{JS_PERFORMANCE_LINK}})
- [数据库优化技巧]({{DB_OPTIMIZATION_LINK}})

### 代码质量
- [Clean Code原则]({{CLEAN_CODE_LINK}})
- [重构技巧]({{REFACTORING_LINK}})

---

## 🎯 改进行动计划

### 第一周 (紧急修复)
- [ ] 修复所有安全漏洞
- [ ] 解决稳定性问题
- [ ] 部署热修复版本

### 第二周 (性能优化)  
- [ ] 实施性能优化建议
- [ ] 重构关键模块
- [ ] 性能测试验证

### 第三-四周 (质量提升)
- [ ] 完善单元测试覆盖
- [ ] 改进代码文档
- [ ] 团队代码审查培训

---

## 📋 后续跟踪

### 复查计划
- **第一次复查**: {{FIRST_REVIEW_DATE}}
- **最终复查**: {{FINAL_REVIEW_DATE}}

### 成功标准
- [ ] 所有高优先级问题已解决
- [ ] 代码覆盖率提升至 >80%
- [ ] 性能指标达到预期
- [ ] 团队采纳最佳实践

### 联系信息
如有疑问或需要进一步的代码审查支持，请随时联系技术团队。

---
**报告生成时间**: {{REPORT_GENERATION_TIME}}  
**下次审查建议**: {{NEXT_REVIEW_SUGGESTION}}