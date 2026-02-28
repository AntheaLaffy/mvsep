# MVSEP CLI 安装指南

## 环境要求

- Python 3.8+
- pip

## 安装方式

### 从 PyPI 安装（推荐）

```bash
pip install mvsep-cli
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/mvsep/mvsep-cli.git
cd mvsep-cli

# 安装
pip install -e .
```

## 站点选择

MVSEP 提供两个站点：

| 站点 | 地址 | 推荐地区 |
|------|------|----------|
| 主站 | https://mvsep.com | 全球 |
| 镜像站 | https://mirror.mvsep.com | 中国大陆 |

**注意**：如果访问主站较慢，建议使用镜像站或开启代理。

CLI 默认使用主站，可通过配置切换：

```bash
# 使用主站（默认）
mvsep config set-mirror main

# 使用中国镜像站
mvsep config set-mirror mirror
```

## 账号信息

测试token（由我提供）：

0VZENEq6t0FMsoF6NYRXD021KZHKBg

**注意**：请不要滥用，否则我直接重置了。

## 配置 API 密钥

1. 访问站点登录账号：
   - 主站：https://mvsep.com/login
   - 镜像站：https://mirror.mvsep.com/login

2. 访问 API 页面获取密钥：
   - 主站：https://mvsep.com/user-api
   - 镜像站：https://mirror.mvsep.com/user-api

3. 配置 CLI：

```bash
mvsep config set-token YOUR_API_TOKEN
```

## 验证安装

```bash
mvsep --help
mvsep config show
```

## 快速开始

```bash
# 查看可用的分离类型
mvsep list --popular

# 运行分离任务
mvsep run audio.wav -t 49 --add-opt1 5
```

## 常见问题

### Q: 如何切换站点？

```bash
mvsep config set-mirror mirror  # 使用镜像站
mvsep config set-mirror main    # 使用主站
```

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

### Q: 如何卸载？

```bash
pip uninstall mvsep-cli
```
