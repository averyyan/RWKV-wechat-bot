# RWKV-wechat-bot

config 文件夹下要建一个config.json文件

、、、
{
    "server":{
        "host":"",
        "port":""
    },
    "wechat":{
        "app_id":""
        "token":""
    },
    "rwkv": {
        "model": "xx/rwkv-x060-eng_single_round_qa-1B6-20240430-ctx1024.pth" #模型地址
    }
}

、、、

将RWKV接入微信公众平台

实现了一个简单的对话功能，试用用了0.1B 可以在5秒内回复，如果是实际生产需要session的模式

测试了1.6B state turning后的模型，特别适合幽默聊天，token少的时候可以在5秒内回复

只实现了单轮对话
