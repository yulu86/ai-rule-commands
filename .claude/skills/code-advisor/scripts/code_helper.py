#!/usr/bin/env python3
"""
代码助手脚本 - 辅助multi-model-advisor查询的预处理和后处理
支持智能检测Godot项目并提供针对性的代码建议
"""

import re
import json
import os
from typing import Dict, List, Any

class CodeHelper:
    """代码助手工具类 - 支持通用项目和Godot项目的智能检测"""

    def __init__(self):
        self.task_patterns = {
            'implement': r'实现|编写|输出|生成',
            'review': r'检视|审查|检查|审核',
            'explain': r'解释|说明|分析|讲解'
        }
        self.godot_patterns = {
            'project_file': r'project\.godot',
            'gdscript': r'\.gd$',
            'scene': r'\.tscn$',
            'resource': r'\.tres$'
        }

    def detect_task_type(self, user_input: str) -> str:
        """检测任务类型"""
        for task_type, pattern in self.task_patterns.items():
            if re.search(pattern, user_input):
                return task_type
        return 'implement'  # 默认为实现任务

    def extract_code_context(self, user_input: str) -> Dict[str, Any]:
        """提取代码上下文信息"""
        project_type = self._detect_project_type()
        
        context = {
            'language': self._detect_language(user_input, project_type),
            'framework': self._detect_framework(user_input, project_type),
            'task_type': self.detect_task_type(user_input),
            'project_type': project_type,
            'requirements': user_input
        }
        return context

    def _detect_project_type(self) -> str:
        """智能检测项目类型"""
        current_dir = os.getcwd()
        
        # 检查是否存在project.godot文件（最可靠的Godot项目标识）
        if os.path.exists(os.path.join(current_dir, 'project.godot')):
            return 'godot'
            
        # 只检查当前目录（不递归）中的Godot相关文件，避免误检
        try:
            files_in_current_dir = os.listdir(current_dir)
            for file in files_in_current_dir:
                if any(re.search(pattern, file) for pattern in [
                    self.godot_patterns['gdscript'],
                    self.godot_patterns['scene'], 
                    self.godot_patterns['resource']
                ]):
                    return 'godot'
        except (OSError, PermissionError):
            pass
        
        return 'general'
    
    def _detect_language(self, text: str, project_type: str = 'general') -> str:
        """检测编程语言"""
        # 如果是Godot项目，优先检测GDScript
        if project_type == 'godot':
            if re.search(r'\bgdscript|gd\b', text, re.IGNORECASE):
                return 'gdscript'
            return 'gdscript'  # Godot项目默认为GDScript
        
        # 通用语言检测
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

    def _detect_framework(self, text: str, project_type: str = 'general') -> str:
        """检测框架"""
        # 如果是Godot项目，检测Godot相关概念
        if project_type == 'godot':
            godot_features = {
                'godot-4.5': r'\bgodot.*4\.5|godot.*45\b',
                'gdscript': r'\bgdscript|gd\b',
                'scene-tree': r'\bscene.*tree|场景树\b',
                'signals': r'\bsignal|信号\b',
                'nodes': r'\bnode|节点\b',
                'resources': r'\bresource|资源\b'
            }
            
            for feature, pattern in godot_features.items():
                if re.search(pattern, text, re.IGNORECASE):
                    return feature
            return 'godot'
        
        # 通用框架检测
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

    def generate_system_prompt(self, task_type: str, language: str, project_type: str = 'general') -> str:
        """生成系统提示词 - 根据项目类型和任务类型动态调整"""
        if project_type == 'godot':
            # Godot项目专用提示词
            godot_prompts = {
                'implement': "你是一位专业的 Godot 4.5+ 游戏开发工程师，精通 GDScript、场景系统、信号机制和资源管理。请生成符合 Godot 最佳实践的代码，充分利用 Godot 4.5+ 的新特性如 GPU 粒子系统、改进的物理引擎、增强的导入系统等。注意性能优化和内存管理。",
                'review': "你是一位资深的 Godot 游戏开发专家，擅长 Godot 4.5+ 架构设计、性能优化和最佳实践。请从游戏开发角度审查代码，关注场景结构、信号连接、资源加载、性能优化、内存管理和 Godot 特定的问题。",
                'explain': "你是一位 Godot 技术专家，精通 Godot 4.5+ 的各个系统。请详细解释代码在 Godot 引擎中的工作原理，包括场景树、信号系统、资源生命周期、渲染管线等相关概念。"
            }
            return godot_prompts.get(task_type, godot_prompts['implement'])
        
        # 通用项目提示词
        language_names = {
            'python': 'Python',
            'javascript': 'JavaScript',
            'java': 'Java',
            'c++': 'C++',
            'c#': 'C#',
            'go': 'Go',
            'rust': 'Rust',
            'typescript': 'TypeScript'
        }
        
        lang_name = language_names.get(language, language)
        
        base_prompts = {
            'implement': f"你是一个专业的{lang_name}软件开发工程师，擅长编写高质量、可维护的代码。请生成符合最佳实践的{lang_name}代码。",
            'review': f"你是一个资深的{lang_name}代码审查专家，专注于代码质量、性能优化和安全性。请对提供的{lang_name}代码进行全面审查。",
            'explain': f"你是一个{lang_name}技术专家，擅长用清晰易懂的语言解释复杂代码的功能和设计思路。请深入分析{lang_name}代码的实现细节。"
        }

        return base_prompts.get(task_type, base_prompts['implement'])

    def format_query(self, user_input: str) -> Dict[str, Any]:
        """格式化查询参数"""
        context = self.extract_code_context(user_input)

        return {
            'question': user_input,
            'models': ['qwen3-coder:30b'],
            'system_prompt': self.generate_system_prompt(
                context['task_type'], 
                context['language'], 
                context['project_type']
            ),
            'project_type': context['project_type'],
            'detected_language': context['language'],
            'framework': context['framework']
        }
    
    def get_godot_tools_suggestions(self, user_input: str) -> List[str]:
        """根据用户输入提供Godot MCP工具使用建议"""
        if self._detect_project_type() != 'godot':
            return []
        
        suggestions = []
        input_lower = user_input.lower()
        
        if any(keyword in input_lower for keyword in ['创建', '新建', 'scene', '场景']):
            suggestions.append('mcp__godot__create_scene - 创建新场景文件')
        
        if any(keyword in input_lower for keyword in ['节点', 'node', '添加']):
            suggestions.append('mcp__godot__add_node - 向场景添加节点')
            
        if any(keyword in input_lower for keyword in ['精灵', 'sprite', '图片', '纹理']):
            suggestions.append('mcp__godot__load_sprite - 加载精灵资源')
            
        if any(keyword in input_lower for keyword in ['项目信息', 'project', '版本']):
            suggestions.extend([
                'mcp__godot__get_project_info - 获取项目元数据',
                'mcp__godot__get_godot_version - 获取Godot版本'
            ])
        
        if any(keyword in input_lower for keyword in ['运行', '测试', 'play']):
            suggestions.extend([
                'mcp__godot__run_project - 运行Godot项目',
                'mcp__godot__get_debug_output - 获取调试输出'
            ])
        
        return suggestions

# 使用示例
if __name__ == "__main__":
    helper = CodeHelper()

    # 测试任务检测（包括Godot项目检测）
    test_inputs = [
        "实现一个Python函数来排序数组",
        "检视这段JavaScript代码的性能", 
        "解释这个React组件的工作原理",
        "创建一个玩家控制器脚本，支持8方向移动",
        "审查这个敌人AI的性能问题",
        "实现一个Godot 4.5的粒子系统效果"
    ]

    for input_text in test_inputs:
        context = helper.extract_code_context(input_text)
        formatted = helper.format_query(input_text)
        
        print(f"输入: {input_text}")
        print(f"检测到的任务类型: {context['task_type']}")
        print(f"项目类型: {context['project_type']}")
        print(f"编程语言: {context['language']}")
        print(f"框架/特性: {context['framework']}")
        print(f"系统提示: {formatted['system_prompt'][:100]}...")
        
        # 如果检测到Godot项目，显示工具建议
        if context['project_type'] == 'godot':
            tools_suggestions = helper.get_godot_tools_suggestions(input_text)
            if tools_suggestions:
                print(f"建议使用的Godot工具: {', '.join(tools_suggestions)}")
        
        print("-" * 50)