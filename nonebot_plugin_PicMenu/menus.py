# -*- coding:utf-8 -*-
# @Author   : Hamo
# @Email    : 190395489@qq.com
# @Time     : 2022/5/17 23:34
# @File     : menus.py
# @Faction  :
# @Version  :
# ===============程序开始===============
from PIL import Image
from dataclasses import dataclass
from fuzzywuzzy import process, fuzz
import nonebot.plugin
import importlib
import abc
import json
from pathlib import Path
from typing import Union, Dict, Optional, List, Tuple

from .img_tool import *

# 功能的数据信息
@dataclass
class FuncData:
    func: str
    trigger_method: str
    trigger_condition: str
    brief_des: str
    detail_des: str

# 插件菜单的数据信息
@dataclass
class PluginMenuData:
    name: str
    description: str
    usage: str
    funcs: List[FuncData]
    template: str

class PicTemplate(object):  # 模板类
    def __init__(self):
        pass

    @abc.abstractmethod
    def load_resource(self):
        pass

    @abc.abstractmethod
    def generate_main_menu(self, data: Tuple[List, List]) -> Image:
        pass

    @abc.abstractmethod
    def generate_plugin_menu(self, plugin_data: PluginMenuData) -> Image:
        pass

    @abc.abstractmethod
    def generate_command_details(self, func_data: FuncData) -> Image:
        pass

class Template(PicTemplate):
    def __init__(self):
        super().__init__()
        self.name = 'default'
        self.load_resource()
        self.colors = {
            'blue': (34, 52, 73),
            'yellow': (224, 164, 25),
            'white': (237, 239, 241)
        }
        self.basic_font_size = 25

    def load_resource(self):
        cwd = Path.cwd()
        with (cwd / 'menu_config'/ 'config.json').open('r', encoding='utf-8') as fp:
            config = json.loads(fp.read())
        self.using_font = config['default']

    def generate_main_menu(self, data) -> Image:
        """
        生成主菜单
        :param data: 元组(列表， 列表)
        :return: Image对象
        """
        column_count = len(data) + 1
        row_count = len(data[0])
        # 数据尺寸测算
        row_size_list = []
        for x in range(row_count):
            index_size = calculate_text_size(str(x + 1), self.basic_font_size, self.using_font)
            plugin_name_size = calculate_text_size(data[0][x], self.basic_font_size, self.using_font)
            plugin_description_size = multi_text(data[1][x],
                                                 default_font=self.using_font,
                                                 default_size=25,
                                                 box_size=(300, 0)
                                                 ).size
            row_size_list.append((index_size, plugin_name_size, plugin_description_size))
        # 边距
        margin = 10
        row_height_list = [max(map(lambda i: i[1], row_size_list[x])) + margin * 2 for x in range(row_count)]
        col_max_width_tuple = (
            max((x[0][0] + margin * 2 for x in row_size_list)),
            max((x[1][0] + margin * 2 for x in row_size_list)),
            max((x[2][0] + margin * 2 for x in row_size_list))
        )
        table_width = sum(col_max_width_tuple) + 3
        table_height = sum(row_height_list) + 3
        table = ImageFactory(
            Image.new('RGBA', (table_width, table_height), self.colors['white'])
        )
        initial_point, basis_point = (1, 1), [1, 1]
        for row_id in range(row_count):
            for col_id in range(column_count):
                box_size = (col_max_width_tuple[col_id], row_height_list[row_id])
                table.add_box(f'box_{row_id}_{col_id}',
                              tuple(basis_point),
                              tuple(box_size))
                table.rectangle(f'box_{row_id}_{col_id}', outline=self.colors['blue'], width=2)
                basis_point[0] += box_size[0]
            basis_point[0] = initial_point[0]
            basis_point[1] += row_height_list[row_id]
        for x in range(row_count):
            id_text = simple_text(str(x + 1), self.basic_font_size, self.using_font, self.colors['blue'])
            table.img_paste(
                id_text,
                table.align_box(f'box_{x}_0', id_text, align='center'),
                isalpha=True
            )
            plugin_name_text = simple_text(data[0][x], self.basic_font_size, self.using_font, self.colors['blue'])
            table.img_paste(
                plugin_name_text,
                table.align_box(f'box_{x}_1', plugin_name_text, align='center'),
                isalpha=True
            )
            plugin_description_text = multi_text(data[1][x],
                                                 box_size=(300, 0),
                                                 default_font=self.using_font,
                                                 default_color=self.colors['blue'],
                                                 default_size=self.basic_font_size
                                                 )
            table.img_paste(
                plugin_description_text,
                table.align_box(f'box_{x}_2', plugin_description_text, align='center'),
                isalpha=True
            )
        table_size = table.img.size
        main_menu = ImageFactory(
            Image.new('RGBA', (table_size[0] + 140, table_size[1] + 190), color=self.colors['white'])
        )
        main_menu.img_paste(
            table.img,
            main_menu.align_box('self', table.img, pos=(0, 150), align='horizontal')
        )
        main_menu.add_box('border_box',
                          main_menu.align_box('self',
                                              (table_size[0] + 40, table_size[1] + 70),
                                              pos=(0, 100),
                                              align='horizontal'),
                          (table_size[0] + 40, table_size[1] + 70))
        main_menu.rectangle('border_box', outline=self.colors['blue'], width=5)
        border_box_top_left = main_menu.boxes['border_box'].topLeft
        main_menu.rectangle(Box((border_box_top_left[0] - 25, border_box_top_left[1] - 25),
                                (50, 50)), outline=self.colors['yellow'], width=5)
        main_menu.add_box('title_box', (0, 0), (main_menu.get_size()[0], 100))
        title = simple_text('插件菜单', 60, self.using_font, self.colors['blue'])
        main_menu.img_paste(title, main_menu.align_box('title_box', title, align='center'), isalpha=True)
        return main_menu.img

    def generate_plugin_menu(self, plugin_data: PluginMenuData) -> Image:
        """
        生成插件命令菜单
        :param plugin_data: PluginMenuData对象
        :return: Image对象
        """
        plugin_name = plugin_data.name
        data = plugin_data.funcs
        column_count = 5
        row_count = len(data)
        # 数据尺寸测算
        row_size_list = []
        for index, func_data in enumerate(data):
            index_size = calculate_text_size(str(index + 1), self.basic_font_size, self.using_font)
            func_size = calculate_text_size(func_data.func, self.basic_font_size, self.using_font)
            method_size = calculate_text_size(func_data.trigger_method, self.basic_font_size, self.using_font)
            condition_size = calculate_text_size(func_data.trigger_condition, self.basic_font_size, self.using_font)
            brief_des_size = multi_text(func_data.brief_des,
                                        default_font=self.using_font,
                                        default_size=25,
                                        box_size=(300, 0)
                                        ).size
            row_size_list.append((index_size, func_size, method_size, condition_size, brief_des_size))
        # 边距
        margin = 10
        # 测行高
        row_height_list = [max(map(lambda i: i[1], row_size_list[x])) + margin * 2 for x in range(row_count)]
        col_max_width_tuple = (
            max((x[0][0] + margin * 2 for x in row_size_list)),
            max((x[1][0] + margin * 2 for x in row_size_list)),
            max((x[2][0] + margin * 2 for x in row_size_list)),
            max((x[3][0] + margin * 2 for x in row_size_list)),
            max((x[4][0] + margin * 2 for x in row_size_list))
        )
        # 建立表格画板
        table_width = sum(col_max_width_tuple) + 3
        table_height = sum(row_height_list) + 3
        table = ImageFactory(
            Image.new('RGBA', (table_width, table_height), self.colors['white'])
        )
        initial_point, basis_point = (1, 1), [1, 1]
        # 建立基准box
        for row_id in range(row_count):
            for col_id in range(column_count):
                box_size = (col_max_width_tuple[col_id], row_height_list[row_id])
                table.add_box(f'box_{row_id}_{col_id}',
                              tuple(basis_point),
                              tuple(box_size))
                table.rectangle(f'box_{row_id}_{col_id}', outline=self.colors['blue'], width=2)
                basis_point[0] += box_size[0]
            basis_point[0] = initial_point[0]
            basis_point[1] += row_height_list[row_id]
        # 填字
        for index, func_data in enumerate(data):
            # 第一个cell填id
            id_text = simple_text(str(index + 1), self.basic_font_size, self.using_font, self.colors['blue'])
            table.img_paste(
                id_text,
                table.align_box(f'box_{index}_0', id_text, align='center'),
                isalpha=True
            )
            # 第二个cell里填func（功能）
            func_text = simple_text(func_data.func, self.basic_font_size, self.using_font, self.colors['blue'])
            table.img_paste(
                func_text,
                table.align_box(f'box_{index}_1', func_text, align='center'),
                isalpha=True
            )
            # 第三个cell里填trigger_method（触发方式）
            trigger_method_text = simple_text(func_data.trigger_method, self.basic_font_size, self.using_font,
                                              self.colors['blue'])
            table.img_paste(
                trigger_method_text,
                table.align_box(f'box_{index}_2', trigger_method_text, align='center'),
                isalpha=True
            )
            # 第四个cell里填trigger_condition（触发条件）
            trigger_condition_text = simple_text(func_data.trigger_condition, self.basic_font_size, self.using_font,
                                                 self.colors['blue'])
            table.img_paste(
                trigger_condition_text,
                table.align_box(f'box_{index}_3', trigger_condition_text, align='center'),
                isalpha=True
            )
            # 第五个cell里填brief_des（功能简述）
            brief_des_text = multi_text(func_data.brief_des,
                                        box_size=(300, 0),
                                        default_font=self.using_font,
                                        default_color=self.colors['blue'],
                                        default_size=self.basic_font_size
                                        )
            table.img_paste(
                brief_des_text,
                table.align_box(f'box_{index}_4', brief_des_text, align='center'),
                isalpha=True
            )
        # 获取table尺寸
        table_size = table.img.size
        # usage的文字描述
        usage_text = multi_text('用法：' + plugin_data.usage,
                                box_size=(table_size[0] - 30, 0),
                                default_font=self.using_font,
                                default_color=self.colors['blue'],
                                default_size=self.basic_font_size
                                )
        usage_text_size = usage_text.size
        # 底部画板，大小根据table大小和usage文字大小确定
        main_menu = ImageFactory(
            Image.new(
                'RGBA',
                (table_size[0] + 140,
                 table_size[1] + usage_text_size[1] + 210),
                color=self.colors['white']
            )
        )
        # 在底部画板上粘贴usage
        pos, _ = main_menu.img_paste(
            usage_text,
            main_menu.align_box('self', usage_text, pos=(0, 130), align='horizontal'),
            isalpha=True
        )
        # 在底部画板上粘贴表格
        main_menu.img_paste(
            table.img,
            main_menu.align_box('self', table.img, pos=(0, pos[1] + usage_text.size[1] + 20), align='horizontal')
        )
        # 给表格添加装饰性边框
        main_menu.add_box('border_box',
                          main_menu.align_box('self',
                                              (table_size[0] + 40, table_size[1] + 70),
                                              pos=(0, 100),
                                              align='horizontal'),
                          (table_size[0] + 40, table_size[1] + usage_text_size[1] + 70))
        main_menu.rectangle('border_box', outline=self.colors['blue'], width=5)
        border_box_top_left = main_menu.boxes['border_box'].topLeft
        main_menu.rectangle(Box((border_box_top_left[0] - 25, border_box_top_left[1] - 25),
                                (50, 50)), outline=self.colors['yellow'], width=5)
        main_menu.add_box('title_box', (0, 0), (main_menu.get_size()[0], 100))
        title = simple_text(plugin_name, 60, self.using_font, self.colors['blue'])
        main_menu.img_paste(title, main_menu.align_box('title_box', title, align='center'), isalpha=True)
        return main_menu.img

    def generate_command_details(self, func_data: FuncData) -> Image:
        """
        生成命令详细数据
        :param func_data: FuncData对象
        :return:
        """
        # 需要生成的列表
        string_list = [
            func_data.func,
            func_data.trigger_method,
            func_data.trigger_condition,
            func_data.detail_des
        ]
        # 获取标签文字
        basis_text_list = [simple_text(text, self.basic_font_size, self.using_font, self.colors['blue'])
                           for text in ['功能：', '触发方式：', '触发条件：', '详细描述：']]
        # 获取标签文字的大小
        basis_text_size_list = [x.size for x in basis_text_list]
        # 信息起始位置
        info_text_start_x = max([x[0] for x in basis_text_size_list])
        # 将文字转换为图片
        text_img_list = []
        for x in string_list:
            text_img_list.append(
                multi_text(x,
                           box_size=(680-info_text_start_x, 0),
                           default_font=self.using_font,
                           default_color=self.colors['blue'],
                           default_size=self.basic_font_size,
                           v_border_ignore=True
                           )
            )
        # 获取文字图片的大小
        text_size_list = [x.size for x in text_img_list]
        # 获取同一行最大高度
        line_max_height_list = [max(x) for x in
                                zip(map(lambda y: y[1], text_size_list), map(lambda y: y[1], basis_text_size_list))]
        # 文字画板，每行间距30
        text_img = ImageFactory(Image.new('RGBA',
                                          (680, sum(line_max_height_list) + 90),
                                          color=self.colors['white']))
        # - 添加func的box
        text_img.add_box('func_box', (0, 0), (680, max((basis_text_size_list[0][1], text_size_list[0][1]))))
        # 粘贴func标签
        pos, _ = text_img.img_paste(basis_text_list[0],
                                    text_img.align_box('func_box', basis_text_list[0]),
                                    isalpha=True)
        # 粘贴func图片
        text_img.img_paste(text_img_list[0],
                           text_img.align_box('func_box', text_img_list[0],
                                              pos=(info_text_start_x + 40, pos[1])),
                           isalpha=True)
        # - 添加trigger_method的box
        text_img.add_box('trigger_method_box', (0, text_img.boxes['func_box'].bottom + 30),
                         (680, max((basis_text_size_list[1][1], text_size_list[1][1]))))
        # 粘贴trigger_method标签
        pos, _ = text_img.img_paste(basis_text_list[1],
                                    text_img.align_box('trigger_method_box', basis_text_list[1]),
                                    isalpha=True)
        # 粘贴trigger_method图片
        text_img.img_paste(text_img_list[1],
                           text_img.align_box('trigger_method_box', text_img_list[1],
                                              pos=(info_text_start_x + 40, pos[1])),
                           isalpha=True)
        # - 添加trigger_condition的box
        text_img.add_box('trigger_condition_box', (0, text_img.boxes['trigger_method_box'].bottom + 30),
                         (680, max((basis_text_size_list[2][1], text_size_list[2][1]))))
        # 粘贴trigger_condition标签
        pos, _ = text_img.img_paste(basis_text_list[2],
                                    text_img.align_box('trigger_condition_box', basis_text_list[2]),
                                    isalpha=True)
        # 粘贴trigger_condition图片
        text_img.img_paste(text_img_list[2],
                           text_img.align_box('trigger_condition_box', text_img_list[2],
                                              pos=(info_text_start_x + 40, pos[1])),
                           isalpha=True)
        # - 添加detail_des的box
        text_img.add_box('detail_des_box', (0, text_img.boxes['trigger_condition_box'].bottom + 30),
                         (680, max((basis_text_size_list[3][1], text_size_list[3][1]))))
        # 粘贴detail_des标签
        pos, _ = text_img.img_paste(basis_text_list[3],
                                    text_img.align_box('detail_des_box', basis_text_list[3]),
                                    isalpha=True)
        # 粘贴detail_des图片
        text_img.img_paste(text_img_list[3],
                           text_img.align_box('detail_des_box', text_img_list[3],
                                              pos=(info_text_start_x + 40, pos[1])),
                           isalpha=True)
        text_img_size = text_img.img.size
        detail_img = ImageFactory(Image.new('RGBA', (800, text_img_size[1] + 180), color=self.colors['white']))
        detail_img.add_box('text_border_box', (20, 100), (760, text_img_size[1] + 60))
        detail_img.rectangle('text_border_box', outline=self.colors['blue'], width=1)
        detail_img.img_paste(text_img.img, detail_img.align_box('text_border_box', text_img.img, align='center'))
        detail_img.add_box('upper_box', (0, 0), (800, 100))
        detail_img.add_box('blue_box', detail_img.align_box('upper_box', (700, 20), align='center'), (700, 20))
        detail_img.rectangle('blue_box', outline=self.colors['blue'], width=5)
        detail_img.add_box('yellow_box',
                           (detail_img.boxes['blue_box'].left - 25, detail_img.boxes['blue_box'].top - 15), (50, 50))
        detail_img.rectangle('yellow_box', outline=self.colors['yellow'], width=5)
        return detail_img.img


class DataManager(object):
    def __init__(self):
        self.plugin_menu_data_list: List[PluginMenuData] = []  # 存放menu数据的列表
        self.plugin_names = []

    def load_plugin_info(self):
        # 取已经加载的插件信息
        for plugin in nonebot.plugin.get_loaded_plugins():
            meta_data = plugin.metadata
            # 判断有元信息
            if meta_data is None:
                continue
            if 'menu_data' in meta_data.extra:
                menu_data = meta_data.extra['menu_data']
                # 判断是否设置模板
                if 'menu_template' in meta_data.extra:
                    menu_template = meta_data.extra['menu_template']
                else:
                    menu_template = 'default'
            else:
                continue
            # 数据整合
            self.plugin_menu_data_list.append(
                PluginMenuData(
                    name=meta_data.name,
                    description=meta_data.description,
                    usage=meta_data.usage,
                    funcs=[
                        FuncData(
                            func=data['func'],
                            trigger_method=data['trigger_method'],
                            trigger_condition=data['trigger_condition'],
                            brief_des=data['brief_des'],
                            detail_des=data['detail_des'],
                        ) for data in menu_data
                    ],
                    template=menu_template
                )
            )
            self.plugin_names.append(meta_data.name)

    def get_main_menu_data(self) -> Tuple[List, List]:
        """
        获取生成主菜单的信息
        :return: 元组（列表[插件名]，列表[插件描述]）
        """
        descriptions = [
            menu_data.description for menu_data in self.plugin_menu_data_list
        ]
        return self.plugin_names, descriptions

    def get_plugin_menu_data(self, plugin_name: str) -> Union[PluginMenuData, str]:
        """
        获取生成插件菜单的数据
        :param plugin_name: 插件名
        :return:
        """
        if plugin_name.isdigit():  # 判断是否为下标，是则进行下标索引，否则进行模糊匹配
            index = int(plugin_name) - 1
            if 0 <= index < len(self.plugin_menu_data_list):
                return self.plugin_menu_data_list[index]
            else:  # 超限处理
                return 'PluginIndexOutRange'
        else:  # 模糊匹配
            result = self.fuzzy_match_and_check(plugin_name, self.plugin_names)
            if result is not None:
                for plugin_data in self.plugin_menu_data_list:
                    if result == plugin_data.name:
                        return plugin_data
            else:
                return 'CannotMatchPlugin'

    def get_command_details_data(self, plugin_data: PluginMenuData, func: str):
        """
        获取生成命令详细菜单的数据
        :param plugin_data: 插件名（从聊天中直接获得的初始数据）
        :param func: 命令（从聊天中直接获得的初始数据）
        :return:
        """
        funcs = plugin_data.funcs
        if func.isdigit():  # 判断是否为下标，是则进行下标索引，否则进行模糊匹配
            index = int(func) - 1
            if 0 <= index < len(funcs):
                func = funcs[index]
                return func
            else:  # 超限处理
                return 'CommandIndexOutRange'
        else:
            func_list = [func.func for func in funcs]  # 功能名的列表
            fuzzy_func = self.fuzzy_match_and_check(func, func_list)  # 模糊匹配
            if fuzzy_func is not None:
                for func_data in funcs:
                    if fuzzy_func == func_data.func:
                        return func_data
            else:  # 过于模糊
                return 'CannotMatchCommand'

    def fuzzy_match_and_check(self, item: str, match_list: List[str]) -> Union[None, str]:
        """
        模糊匹配函数
        :param item: 待匹配数据
        :param match_list: 全部数据的列表
        :return: 最合适匹配结果
        """
        if item in match_list:  # 在列表中直接返回结果
            return item
        else:
            vague_result = [x[0] for x in process.extract(item, match_list, scorer=fuzz.partial_ratio, limit=10)]
            vague_result = [x[0] for x in process.extract(item, vague_result, scorer=fuzz.WRatio, limit=10)]
            result = list(process.extract(item, vague_result, scorer=fuzz.ratio, limit=1))[0]
            if result[1] < 45:  # 置信度过小返回空值
                return None
            else:
                return result[0]


class TemplateManager(object):
    def __init__(self):
        self.template_container = {'default': Template}  # 模板装载对象
        self.templates_path = Path.cwd() / 'menu_config' / 'template'  # 模板路径
        self.load_templates()

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


class MenuManager(object):  # 菜单总管理
    def __init__(self):
        self.cwd = Path.cwd()
        self.config_folder_make()
        self.data_manager = DataManager()
        self.template_manager = TemplateManager()

    def load_plugin_info(self):
        self.data_manager.load_plugin_info()

    # 初始化文件结构
    def config_folder_make(self):
        if not (self.cwd / 'menu_config').exists():
            (self.cwd / 'menu_config').mkdir()
        if not (self.cwd / 'menu_config' / 'fonts').exists():
            (self.cwd / 'menu_config' / 'fonts').mkdir()
        if not (self.cwd / 'menu_config' / 'templates').exists():
            (self.cwd / 'menu_config' / 'templates').mkdir()
        if not (self.cwd / 'menu_config' / 'config.json').exists():
            with (self.cwd / 'menu_config' / 'config.json').open('w', encoding='utf-8') as fp:
                fp.write(json.dumps({'default': 'font_path'}))

    def generate_main_menu_image(self) -> Image:  # 生成主菜单图片
        data = self.data_manager.get_main_menu_data()
        template = self.template_manager.select_template('default')
        img = template().generate_main_menu(data)
        return img

    def generate_plugin_menu_image(self, plugin_name) -> Image:  # 生成二级菜单图片
        init_data = self.data_manager.get_plugin_menu_data(plugin_name)
        if isinstance(init_data, str):  # 判断是否匹配到插件
            return init_data
        else:
            data = init_data
            template = self.template_manager.select_template(data.template)  # 获取模板
            img = template().generate_plugin_menu(data)
            return img

    def generate_command_details_image(self, plugin_name, func) -> Image:  # 生成三级菜单图片
        plugin_data = self.data_manager.get_plugin_menu_data(plugin_name)
        if isinstance(plugin_data, str):  # 判断是否匹配到插件
            return plugin_data
        else:
            init_data = self.data_manager.get_command_details_data(plugin_data, func)
        if isinstance(init_data, str):  # 判断是否匹配到功能
            return init_data
        else:
            data = init_data
            template = self.template_manager.select_template(plugin_data.template)  # 获取模板
            img = template().generate_command_details(data)
            return img
