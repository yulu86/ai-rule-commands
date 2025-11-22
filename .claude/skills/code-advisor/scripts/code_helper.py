#!/usr/bin/env python3
"""
代码助手脚本 - 辅助multi-model-advisor查询的预处理和后处理
"""

import re
import json
from typing import Dict, List, Any

class CodeHelper:
    """代码助手工具类"""

    def __init__(self):
        self.task_patterns = {
            'implement': r'实现|编写|输出|生成',
            'review': r'检视|审查|检查|审核',
            'explain': r'解释|说明|分析|讲解'
        }

    def detect_task_type(self, user_input: str) -> str:
        """检测任务类型"""
        for task_type, pattern in self.task_patterns.items():
            if re.search(pattern, user_input):
                return task_type
        return 'implement'  # 默认为实现任务

    def extract_code_context(self, user_input: str) -> Dict[str, Any]:
        """提取代码上下文信息"""
        context = {
            'language': self._detect_language(user_input),
            'framework': self._detect_framework(user_input),
            'task_type': self.detect_task_type(user_input),
            'requirements': user_input
        }
        return context

    def _detect_language(self, text: str) -> str:
        """检测编程语言"""
        languages = {
            'python': r'\bpython|py\b',
            'javascript': r'\bjavascript|js|node\b',
            'java': r'\bjava\b',
            'c++': r'\bc\+\+|cpp\b',
            'c#': r'\bcsharp|c#\b',
            'go': r'\bgolang|go\b',
            'rust': r'\brust\b',
            'typescript': r'\btypescript|ts\b'
        }

        for lang, pattern in languages.items():
            if re.search(pattern, text, re.IGNORECASE):
                return lang
        return 'python'  # 默认语言

    def _detect_framework(self, text: str) -> str:
        """检测框架"""
        frameworks = {
            'react': r'\breact\b',
            'vue': r'\bvue\b',
            'django': r'\bdjango\b',
            'flask': r'\bflask\b',
            'express': r'\bexpress\b',
            'spring': r'\bspring\b',
            'fastapi': r'\bfastapi\b'
        }

        for framework, pattern in frameworks.items():
            if re.search(pattern, text, re.IGNORECASE):
                return framework
        return 'none'

    def generate_system_prompt(self, task_type: str, language: str) -> str:
        """生成系统提示词"""
        base_prompts = {
            'implement': f"你是一个专业的{language}软件开发工程师，擅长编写高质量、可维护的代码。请生成符合最佳实践的{language}代码。",
            'review': f"你是一个资深的{language}代码审查专家，专注于代码质量、性能优化和安全性。请对提供的{language}代码进行全面审查。",
            'explain': f"你是一个{language}技术专家，擅长用清晰易懂的语言解释复杂代码的功能和设计思路。请深入分析{language}代码的实现细节。"
        }

        return base_prompts.get(task_type, base_prompts['implement'])

    def format_query(self, user_input: str) -> Dict[str, Any]:
        """格式化查询参数"""
        context = self.extract_code_context(user_input)

        return {
            'question': user_input,
            'models': ['qwen3-coder:30b'],
            'system_prompt': self.generate_system_prompt(context['task_type'], context['language'])
        }

# 使用示例
if __name__ == "__main__":
    helper = CodeHelper()

    # 测试任务检测
    test_inputs = [
        "实现一个Python函数来排序数组",
        "检视这段JavaScript代码的性能",
        "解释这个React组件的工作原理"
    ]

    for input_text in test_inputs:
        context = helper.extract_code_context(input_text)
        formatted = helper.format_query(input_text)

        print(f"输入: {input_text}")
        print(f"检测到的任务类型: {context['task_type']}")
        print(f"编程语言: {context['language']}")
        print(f"系统提示: {formatted['system_prompt']}")
        print("-" * 50)