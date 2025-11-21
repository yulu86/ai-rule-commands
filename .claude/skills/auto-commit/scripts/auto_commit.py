#!/usr/bin/env python3
"""
Auto Commit Script for Claude Code Skill
快速生成git commit message并自动提交
"""

import subprocess
import sys
import os
from typing import List, Tuple
import re

class GitAutoCommit:
    def __init__(self):
        self.git_root = self._get_git_root()
    
    def _get_git_root(self) -> str:
        """获取git仓库根目录"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            raise RuntimeError("当前目录不是git仓库")
    
    def _run_git_command(self, cmd: List[str]) -> Tuple[str, str]:
        """执行git命令并返回输出"""
        try:
            result = subprocess.run(
                ['git'] + cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip(), result.stderr.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git命令执行失败: {e.stderr.strip()}")
    
    def get_git_status(self) -> dict:
        """获取git状态信息"""
        # 获取所有变更
        stdout, _ = self._run_git_command(['status', '--porcelain'])
        changes = stdout.split('\n') if stdout else []
        
        # 分类变更文件
        staged_files = []
        modified_files = []
        untracked_files = []
        
        for change in changes:
            if not change.strip():
                continue
            
            status = change[:2]
            file_path = change[3:]
            
            if status[0] in ['A', 'M', 'D', 'R', 'C']:
                staged_files.append((status[0], file_path))
            if status[1] in ['M', 'D']:
                modified_files.append((status[1], file_path))
            if status == '??':
                untracked_files.append(file_path)
        
        # 获取diff信息用于生成commit message
        diff_output = ""
        if staged_files:
            diff_stdout, _ = self._run_git_command(['diff', '--cached', '--stat'])
            diff_output = diff_stdout
        
        return {
            'staged_files': staged_files,
            'modified_files': modified_files,
            'untracked_files': untracked_files,
            'diff_summary': diff_output,
            'has_changes': bool(staged_files or modified_files or untracked_files)
        }
    
    def generate_commit_message(self, status: dict) -> str:
        """根据状态生成commit message"""
        changes = []
        
        # 分析暂存文件
        for status_code, file_path in status['staged_files']:
            if status_code == 'A':
                changes.append(f"添加 {self._get_file_description(file_path)}")
            elif status_code == 'M':
                changes.append(f"更新 {self._get_file_description(file_path)}")
            elif status_code == 'D':
                changes.append(f"删除 {self._get_file_description(file_path)}")
            elif status_code == 'R':
                changes.append(f"重命名 {self._get_file_description(file_path)}")
        
        # 分析未暂存的修改文件（如果暂存为空，自动添加）
        if not status['staged_files'] and status['modified_files']:
            for status_code, file_path in status['modified_files']:
                if status_code == 'M':
                    changes.append(f"修改 {self._get_file_description(file_path)}")
                elif status_code == 'D':
                    changes.append(f"删除 {self._get_file_description(file_path)}")
        
        # 分析新文件（如果暂存为空，自动添加）
        if not status['staged_files'] and status['untracked_files']:
            for file_path in status['untracked_files']:
                changes.append(f"新增 {self._get_file_description(file_path)}")
        
        if not changes:
            return "清理代码和格式调整"
        
        # 生成commit message
        if len(changes) == 1:
            commit_msg = changes[0]
        else:
            # 多个变更时，生成摘要
            file_types = self._analyze_file_types(status)
            commit_msg = self._generate_summary_commit(changes, file_types)
        
        # 确保commit message不超过72字符
        if len(commit_msg) > 72:
            commit_msg = commit_msg[:69] + "..."
        
        return commit_msg
    
    def _get_file_description(self, file_path: str) -> str:
        """获取文件的描述"""
        file_ext = os.path.splitext(file_path)[1]
        file_name = os.path.basename(file_path)
        
        # 根据文件扩展名推断类型
        type_mapping = {
            '.py': 'Python文件',
            '.js': 'JavaScript文件', 
            '.ts': 'TypeScript文件',
            '.jsx': 'React组件',
            '.tsx': 'React TypeScript组件',
            '.css': '样式文件',
            '.scss': 'SCSS样式',
            '.html': 'HTML页面',
            '.md': '文档',
            '.json': '配置文件',
            '.yml': 'YAML配置',
            '.yaml': 'YAML配置',
            '.xml': 'XML配置',
            '.sql': 'SQL脚本',
            '.sh': 'Shell脚本',
            '.bat': '批处理脚本',
            '.txt': '文本文件',
            '.gitignore': 'Git忽略文件',
            '.env': '环境变量文件',
            '': file_name  # 无扩展名文件
        }
        
        return type_mapping.get(file_ext, file_name)
    
    def _analyze_file_types(self, status: dict) -> dict:
        """分析变更的文件类型"""
        types = {'code': 0, 'config': 0, 'docs': 0, 'other': 0}
        
        all_files = status['staged_files'] + [(f[0], f[1]) for f in status['modified_files']] + [(f, f) for f in status['untracked_files']]
        
        for _, file_path in all_files:
            file_ext = os.path.splitext(file_path)[1].lower()
            file_name = os.path.basename(file_path).lower()
            
            if file_ext in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.cs', '.go', '.rs']:
                types['code'] += 1
            elif file_ext in ['.json', '.yml', '.yaml', '.xml', '.ini', '.cfg', '.conf'] or file_name in ['.gitignore', '.env']:
                types['config'] += 1
            elif file_ext in ['.md', '.txt', '.rst', '.adoc']:
                types['docs'] += 1
            else:
                types['other'] += 1
        
        return types
    
    def _generate_summary_commit(self, changes: List[str], file_types: dict) -> str:
        """生成汇总commit message"""
        dominant_type = max(file_types.items(), key=lambda x: x[1])[0]
        count = sum(file_types.values())
        
        if dominant_type == 'code' and file_types['code'] > 1:
            return f"代码重构和功能优化，涉及{count}个文件"
        elif dominant_type == 'config':
            return f"更新配置文件，调整项目设置"
        elif dominant_type == 'docs':
            return f"更新文档，完善项目说明"
        else:
            # 提取主要操作类型
            actions = []
            for change in changes[:3]:  # 只取前3个
                action = change.split()[0]  # 提取动词
                if action not in actions:
                    actions.append(action)
            
            if len(actions) == 1:
                return f"{actions[0]}多个文件"
            else:
                return f"文件操作：{', '.join(actions[:2])}等"
    
    def auto_commit(self, commit_message: str = None) -> bool:
        """执行自动提交"""
        try:
            status = self.get_git_status()
            
            if not status['has_changes']:
                print("没有需要提交的变更")
                return False
            
            # 如果没有暂存文件，自动添加所有变更
            if not status['staged_files']:
                print("检测到未暂存的变更，自动添加...")
                self._run_git_command(['add', '.'])
                # 重新获取状态
                status = self.get_git_status()
            
            # 生成commit message
            if not commit_message:
                commit_message = self.generate_commit_message(status)
            
            print(f"提交信息: {commit_message}")
            
            # 执行提交
            self._run_git_command(['commit', '-m', commit_message])
            print("✅ 提交成功")
            
            return True
            
        except Exception as e:
            print(f"❌ 提交失败: {e}")
            return False

def main():
    """主函数"""
    try:
        committer = GitAutoCommit()
        
        # 检查是否有命令行参数指定commit message
        commit_message = sys.argv[1] if len(sys.argv) > 1 else None
        
        # 显示当前状态
        status = committer.get_git_status()
        if status['has_changes']:
            print("📋 检测到以下变更:")
            for status_code, file_path in status['staged_files']:
                print(f"  暂存: {status_code} {file_path}")
            for status_code, file_path in status['modified_files']:
                print(f"  修改: {status_code} {file_path}")
            for file_path in status['untracked_files']:
                print(f"  新增: ?? {file_path}")
            print()
        
        # 执行自动提交
        success = committer.auto_commit(commit_message)
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()