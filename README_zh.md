# MVSEP CLI

[English](./README.md) | [中文](./README_zh.md)

[MVSEP](https://mvsep.com) 音乐分离 API 的命令行工具。

## 功能特性

- 上传音频文件并创建分离任务
- 实时监控任务状态
- 自动下载分离后的音轨
- 支持多种分离算法和模型（从 API 动态获取）
- 可配置的默认设置
- 支持镜像站点（中国）
- 自动重试机制（处理限速和服务器错误）
- 调试模式便于问题排查

## 安装

### 环境要求

- Python 3.8+
- pip

### 从 PyPI 安装（推荐）

```bash
pip install mvsep-cli
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/AntheaLaffy/mvsep.git
cd mvsep-cli

# 安装
pip install -e .
```

### 验证安装

```bash
mvsep --help
mvsep config show
```

## 镜像站点

MVSEP 提供镜像站点以便地区更好地访问：

| 镜像 | 地址 |
|------|------|
| 主站 | https://mvsep.com |
| 镜像 | https://mirror.mvsep.com (中国) |

设置首选镜像：

```bash
mvsep config set-mirror mirror  # 使用中国镜像
mvsep config set-mirror main    # 使用主站
```

## 快速开始

1. 设置 API 令牌：

```bash
mvsep config set-token 你的API令牌
```

从 https://mvsep.com/user-api 获取 API 令牌

**测试令牌（仅供测试，请勿滥用）**：
```
0VZENEq6t0FMsoF6NYRXD021KZHKBg
```

2. 查看可用的算法：

```bash
# 列出所有算法
mvsep list

# 搜索特定算法
mvsep list -s karaoke

# 显示特定算法的模型
mvsep list --models 49

# 或使用 algorithms 命令
mvsep algorithms
mvsep algorithms -i 20
```

3. 运行分离任务：

```bash
mvsep run audio.wav -t 49 --add-opt1 5
```

4. 或手动上传并等待：

```bash
mvsep upload audio.wav -t 49 --add-opt1 5 --wait
```

## 配置

```bash
# 显示当前配置
mvsep config show

# 设置 API 令牌
mvsep config set-token 你的令牌

# 设置默认输出目录
mvsep config set-output-dir /path/to/output

# 设置默认输出格式 (1 = wav 16bit)
mvsep config set-output-format 1

# 设置轮询间隔（秒）
mvsep config set-interval 5
```

## 命令

| 命令 | 描述 |
|------|------|
| `mvsep run <文件>` | 完整流程：上传 + 等待 + 下载 |
| `mvsep upload <文件>` | 上传并创建任务 |
| `mvsep status <hash>` | 查看任务状态 |
| `mvsep wait <hash>` | 等待任务完成 |
| `mvsep download <hash>` | 下载结果 |
| `mvsep list` | 列出可用算法（从 API 获取） |
| `mvsep list --models <类型>` | 显示特定分离类型的模型 |
| `mvsep list --search <关键词>` | 按关键词搜索算法 |
| `mvsep list --popular` | 显示热门算法 |
| `mvsep algorithms` | 列出所有算法的详细选项 |
| `mvsep algorithms -i <ID>` | 显示特定算法的详细选项 |
| `mvsep history` | 显示任务历史 |
| `mvsep config` | 管理配置 |

## 选项

`upload` 和 `run` 命令的通用选项：

- `-t, --sep-type` - 分离类型（使用 `mvsep list` 查看可用类型）
- `-f, --output-format` - 输出格式（默认：1 = wav 16bit）
- `--add-opt1` - 模型选项 1
- `--add-opt2` - 模型选项 2
- `--add-opt3` - 模型选项 3
- `-o, --output-dir` - 输出目录
- `-i, --interval` - 轮询间隔（秒）
- `--wait` - 上传后等待完成
- `--timeout` - 最大等待时间（秒）
- `--demo` - 发布到演示页面

## 示例

```bash
# 列出热门分离类型
mvsep list --popular

# 搜索卡拉OK模型
mvsep list -s karaoke

# 显示 MVSep Karaoke 的模型（类型 49）
mvsep list --models 49
mvsep algorithms -i 49

# 显示 Demucs4 HT 的模型（类型 20）
mvsep list --models 20

# 使用特定模型上传（类型 49，模型 5 = BS Roformer by frazer and becruily）
mvsep upload song.wav -t 49 --add-opt1 5 --wait

# 完整流程并指定输出格式
mvsep run song.wav -t 49 --add-opt1 5 -f 2 -o ./output

# 下载之前的结果
mvsep download 20260227153708-abc123-vocals.wav -o ./output

# 查看任务状态
mvsep status 20260227153708-abc123-vocals.wav

# 显示任务历史
mvsep history
```

## 输出格式

| 值 | 格式 |
|----|------|
| 0 | mp3 (320 kbps) |
| 1 | wav (16 bit) |
| 2 | flac (16 bit) |
| 3 | m4a (有损) |
| 4 | wav (32 bit) |
| 5 | flac (24 bit) |

## 高级用法

### 使用远程 URL

可以处理远程 URL 的音频（需要 API 支持）：

```python
from mvsep_cli.api import MVSEP_API

api = MVSEP_API("YOUR_TOKEN")
result = api.create_task(
    remote_url="https://example.com/audio.wav",
    sep_type=49,
    add_opt1="5"
)
```

### 调试模式

启用调试日志以便问题排查：

```python
api = MVSEP_API("YOUR_TOKEN", debug=True)
```

### 自定义重试设置

调整限速时的重试行为：

```python
api = MVSEP_API("YOUR_TOKEN", retries=30, retry_interval=20)
```

## 许可证

Apache License 2.0

## 常见问题

### Q: 如何升级？

```bash
pip install --upgrade mvsep-cli
```

### Q: 配置文件在哪里？

- Linux/macOS: `~/.mvsep_cli_config`
- Windows: `%USERPROFILE%\.mvsep_cli_config`

### Q: 任务历史在哪里？

- Linux/macOS: `~/.mvsep_tasks.json`
- Windows: `%USERPROFILE%\.mvsep_tasks.json`

### Q: 如何找到合适的模型？

1. 搜索你想要的算法类型：
   ```bash
   mvsep list -s demucs
   ```

2. 查看该算法的可用模型：
   ```bash
   mvsep list --models 20  # For Demucs4 HT
   ```

3. SDR（Signal to Distortion Ratio，信号失真比）越高的模型通常越好

### Q: 如何卸载？

```bash
pip uninstall mvsep-cli
```
