from context.chat import context
from llm import llm
context.add_user("今天天气怎么样")
llm.completions(context)
print(context.bot_last_msg())

