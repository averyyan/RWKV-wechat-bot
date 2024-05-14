# 聊天上下文


from functools import lru_cache
from pydantic import BaseModel, Field, field_validator, root_validator, validator


class ChatContext(BaseModel):
    user: str = Field(default="User")
    bot: str = Field(default="Assistant")
    pre_data: list = Field(default=None)
    data: list = Field(default=[])
    can_flush: bool = Field(
        default=False,
        description="判断是否接受大模型输出，在判断存在停止词后停止接收和输出"
    )
    stop: list = Field(default=[
        "\n\n",
        "\n\nUser",
        "\n\nQuestion",
        "\n\nQ",
        "\n\nHuman",
        "\n\nBob",
        "\n\nAssistant",
        "\n\nAnswer",
        "\n\nA",
        "\n\nBot",
        "\n\nAlice",
    ])

    def __init__(self, **data):
        super().__init__(**data)
        user = self.model_fields.get("user").default
        bot = self.model_fields.get("bot").default
        self.pre_data = [
            user+": 你好",
            bot+": 我是AI助理,请问有什么可以帮您",
        ]

    # 转化成模型接收的prompt
    def prompt(self) -> str:
        return "\n\n".join(self.pre_data+self.data)

    # 添加用户输入
    def add_user(self, msg: str):
        self.data.append(self.user+": "+msg)

    # 添加助手输入注意起始部分没有空格
    def add_assistant(self, msg: str):
        self.data.append(self.bot+":"+msg)

    # 开始接收模型输出
    def begin_flush(self):
        self.add_assistant("")
        self.can_flush = True

    # 停止接收模型输出
    def end_flush(self):
        self.can_flush = False
        # TODO 单轮对话
        self.clear_data()

    # 接收模型输出
    def flush_assistant(self, msg: str):
        if self.can_flush is True:
            last_msg = self.data.pop()
            last_msg += msg
            for stop in self.stop:
                if stop in last_msg:
                    self.end_flush()
                    self.data.append(last_msg.split(stop)[0])
                    return
            self.data.append(last_msg)

    # 单轮对话清理数据
    def clear_data(self):
        self.data = []

    # 获取最近的bot回复，用于公众平台等信息回复
    def bot_last_msg(self):
        msg = self.data.pop()
        return msg.split(self.bot+": ")[1]


@lru_cache
def load_context() -> ChatContext:
    return ChatContext()


context = load_context()
