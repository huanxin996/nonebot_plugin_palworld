<!-- markdownlint-disable MD033 -->

<div align="center">

# 🌟 NoneBot Plugin PalWorld 插件 🌟

</div>

<p align="center">
  <a href="https://github.com/huanxin996/nonebot_plugin_hx-yinying"><img src="https://raw.githubusercontent.com/huanxin996/nonebot_plugin_hx-yinying/main/.venv/hx_img.png" width="200" height="200" alt="yinying"></a>
</p>

<div align="center">

✨ **一个用于管理幻兽帕鲁服务器的 NoneBot 插件** ✨  
支持查看服务器状态、发送公告、管理玩家等功能。

</div>

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/huanxin996/nonebot_plugin_palworld?style=social)](https://github.com/huanxin996/nonebot_plugin_palworld)
[![GitHub issues](https://img.shields.io/github/issues/huanxin996/nonebot_plugin_palworld)](https://github.com/huanxin996/nonebot_plugin_palworld/issues)
[![GitHub license](https://img.shields.io/github/license/huanxin996/nonebot_plugin_palworld)](https://github.com/huanxin996/nonebot_plugin_palworld/blob/main/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/nonebot-plugin-palworld)](https://pypi.org/project/nonebot-plugin-palworld/)
[![Python version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Release](https://img.shields.io/github/v/release/huanxin996/nonebot_plugin_palworld?include_prereleases)](https://github.com/huanxin996/nonebot_plugin_palworld/releases)
[![Downloads](https://img.shields.io/pypi/dm/nonebot-plugin-palworld)](https://pypi.org/project/nonebot-plugin-palworld/)
[![NoneBot](https://img.shields.io/badge/NoneBot-2.0-brightgreen)](https://v2.nonebot.dev/)

</div>

---

## 安装📦

### 方式一：通过 pip 安装

```bash
pip install nonebot-plugin-palworld
```

### 方式二：通过 NB-CLI 安装

```bash
nb plugin install nonebot-plugin-palworld
```

### 方式三：通过 Git 安装

```bash
git clone https://github.com/huanxin996/nonebot_plugin_palworld.git
cd nonebot_plugin_palworld
pip install .
```

然后配置插件所需的参数（参考下方配置项）。

---

## 📋 配置项

以下是插件的配置项列表，所有配置项均可在 NoneBot 的配置文件（`.env` 或 `.env.prod`）中设置：

| 配置项 | 类型 | 默认值 | 说明 |
|------|------|------|------|
| `palworld_host_port` | `str` | `127.0.0.1:8211` | 幻兽帕鲁服务器地址和端口<br>**格式**: `host:port`<br>**示例**: `192.168.1.100:8211`<br>**必填** |
| `pallworld_user` | `str` | `Admin` | 幻兽帕鲁服务器管理员用户名<br>**示例**: `ServerAdmin`<br>**必填** |
| `palworld_token` | `str` 或 `int` | `your_token_here` | 访问令牌，用于身份验证<br>**示例**: `12345abcde`<br>**必填** |
| `palworld_images_send` | `bool` | `True` | 是否启用图片消息发送功能<br>**可选值**: `True`（启用）, `False`（禁用） |

---

## 🚀 如何使用？

### 📜 命令列表

以下是插件支持的命令及其功能：

#### **服务器管理**

- **`pl管理 状态`**  
  查看服务器状态。

- **`pl管理 公告 [内容]`**  
  发送服务器公告。  
  **参数**：  
  - `内容`（必需）：公告内容。

- **`pl管理 玩家列表`**  
  查看当前在线玩家列表。

- **`pl管理 玩家信息 [名称]`**  
  查看指定玩家的信息。  
  **参数**：  
  - `名称`（必需）：玩家名称。

#### **玩家管理**

- **`pl管理 踢出 [玩家ID] [原因?]`**  
  踢出指定玩家，原因可选。  
  **参数**：  
  - `玩家ID`（必需）：玩家 ID。  
  - `原因`（可选）：踢出原因，默认为"你被踢了"。

- **`pl管理 封禁 [玩家ID] [原因?]`**  
  封禁指定玩家，原因可选。  
  **参数**：  
  - `玩家ID`（必需）：玩家 ID。  
  - `原因`（可选）：封禁原因，默认为"你已被该服务器封禁"。

- **`pl管理 解封 [玩家ID]`**  
  解封指定玩家。  
  **参数**：  
  - `玩家ID`（必需）：玩家 ID。

#### **服务器控制**

- **`pl管理 关服 [时间] [原因?]`**  
  发送关服命令，时间为秒，原因可选。  
  **参数**：  
  - `时间`（必需）：关闭等待时间（秒）。  
  - `原因`（可选）：关服原因，默认为"服务器即将关闭"。

- **`pl管理 强制关服`**  
  立即强制关闭服务器。

---

## 🔗 相关链接

- [幻兽帕鲁官方网站](https://www.pocketpair.jp/palworld)
- [幻兽帕鲁服务器搭建指南](https://github.com/huanxin996/palworld-server-guide)
- [插件问题反馈](https://github.com/huanxin996/nonebot_plugin_palworld/issues)

## 📝 更新日志

### v0.0.1 (2025-01-06)

- 初始版本发布
- 支持基础服务器管理功能
- 支持玩家管理功能

### v0.1.1 (2025-04-15)

- 使用alc支持多平台
- 优化交互体验
- 添加图片发送支持

## 🤝 贡献

欢迎提交 Pull Request 或 Issue！如有任何问题或建议，请提issue，我看到后会第一时间处理。

## 📄 开源许可

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](https://github.com/huanxin996/nonebot_plugin_palworld/blob/main/LICENSE) 文件。

---

<p align="center">✨ 感谢使用 NoneBot Plugin PalWorld 插件！✨</p>

<!-- markdownlint-restore -->