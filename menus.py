# -*- coding:utf-8 -*-
# @Author   : Hamo
# @Email    : 190395489@qq.com
# @Time     : 2022/5/17 23:34
# @File     : menus.py
# @Faction  :
# @Version  :
# ===============程序开始===============
from PIL import Image
from fuzzywuzzy import process, fuzz
from nonebot import logger
import json
import importlib
from pathlib import Path
from typing import Union


class DataManager(object):
    def __init__(self):
        self.dict_container = {}  # 存放menu数据的字典
        self.reload_list = []  # 存放热重载json路径的字典

    def load_dict(self, menu_dict: dict, template: str = 'default'):
        if 'template' not in menu_dict.keys():
            menu_dict.update({'template': template})
        else:
            if template != 'default':
                menu_dict['template'] = template
            else:
                pass
        self.dict_container.update({menu_dict['name']: menu_dict})

    def load_from_code(self, menu_dict: dict, template: str):
        """
        用于从代码直接加载插件的菜单信息的方法
        :param menu_dict: 菜单信息的dict
        :param template: 该插件使用的模板，默认为默认模板
        :return: None
        """
        if self.verify_menu_dict(menu_dict):  # 验证dict，验证通过则加载，不通过只输出log
            self.load_dict(menu_dict, template)
            logger.opt(colors=True).success(f'<y>{menu_dict["name"]}</y> 从代码加载插件菜单信息成功')
            return True
        else:
            logger.opt(colors=True).error(f'<y>{menu_dict["name"]}</y> 从代码加载插件菜单信息失败，请检查dict是否有误')
            return False

    def load_from_json(self, json_path: Union[str, Path]):
        """
        用于从json文件加载插件的菜单信息的方法
        :param json_path: json文件绝对路径
        :return: None
        """
        with open(json_path, 'r', encoding='utf-8') as fp:  # 读取json文件
            menu_dict = json.loads(fp.read())
        if self.verify_menu_dict(menu_dict):  # 验证json文件，验证通过则加载，不通过只输出log
            self.load_dict(menu_dict)
            self.reload_list.append(json_path)
            logger.opt(colors=True).success(f'<y>{menu_dict["name"]}</y> 从json文件加载菜单插件信息成功')
            return True
        else:
            logger.opt(colors=True).error(f'<y>{menu_dict["name"]}</y> 从json文件加载菜单插件信息失败，请检查json是否有误')
            return False

    def reload_from_json(self):
        reload_dict = self.reload_list
        success_list, failed_list = [], []
        for path in reload_dict:
            with open(path, 'r', encoding='utf-8') as fp:  # 读取json文件
                menu_dict = json.loads(fp.read())
            if menu_dict == self.dict_container[menu_dict['name']]: # 若json文件没有修改，则跳过
                continue
            if self.verify_menu_dict(menu_dict):    # 验证json结构
                del self.dict_container[menu_dict['name']]
                self.load_dict(menu_dict)
                success_list.append(menu_dict['name'])
            else:
                failed_list.append(menu_dict['name'])
            if success_list:
                logger.opt(colors=True).success(f'<y>{" ".join(success_list)}</y> 菜单信息重载成功')
            if not success_list:
                logger.opt(colors=True).success(f'<y>{" ".join(success_list)}</y> 菜单信息重载失败，检查json是否有误')
        return success_list

    def verify_menu_dict(self, menu_dict: dict):
        """
        验证传入的dict格式是否正确
        :param menu_dict: 需要验证的的dict
        :return: bool
        """
        if set(menu_dict.keys()) >= {'name', 'description', 'cmds'}:  # 验证key
            for cmd in menu_dict['cmds']:
                if set(cmd.keys()) >= {'cmd', 'type', 'brief_description', 'detail_description'}:
                    pass
                else:
                    return False
                return True
        else:
            return False

    def get_main_menu_data(self):
        """
        获取生成主菜单的信息
        :return:
        """
        main_menu_data = (list(self.dict_container.keys()),
                          [self.dict_container[name]['description'] for name in self.dict_container.keys()])
        return main_menu_data

    def get_plugin_menu_data(self, plugin_name: str):
        """
        获取生成插件菜单的数据
        :param plugin_name: 插件名
        :return:
        """
        if plugin_name.isdigit():  # 判断是否为下标，是则进行下标索引，否则进行模糊匹配
            index = int(plugin_name) - 1
            if index in range(len(self.dict_container)):
                plugin_name = list(self.dict_container.keys())[index]
                return {plugin_name: self.dict_container[plugin_name]['cmds']}, self.dict_container[plugin_name][
                    'template']
            else:  # 超限处理
                return 'PluginIndexOutRange'
        else:  # 模糊匹配
            result = self.fuzzy_match_and_check(plugin_name, list(self.dict_container.keys()))
            if result is not None:
                return {result: self.dict_container[result]['cmds']}, self.dict_container[result]['template']
            else:
                return 'CannotMatchPlugin'

    def get_command_details_data(self, plugin_name: str, cmd: str):
        """
        获取生成命令详细菜单的数据
        :param plugin_name: 插件名
        :param cmd: 命令
        :return:
        """
        data = self.get_plugin_menu_data(plugin_name)
        if isinstance(data, str):
            return data
        else:
            plugin_name = list(self.get_plugin_menu_data(plugin_name)[0].keys())[0]
            cmds = list(self.get_plugin_menu_data(plugin_name)[0].values())[0]
            if cmd.isdigit():  # 判断是否为下标，是则进行下标索引，否则进行模糊匹配
                index = int(cmd) - 1
                if index in range(len(cmds)):
                    cmd = cmds[index]
                    return (cmd['cmd'], cmd['type'], cmd['detail_description']), \
                           self.dict_container[plugin_name]['template']
                else:  # 超限处理
                    return 'CommandIndexOutRange'
            else:
                cmd_list = [cmd_data['cmd'] for cmd_data in cmds]
                fuzzy_cmd = self.fuzzy_match_and_check(cmd, cmd_list)  # 模糊匹配
                if fuzzy_cmd is not None:
                    for cmd_data in cmds:
                        if fuzzy_cmd == cmd_data['cmd']:
                            return (cmd_data['cmd'], cmd_data['type'], cmd_data['detail_description']), \
                                   self.dict_container[plugin_name]['template']
                else:  # 过于模糊
                    return 'CannotMatchCommand'

    def fuzzy_match_and_check(self, item, match_list: list):
        """
        模糊匹配函数
        :param item: 待匹配数据
        :param match_list: 全部数据的列表
        :return: 最合适匹配结果
        """
        if item in match_list:  # 在列表中直接return
            return item
        else:
            vague_result = [x[0] for x in process.extract(item, match_list, scorer=fuzz.partial_ratio, limit=20)]
            vague_result = [x[0] for x in process.extract(item, vague_result, scorer=fuzz.WRatio, limit=20)]
            result = list(process.extract(item, vague_result, scorer=fuzz.ratio, limit=1))[0]
            if result[1] < 45:
                return None
            else:
                return result[0]


class TemplateManager(object):
    def __init__(self):
        self.template_container = {}  # 模板装载对象
        self.templates_path = Path(__file__).parent / 'asserts/templates'  # 模板路径
        self.load_templates()
        self.default_template = self.select_template('default')

    def load_templates(self):  # 从文件加载模板
        template_list = [template for template in self.templates_path.glob('*.py')]
        template_name_list = [template.stem for template in self.templates_path.glob('*.py')]
        for template_name, template_path in zip(template_name_list, template_list):
            template_spec = importlib.util.spec_from_file_location(template_name, template_path)
            template = importlib.util.module_from_spec(template_spec)
            template_spec.loader.exec_module(template)
            self.template_container.update({template_name: template.Template})

    def select_template(self, template_name: str):  # 选择模板
        if template_name in self.template_container:
            return self.template_container[template_name]
        else:
            raise KeyError(f'There is no template named {template_name}')


class Template(object):  # 模板类
    def __init__(self):
        pass

    def generate_main_menu(self):
        pass

    def generate_plugin_menu(self):
        pass

    def generate_command_details(self):
        pass


class MenuManager(object):  # 菜单总管理
    def __init__(self):
        self.data_manager = DataManager()
        self.template_manager = TemplateManager()

    def load_from_code(self, menu_dict: dict, template: str = 'default'):
        """
        用于从代码直接加载插件的菜单信息的方法
        :param menu_dict: 菜单信息的dict
        :param template: 该插件使用的模板，默认为默认模板
        :return: None
        """
        self.data_manager.load_from_code(menu_dict, template)

    def load_from_json(self, json_path: Union[str, Path]):
        """
        用于从json文件加载插件的菜单信息的方法
        :param json_path: json文件绝对路径
        :param template: 该插件菜单使用的模板，默认为默认模板
        :return: None
        """
        return self.data_manager.load_from_json(json_path)

    def generate_main_menu_image(self) -> Image:
        data = self.data_manager.get_main_menu_data()
        img = self.template_manager.default_template().generate_main_menu(data)
        return img

    def generate_plugin_menu_image(self, plugin_name) -> Image:
        init_data = self.data_manager.get_plugin_menu_data(plugin_name)
        if isinstance(init_data, str):
            return init_data
        else:
            data = init_data[0]
            template = self.template_manager.select_template(init_data[1])()
            img = template.generate_plugin_menu(data)
            return img

    def generate_command_details_image(self, plugin_name, cmd) -> Image:
        init_data = self.data_manager.get_command_details_data(plugin_name, cmd)
        if isinstance(init_data, str):
            return init_data
        else:
            data = init_data[0]
            template = self.template_manager.select_template(init_data[1])()
            img = template.generate_command_details(data)
            return img

    def reload_from_json(self):  # json菜单数据重载
        return self.data_manager.reload_from_json()
