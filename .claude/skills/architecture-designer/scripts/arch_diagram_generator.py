#!/usr/bin/env python3
"""
架构图生成器
用于根据配置自动生成Mermaid架构图
"""

import json
import yaml
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class DiagramType(Enum):
    SYSTEM_ARCH = "system_architecture"
    DEPLOYMENT = "deployment"
    DATA_FLOW = "data_flow"
    SEQUENCE = "sequence"

@dataclass
class Component:
    name: str
    type: str
    layer: str
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class Layer:
    name: str
    components: List[Component]
    
    def __post_init__(self):
        if self.components is None:
            self.components = []

@dataclass
class SystemArchitecture:
    name: str
    description: str
    layers: List[Layer]
    external_services: List[Component] = None
    
    def __post_init__(self):
        if self.external_services is None:
            self.external_services = []

class ArchitectureDiagramGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.architecture = self._parse_config(config)
    
    def _parse_config(self, config: Dict[str, Any]) -> SystemArchitecture:
        """解析配置文件"""
        name = config.get('name', 'System Architecture')
        description = config.get('description', '')
        
        layers = []
        for layer_config in config.get('layers', []):
            components = []
            for comp_config in layer_config.get('components', []):
                component = Component(
                    name=comp_config['name'],
                    type=comp_config.get('type', 'service'),
                    layer=layer_config['name'],
                    dependencies=comp_config.get('dependencies', [])
                )
                components.append(component)
            
            layer = Layer(
                name=layer_config['name'],
                components=components
            )
            layers.append(layer)
        
        external_services = []
        for ext_config in config.get('external_services', []):
            service = Component(
                name=ext_config['name'],
                type=ext_config.get('type', 'external'),
                layer='external',
                dependencies=ext_config.get('dependencies', [])
            )
            external_services.append(service)
        
        return SystemArchitecture(
            name=name,
            description=description,
            layers=layers,
            external_services=external_services
        )
    
    def generate_system_architecture_diagram(self) -> str:
        """生成系统架构图"""
        diagram = ["graph TB"]
        
        # 添加样式定义
        diagram.extend([
            "classDef service fill:#e1f5fe,stroke:#01579b,stroke-width:2px",
            "classDef database fill:#f3e5f5,stroke:#4a148c,stroke-width:2px",
            "classDef external fill:#fff3e0,stroke:#e65100,stroke-width:2px",
            "classDef cache fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px"
        ])
        
        # 生成层级结构
        layer_components = {}
        for layer in self.architecture.layers:
            layer_name = layer.name.replace(" ", "_")
            diagram.append(f"    subgraph \"{layer.name}\"")
            
            for component in layer.components:
                node_id = self._get_node_id(component)
                diagram.append(f"        {node_id}[{component.name}]")
                layer_components[component.name] = node_id
                # 添加CSS类
                if component.type == 'database':
                    diagram.append(f"        class {node_id} database")
                elif component.type == 'cache':
                    diagram.append(f"        class {node_id} cache")
                else:
                    diagram.append(f"        class {node_id} service")
            
            diagram.append("    end")
        
        # 添加外部服务
        if self.architecture.external_services:
            diagram.append("    subgraph \"外部服务\"")
            for service in self.architecture.external_services:
                node_id = self._get_node_id(service)
                diagram.append(f"        {node_id}[{service.name}]")
                diagram.append(f"        class {node_id} external")
            diagram.append("    end")
        
        # 添加依赖关系
        diagram.append("")
        for layer in self.architecture.layers:
            for component in layer.components:
                if component.dependencies:
                    from_id = self._get_node_id(component)
                    for dep in component.dependencies:
                        if dep in layer_components:
                            to_id = layer_components[dep]
                            diagram.append(f"    {from_id} --> {to_id}")
        
        # 添加标题
        title = f"# {self.architecture.name}\n"
        if self.architecture.description:
            title += f"## {self.architecture.description}\n"
        
        return title + "\n```mermaid\n" + "\n".join(diagram) + "\n```\n"
    
    def generate_deployment_diagram(self) -> str:
        """生成部署架构图"""
        diagram = ["graph TB"]
        
        # 添加环境层级
        environments = self.config.get('environments', {})
        for env_name, env_config in environments.items():
            diagram.append(f"    subgraph \"{env_name.upper()}环境\"")
            
            # 添加负载均衡器
            if env_config.get('load_balancer'):
                lb_id = f"lb_{env_name}"
                diagram.append(f"        {lb_id}[负载均衡器]")
            
            # 添加服务实例
            for service in env_config.get('services', []):
                service_name = service['name']
                replicas = service.get('replicas', 1)
                
                for i in range(replicas):
                    service_id = f"{service_name}_{env_name}_{i}"
                    diagram.append(f"        {service_id}[{service_name}]")
                    
                    # 连接负载均衡器
                    if env_config.get('load_balancer'):
                        diagram.append(f"        {lb_id} --> {service_id}")
            
            # 添加数据库
            for db in env_config.get('databases', []):
                db_id = f"{db['name']}_{env_name}"
                db_type = db.get('type', 'database')
                diagram.append(f"        {db_id}[({db['name']})]")
                diagram.append(f"        class {db_id} database")
            
            diagram.append("    end")
        
        title = f"# {self.architecture.name} - 部署架构\n"
        return title + "\n```mermaid\n" + "\n".join(diagram) + "\n```\n"
    
    def generate_data_flow_diagram(self) -> str:
        """生成数据流图"""
        diagram = ["flowchart LR"]
        
        # 添加数据源
        data_sources = self.config.get('data_flow', {}).get('sources', [])
        for source in data_sources:
            source_id = f"source_{source['name'].replace(' ', '_')}"
            diagram.append(f"    {source_id}[{source['name']}]")
        
        # 添加处理步骤
        processing_steps = self.config.get('data_flow', {}).get('steps', [])
        for step in processing_steps:
            step_id = f"step_{step['name'].replace(' ', '_')}"
            diagram.append(f"    {step_id}[{step['name']}]")
        
        # 添加数据存储
        data_stores = self.config.get('data_flow', {}).get('stores', [])
        for store in data_stores:
            store_id = f"store_{store['name'].replace(' ', '_')}"
            diagram.append(f"    {store_id}[({store['name']})]")
            diagram.append(f"        class {store_id} database")
        
        # 添加数据流向
        flows = self.config.get('data_flow', {}).get('flows', [])
        for flow in flows:
            from_node = f"source_{flow['from'].replace(' ', '_')}"
            to_node = f"step_{flow['to'].replace(' ', '_')}" if flow['to'] in [s['name'] for s in processing_steps] else f"store_{flow['to'].replace(' ', '_')}"
            diagram.append(f"    {from_node} --> {to_node}")
        
        title = f"# {self.architecture.name} - 数据流架构\n"
        return title + "\n```mermaid\n" + "\n".join(diagram) + "\n```\n"
    
    def generate_sequence_diagram(self) -> str:
        """生成时序图"""
        diagram = ["sequenceDiagram"]
        
        # 添加参与者
        participants = self.config.get('sequence', {}).get('participants', [])
        for participant in participants:
            participant_id = participant['name'].replace(' ', '_')
            diagram.append(f"    participant {participant_id} as {participant['name']}")
        
        # 添加交互步骤
        steps = self.config.get('sequence', {}).get('steps', [])
        for step in steps:
            if step['type'] == 'request':
                from_part = step['from'].replace(' ', '_')
                to_part = step['to'].replace(' ', '_')
                message = step.get('message', '')
                diagram.append(f"    {from_part}->>{to_part}: {message}")
            elif step['type'] == 'response':
                from_part = step['from'].replace(' ', '_')
                to_part = step['to'].replace(' ', '_')
                message = step.get('message', '')
                diagram.append(f"    {from_part}-->>{to_part}: {message}")
            elif step['type'] == 'note':
                participant = step['participant'].replace(' ', '_')
                note = step.get('note', '')
                diagram.append(f"    Note over {participant}: {note}")
        
        title = f"# {self.architecture.name} - 交互时序图\n"
        return title + "\n```mermaid\n" + "\n".join(diagram) + "\n```\n"
    
    def _get_node_id(self, component: Component) -> str:
        """生成组件节点ID"""
        return component.name.replace(' ', '_').replace('-', '_').lower()
    
    def generate_all_diagrams(self) -> str:
        """生成所有架构图"""
        diagrams = []
        
        # 系统架构图
        if any(layer.components for layer in self.architecture.layers):
            diagrams.append(self.generate_system_architecture_diagram())
        
        # 部署架构图
        if self.config.get('environments'):
            diagrams.append(self.generate_deployment_diagram())
        
        # 数据流图
        if self.config.get('data_flow'):
            diagrams.append(self.generate_data_flow_diagram())
        
        # 时序图
        if self.config.get('sequence'):
            diagrams.append(self.generate_sequence_diagram())
        
        return "\n".join(diagrams)

def load_config(config_file: str) -> Dict[str, Any]:
    """加载配置文件"""
    if config_file.endswith('.json'):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif config_file.endswith(('.yml', '.yaml')):
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Unsupported config file format. Use .json, .yml, or .yaml")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='生成架构图')
    parser.add_argument('config_file', help='配置文件路径')
    parser.add_argument('-o', '--output', default='architecture_diagrams.md', help='输出文件路径')
    parser.add_argument('-t', '--type', choices=['system', 'deployment', 'dataflow', 'sequence', 'all'], 
                       default='all', help='生成的图表类型')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config_file)
    
    # 生成图表
    generator = ArchitectureDiagramGenerator(config)
    
    if args.type == 'system':
        output = generator.generate_system_architecture_diagram()
    elif args.type == 'deployment':
        output = generator.generate_deployment_diagram()
    elif args.type == 'dataflow':
        output = generator.generate_data_flow_diagram()
    elif args.type == 'sequence':
        output = generator.generate_sequence_diagram()
    else:  # all
        output = generator.generate_all_diagrams()
    
    # 写入文件
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"架构图已生成: {args.output}")

if __name__ == '__main__':
    main()