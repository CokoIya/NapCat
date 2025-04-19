from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonNormalMessageReceived, GroupNormalMessageReceived
import json, os

@register(
    name="Akarin",
    description="赤座灯里角色扮演插件",
    version="0.1",
    author="Akarin9"
)
class AkarinPlugin(BasePlugin):
    def __init__(self, host: APIHost):
        super().__init__(host)
        # 加载本地 prompts/akarin.json
        p = os.path.join(os.path.dirname(__file__), "prompts", "akarin.json")
        with open(p, "r", encoding="utf-8") as f:
            self.base_prompt = json.load(f)["prompt"]

    async def initialize(self):
        # 初始化钩子（可选）
        pass

    @handler(PersonNormalMessageReceived)
    async def on_private_message(self, ctx: EventContext):
        # 私聊直接对话
        user_msg = ctx.event.text_message
        messages = self.base_prompt + [{"role": "user", "content": user_msg}]
        res = await llm_func("chat.completions", messages=messages)
        reply = res["choices"][0]["message"]["content"]
        ctx.add_return("reply", [reply])
        ctx.prevent_default()

    @handler(GroupNormalMessageReceived)
    async def on_group_message(self, ctx: EventContext):
        # 群聊需 @ 机器人才能触发
        if not ctx.event.is_mentioned:
            return
        user_msg = ctx.event.text_message
        messages = self.base_prompt + [{"role": "user", "content": user_msg}]
        res = await llm_func("chat.completions", messages=messages)
        reply = res["choices"][0]["message"]["content"]
        ctx.add_return("reply", [reply])
        ctx.prevent_default()
