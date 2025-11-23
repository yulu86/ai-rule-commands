#!/usr/bin/env python3
"""
安全漏洞扫描工具
检测代码中的常见安全问题
"""

import os
import re
import sys
import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SecurityIssue:
    """安全问题数据类"""
    file_path: str
    line_number: int
    severity: str  # 'critical', 'high', 'medium', 'low'
    category: str  # 'injection', 'xss', 'auth', 'crypto', etc.
    title: str
    description: str
    recommendation: str
    code_snippet: str

class SecurityScanner:
    """安全漏洞扫描器"""
    
    def __init__(self):
        self.issues: List[SecurityIssue] = []
        self.patterns = self._load_security_patterns()
    
    def _load_security_patterns(self) -> Dict[str, List[Dict]]:
        """加载安全检测模式"""
        return {
            'sql_injection': [
                {
                    'pattern': r'(execute|query|raw|exec)\s*\(\s*["\'].*?\+.*?["\']',
                    'severity': 'critical',
                    'description': 'SQL字符串拼接，存在注入风险',
                    'recommendation': '使用参数化查询或ORM'
                },
                {
                    'pattern': r'format\s*\(\s*["\'].*?%.*?["\']',
                    'severity': 'high', 
                    'description': '字符串格式化构建SQL语句',
                    'recommendation': '使用参数绑定'
                }
            ],
            'xss': [
                {
                    'pattern': r'(innerHTML|outerHTML)\s*=\s*.*?\+',
                    'severity': 'high',
                    'description': '直接插入用户输入到HTML，存在XSS风险',
                    'recommendation': '使用textContent或进行HTML转义'
                },
                {
                    'pattern': r'document\.write\s*\(\s*.*?\+',
                    'severity': 'critical',
                    'description': 'document.write使用用户输入，XSS风险极高',
                    'recommendation': '使用DOM API更新页面内容'
                }
            ],
            'command_injection': [
                {
                    'pattern': r'(os\.system|subprocess\.call|exec|shell_exec)\s*\(\s*.*?\+',
                    'severity': 'critical',
                    'description': '命令行参数拼接，存在命令注入风险',
                    'recommendation': '使用参数化命令或严格验证输入'
                }
            ],
            'path_traversal': [
                {
                    'pattern': r'open\s*\(\s*["\'].*?\+.*?["\']',
                    'severity': 'high',
                    'description': '文件路径拼接，存在路径遍历风险',
                    'recommendation': '验证文件路径，限制访问目录'
                }
            ],
            'hardcoded_secrets': [
                {
                    'pattern': r'(password|passwd|pwd|secret|key|token)\s*=\s*["\'][^"\']{4,}["\']',
                    'severity': 'high',
                    'description': '硬编码的敏感信息',
                    'recommendation': '使用环境变量或配置文件存储敏感信息'
                },
                {
                    'pattern': r'(api_key|apikey|access_key)\s*=\s*["\'][^"\']{10,}["\']',
                    'severity': 'high',
                    'description': '硬编码的API密钥',
                    'recommendation': '使用安全的密钥管理方案'
                }
            ],
            'weak_crypto': [
                {
                    'pattern': r'(md5|sha1)\s*\(',
                    'severity': 'medium',
                    'description': '使用弱哈希算法',
                    'recommendation': '使用SHA-256或更强的哈希算法'
                },
                {
                    'pattern': r'des_|3des|rc4',
                    'severity': 'high',
                    'description': '使用弱加密算法',
                    'recommendation': '使用AES等现代加密算法'
                }
            ],
            'insecure_random': [
                {
                    'pattern': r'(Math\.random|random\.random|random\.randint)\s*\(',
                    'severity': 'medium',
                    'description': '使用不安全的随机数生成器',
                    'recommendation': '使用加密安全的随机数生成器'
                }
            ],
            'debug_info': [
                {
                    'pattern': r'(console\.log|print|alert)\s*\(\s*.*?(password|token|key|secret)',
                    'severity': 'low',
                    'description': '可能泄露敏感信息的调试输出',
                    'recommendation': '移除或注释掉敏感信息的调试输出'
                }
            ]
        }
    
    def scan_file(self, file_path: str) -> List[SecurityIssue]:
        """扫描单个文件"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            for line_num, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # 跳过注释行
                if line_stripped.startswith('#') or line_stripped.startswith('//') or line_stripped.startswith('/*'):
                    continue
                
                # 检查各种安全模式
                for category, patterns in self.patterns.items():
                    for pattern_info in patterns:
                        matches = re.finditer(pattern_info['pattern'], line, re.IGNORECASE)
                        for match in matches:
                            # 获取代码片段
                            start_pos = max(0, match.start() - 20)
                            end_pos = min(len(line), match.end() + 20)
                            code_snippet = line[start_pos:end_pos].strip()
                            
                            issue = SecurityIssue(
                                file_path=file_path,
                                line_number=line_num,
                                severity=pattern_info['severity'],
                                category=category,
                                title=f"{category.replace('_', ' ').title()} 检测",
                                description=pattern_info['description'],
                                recommendation=pattern_info['recommendation'],
                                code_snippet=code_snippet
                            )
                            issues.append(issue)
            
            # 特定语言的额外检查
            if file_ext == '.py':
                issues.extend(self._scan_python_issues(lines, file_path))
            elif file_ext in ['.js', '.jsx', '.ts', '.tsx']:
                issues.extend(self._scan_javascript_issues(lines, file_path))
        
        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")
        
        return issues
    
    def _scan_python_issues(self, lines: List[str], file_path: str) -> List[SecurityIssue]:
        """Python特定的安全问题检查"""
        issues = []
        
        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # 检查pickle反序列化
            if re.search(r'pickle\.loads?|cPickle\.loads?', line, re.IGNORECASE):
                issues.append(SecurityIssue(
                    file_path=file_path,
                    line_number=line_num,
                    severity='high',
                    category='deserialization',
                    title='不安全的反序列化',
                    description='使用pickle进行反序列化存在代码执行风险',
                    recommendation='使用JSON或其他安全的序列化格式',
                    code_snippet=line.strip()
                ))
            
            # 检查eval/exec
            if re.search(r'\b(eval|exec)\s*\(', line):
                issues.append(SecurityIssue(
                    file_path=file_path,
                    line_number=line_num,
                    severity='critical',
                    category='code_injection',
                    title='危险的代码执行',
                    description='使用eval或exec执行动态代码存在安全风险',
                    recommendation='避免使用eval/exec，考虑使用更安全的替代方案',
                    code_snippet=line.strip()
                ))
        
        return issues
    
    def _scan_javascript_issues(self, lines: List[str], file_path: str) -> List[SecurityIssue]:
        """JavaScript特定的安全问题检查"""
        issues = []
        
        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # 检查eval
            if re.search(r'\beval\s*\(', line):
                issues.append(SecurityIssue(
                    file_path=file_path,
                    line_number=line_num,
                    severity='critical',
                    category='code_injection',
                    title='使用eval函数',
                    description='eval函数存在代码注入风险',
                    recommendation='避免使用eval，使用JSON.parse或其他安全替代方案',
                    code_snippet=line.strip()
                ))
            
            # 检查innerHTML赋值
            if re.search(r'innerHTML\s*=\s*.*?[+{]', line):
                issues.append(SecurityIssue(
                    file_path=file_path,
                    line_number=line_num,
                    severity='high',
                    category='xss',
                    title='潜在的XSS漏洞',
                    description='直接赋值innerHTML可能导致XSS攻击',
                    recommendation='使用textContent或对输入进行HTML转义',
                    code_snippet=line.strip()
                ))
        
        return issues
    
    def scan_directory(self, directory: str) -> List[SecurityIssue]:
        """扫描目录中的所有代码文件"""
        all_issues = []
        
        for root, dirs, files in os.walk(directory):
            # 跳过常见的非代码目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # 只扫描代码文件
                if file_ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp']:
                    file_issues = self.scan_file(file_path)
                    all_issues.extend(file_issues)
        
        return all_issues
    
    def generate_report(self, issues: List[SecurityIssue]) -> Dict[str, Any]:
        """生成安全扫描报告"""
        if not issues:
            return {
                "summary": {
                    "total_issues": 0,
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                },
                "issues": [],
                "recommendations": ["未发现安全漏洞，继续保持良好的安全编码实践"]
            }
        
        # 按严重程度统计
        severity_counts = {
            'critical': sum(1 for issue in issues if issue.severity == 'critical'),
            'high': sum(1 for issue in issues if issue.severity == 'high'),
            'medium': sum(1 for issue in issues if issue.severity == 'medium'),
            'low': sum(1 for issue in issues if issue.severity == 'low')
        }
        
        # 按严重程度排序
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_issues = sorted(issues, key=lambda x: (severity_order[x.severity], x.file_path, x.line_number))
        
        # 生成建议
        recommendations = []
        
        if severity_counts['critical'] > 0:
            recommendations.append(f"发现 {severity_counts['critical']} 个严重安全漏洞，需要立即修复")
        
        if severity_counts['high'] > 0:
            recommendations.append(f"发现 {severity_counts['high']} 个高风险问题，建议尽快修复")
        
        recommendations.extend([
            "定期进行安全代码审查",
            "使用静态分析工具进行自动化安全检测",
            "建立安全编码规范和培训机制"
        ])
        
        return {
            "summary": {
                "total_issues": len(issues),
                **severity_counts
            },
            "issues": [
                {
                    "file": issue.file_path,
                    "line": issue.line_number,
                    "severity": issue.severity,
                    "category": issue.category,
                    "title": issue.title,
                    "description": issue.description,
                    "recommendation": issue.recommendation,
                    "code": issue.code_snippet
                }
                for issue in sorted_issues
            ],
            "recommendations": recommendations
        }

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("Usage: python security_scan.py <file_or_directory>")
        sys.exit(1)
    
    path = sys.argv[1]
    scanner = SecurityScanner()
    
    if os.path.isfile(path):
        # 扫描单个文件
        issues = scanner.scan_file(path)
    
    elif os.path.isdir(path):
        # 扫描目录
        issues = scanner.scan_directory(path)
    
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)
    
    # 生成并输出报告
    report = scanner.generate_report(issues)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 如果有严重问题，返回非零退出码
    if any(issue['severity'] in ['critical', 'high'] for issue in report['issues']):
        sys.exit(1)

if __name__ == "__main__":
    main()