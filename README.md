<!-- markdownlint-disable MD033 MD036 MD041 -->
# PalWorld Api

<p align="center">
  <a href="https://huanxinbot.com/"><img src="https://raw.githubusercontent.com/huanxin996/nonebot_plugin_hx-yinying/main/.venv/hx_img.png" width="200" height="200" alt="这里放一张oc饭🤤"></a>
</p>

<div align="center">

## 配置项

<details>
  <summary><b style="font-size: 1.5rem">配置项列表</b></summary>

### palworld_host_port

- 类型：`str`
- 默认值：`127.0.0.1:8081`
- 说明：幻兽帕鲁的主机+开放的restapi的端口
- 重要：必填

### palworld_token

- 类型：`str`
- 默认值：`your_token_here`
- 说明：你的服务器管理密码
- 重要：必填

</details>
<br>

## 如何使用？

- pl状态 ：获取服务器状态
- pl公告：向服务器发送一条字幕；参数：要发送的文本(必需)
- pl玩家列表：获取当前服务器在线玩家列表
- pl玩家信息：获取知道玩家在服务器的信息，需要玩家id；参数：玩家id(必需)
- pl踢出：踢出服务器指定玩家，需要玩家id；参数：玩家id(必需)，踢出原因(非必需)
- pl封禁：封禁服务器内指定玩家，需要玩家id；参数：玩家id(必需)，封禁原因(非必需)
- pl解封：解封指定玩家
- pl关服：关停服务器；参数：关闭等待时间(数字)(非必需，默认30s)，关停前发送信息(必需)
- pl强制关服：强制关停服务器

### 作者说的一些话: 

本人代码水平很差，将就着用罢，有问题请提iss
