import re

from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Event
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN
from nonebot.matcher import Matcher
from nonebot.params import Depends
from nonebot.permission import SUPERUSER
from nonebot.plugin.on import on_fullmatch, on_startswith

from .img_tool import img2b64
from .manager import MenuManager
from .metadata import __plugin_meta__ as __plugin_meta__

driver = get_driver()


@driver.on_bot_connect
async def _():
    if not menu_manager.data_manager.plugin_menu_data_list:
        menu_manager.load_plugin_info()


menu_manager = MenuManager()
menu = on_startswith("菜单", priority=5)
switch = on_fullmatch("开关菜单", permission=SUPERUSER | GROUP_ADMIN, priority=5)


menu_switch = True


@switch.handle()
async def _():
    global menu_switch
    menu_switch = not menu_switch
    if menu_switch:
        await switch.finish(MessageSegment.text("菜单已开启"))
    else:
        await switch.finish(MessageSegment.text("菜单已关闭"))


async def check_switch(matcher: Matcher):
    if not menu_switch:
        matcher.skip()


@menu.handle()
async def _(event: Event, check=Depends(check_switch)):
    msg = event.get_plaintext()
    cmd_prefix_re = "|".join([x for x in driver.config.command_start if x])
    prefix_re = f"({cmd_prefix_re})?(菜单|功能|帮助) ?"

    if match_result := re.match(rf"^{prefix_re}(?P<name>.*?) (?P<cmd>.*?)$", msg):
        plugin_name = match_result.group("name").strip()
        cmd = match_result.group("cmd").strip()
        temp = menu_manager.generate_func_details_image(plugin_name, cmd)
        if isinstance(temp, str):
            if temp == "PluginIndexOutRange":
                await menu.finish(MessageSegment.text("插件序号不存在"))
            elif temp == "CannotMatchPlugin":
                await menu.finish(MessageSegment.text("插件名过于模糊或不存在"))
            elif temp == "PluginNoFuncData":
                await menu.finish(MessageSegment.text("该插件无功能数据"))
            elif temp == "CommandIndexOutRange":
                await menu.finish(MessageSegment.text("命令序号不存在"))
            else:
                await menu.finish(MessageSegment.text("命令过于模糊或不存在"))
        else:
            await menu.finish(MessageSegment.image("base64://" + img2b64(temp)))

    elif match_result := re.match(rf"^{prefix_re}(?P<name>.*)$", msg):
        plugin_name = match_result.group("name").strip()
        temp = menu_manager.generate_plugin_menu_image(plugin_name)
        if isinstance(temp, str):
            if temp == "PluginIndexOutRange":
                await menu.finish(MessageSegment.text("插件序号不存在"))
            else:
                await menu.finish(MessageSegment.text("插件名过于模糊或不存在"))
        else:
            await menu.finish(MessageSegment.image("base64://" + img2b64(temp)))

    else:
        img = menu_manager.generate_main_menu_image()
        await menu.finish(MessageSegment.image("base64://" + img2b64(img)))
