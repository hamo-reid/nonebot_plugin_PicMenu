from nonebot.permission import SUPERUSER
from nonebot.plugin.on import on_command, on_startswith, on_regex
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.plugin import export
export = export()

import re
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))

from .menus import MenuManager
from .img_tool import img2b64


menu_manager = MenuManager()
menu_info_path = Path(__file__).parent / 'menu.json'
menu_manager.load_from_json(menu_info_path)
menu = on_startswith(('菜单', '/菜单'))

@menu.handle()
async def _(event: Event):
    msg = str(event.get_message())
    if match_result := re.match(r'^菜单 (.*?) (.*?)$|^/菜单 (.*?) (.*?)$', msg):
        result = [x for x in match_result.groups() if x is not None]
        plugin_name = result[0]
        cmd = result[1]
        temp = menu_manager.generate_command_details_image(plugin_name, cmd)
        if isinstance(temp, str):
            if temp == 'PluginIndexOutRange':
                await menu.finish(MessageSegment.text('插件序号不存在'))
            elif temp == 'CannotMatchPlugin':
                await menu.finish(MessageSegment.text('插件名过于模糊或不存在'))
            elif temp == 'CommandIndexOutRange':
                await menu.finish(MessageSegment.text('命令序号不存在'))
            else:
                await menu.finish(MessageSegment.text('命令过于模糊或不存在'))
        else:
            await menu.finish(MessageSegment.image('base64://' + img2b64(temp)))
    elif match_result := re.match(r'^菜单 (.*)$|^/菜单 (.*)$', msg):
        result = [x for x in match_result.groups() if x is not None]
        plugin_name = result[0]
        temp = menu_manager.generate_plugin_menu_image(plugin_name)
        if isinstance(temp, str):
            if temp == 'PluginIndexOutRange':
                await menu.finish(MessageSegment.text('插件序号不存在'))
            else:
                await menu.finish(MessageSegment.text('插件名过于模糊或不存在'))
        else:
            await menu.finish(MessageSegment.image('base64://' + img2b64(temp)))
    else:
        img = menu_manager.generate_main_menu_image()
        await menu.finish(MessageSegment.image('base64://' + img2b64(img)))


reload = on_command('reload', permission=SUPERUSER)
@reload.handle()
async def _():
    success_list, failed_list = menu_manager.reload_from_json()
    if success_list:
        await reload.send(MessageSegment.text(','.join(success_list) + '菜单信息已成功重载'))
    if failed_list:
        await reload.send(MessageSegment.text('，'.join(failed_list) + '菜单信息重载失败，检查json是否有误'))
