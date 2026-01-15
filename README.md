# AI Feedback Tool

一个用于AI助手与用户交互的反馈循环工具，支持CLI和GUI两种模式。

## ✨ 功能特性

- **双模式支持**:
  - **CLI模式**: 命令行交互，轻量快速，适合纯文本反馈
  - **GUI模式**: 图形界面，支持图片上传和粘贴
- **图片支持** (GUI模式):
  - 📎 上传本地图片文件
  - 📋 Ctrl+V 智能粘贴剪贴板图片
  - 自动保存到`feedback/`目录
- **智能粘贴**: 自动识别剪贴板内容类型（图片/文本）
- **警告抑制**: 完全抑制libpng等C库警告，输出干净

## 📦 安装依赖

```bash
pip install pillow
```

## 🚀 使用方法

**推荐使用 `ai_feedback_tool_blocking.py`**（自动抑制stderr警告）

### CLI模式
```bash
python ai_feedback_tool_blocking.py --cli --summary "AI任务摘要"
```

### GUI模式（推荐）
```bash
python ai_feedback_tool_blocking.py --gui --summary "AI任务摘要" --timeout 9999
```

## � 反馈循环工作流程

这个工具设计用于AI助手与用户的持续交互循环：

1. **AI完成任务** → 调用反馈工具，展示工作摘要
2. **用户提供反馈** → 通过CLI输入或GUI界面（支持文本+图片）
3. **AI处理反馈** → 根据用户反馈继续工作
4. **循环继续** → 再次调用反馈工具，直到用户输入"end"结束

### 典型使用场景

- AI代码分析 → 用户提供截图反馈 → AI修复问题
- AI生成文档 → 用户标注修改点 → AI优化内容
- AI调试程序 → 用户上传错误截图 → AI定位并解决

## �📁 项目结构

```
.
├── ai_feedback_tool_simple.py   # 核心实现（CLI+GUI）
├── ai_feedback_tool_blocking.py # 推荐使用（抑制stderr警告）
├── feedback/                    # 图片自动保存目录
├── README.md
├── LICENSE
└── .gitignore
```

## 🔧 参数说明

| 参数 | 必选 | 说明 |
|------|------|------|
| `--cli` / `--gui` | ✅ | 选择CLI或GUI模式（二选一） |
| `--summary` / `-s` | ❌ | AI工作摘要，显示在界面顶部 |
| `--timeout` / `-t` | ❌ | 超时时间（秒），默认6000 |

## 💡 使用示例

### GUI模式示例
```bash
# AI完成代码分析后调用
python ai_feedback_tool_blocking.py --gui --summary "已完成代码分析，发现3个潜在问题" --timeout 9999

# 用户可以：
# - 输入文本反馈
# - 上传错误截图
# - 粘贴剪贴板图片（Ctrl+V）
# - 点击"提交给AI"返回反馈
```

### CLI模式示例
```bash
# 轻量级文本交互
python ai_feedback_tool_blocking.py --cli --summary "代码优化完成"

# 用户输入反馈（多行）
> 请检查第50行的逻辑
> 还需要添加错误处理
> end  # 输入end结束
```

## 🛠️ 技术特性

- **底层stderr重定向**: 使用`os.dup2`在文件描述符层面抑制C库警告
- **智能粘贴检测**: 自动识别剪贴板内容类型，避免误操作
- **跨平台支持**: Windows/Linux/macOS兼容

## 📝 License

MIT License
