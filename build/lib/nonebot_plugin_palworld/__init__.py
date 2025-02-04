from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent, Message
from nonebot.plugin.on import on_command
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from typing import Union
from .config import Config
from .api import *


__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_palworld",
    description="幻歆",
    usage=(
        "支持幻兽帕鲁服务器提供的rest接口\n"
        "支持全部接口"
    ),
    type="application",
    homepage="https://github.com/huanxin996/nonebot_plugin_palworld",
    config=Config,
    supported_adapters={
        "~onebot.v11"
    },
)


palworld_status = on_command("pl状态",aliases={"plworld_status"}, priority=15, block=True)
plworld_announce = on_command("pl公告",aliases={"plworld_announce"}, priority=15, block=True)
plworld_playerlist = on_command("pl玩家列表",aliases={"plworld_playerlist"}, priority=15, block=True)
plworld_playerinfo = on_command("pl玩家信息",aliases={"plworld_playerinfo"}, priority=15, block=True)
plworld_kick = on_command("pl踢出",aliases={"plworld_kick"}, priority=15, block=True)
plworld_ban = on_command("pl封禁",aliases={"plworld_ban"}, priority=15, block=True)
plworld_unban = on_command("pl解封",aliases={"plworld_unban"}, priority=15, block=True)
plworld_down = on_command("pl关服",aliases={"plworld_down"}, priority=15, block=True)
plworld_shutdown = on_command("pl强制关服",aliases={"plworld_shutdown"}, priority=15, block=True)

@palworld_status.handle()
async def palworld_zt_handle(event: Union[GroupMessageEvent, PrivateMessageEvent]):
    server_metrics = await get_server_status()
    server_info = await get_server_info()
    if not server_metrics or not server_info:
        await palworld_status.finish("获取服务器状态失败,请检查后台输出")
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
    msg = f"幻兽帕鲁服务器状态：\n服务器名称：{server_name}\n服务器版本：{server_version}\n服务器FPS：{fps}\n服务器延迟：{int(time_late)}ms\n在线人数：{online_off}\n服务器运行时间：{uptime_format}\n服务器运行天数：{day}天\n世界GUID：{world_guid}"
    await palworld_status.finish(msg)

@plworld_announce.handle()
async def palworld_announce_handle(event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    connect = args.extract_plain_text().strip()
    if not connect:
        await plworld_announce.finish("请输入公告内容")
    result = await send_announce(connect)
    if result:
        await plworld_announce.finish("公告发送成功，服务器返回：{result}")
    else:
        await plworld_announce.finish(f"公告发送失败,错误码:{result}")

@plworld_playerlist.handle()
async def palworld_playerlist_handle(event: Union[GroupMessageEvent, PrivateMessageEvent]):
    response = await get_server_players()
    if response and "players" in response:
        players = response["players"]
        if players:
            player_info = []
            for player in players:
                info = (
                    f"玩家: {player.get('name', 'Unknown')}\n"
                    f"等级: {player.get('level', 0)}\n"
                    f"建筑数: {player.get('building_count', 0)}\n"
                    f"坐标: ({player.get('location_x', 0):.1f}, {player.get('location_y', 0):.1f})\n"
                    f"延迟: {int(player.get('ping', 0))}ms\n"
                    f"------------"
                )
                player_info.append(info)
    await plworld_playerlist.finish("当前在线玩家：\n" + "\n".join(player_info))

@plworld_playerinfo.handle()
async def palworld_playerinfo_handle(event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    name = args.extract_plain_text().strip()
    if not name:
        await plworld_playerinfo.finish("请输入玩家名称")
    response = await get_server_players()
    if response and "players" in response:
        players = response["players"]
    else:
        await plworld_playerinfo.finish(f"获取玩家信息失败,可能该玩家不在该服务器")
    
@plworld_kick.handle()
async def palworld_kick_handle(event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await plworld_kick.finish("请输入玩家ID")
    if len(args) == 1:
        result = await kick_player(args[0],"你被踢了")
    elif len(args) == 2:
        result = await kick_player(args[0],args[1])
    else:
        await plworld_kick.finish("参数错误")
    if result:
        await plworld_kick.finish(f"踢出玩家成功")
    else:
        await plworld_kick.finish(f"踢出玩家失败,错误码:{result}")


@plworld_down.handle()
async def plworld_shutdown_handle(event:Union[GroupMessageEvent,PrivateMessageEvent],args:Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await plworld_kick.finish("请输入参数")
    if len(args) == 1:
        result = await shutdown_server(30,args[1])
    elif len(args) == 2:
        result = await shutdown_server(int(args[0]),args[1])
    if result == 200:
        await plworld_shutdown.finish(f"已发送关闭命令,服务器将在30秒后关闭，服务器返回：{result}")
    else:
        await plworld_shutdown.finish(f"发送关闭命令失败,错误码:{result}")


@plworld_shutdown.handle()
async def plworld_shutdown_handle(event: Union[GroupMessageEvent, PrivateMessageEvent]):
    result = await stop_server()
    if result:
        await plworld_shutdown.finish(f"强制关停服务器，服务器返回：{result}")
    else:
        await plworld_shutdown.finish(f"强制关停失败,错误码:{result}")
    

@plworld_ban.handle()
async def plworld_ban_handle(event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await plworld_kick.finish("请输入玩家ID")
    if len(args) == 1:
        result = await ban_player(args[0],"你已被该服务器封禁")
    elif len(args) == 2:
        result = await shutdown_server(int(args[0]),args[1])
    if result:
        await plworld_shutdown.finish(f"已封禁该玩家，服务器返回：{result}")
    else:
        await plworld_shutdown.finish(f"发送关闭命令失败,错误码:{result}")


@plworld_unban.handle()
async def plworld_unban_handle(event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await plworld_unban.finish("请输入玩家ID")
    elif len(args) != 1:
        await plworld_unban.finish("参数错误")
    result = await unban_player(args[0])
    if result:
        await plworld_unban.finish(f"已解封该玩家，服务器返回：{result}")
    else:
        await plworld_unban.finish(f"解封失败，请检查服务器是否开启,错误码:{result}")