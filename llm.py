# 模型部分

from functools import lru_cache
from rwkv_pip_package.src.rwkv.model import RWKV
from rwkv_pip_package.src.rwkv.utils import PIPELINE, PIPELINE_ARGS
from config.config import config
from pydantic import BaseModel, Field
from typing import Any
from context.chat import context, ChatContext


model: RWKV = RWKV(
    model=config.rwkv.model,
    strategy=config.rwkv.strategy,
    verbose=config.rwkv.verbose,
)

pipeline: PIPELINE = PIPELINE(model, "rwkv_vocab_v20230424")

args = PIPELINE_ARGS(
    temperature=1.0,  # 用于调整随机从生成模型中抽样的程度 越大随机性越高
    top_p=0.8,  # 较低的`top_p`值（如0.8）使生成的文本更加可预测和相关，而较高的值增加了文本的多样性和创造性。
    top_k=100,  # 较小的`k`值可以提高文本的相关性和连贯性，而较大的`k`值则增加了文本的多样性
    alpha_frequency=0.25,  # 重复度惩罚因子减少重复生成的字
    alpha_presence=0.35,  # 主题的重复度 控制围绕主题程度，越大越可能谈论新主题。
    alpha_decay=0.996,  # gradually decay the penalty 逐渐减轻处罚
    token_ban=[0],  # ban the generation of some tokens 禁止某些token生成
    # stop generation whenever you see any token here 结束符，模型生成结束符则停止生成
    token_stop=[261],
    chunk_len=256  # 分割节省内存
)


class LLM(BaseModel):
    model: Any = Field(default=None)
    pipeline: Any = Field(default=None)
    args: Any = Field(default=None)

    # TODO ctx这里应该是抽象
    def completions(self, ctx: ChatContext) -> str:
        ctx.begin_flush()
        self.pipeline.generate(
            ctx.prompt(),
            token_count=500,
            args=args,
            callback=ctx.flush_assistant,
        )


@lru_cache
def load_llm():
    return LLM(
        model=model,
        pipeline=pipeline,
        args=args
    )


llm = load_llm()
