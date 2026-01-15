#!/usr/bin/env python3
"""
AI反馈工具 - 简化版
支持CLI和GUI模式，GUI支持图片上传和粘贴
"""

import sys
import os

# GUI模式下重定向底层stderr文件描述符，彻底抑制libpng C库警告
if '--gui' in sys.argv:
    # 保存原始stderr文件描述符
    _original_stderr_fd = os.dup(2)
    # 打开null设备
    if os.name == 'nt':  # Windows
        _devnull = os.open('nul', os.O_WRONLY)
    else:  # Linux/Mac
        _devnull = os.open('/dev/null', os.O_WRONLY)
    # 将stderr文件描述符重定向到null设备
    os.dup2(_devnull, 2)
    os.close(_devnull)

import argparse
import warnings
from datetime import datetime
from pathlib import Path

# 抑制Python警告
warnings.filterwarnings("ignore")


def collect_feedback_cli(summary: str = "", timeout: int = 600):
    """
    收集用户反馈 - CLI模式
    
    Args:
        summary: AI工作摘要
        timeout: 超时时间（秒）
    
    Returns:
        反馈列表
    """
    if summary:
        print(f"📋 {summary}")
    print("💬 反馈 (输入end结束):")
    
    feedback_list = []
    
    try:
        while True:
            user_input = input("> ").strip()
            
            if user_input.lower() in ['end', '结束', 'exit', 'quit']:
                break
            
            if user_input:
                feedback_list.append({
                    "type": "text",
                    "content": user_input,
                    "timestamp": datetime.now().isoformat()
                })
    
    except (KeyboardInterrupt, EOFError):
        pass
    
    return feedback_list


def collect_feedback_gui(summary: str = "", timeout: int = 600):
    """
    收集用户反馈 - GUI模式
    支持文本输入、图片上传、图片粘贴
    
    Args:
        summary: AI工作摘要
        timeout: 超时时间（秒）
    
    Returns:
        反馈列表（图片返回绝对路径）
    """
    try:
        import tkinter as tk
        from tkinter import ttk, scrolledtext, messagebox, filedialog
        
        from PIL import Image, ImageTk, ImageGrab
        
        # 抑制PIL的libpng警告
        import logging
        logging.getLogger('PIL').setLevel(logging.ERROR)
        
    except ImportError:
        return collect_feedback_cli(summary, timeout)
    
    feedback_list = []
    image_counter = 0
    current_dir = os.getcwd()
    
    # 创建feedback子目录用于保存图片
    feedback_dir = os.path.join(current_dir, "feedback")
    if not os.path.exists(feedback_dir):
        os.makedirs(feedback_dir)
    
    root = tk.Tk()
    root.title("🤖 AI助手请求用户反馈")
    root.geometry("800x700")
    
    def save_image_to_disk(image, source="upload"):
        """保存图片到当前目录并返回绝对路径"""
        nonlocal image_counter
        image_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"feedback_image_{timestamp}_{image_counter}.png"
        filepath = os.path.join(feedback_dir, filename)
        
        try:
            image.save(filepath, "PNG")
            return os.path.abspath(filepath)
        except Exception as e:
            messagebox.showerror("错误", f"保存图片失败: {e}")
            return None
    
    def upload_images():
        """上传图片文件"""
        file_paths = filedialog.askopenfilenames(
            title="选择图片文件",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                ("所有文件", "*.*")
            ]
        )
        
        for file_path in file_paths:
            try:
                img = Image.open(file_path)
                saved_path = save_image_to_disk(img, "upload")
                if saved_path:
                    feedback_list.append({
                        "type": "image",
                        "content": saved_path,
                        "timestamp": datetime.now().isoformat()
                    })
                    image_listbox.insert(tk.END, f"📎 {os.path.basename(saved_path)}")
                    status_label.config(text=f"✅ 已上传: {os.path.basename(saved_path)}")
            except Exception as e:
                messagebox.showerror("错误", f"无法打开图片 {file_path}: {e}")
    
    def paste_image(show_warning=True):
        """从剪贴板粘贴图片"""
        try:
            img = ImageGrab.grabclipboard()
            if img is None:
                if show_warning:
                    messagebox.showwarning("提示", "剪贴板中没有图片！\n请先复制图片后再粘贴。")
                return False
            
            if isinstance(img, Image.Image):
                saved_path = save_image_to_disk(img, "paste")
                if saved_path:
                    feedback_list.append({
                        "type": "image",
                        "content": saved_path,
                        "timestamp": datetime.now().isoformat()
                    })
                    image_listbox.insert(tk.END, f"📋 {os.path.basename(saved_path)}")
                    status_label.config(text=f"✅ 已粘贴: {os.path.basename(saved_path)}")
                return True
            else:
                if show_warning:
                    messagebox.showwarning("提示", "剪贴板内容不是图片格式")
                return False
        except Exception as e:
            messagebox.showerror("错误", f"粘贴图片失败: {e}")
            return False
    
    def submit_feedback():
        """提交反馈"""
        text_content = text_input.get("1.0", tk.END).strip()
        if text_content:
            feedback_list.append({
                "type": "text",
                "content": text_content,
                "timestamp": datetime.now().isoformat()
            })
        
        if not feedback_list:
            messagebox.showwarning("警告", "请提供反馈内容！")
            return
        
        if messagebox.askyesno("确认", f"确定提交 {len(feedback_list)} 项反馈给AI吗？"):
            root.quit()
            root.destroy()
    
    def cancel_feedback():
        """取消反馈"""
        if messagebox.askyesno("确认", "确定取消反馈吗？"):
            feedback_list.clear()
            root.quit()
            root.destroy()
    
    # 标题
    title_label = tk.Label(root, text="🤖 AI助手请求用户反馈", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)
    
    # 摘要区域
    if summary:
        summary_frame = tk.LabelFrame(root, text="📋 AI工作摘要", font=("Arial", 10, "bold"))
        summary_frame.pack(fill="x", padx=10, pady=5)
        
        summary_text = scrolledtext.ScrolledText(summary_frame, height=4, wrap=tk.WORD)
        summary_text.pack(fill="x", padx=5, pady=5)
        summary_text.insert("1.0", summary)
        summary_text.config(state="disabled")
    
    # 文本反馈区域
    text_frame = tk.LabelFrame(root, text="💬 文本反馈", font=("Arial", 10, "bold"))
    text_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    text_input = scrolledtext.ScrolledText(text_frame, height=8, wrap=tk.WORD)
    text_input.pack(fill="both", expand=True, padx=5, pady=5)
    
    # 图片反馈区域
    image_frame = tk.LabelFrame(root, text="📷 图片反馈", font=("Arial", 10, "bold"))
    image_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    image_listbox = tk.Listbox(image_frame, height=6)
    image_listbox.pack(fill="both", expand=True, padx=5, pady=5)
    
    # 图片操作按钮
    image_btn_frame = tk.Frame(image_frame)
    image_btn_frame.pack(fill="x", padx=5, pady=5)
    
    ttk.Button(image_btn_frame, text="📎 上传图片", command=upload_images).pack(side="left", padx=5)
    ttk.Button(image_btn_frame, text="📋 粘贴图片 (Ctrl+V)", command=paste_image).pack(side="left", padx=5)
    
    # 状态栏
    status_label = tk.Label(root, text=f"📁 图片保存目录: {feedback_dir}", anchor="w", relief=tk.SUNKEN)
    status_label.pack(fill="x", side="bottom", padx=10, pady=5)
    
    # 提交按钮
    btn_frame = tk.Frame(root)
    btn_frame.pack(fill="x", padx=10, pady=10)
    
    ttk.Button(btn_frame, text="✅ 提交给AI", command=submit_feedback).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="❌ 取消", command=cancel_feedback).pack(side="right", padx=5)
    
    # 绑定快捷键 - 只在剪贴板有图片时才粘贴图片，否则让文本框正常处理
    def smart_paste(event):
        """智能粘贴：检测剪贴板内容类型"""
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                paste_image(show_warning=False)
                return "break"  # 阻止默认行为
        except:
            pass
        return None  # 让文本框正常处理文本粘贴
    
    root.bind("<Control-v>", smart_paste)
    
    root.mainloop()
    return feedback_list


def main():
    parser = argparse.ArgumentParser(
        description="AI反馈工具 - 简化版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # CLI模式
  python ai_feedback_tool_simple.py --cli --summary "完成了代码分析"
  
  # GUI模式（支持图片上传和粘贴）
  python ai_feedback_tool_simple.py --gui --summary "完成了代码分析"
        """
    )
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--cli', action='store_true', help='使用命令行模式')
    mode_group.add_argument('--gui', action='store_true', help='使用GUI模式（支持图片）')
    
    parser.add_argument('--summary', '-s', type=str, default='', help='AI工作摘要')
    parser.add_argument('--timeout', '-t', type=int, default=6000, help='超时时间（秒）')
    
    args = parser.parse_args()
    
    # 收集反馈
    if args.gui:
        feedback = collect_feedback_gui(summary=args.summary, timeout=args.timeout)
    else:
        feedback = collect_feedback_cli(summary=args.summary, timeout=args.timeout)
    
    # 输出反馈到stdout供AI终端接收
    if feedback:
        print("\n" + "="*60)
        print("📬 收到用户反馈:")
        print("="*60)
        for item in feedback:
            if item['type'] == 'text':
                print(f"💬 {item['content']}")
            elif item['type'] == 'image':
                print(f"🖼️ 图片: {item['content']}")
        print("="*60 + "\n")
    else:
        print("\n⚠️ 未收到反馈或用户取消\n")
    
    return feedback


if __name__ == "__main__":
    main()
