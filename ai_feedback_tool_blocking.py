#!/usr/bin/env python3
"""
AI反馈工具 - 阻塞版本
完全抑制stderr输出，包括libpng警告
"""

import sys
import os
import subprocess

def main():
    # 构建命令
    script_path = os.path.join(os.path.dirname(__file__), 'ai_feedback_tool_simple.py')
    cmd = [sys.executable, script_path] + sys.argv[1:]
    
    # 运行并抑制stderr
    if os.name == 'nt':  # Windows
        with open('nul', 'w') as devnull:
            result = subprocess.run(cmd, stderr=devnull)
    else:  # Linux/Mac
        with open('/dev/null', 'w') as devnull:
            result = subprocess.run(cmd, stderr=devnull)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
