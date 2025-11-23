#!/usr/bin/env python3
"""
Godot API查询脚本
用于快速查找Godot API文档和使用示例
"""

import sys
import json
import subprocess
from typing import Optional, Dict, List

class GodotAPIQuery:
    def __init__(self):
        self.context_cache = {}
    
    def resolve_library_id(self, library_name: str) -> Optional[str]:
        """
        使用context7解析Godot库ID
        """
        try:
            # 调用context7 resolve-library-id
            result = subprocess.run([
                'claude', 'skill', 'context7'
            ], input=f'resolve-library-id "{library_name}"', 
               text=True, capture_output=True)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                # 解析输出获取库ID
                if '/' in output:
                    return output.split('\n')[-1].strip()
            return None
        except Exception as e:
            print(f"Error resolving library ID: {e}")
            return None
    
    def get_library_docs(self, library_id: str, topic: str = "") -> str:
        """
        获取Godot库文档
        """
        try:
            # 构建查询命令
            query = f'get-library-docs "{library_id}"'
            if topic:
                query += f' --topic "{topic}"'
            
            result = subprocess.run([
                'claude', 'skill', 'context7'
            ], input=query, text=True, capture_output=True)
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"Error getting library docs: {e}"
    
    def search_godot_class(self, class_name: str) -> str:
        """
        搜索Godot类文档
        """
        # 常见的Godot库ID模式
        possible_ids = [
            "/godot/godot",
            "/godotengine/godot", 
            "/godot-docs/godot"
        ]
        
        for lib_id in possible_ids:
            docs = self.get_library_docs(lib_id, class_name)
            if docs and "Error:" not in docs:
                return docs
        
        return f"No documentation found for class: {class_name}"
    
    def search_godot_method(self, class_name: str, method_name: str) -> str:
        """
        搜索特定类的方法文档
        """
        topic = f"{class_name}.{method_name}"
        return self.search_godot_class(topic)
    
    def get_usage_examples(self, class_name: str, method_name: str = "") -> str:
        """
        获取使用示例
        """
        topic = f"{class_name}"
        if method_name:
            topic += f" {method_name} examples"
        
        return self.search_godot_class(topic)
    
    def get_best_practices(self, feature: str) -> str:
        """
        获取最佳实践指导
        """
        topic = f"{feature} best practices"
        return self.search_godot_class(topic)

def main():
    """主函数 - 提供命令行接口"""
    if len(sys.argv) < 2:
        print("Usage: python query_godot_api.py <command> [args...]")
        print("Commands:")
        print("  class <class_name>           - 搜索类文档")
        print("  method <class> <method>      - 搜索方法文档")
        print("  example <class> [method]     - 获取使用示例")
        print("  practice <feature>           - 获取最佳实践")
        sys.exit(1)
    
    query = GodotAPIQuery()
    command = sys.argv[1].lower()
    
    if command == "class":
        if len(sys.argv) < 3:
            print("Usage: python query_godot_api.py class <class_name>")
            sys.exit(1)
        class_name = sys.argv[2]
        result = query.search_godot_class(class_name)
        
    elif command == "method":
        if len(sys.argv) < 4:
            print("Usage: python query_godot_api.py method <class_name> <method_name>")
            sys.exit(1)
        class_name = sys.argv[2]
        method_name = sys.argv[3]
        result = query.search_godot_method(class_name, method_name)
        
    elif command == "example":
        if len(sys.argv) < 3:
            print("Usage: python query_godot_api.py example <class_name> [method_name]")
            sys.exit(1)
        class_name = sys.argv[2]
        method_name = sys.argv[3] if len(sys.argv) > 3 else ""
        result = query.get_usage_examples(class_name, method_name)
        
    elif command == "practice":
        if len(sys.argv) < 3:
            print("Usage: python query_godot_api.py practice <feature>")
            sys.exit(1)
        feature = sys.argv[2]
        result = query.get_best_practices(feature)
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
    
    print(result)

if __name__ == "__main__":
    main()