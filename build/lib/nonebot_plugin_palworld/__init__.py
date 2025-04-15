from nonebot import require
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import on_alconna, Alconna, Args, Option, CommandMeta, Arparma
from nonebot_plugin_alconna.uniseg import UniMessage, MsgTarget
from nonebot.plugin import PluginMetadata,inherit_supported_adapters
from .config import Config,hx_config
from .image import (
    generate_server_status_image,
    generate_announcement_image,
    generate_player_list_image,
    generate_player_info_image,
    generate_shutdown_image,
    generate_kick_image,
    generate_ban_image,
    generate_unban_image,
    generate_force_shutdown_image,
)
from .api import *

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_palworld",
    description=(
        "用于管理幻兽帕鲁服务器的插件，支持查看服务器状态、发送公告、管理玩家等功能。"
    ),
    usage=(
        "命令列表：\n"
        "pl管理 状态 - 查看服务器状态\n"
        "pl管理 公告 [内容] - 发送服务器公告\n"
        "pl管理 玩家列表 - 查看当前在线玩家列表\n"
        "pl管理 玩家信息 [名称] - 查看指定玩家的信息\n"
        "pl管理 踢出 [玩家ID] [原因?] - 踢出指定玩家，原因可选\n"
        "pl管理 封禁 [玩家ID] [原因?] - 封禁指定玩家，原因可选\n"
        "pl管理 解封 [玩家ID] - 解封指定玩家\n"
        "pl管理 关服 [时间] [原因?] - 发送关服命令，时间为秒，原因可选\n"
        "pl管理 强制关服 - 立即强制关闭服务器"
    ),
    type="application",
    homepage="https://github.com/huanxin996/nonebot_plugin_palworld",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)

# 定义命令
palworld_manager = on_alconna(
    Alconna(
        "pl管理",
        Option("状态", help_text="查看服务器状态"),
        Option("公告", Args["内容", str], help_text="发送服务器公告"),
        Option("玩家列表", help_text="查看当前在线玩家列表"),
        Option("玩家信息", Args["名称", str], help_text="查看指定玩家的信息"),
        Option("踢出", Args["玩家ID", str] + Args["原因?", str], help_text="踢出指定玩家，原因可选"),
        Option("封禁", Args["玩家ID", str] + Args["原因?", str], help_text="封禁指定玩家，原因可选"),
        Option("解封", Args["玩家ID", str], help_text="解封指定玩家"),
        Option("关服", Args["时间", int] + Args["原因?", str], help_text="发送关服命令，时间为秒，原因可选"),
        Option("强制关服", help_text="立即强制关闭服务器"),
        meta=CommandMeta(
            description="管理幻兽帕鲁服务器",
            usage=(
                "pl管理 状态\n"
                "pl管理 公告 [内容]\n"
                "pl管理 玩家列表\n"
                "pl管理 玩家信息 [名称]\n"
                "pl管理 踢出 [玩家ID] [原因?]\n"
                "pl管理 封禁 [玩家ID] [原因?]\n"
                "pl管理 解封 [玩家ID]\n"
                "pl管理 关服 [时间] [原因?]\n"
                "pl管理 强制关服"
            )
        )
    ),
    aliases={"pl", "palworld"},
    use_cmd_start=True,
    block=True
)

@palworld_manager.handle()
async def handle_palworld_manager(result: Arparma, target: MsgTarget):
    if result.find("状态"):
        log.debug("获取服务器状态")
        server_metrics = await get_server_status()
        server_info = await get_server_info()
        if not server_metrics or not server_info:
            await target.send("获取服务器状态失败,请检查后台输出")
            return
        fps = server_metrics["serverfps"]
        time_late = server_metrics["serverframetime"]
        online = server_metrics["currentplayernum"]
        max_players = server_metrics["maxplayernum"]
        uptime = server_metrics["uptime"]
        day = server_metrics["days"]
        online_off = f"{online}/{max_players}"
        uptime_format = format_uptime(uptime)
        server_version = server_info.get("version")
        world_guid = server_info.get("worldguid")
        server_name = server_info.get("servername")
        msg = (
            f"幻兽帕鲁服务器状态：\n"
            f"服务器名称：{server_name}\n"
            f"服务器版本：{server_version}\n"
            f"服务器FPS：{fps}\n"
            f"服务器延迟：{int(time_late)}ms\n"
            f"在线人数：{online_off}\n"
            f"服务器运行时间：{uptime_format}\n"
            f"服务器运行天数：{day}天\n"
            f"世界GUID：{world_guid}"
        )
        if hx_config.palworld_images_send:
            try:
                image_data = await generate_server_status_image(server_info, server_metrics)
                await target.send(UniMessage.image(raw=image_data))
            except Exception as e:
                log.error(f"图片发送失败，回退到文字消息: {e}")
                await target.send(msg)
        else:
            await target.send(msg)

    elif result.find("公告"):
        content = result.query[str]("公告.内容")
        log.debug(f"发送公告: {content}")
        if not content:
            await target.send("请输入公告内容")
            return
        result = await send_announce(content)
        if result:
            msg = f"公告发送成功，服务器返回：{result}"
        else:
            msg = f"公告发送失败,错误码:{result}"
        if hx_config.palworld_images_send:
            try:
                image_data = await generate_announcement_image(msg)
                await target.send(UniMessage.image(raw=image_data))
            except Exception as e:
                log.error(f"图片发送失败，回退到文字消息: {e}")
                await target.send(msg)
        else:
            await target.send(msg)

    elif result.find("玩家列表"):
        log.debug("获取玩家列表")
        response = await get_server_players()
        if response and "players" in response:
            players = response["players"]
            if players:
                if hx_config.palworld_images_send:
                    try:
                        image_data = await generate_player_list_image(players)
                        await target.send(UniMessage.image(raw=image_data))
                    except Exception as e:
                        log.error(f"图片发送失败，回退到文字消息: {e}")
                        player_info = "\n".join([
                            f"玩家: {player.get('name', 'Unknown')}, 等级: {player.get('level', 0)}, 延迟: {player.get('ping', 0)}ms"
                            for player in players
                        ])
                        await target.send(f"当前在线玩家：\n{player_info}")
                else:
                    player_info = "\n".join([
                        f"玩家: {player.get('name', 'Unknown')}, 等级: {player.get('level', 0)}, 延迟: {player.get('ping', 0)}ms"
                        for player in players
                    ])
                    await target.send(f"当前在线玩家：\n{player_info}")
            else:
                await target.send("当前没有在线玩家")
        else:
            await target.send("获取玩家列表失败")

    elif result.find("玩家信息"):
        name = result.query[str]("玩家信息.名称")
        log.debug(f"获取玩家信息: {name}")
        response = await get_server_players()
        if response and "players" in response:
            players = response["players"]
            for player in players:
                if hx_config.palworld_images_send:
                    try:
                        image_data = await generate_player_info_image(player)
                        await target.send(UniMessage.image(raw=image_data))
                    except Exception as e:
                        log.error(f"图片发送失败，回退到文字消息: {e}")
                        info = (
                            f"玩家: {player.get('name', 'Unknown')}\n"
                            f"等级: {player.get('level', 0)}\n"
                            f"建筑数: {player.get('building_count', 0)}\n"
                            f"坐标: ({player.get('location_x', 0):.1f}, {player.get('location_y', 0):.1f})\n"
                            f"延迟: {int(player.get('ping', 0))}ms"
                        )
                        await target.send(info)
                else:
                    info = (
                        f"玩家: {player.get('name', 'Unknown')}\n"
                        f"等级: {player.get('level', 0)}\n"
                        f"建筑数: {player.get('building_count', 0)}\n"
                        f"坐标: ({player.get('location_x', 0):.1f}, {player.get('location_y', 0):.1f})\n"
                        f"延迟: {int(player.get('ping', 0))}ms"
                    )
                    await target.send(info)
                return
        await target.send(f"未找到玩家 {name}")

    elif result.find("踢出"):
        player_id = result.query[str]("踢出.玩家ID")
        reason = result.query[str]("踢出.原因") or "你被踢了"
        log.debug(f"踢出玩家: {player_id}， 原因: {reason}")
        result = await kick_player(player_id, reason)
        if result:
            msg = f"踢出玩家成功\n玩家ID：{player_id}\n原因：{reason}"
            if hx_config.palworld_images_send:
                try:
                    image_data = await generate_kick_image(player_id, reason)
                    await target.send(UniMessage.image(raw=image_data))
                except Exception as e:
                    log.error(f"图片发送失败，回退到文字消息: {e}")
                    await target.send(msg)
            else:
                await target.send(msg)
        else:
            await target.send(f"踢出玩家失败,错误码:{result}")

    elif result.find("封禁"):
        player_id = result.query[str]("封禁.玩家ID")
        reason = result.query[str]("封禁.原因") or "你已被该服务器封禁"
        log.debug(f"封禁玩家: {player_id}， 原因: {reason}")
        result = await ban_player(player_id, reason)
        if result:
            msg = f"已封禁该玩家\n玩家ID：{player_id}\n原因：{reason}"
            if hx_config.palworld_images_send:
                try:
                    image_data = await generate_ban_image(player_id, reason)
                    await target.send(UniMessage.image(raw=image_data))
                except Exception as e:
                    log.error(f"图片发送失败，回退到文字消息: {e}")
                    await target.send(msg)
            else:
                await target.send(msg)
        else:
            await target.send(f"封禁失败,错误码:{result}")

    elif result.find("解封"):
        player_id = result.query[str]("解封.玩家ID")
        log.debug(f"解封玩家: {player_id}")
        result = await unban_player(player_id)
        if result:
            msg = f"已解封该玩家\n玩家ID：{player_id}"
            if hx_config.palworld_images_send:
                try:
                    image_data = await generate_unban_image(player_id)
                    await target.send(UniMessage.image(raw=image_data))
                except Exception as e:
                    log.error(f"图片发送失败，回退到文字消息: {e}")
                    await target.send(msg)
            else:
                await target.send(msg)
        else:
            await target.send(f"解封失败，请检查服务器是否开启,错误码:{result}")

    elif result.find("关服"):
        time = result.query[int]("关服.时间")
        reason = result.query[str]("关服.原因") or "服务器即将关闭"
        log.debug(f"关服: {time}, 原因: {reason}")
        result = await shutdown_server(time, reason)
        if result == 200:
            msg = f"已发送关闭命令,服务器将在{time}秒后关闭，原因：{reason}"
        else:
            msg = f"发送关闭命令失败,错误码:{result}"
        if hx_config.palworld_images_send:
            try:
                image_data = await generate_shutdown_image(time, reason)
                await target.send(UniMessage.image(raw=image_data))
            except Exception as e:
                log.error(f"图片发送失败，回退到文字消息: {e}")
                await target.send(msg)
        else:
            await target.send(msg)

    elif result.find("强制关服"):
        log.debug("强制关服")
        result = await stop_server()
        if result:
            msg = f"强制关停服务器成功"
            if hx_config.palworld_images_send:
                try:
                    image_data = await generate_force_shutdown_image()
                    await target.send(UniMessage.image(raw=image_data))
                except Exception as e:
                    log.error(f"图片发送失败，回退到文字消息: {e}")
                    await target.send(msg)
            else:
                await target.send(msg)
        else:
            await target.send(f"强制关停失败,错误码:{result}")
    else:
        log.debug("未知命令")