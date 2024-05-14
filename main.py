from typing import Optional, Union
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse
import uvicorn
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from config.config import config
from wechatpy.crypto import WeChatCrypto
from wechatpy import parse_message, create_reply
from wechatpy.messages import TextMessage
from context.chat import context
from llm import llm

app = FastAPI()


@app.get("/")
def root(signature: Optional[str], timestamp: Optional[int], nonce: Optional[str], echostr: Optional[str], response: Response) -> str:
    try:
        check_signature(config.wechat.token, signature, timestamp, nonce)
    except InvalidSignatureException:
        response.status_code = status.HTTP_403_FORBIDDEN
        return
    return HTMLResponse(content=echostr)


@app.post("/")
async def msg(signature: Optional[str], timestamp: Optional[int], nonce: Optional[str], openid: Optional[str], request: Request):
    msg: TextMessage = parse_message(await request.body())
    if msg.type == "text":
        context.add_user(msg.content)
        print(context.prompt())
        llm.completions(context)
        content = create_reply(context.bot_last_msg(), msg).render()
        context.begin_flush()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content=create_reply("功能未支持", msg).render())


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.server.host,
        port=config.server.port,
    )
