import json
import os

from pydantic import BaseModel, Field
from functools import lru_cache


class ServerConfig(BaseModel):
    host: str = Field(default="0.0.0.0", description="服务器IP")
    port: int = Field(default=8080, description="服务器端口")


class WechatConfig(BaseModel):
    app_id: str = Field(description="公众平台app_id配置")
    token: str = Field(description="公众平台token配置")

class RWKVConfig(BaseModel):
    model: str = Field(description="模型地址")
    strategy: str = Field(default="cuda fp16", description="模型运行模式")
    verbose: bool = Field(default=False, description="是否输出调试信息")


class AppConfig(BaseModel):
    server: ServerConfig = Field(default=None, description="服务器配置")
    wechat: WechatConfig = Field(default=None, description="微信公众平台配置")
    rwkv: RWKVConfig = Field(default=None, description="RWKV模型配置")


@lru_cache
def load_config() -> AppConfig:
    # 获取当前文件所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接配置文件的完整路径
    config_path = os.path.join(current_dir, "config.json")
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    return AppConfig(**config)


config = load_config()
