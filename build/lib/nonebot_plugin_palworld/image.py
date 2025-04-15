import io,os,sys
from PIL import Image, ImageDraw, ImageFont

def get_font_path():
    """获取字体路径"""
    system = sys.platform
    if system.startswith('win'):
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/simhei.ttf"
        ]
    elif system.startswith('linux'):
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"
        ]
    elif system.startswith('darwin'):
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            "/System/Library/Fonts/STHeiti Light.ttc"
        ]
    else:
        return None
    for path in font_paths:
        if os.path.exists(path):
            return path
    return None

def generate_base_image(text: str, title: str = "信息") -> bytes:
    """通用图片生成"""
    font_path = get_font_path()
    if font_path is None:
        font_title = ImageFont.load_default()
        font_content = ImageFont.load_default()
    else:
        font_title = ImageFont.truetype(font_path, 28)
        font_content = ImageFont.truetype(font_path, 22)
    lines = text.split("\n")
    max_width = max(
        [font_content.getbbox(line)[2] for line in lines] + [font_title.getbbox(title)[2]]
    ) + 40
    line_height = font_content.getbbox("A")[3] + 10
    title_height = font_title.getbbox("A")[3] + 30
    img_height = title_height + line_height * len(lines) + 50
    img = Image.new("RGB", (max_width, img_height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    border_color = (212, 175, 55)
    border_width = 5
    draw.rectangle(
        [(border_width // 2, border_width // 2), (max_width - border_width // 2 - 1, img_height - border_width // 2 - 1)],
        outline=border_color,
        width=border_width,
    )
    draw.text((20, 20), title, fill=(255, 215, 0), font=font_title)
    y = title_height + 20
    for line in lines:
        draw.text((20, y), line, fill=(255, 255, 255), font=font_content)
        y += line_height
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

async def generate_server_status_image(server_info: dict, server_metrics: dict) -> bytes:
    """生成服务器状态的图片"""
    text = (
        f"服务器名称：{server_info.get('servername')}\n"
        f"服务器版本：{server_info.get('version')}\n"
        f"服务器FPS：{server_metrics.get('serverfps')}\n"
        f"服务器延迟：{int(server_metrics.get('serverframetime', 0))}ms\n"
        f"在线人数：{server_metrics.get('currentplayernum')}/{server_metrics.get('maxplayernum')}\n"
        f"服务器运行时间：{server_metrics.get('uptime')}\n"
        f"服务器运行天数：{server_metrics.get('days')}天\n"
        f"世界GUID：{server_info.get('worldguid')}"
    )
    return generate_base_image(text, title="服务器状态")

async def generate_announcement_image(content: str) -> bytes:
    """生成公告的图片"""
    text = f"公告内容：\n{content}"
    return generate_base_image(text, title="服务器公告")

async def generate_player_list_image(players: list) -> bytes:
    """生成玩家列表的图片"""
    if not players:
        text = "当前没有在线玩家"
    else:
        text = "\n".join([
            f"玩家: {player.get('name', 'Unknown')}, 等级: {player.get('level', 0)}, 延迟: {player.get('ping', 0)}ms"
            for player in players
        ])
    return generate_base_image(text, title="在线玩家列表")

async def generate_player_info_image(player: dict) -> bytes:
    """生成单个玩家信息的图片"""
    text = (
        f"玩家名称：{player.get('name', 'Unknown')}\n"
        f"等级：{player.get('level', 0)}\n"
        f"建筑数：{player.get('building_count', 0)}\n"
        f"坐标：({player.get('location_x', 0):.1f}, {player.get('location_y', 0):.1f})\n"
        f"延迟：{player.get('ping', 0)}ms"
    )
    return generate_base_image(text, title="玩家信息")

async def generate_shutdown_image(time: int, reason: str) -> bytes:
    """生成关服命令的图片"""
    text = (
        f"关服时间：{time}秒\n"
        f"关服原因：{reason}"
    )
    return generate_base_image(text, title="关服命令")

async def generate_kick_image(player_id: str, reason: str) -> bytes:
    """生成踢出玩家的图片"""
    text = (
        f"玩家ID：{player_id}\n"
        f"踢出原因：{reason}"
    )
    return generate_base_image(text, title="踢出玩家")

async def generate_ban_image(player_id: str, reason: str) -> bytes:
    """生成封禁玩家的图片"""
    text = (
        f"玩家ID：{player_id}\n"
        f"封禁原因：{reason}"
    )
    return generate_base_image(text, title="封禁玩家")

async def generate_unban_image(player_id: str) -> bytes:
    """生成解封玩家的图片"""
    text = f"玩家ID：{player_id}\n已成功解封"
    return generate_base_image(text, title="解封玩家")

async def generate_force_shutdown_image() -> bytes:
    """生成强制关服的图片"""
    text = "服务器已被强制关闭"
    return generate_base_image(text, title="强制关服")