#!/usr/bin/env python3
"""
Godot架构Mermaid图表生成工具
用于自动生成各种类型的架构图表
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class DiagramType(Enum):
    SYSTEM_ARCHITECTURE = "system_architecture"
    COMPONENT_ENTITY = "component_entity"
    STATE_MACHINE = "state_machine"
    DATA_FLOW = "data_flow"
    SEQUENCE = "sequence"
    CLASS = "class"
    DEPLOYMENT = "deployment"

@dataclass
class Component:
    """组件定义"""
    name: str
    type: str
    responsibility: str
    dependencies: List[str] = None
    interfaces: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.interfaces is None:
            self.interfaces = []

@dataclass
class State:
    """状态定义"""
    name: str
    description: str
    entry_actions: List[str] = None
    exit_actions: List[str] = None
    transitions: Dict[str, str] = None  # {event: target_state}
    
    def __post_init__(self):
        if self.entry_actions is None:
            self.entry_actions = []
        if self.exit_actions is None:
            self.exit_actions = []
        if self.transitions is None:
            self.transitions = {}

@dataclass
class SystemLayer:
    """系统层定义"""
    name: str
    components: List[str]
    description: str = ""

class GodotMermaidGenerator:
    """Godot架构Mermaid图表生成器"""
    
    def __init__(self):
        self.components: Dict[str, Component] = {}
        self.states: Dict[str, State] = {}
        self.layers: List[SystemLayer] = []
    
    def add_component(self, component: Component):
        """添加组件"""
        self.components[component.name] = component
    
    def add_state(self, state: State):
        """添加状态"""
        self.states[state.name] = state
    
    def add_layer(self, layer: SystemLayer):
        """添加系统层"""
        self.layers.append(layer)
    
    def generate_system_architecture(self, title: str = "系统架构图") -> str:
        """生成系统架构图"""
        lines = [
            "```mermaid",
            f"graph TB",
            f'    title {title}',
            ""
        ]
        
        # 添加系统层
        layer_id = 0
        component_ids = {}
        
        for layer in self.layers:
            layer_name = f"L{layer_id}_{layer.name.replace(' ', '_')}"
            lines.append(f"    subgraph \"{layer.name}\"")
            
            for comp_name in layer.components:
                if comp_name in self.components:
                    comp_id = f"C{comp_name.replace(' ', '_')}"
                    component_ids[comp_name] = comp_id
                    component = self.components[comp_name]
                    
                    # 添加组件节点
                    lines.append(f"        {comp_id}[{component.name}]")
            
            lines.append("    end")
            layer_id += 1
        
        lines.append("")
        
        # 添加组件间依赖关系
        for comp_name, component in self.components.items():
            if comp_name in component_ids:
                comp_id = component_ids[comp_name]
                
                for dep in component.dependencies:
                    if dep in component_ids:
                        dep_id = component_ids[dep]
                        lines.append(f"    {comp_id} --> {dep_id}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_component_entity_diagram(self, entity_name: str, components: List[str]) -> str:
        """生成组件实体图"""
        lines = [
            "```mermaid",
            "graph TD",
            f'    title {entity_name} 组件架构',
            ""
        ]
        
        # 主实体节点
        entity_id = entity_name.replace(" ", "_")
        lines.append(f"    subgraph \"{entity_name}\"")
        
        # 添加组件
        comp_ids = {}
        for comp_name in components:
            if comp_name in self.components:
                comp = self.components[comp_name]
                comp_id = f"{entity_id}_{comp_name.replace(' ', '_')}"
                comp_ids[comp_name] = comp_id
                lines.append(f"        {comp_id}[{comp_name}]")
        
        lines.append("    end")
        lines.append("")
        
        # 添加组件间关系
        for comp_name in components:
            if comp_name in self.components and comp_name in comp_ids:
                comp = self.components[comp_name]
                comp_id = comp_ids[comp_name]
                
                for dep in comp.dependencies:
                    if dep in comp_ids:
                        dep_id = comp_ids[dep]
                        lines.append(f"    {comp_id} --> {dep_id}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_state_machine_diagram(self, machine_name: str = "游戏状态机") -> str:
        """生成状态机图"""
        lines = [
            "```mermaid",
            "stateDiagram-v2",
            f'    title {machine_name}',
            ""
        ]
        
        # 添加状态和转换
        for state_name, state in self.states.items():
            safe_name = state_name.replace(" ", "_").replace("-", "_")
            
            # 添加状态
            lines.append(f"    [*] --> {safe_name}" if state_name == list(self.states.keys())[0] else f"    state {safe_name}")
            
            # 添加转换
            for event, target_state in state.transitions.items():
                target_safe = target_state.replace(" ", "_").replace("-", "_")
                lines.append(f"    {safe_name} --> {target_safe}: {event}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_sequence_diagram(self, title: str, actors: List[str], interactions: List[Tuple[str, str, str]]) -> str:
        """生成序列图"""
        lines = [
            "```mermaid",
            "sequenceDiagram",
            f'    title {title}',
            ""
        ]
        
        # 添加参与者
        for actor in actors:
            lines.append(f"    participant {actor}")
        
        lines.append("")
        
        # 添加交互
        for sender, receiver, message in interactions:
            lines.append(f"    {sender}->> {receiver}: {message}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_class_diagram(self, title: str = "类图") -> str:
        """生成类图"""
        lines = [
            "```mermaid",
            "classDiagram",
            f'    title {title}',
            ""
        ]
        
        # 添加类
        for comp_name, component in self.components.items():
            class_name = comp_name.replace(" ", "_")
            lines.append(f"    class {class_name} {{")
            lines.append(f"        +{class_name}()")
            
            # 添加方法
            for interface in component.interfaces:
                lines.append(f"        +{interface}()")
            
            lines.append(f"        - responsibility: {component.responsibility}")
            lines.append("    }")
            lines.append("")
        
        # 添加继承关系（这里简化处理，基于组件类型）
        for comp_name, component in self.components.items():
            class_name = comp_name.replace(" ", "_")
            
            # 如果是Manager类型，可能继承自Node
            if "Manager" in class_name:
                lines.append(f"    Node <|-- {class_name}")
            # 如果是Component类型
            elif "Component" in class_name:
                lines.append(f"    Component <|-- {class_name}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_data_flow_diagram(self, title: str = "数据流图", processes: List[Dict], data_stores: List[Dict], flows: List[Tuple]) -> str:
        """生成数据流图"""
        lines = [
            "```mermaid",
            "graph LR",
            f'    title {title}',
            ""
        ]
        
        # 添加处理过程
        for process in processes:
            proc_id = process.get('id', process['name'].replace(' ', '_'))
            lines.append(f"    {proc_id}[{process['name']}]")
        
        # 添加数据存储
        for store in data_stores:
            store_id = store.get('id', store['name'].replace(' ', '_'))
            lines.append(f"    {store_id}[({store['name']})]")
        
        lines.append("")
        
        # 添加数据流
        for flow in flows:
            source, target, data = flow
            source_id = source.replace(' ', '_')
            target_id = target.replace(' ', '_')
            lines.append(f"    {source_id} --> {target_id}: {data}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_gantt_chart(self, title: str, tasks: List[Dict], milestones: List[Dict] = None) -> str:
        """生成甘特图"""
        lines = [
            "```mermaid",
            "gantt",
            f'    title {title}',
            "    dateFormat  YYYY-MM-DD",
            ""
        ]
        
        # 添加任务
        current_section = None
        for task in tasks:
            section = task.get('section', '')
            if section != current_section:
                current_section = section
                lines.append(f"    section {section}")
            
            task_name = task['name']
            start_date = task['start']
            end_date = task['end']
            
            if 'dependencies' in task:
                deps = ", ".join(task['dependencies'])
                lines.append(f"    {task_name} :active, {deps}, {start_date}, {end_date}")
            else:
                lines.append(f"    {task_name} :active, {start_date}, {end_date}")
        
        # 添加里程碑
        if milestones:
            lines.append("")
            lines.append("    section 里程碑")
            for milestone in milestones:
                lines.append(f"    {milestone['name']} :milestone, {milestone['date']}, 0d")
        
        lines.append("```")
        return "\n".join(lines)

def create_sample_godot_architecture():
    """创建示例Godot架构"""
    generator = GodotMermaidGenerator()
    
    # 添加系统层
    generator.add_layer(SystemLayer("表现层", ["UI系统", "音频系统", "特效系统"]))
    generator.add_layer(SystemLayer("应用层", ["游戏管理器", "场景管理器", "事件管理器"]))
    generator.add_layer(SystemLayer("领域层", ["玩家系统", "敌人系统", "道具系统"]))
    generator.add_layer(SystemLayer("基础设施层", ["输入系统", "物理系统", "存档系统"]))
    
    # 添加组件
    generator.add_component(Component("UI系统", "Manager", "管理所有UI界面和交互", ["游戏管理器"], ["show_ui", "hide_ui", "update_ui"]))
    generator.add_component(Component("游戏管理器", "Manager", "控制游戏主循环和状态", ["场景管理器", "输入系统"], ["start_game", "pause_game", "game_over"]))
    generator.add_component(Component("玩家系统", "Entity", "管理玩家状态和行为", ["游戏管理器", "输入系统"], ["move", "attack", "take_damage"]))
    generator.add_component(Component("输入系统", "Manager", "处理用户输入", [], ["get_input", "bind_action", "process_input"]))
    
    # 添加状态
    generator.add_state(State("主菜单", "游戏启动时的主界面", ["加载资源", "显示菜单"], ["清理资源"], {"开始游戏": "游戏中"}))
    generator.add_state(State("游戏中", "主要游戏状态", ["开始计时", "启用控制"], ["暂停计时", "禁用控制"], {"暂停": "暂停菜单", "游戏结束": "结束画面"}))
    generator.add_state(State("暂停菜单", "游戏暂停状态", ["显示暂停界面"], ["隐藏暂停界面"], {"继续": "游戏中", "返回主菜单": "主菜单"}))
    
    return generator

def generate_complete_architecture_docs():
    """生成完整的架构文档"""
    generator = create_sample_godot_architecture()
    
    docs = [
        "# Godot 2D游戏架构设计",
        "",
        "## 1. 系统架构总览",
        "",
        generator.generate_system_architecture(),
        "",
        "## 2. 玩家实体组件架构",
        "",
        generator.generate_component_entity_diagram("玩家实体", ["玩家系统"]),
        "",
        "## 3. 游戏状态机",
        "",
        generator.generate_state_machine_diagram(),
        "",
        "## 4. 组件交互序列图",
        ""
    ]
    
    # 添加序列图
    sequence_actors = ["玩家", "输入系统", "游戏管理器", "UI系统"]
    sequence_interactions = [
        ("玩家", "输入系统", "按下移动键"),
        ("输入系统", "游戏管理器", "发送移动事件"),
        ("游戏管理器", "玩家系统", "更新玩家位置"),
        ("玩家系统", "游戏管理器", "位置改变通知"),
        ("游戏管理器", "UI系统", "更新UI显示")
    ]
    
    docs.append(generator.generate_sequence_diagram("玩家移动交互流程", sequence_actors, sequence_interactions))
    
    # 添加类图
    docs.extend([
        "",
        "## 5. 系统类图",
        "",
        generator.generate_class_diagram("核心系统类图"),
        "",
        "## 6. 开发时间线",
        ""
    ])
    
    # 添加甘特图
    tasks = [
        {"name": "需求分析", "start": "2024-01-01", "end": "2024-01-07", "section": "设计阶段"},
        {"name": "架构设计", "start": "2024-01-08", "end": "2024-01-21", "section": "设计阶段"},
        {"name": "原型开发", "start": "2024-01-22", "end": "2024-02-04", "section": "开发阶段"},
        {"name": "核心功能", "start": "2024-02-05", "end": "2024-02-25", "section": "开发阶段", "dependencies": ["原型开发"]},
        {"name": "性能优化", "start": "2024-03-01", "end": "2024-03-15", "section": "优化阶段"},
        {"name": "测试验证", "start": "2024-03-16", "end": "2024-03-30", "section": "优化阶段"}
    ]
    
    milestones = [
        {"name": "Alpha版本", "date": "2024-02-25"},
        {"name": "Beta版本", "date": "2024-03-30"},
        {"name": "正式发布", "date": "2024-04-15"}
    ]
    
    docs.append(generator.generate_gantt_chart("项目开发时间线", tasks, milestones))
    
    return "\n".join(docs)

def save_diagram_to_file(diagram_content: str, filename: str):
    """保存图表到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(diagram_content)
    print(f"图表已保存到: {filename}")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python mermaid_generator.py generate_sample [输出文件]")
        print("  python mermaid_generator.py interactive  # 交互式生成")
        return
    
    command = sys.argv[1]
    
    if command == "generate_sample":
        output_file = sys.argv[2] if len(sys.argv) > 2 else "godot_architecture.md"
        docs = generate_complete_architecture_docs()
        save_diagram_to_file(docs, output_file)
    
    elif command == "interactive":
        print("🚀 Godot架构图表生成器 - 交互模式")
        print("请按照提示输入信息来生成图表")
        
        # 这里可以添加交互式界面
        print("交互模式开发中...")

if __name__ == "__main__":
    main()