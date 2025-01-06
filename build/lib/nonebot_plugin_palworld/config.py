__author__ = "HuanXin"
import nonebot
from pydantic import BaseModel
from nonebot import get_plugin_config


class Config(BaseModel):
    palworld_host_port: str = None
    palworld_token:str = None

global_config = nonebot.get_driver().config
hx_config = get_plugin_config(Config)