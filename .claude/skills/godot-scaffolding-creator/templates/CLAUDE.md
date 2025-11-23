# 协同开发
- AI: 负责.gd/.gdshader开发，必须用godot MCP工具创建文件
- 用户: 负责.tscn开发
- AI指导用户处理.tscn/项目配置/.gd中节点引用
- 测试/调试: 用godot MCP工具运行项目并获取日志

# godot MCP工具
- 优先使用godot MCP工具：
launch_editor, run_project, get_debug_output, stop_project, get_godot_version, list_projects, get_project_info, create_scene, add_node, load_sprite, export_mesh_library, save_scene, get_uid, update_project_uids