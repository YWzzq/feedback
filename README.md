# AI Feedback Tool

一个用于AI助手与用户交互的反馈工具，支持CLI和GUI模式。

## ✨ 功能特性

- **CLI模式**: 命令行交互，轻量快速
- **GUI模式**: 图形界面，支持图片上传和粘贴
- **图片支持**: 
  - 📎 上传本地图片文件
  - 📋 Ctrl+V 粘贴剪贴板图片
- **智能粘贴**: 自动识别剪贴板内容类型
- **反馈存储**: 图片自动保存到`feedback/`目录

## 📦 安装依赖

```bash
pip install pillow
```

## 🚀 使用方法

### CLI模式
```bash
python ai_feedback_tool_simple.py --cli --summary "任务摘要"
```

### GUI模式（推荐）
```bash
python ai_feedback_tool_simple.py --gui --summary "任务摘要"
```

### 使用阻塞版本（抑制警告）
```bash
python ai_feedback_tool_blocking.py --gui --summary "任务摘要"
```

## 📁 项目结构

```
.
├── ai_feedback_tool_simple.py   # 主程序（CLI+GUI）
├── ai_feedback_tool_blocking.py # 阻塞版本（抑制stderr警告）
├── feedback/                    # 图片保存目录
├── README.md
├── LICENSE
└── .gitignore
```

## 🔧 参数说明

| 参数 | 说明 |
|------|------|
| `--cli` | 使用命令行模式 |
| `--gui` | 使用GUI模式（支持图片） |
| `--summary` / `-s` | AI工作摘要 |
| `--timeout` / `-t` | 超时时间（秒），默认6000 |

## 📝 License

MIT License
