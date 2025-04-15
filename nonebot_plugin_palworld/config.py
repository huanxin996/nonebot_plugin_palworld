__author__ = "HuanXin"
import re,nonebot
from typing import Optional,Union
from nonebot.compat import PYDANTIC_V2
from pydantic import BaseModel, Field
from nonebot.log import logger
from nonebot.plugin import get_plugin_config


if PYDANTIC_V2:
    from pydantic import field_validator
else:
    from pydantic import validator as field_validator


class PalworldConfigError(Exception):
    """帕鲁配置相关异常"""
    pass

class Config(BaseModel):
    palworld_host_port: Optional[Union[str, int]] = Field(
        default="127.0.0.1:8211",
        description="幻兽帕鲁服务器地址和端口(格式: host:port)"
    )
    pallworld_user: Optional[Union[str, int]] = Field(
        default="Admin",
        description="幻兽帕鲁服务器用户名"
    )
    palworld_token: Optional[Union[str, int]] = Field(
        default="your_token_here",
        description="幻兽帕鲁服务器访问令牌(字符串格式)"
    )
    palworld_images_send: Optional[bool] = Field(
        default=True,
        description="是否发送图片"
    )

    @field_validator('palworld_host_port')
    @classmethod
    def validate_host_port(cls, v: Optional[Union[str, int]]) -> Optional[str]:
        if v is None:
            return v
        if isinstance(v, int):
            v = str(v)
        if not isinstance(v, str):
            raise ValueError("服务器地址必须是字符串格式或整数")
        pattern = r'^[\w.-]+:\d+$'
        if not re.match(pattern, v):
            raise ValueError("服务器地址格式错误，应为 host:port")
        return v

global_config = nonebot.get_driver().config
hx_config = get_plugin_config(Config)