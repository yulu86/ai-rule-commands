#!/usr/bin/env python3
"""
Godot开发工具脚本
集成MCP工具支持，提供项目运行、调试、场景编辑等功能
"""

import sys
import json
import subprocess
import argparse
from typing import Optional, Dict, List, Any

class GodotDevTools:
    def __init__(self):
        self.project_path = None
        self.current_scene = None
        self.debug_history = []
    
    def run_project(self, project_path: str, scene: str = None) -> bool:
        """
        运行Godot项目
        """
        try:
            cmd = ['claude', 'mcp__godot__run_project', '--projectPath', project_path]
            if scene:
                cmd.extend(['--scene', scene])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"项目运行成功: {project_path}")
                if scene:
                    print(f"场景: {scene}")
                return True
            else:
                print(f"项目运行失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"运行项目时出错: {e}")
            return False
    
    def stop_project(self) -> bool:
        """
        停止当前运行的Godot项目
        """
        try:
            result = subprocess.run(['claude', 'mcp__godot__stop_project'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("项目已停止")
                return True
            else:
                print(f"停止项目失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"停止项目时出错: {e}")
            return False
    
    def get_debug_output(self) -> str:
        """
        获取当前调试输出和错误信息
        """
        try:
            result = subprocess.run(['claude', 'mcp__godot__get_debug_output'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    self.debug_history.append(output)
                return output
            else:
                return f"获取调试输出失败: {result.stderr}"
        except Exception as e:
            return f"获取调试输出时出错: {e}"
    
    def launch_editor(self, project_path: str) -> bool:
        """
        启动Godot编辑器
        """
        try:
            result = subprocess.run(['claude', 'mcp__godot__launch_editor', 
                                  '--projectPath', project_path], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Godot编辑器已启动: {project_path}")
                return True
            else:
                print(f"启动编辑器失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"启动编辑器时出错: {e}")
            return False
    
    def get_project_info(self, project_path: str) -> Optional[Dict]:
        """
        获取Godot项目信息
        """
        try:
            result = subprocess.run(['claude', 'mcp__godot__get_project_info', 
                                  '--projectPath', project_path], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # 尝试解析JSON输出
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {"raw_output": result.stdout}
            else:
                print(f"获取项目信息失败: {result.stderr}")
                return None
        except Exception as e:
            print(f"获取项目信息时出错: {e}")
            return None
    
    def create_scene(self, project_path: str, scene_path: str, 
                    root_node_type: str = "Node2D") -> bool:
        """
        创建新的Godot场景文件
        """
        try:
            cmd = ['claude', 'mcp__godot__create_scene', 
                  '--projectPath', project_path,
                  '--scenePath', scene_path,
                  '--rootNodeType', root_node_type]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"场景创建成功: {scene_path}")
                return True
            else:
                print(f"创建场景失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"创建场景时出错: {e}")
            return False
    
    def add_node(self, project_path: str, scene_path: str, node_type: str, 
                node_name: str, parent_node_path: str = "root", 
                properties: Dict = None) -> bool:
        """
        向现有场景添加节点
        """
        try:
            cmd = ['claude', 'mcp__godot__add_node',
                  '--projectPath', project_path,
                  '--scenePath', scene_path,
                  '--nodeType', node_type,
                  '--nodeName', node_name,
                  '--parentNodePath', parent_node_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"节点添加成功: {node_name} ({node_type})")
                return True
            else:
                print(f"添加节点失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"添加节点时出错: {e}")
            return False
    
    def save_scene(self, project_path: str, scene_path: str, 
                  new_path: str = None) -> bool:
        """
        保存场景文件
        """
        try:
            cmd = ['claude', 'mcp__godot__save_scene',
                  '--projectPath', project_path,
                  '--scenePath', scene_path]
            
            if new_path:
                cmd.extend(['--newPath', new_path])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                save_path = new_path or scene_path
                print(f"场景保存成功: {save_path}")
                return True
            else:
                print(f"保存场景失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"保存场景时出错: {e}")
            return False
    
    def load_sprite(self, project_path: str, scene_path: str, 
                   node_path: str, texture_path: str) -> bool:
        """
        将精灵加载到Sprite2D节点
        """
        try:
            cmd = ['claude', 'mcp__godot__load_sprite',
                  '--projectPath', project_path,
                  '--scenePath', scene_path,
                  '--nodePath', node_path,
                  '--texturePath', texture_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"精灵加载成功: {texture_path} -> {node_path}")
                return True
            else:
                print(f"加载精灵失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"加载精灵时出错: {e}")
            return False
    
    def interactive_debug_session(self, project_path: str):
        """
        交互式调试会话
        """
        print(f"开始调试会话: {project_path}")
        print("可用命令: run, stop, output, info, quit")
        
        while True:
            try:
                cmd = input("\ndebug> ").strip().lower()
                
                if cmd == "quit" or cmd == "q":
                    break
                elif cmd == "run" or cmd == "r":
                    self.run_project(project_path)
                elif cmd == "stop" or cmd == "s":
                    self.stop_project()
                elif cmd == "output" or cmd == "o":
                    output = self.get_debug_output()
                    if output:
                        print("调试输出:")
                        print(output)
                    else:
                        print("没有调试输出")
                elif cmd == "info" or cmd == "i":
                    info = self.get_project_info(project_path)
                    if info:
                        print("项目信息:")
                        print(json.dumps(info, indent=2, ensure_ascii=False))
                elif cmd == "help" or cmd == "h":
                    print("可用命令:")
                    print("  run/r     - 运行项目")
                    print("  stop/s    - 停止项目")
                    print("  output/o  - 获取调试输出")
                    print("  info/i    - 获取项目信息")
                    print("  help/h    - 显示帮助")
                    print("  quit/q    - 退出调试会话")
                else:
                    print("未知命令，输入 'help' 查看可用命令")
                    
            except KeyboardInterrupt:
                print("\n正在退出调试会话...")
                break
            except Exception as e:
                print(f"命令执行出错: {e}")
        
        # 确保项目停止
        self.stop_project()
        print("调试会话结束")
    
    def create_debug_scene(self, project_path: str, scene_name: str = "debug_scene") -> bool:
        """
        创建调试场景
        """
        scene_path = f"{scene_name}.tscn"
        
        # 创建场景
        if not self.create_scene(project_path, scene_path, "Node2D"):
            return False
        
        # 添加调试标签
        if not self.add_node(project_path, scene_path, "Label", "DebugInfo"):
            return False
        
        # 添加调试相机
        if not self.add_node(project_path, scene_path, "Camera2D", "DebugCamera"):
            return False
        
        # 保存场景
        return self.save_scene(project_path, scene_path)

def main():
    """主函数 - 提供命令行接口"""
    parser = argparse.ArgumentParser(description="Godot开发工具集")
    parser.add_argument('command', help="执行命令")
    parser.add_argument('--project', '-p', required=True, help="Godot项目路径")
    parser.add_argument('--scene', '-s', help="场景路径")
    parser.add_argument('--name', '-n', help="节点名称")
    parser.add_argument('--type', '-t', help="节点类型")
    parser.add_argument('--parent', default="root", help="父节点路径")
    parser.add_argument('--output', '-o', help="输出文件路径")
    
    args = parser.parse_args()
    
    tools = GodotDevTools()
    
    if args.command == "run":
        success = tools.run_project(args.project, args.scene)
        sys.exit(0 if success else 1)
        
    elif args.command == "stop":
        success = tools.stop_project()
        sys.exit(0 if success else 1)
        
    elif args.command == "output":
        output = tools.get_debug_output()
        if output:
            print(output)
        sys.exit(0 if output else 1)
        
    elif args.command == "launch":
        success = tools.launch_editor(args.project)
        sys.exit(0 if success else 1)
        
    elif args.command == "info":
        info = tools.get_project_info(args.project)
        if info:
            print(json.dumps(info, indent=2, ensure_ascii=False))
        sys.exit(0 if info else 1)
        
    elif args.command == "create-scene":
        if not args.scene:
            print("错误: 创建场景需要指定 --scene 参数")
            sys.exit(1)
        node_type = args.type or "Node2D"
        success = tools.create_scene(args.project, args.scene, node_type)
        sys.exit(0 if success else 1)
        
    elif args.command == "add-node":
        if not args.scene or not args.type or not args.name:
            print("错误: 添加节点需要指定 --scene, --type, --name 参数")
            sys.exit(1)
        success = tools.add_node(args.project, args.scene, args.type, 
                                args.name, args.parent)
        sys.exit(0 if success else 1)
        
    elif args.command == "save-scene":
        if not args.scene:
            print("错误: 保存场景需要指定 --scene 参数")
            sys.exit(1)
        success = tools.save_scene(args.project, args.scene)
        sys.exit(0 if success else 1)
        
    elif args.command == "debug":
        tools.interactive_debug_session(args.project)
        sys.exit(0)
        
    elif args.command == "create-debug-scene":
        scene_name = args.scene or "debug_scene"
        success = tools.create_debug_scene(args.project, scene_name)
        sys.exit(0 if success else 1)
        
    else:
        print(f"未知命令: {args.command}")
        print("可用命令:")
        print("  run              - 运行项目")
        print("  stop             - 停止项目")
        print("  output           - 获取调试输出")
        print("  launch           - 启动编辑器")
        print("  info             - 获取项目信息")
        print("  create-scene     - 创建场景")
        print("  add-node         - 添加节点")
        print("  save-scene       - 保存场景")
        print("  debug            - 交互式调试会话")
        print("  create-debug-scene - 创建调试场景")
        sys.exit(1)

if __name__ == "__main__":
    main()