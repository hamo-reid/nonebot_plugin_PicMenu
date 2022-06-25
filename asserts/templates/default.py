from PIL import Image
from img_tool import *


class Template(object):
    def __init__(self):
        self.colors = {
            'blue': (34, 52, 73),
            'yellow': (224, 164, 25),
            'white': (237, 239, 241)
        }
        self.basic_font_size = 25
        self.using_font = './assets/fonts/苹方黑体-准-简.ttf'

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

    def generate_plugin_menu(self, cmd_data) -> Image:
        """
        生成插件命令菜单
        :param cmd_data: 字典{str(插件名): 列表[dict{cmd, type, brief_description}]}
        :return: Image对象
        """
        plugin_name = tuple(cmd_data.keys())[0]
        data = cmd_data[plugin_name]
        column_count = len(data[0])
        row_count = len(data)
        # 数据尺寸测算
        row_size_list = []
        for x in range(row_count):
            index_size = calculate_text_size(str(x + 1), self.basic_font_size, self.using_font)
            cmd_size = calculate_text_size(data[x]['cmd'], self.basic_font_size, self.using_font)
            type_size = calculate_text_size(data[x]['type'], self.basic_font_size, self.using_font)
            brief_description_size = multi_text(data[x]['brief_description'],
                                                default_font=self.using_font,
                                                default_size=25,
                                                box_size=(300, 0)
                                                ).size
            row_size_list.append((index_size, cmd_size, type_size, brief_description_size))
        # 边距
        margin = 10
        row_height_list = [max(map(lambda i: i[1], row_size_list[x])) + margin * 2 for x in range(row_count)]
        col_max_width_tuple = (
            max((x[0][0] + margin * 2 for x in row_size_list)),
            max((x[1][0] + margin * 2 for x in row_size_list)),
            max((x[2][0] + margin * 2 for x in row_size_list)),
            max((x[3][0] + margin * 2 for x in row_size_list))
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
        # 填字
        for x in range(row_count):
            id_text = simple_text(str(x + 1), self.basic_font_size, self.using_font, self.colors['blue'])
            table.img_paste(
                id_text,
                table.align_box(f'box_{x}_0', id_text, align='center'),
                isalpha=True
            )
            cmd_text = simple_text(data[x]['cmd'], self.basic_font_size, self.using_font, self.colors['blue'])
            table.img_paste(
                cmd_text,
                table.align_box(f'box_{x}_1', cmd_text, align='center'),
                isalpha=True
            )
            type_text = simple_text(data[x]['type'], self.basic_font_size, self.using_font, self.colors['blue'])
            table.img_paste(
                type_text,
                table.align_box(f'box_{x}_2', type_text, align='center'),
                isalpha=True
            )
            brief_description_text = multi_text(data[x]['brief_description'],
                                                box_size=(300, 0),
                                                default_font=self.using_font,
                                                default_color=self.colors['blue'],
                                                default_size=self.basic_font_size
                                                )
            table.img_paste(
                brief_description_text,
                table.align_box(f'box_{x}_3', brief_description_text, align='center'),
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
        title = simple_text(plugin_name, 60, self.using_font, self.colors['blue'])
        main_menu.img_paste(title, main_menu.align_box('title_box', title, align='center'), isalpha=True)
        return main_menu.img

    def generate_command_details(self, data) -> Image:
        """
        生成命令详细数据
        :param data:
        :return:
        """
        text_img_list = []
        for x in data:
            text_img_list.append(
                multi_text(x,
                           box_size=(550, 0),
                           default_font=self.using_font,
                           default_color=self.colors['blue'],
                           default_size=self.basic_font_size,
                           v_border_ignore=True
                           )
            )
        text_size_list = [x.size for x in text_img_list]
        basis_text_list = [simple_text(text, self.basic_font_size, self.using_font, self.colors['blue'])
                           for text in ['命令：', '类型：', '描述：']]
        basis_text_size_list = [x.size for x in basis_text_list]
        line_max_height_list = [max(x) for x in zip(map(lambda y: y[1], text_size_list), map(lambda y: y[1], basis_text_size_list))]
        text_img = ImageFactory(Image.new('RGBA',
                                          (680, sum(line_max_height_list) + 60),
                                          color=self.colors['white']))
        text_img.add_box('cmd_box', (0, 0), (680, max((basis_text_size_list[0][1], text_size_list[0][1]))))
        pos = text_img.img_paste(basis_text_list[0],
                           text_img.align_box('cmd_box', basis_text_list[0]),
                           isalpha=True)[0]
        text_img.img_paste(text_img_list[0],
                           text_img.align_box('cmd_box', text_img_list[0],
                                              pos=(basis_text_list[0].size[0]+55, pos[1])),
                           isalpha=True)
        text_img.add_box('type_box', (0, text_img.boxes['cmd_box'].bottom + 30),
                         (680, max((basis_text_size_list[1][1], text_size_list[1][1]))))
        pos = text_img.img_paste(basis_text_list[1],
                           text_img.align_box('type_box', basis_text_list[1]),
                           isalpha=True)[0]
        text_img.img_paste(text_img_list[1],
                           text_img.align_box('type_box', text_img_list[1],
                                              pos=(basis_text_list[1].size[0] + 55, pos[1])),
                           isalpha=True)
        text_img.add_box('detail_box', (0, text_img.boxes['type_box'].bottom + 30),
                         (680, max((basis_text_size_list[2][1], text_size_list[2][1]))))
        pos = text_img.img_paste(basis_text_list[2],
                           text_img.align_box('detail_box', basis_text_list[2]),
                           isalpha=True)[0]
        text_img.img_paste(text_img_list[2],
                           text_img.align_box('detail_box', text_img_list[2],
                                              pos=(basis_text_list[2].size[0] + 55, pos[1])),
                           isalpha=True)
        text_img_size = text_img.img.size
        detail_img = ImageFactory(Image.new('RGBA', (800, text_img_size[1]+180), color=self.colors['white']))
        detail_img.add_box('text_border_box', (20, 100), (760, text_img_size[1]+60))
        detail_img.rectangle('text_border_box', outline=self.colors['blue'], width=1)
        detail_img.img_paste(text_img.img, detail_img.align_box('text_border_box', text_img.img, align='center'))
        detail_img.add_box('upper_box', (0, 0), (800, 100))
        detail_img.add_box('blue_box', detail_img.align_box('upper_box', (700, 20), align='center'), (700, 20))
        detail_img.rectangle('blue_box', outline=self.colors['blue'], width=5)
        detail_img.add_box('yellow_box', (detail_img.boxes['blue_box'].left-25, detail_img.boxes['blue_box'].top-15), (50, 50))
        detail_img.rectangle('yellow_box', outline=self.colors['yellow'], width=5)
        return detail_img.img
