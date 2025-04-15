import aiohttp,base64,asyncio
from aiohttp import ClientTimeout
from nonebot.log import logger as log
from .config import hx_config

def get_auth_token():
    username = hx_config.pallworld_user
    password = hx_config.palworld_token
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def format_uptime(seconds):
    """将秒数转换为天数与时分秒"""
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    if days > 0:
        return f"{days}d:{hours}h:{minutes}m"
    elif hours > 0:
        return f"{hours}h:{minutes}m:{seconds}s"
    elif minutes > 0:
        return f"{minutes}:{seconds}s"
    else:
        return f"{seconds}s"


async def make_get_request(url: str,data:dict) -> dict:
    """
    通用GET请求方法
    :param url: 请求URL
    :param headers: 请求头
    :return: JSON响应数据
    """
    try:
        headers = {
                'Accept': 'application/json',
                'Authorization': get_auth_token()
                }
        timeout = ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers,data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    log.error(f"请求失败: {response}, URL: {url}")
                    return None
    except asyncio.CancelledError:
        log.warning("请求被取消")
        raise
    except Exception as e:
        log.error(f"请求出错: {e}")
        return None


async def make_post_request(url: str, data: dict = {}) -> dict:
    """
    通用POST请求方法
    :param url: 请求URL
    :param data: POST数据
    :return: JSON响应数据
    """
    try:
        default_headers = {
            'Content-Type': 'application/json',
            'Authorization': get_auth_token()
        }
        timeout = ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data, headers=default_headers) as response:
                if response.status == 200:
                    try:
                        return response.text()
                    except Exception as e:
                        return response.status
                else:
                    log.error(f"POST请求失败: {response}, URL: {url}")
                    return None
    except asyncio.CancelledError:
        log.warning("请求被取消")
        raise
    except Exception as e:
        log.error(f"POST请求出错: {e}, URL: {url}")
        return None



async def get_server_info(data: dict = {}) -> dict:
    """获取服务器信息"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/info"
    return await make_get_request(url, data=data)

async def get_server_players(data: dict = {}) -> dict:
    """获取服务器玩家列表"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/players"
    return await make_get_request(url, data=data)

async def get_server_settings(data: dict = {}) -> dict:
    """获取服务器设置"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/settings"
    return await make_get_request(url, data=data)

async def get_server_status(data: dict = {}) -> dict:
    """获取服务器状态"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/metrics"
    return await make_get_request(url, data=data)


async def send_announce(connect: str) -> dict:
    """发送公告"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/announce"
    data = {"message": connect}
    return await make_post_request(url, data=data)

async def save_server() -> None:
    """保存服务器"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/save"
    return await make_post_request(url)


async def shutdown_server(waittime:int=30,message:str="服务器将在30s后关闭") -> None:
    """关闭服务器"""
    data = {"waittime": waittime, "message": message}
    url = f"http://{hx_config.palworld_host_port}/v1/api/shutdown"
    return await make_post_request(url,data=data)


async def stop_server() -> None:
    """停止服务器"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/stop"
    return await make_post_request(url)

async def kick_player(player_id: str,message:str) -> None:
    """踢出玩家"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/kick"
    data = {"userid": player_id, "message": message}
    return await make_post_request(url, data=data)

async def ban_player(player_id: str,message:str) -> None:
    """封禁玩家"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/ban"
    data = {"userid": player_id, "message": message}
    return await make_post_request(url, data=data)

async def unban_player(player_id: str) -> None:
    """解封玩家"""
    url = f"http://{hx_config.palworld_host_port}/v1/api/unban"
    data = {"userid": player_id}
    return await make_post_request(url, data=data)