#!/usr/bin/env python3
"""
Godot 2D游戏测试用例生成器
用于根据模块信息自动生成标准化的测试用例
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

class TestCaseGenerator:
    def __init__(self):
        self.test_cases = []
        self.test_id_counter = 1
        
    def generate_test_case(self, module: str, function: str, 
                          test_steps: List[str], expected_result: str,
                          priority: str = "中", test_type: str = "功能") -> Dict:
        """生成单个测试用例"""
        test_case = {
            "用例ID": f"TC_{self.test_id_counter:03d}",
            "模块": module,
            "功能点": function,
            "测试类型": test_type,
            "测试步骤": "\n".join([f"{i+1}. {step}" for i, step in enumerate(test_steps)]),
            "预期结果": expected_result,
            "优先级": priority,
            "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_id_counter += 1
        return test_case
    
    def generate_module_test_cases(self, module_name: str, module_functions: List[Dict]) -> List[Dict]:
        """为指定模块生成测试用例"""
        module_cases = []
        
        for func in module_functions:
            # 正常流程测试
            normal_case = self.generate_test_case(
                module=module_name,
                function=func["name"],
                test_steps=func["normal_steps"],
                expected_result=func["expected_normal"],
                priority="高",
                test_type="功能"
            )
            module_cases.append(normal_case)
            
            # 异常流程测试（如果有）
            if "error_steps" in func:
                error_case = self.generate_test_case(
                    module=module_name,
                    function=f"{func['name']}_异常",
                    test_steps=func["error_steps"],
                    expected_result=func["expected_error"],
                    priority="中",
                    test_type="异常"
                )
                module_cases.append(error_case)
            
            # 边界条件测试（如果有）
            if "boundary_steps" in func:
                boundary_case = self.generate_test_case(
                    module=module_name,
                    function=f"{func['name']}_边界",
                    test_steps=func["boundary_steps"],
                    expected_result=func["expected_boundary"],
                    priority="中",
                    test_type="边界"
                )
                module_cases.append(boundary_case)
        
        return module_cases
    
    def export_to_markdown(self, output_file: str) -> None:
        """导出测试用例到Markdown文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 自动生成的测试用例\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 按模块分组
            modules = {}
            for case in self.test_cases:
                module = case["模块"]
                if module not in modules:
                    modules[module] = []
                modules[module].append(case)
            
            # 生成每个模块的测试用例表格
            for module, cases in modules.items():
                f.write(f"## {module}模块测试用例\n\n")
                f.write("| 用例ID | 功能点 | 测试类型 | 优先级 | 测试步骤 | 预期结果 |\n")
                f.write("|--------|--------|----------|--------|----------|----------|\n")
                
                for case in cases:
                    f.write(f"| {case['用例ID']} | {case['功能点']} | {case['测试类型']} | "
                           f"{case['优先级']} | {case['测试步骤']} | {case['预期结果']} |\n")
                
                f.write("\n")
    
    def load_module_config(self, config_file: str) -> Dict:
        """从配置文件加载模块信息"""
        if not os.path.exists(config_file):
            return {}
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_from_config(self, config_file: str, output_file: str) -> None:
        """根据配置文件生成测试用例"""
        config = self.load_module_config(config_file)
        
        if not config:
            print(f"无法加载配置文件: {config_file}")
            return
        
        self.test_cases = []
        self.test_id_counter = 1
        
        for module_name, module_data in config.items():
            if "functions" in module_data:
                module_cases = self.generate_module_test_cases(
                    module_name, module_data["functions"]
                )
                self.test_cases.extend(module_cases)
        
        self.export_to_markdown(output_file)
        print(f"已生成 {len(self.test_cases)} 个测试用例到: {output_file}")

def main():
    """示例用法"""
    generator = TestCaseGenerator()
    
    # 示例配置
    example_config = {
        "玩家控制": {
            "functions": [
                {
                    "name": "移动控制",
                    "normal_steps": [
                        "玩家按下右箭头键",
                        "观察玩家精灵位置变化",
                        "验证移动方向正确"
                    ],
                    "expected_normal": "玩家向右移动，动画播放正常",
                    "error_steps": [
                        "玩家按下无效键",
                        "观察玩家位置是否变化"
                    ],
                    "expected_error": "玩家保持原地不动，无错误提示"
                },
                {
                    "name": "跳跃控制", 
                    "normal_steps": [
                        "玩家按下空格键",
                        "观察跳跃动画触发",
                        "验证重力效果"
                    ],
                    "expected_normal": "玩家执行跳跃动作，受重力影响落下"
                }
            ]
        },
        "碰撞检测": {
            "functions": [
                {
                    "name": "敌人碰撞",
                    "normal_steps": [
                        "玩家接触敌人",
                        "观察碰撞效果触发"
                    ],
                    "expected_normal": "玩家受到伤害，生命值减少"
                }
            ]
        }
    }
    
    # 保存示例配置
    with open("example_config.json", "w", encoding="utf-8") as f:
        json.dump(example_config, f, ensure_ascii=False, indent=2)
    
    # 生成测试用例
    generator.generate_from_config("example_config.json", "generated_test_cases.md")

if __name__ == "__main__":
    main()