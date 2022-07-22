<div align="center">

# nonebot-plugin-PicMenu
### Nonebot2 插件菜单插件

<img src="https://img.shields.io/badge/tested_python-3.8.5-blue" alt="python">

<a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/static/v1?label=Nonebot&message=2.0.0%2Dbeta.4&color=green" alt="nonebot">
</a>

<a href="https://pypi.python.org/pypi/nonebot_plugin_PicMenu">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_PicMenu?color=red" alt="pypi">
</a>

<a href="https://pypi.python.org/pypi/nonebot_plugin_PicMenu">
    <img src="https://img.shields.io/pypi/dm/nonebot_plugin_PicMenu" alt="pypi download">
</a>

<a href="https://github.com/hamo-reid/nonebot_plugin_PicMenu/commits/main">
    <img alt="GitHub last commit (branch)" src="https://img.shields.io/github/last-commit/hamo-reid/nonebot_plugin_PicMenu/main?style=plastic">
</a>

</div>

---

## 特性

- 使用PluginMetadata加载数据
- 所有信息以图片方式呈现
- 共三级菜单，依次显示插件总表、插件功能总表、功能详情
- 查询时插件名和功能支持模糊匹配
- 可更换菜单样式模板[目前仅有默认模板]

## [更新记录](https://github.com/hamo-reid/nonenot_plugin_PicMenu/blob/main/History.md)

## 如何添加菜单

在需要添加菜单的插件中添加如下格式的代码

<font color="orange">PluginMetadata需要nb2 2.0.0-beta4版本</font>

**Example:**

```python
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name='测试插件',
    description='测试',
    usage='/test',
    extra={
        'menu_data': [
            {
                'func': '测试',
                'trigger_method': 'on_cmd',
                'trigger_condition': '/test',
                'brief_des': '用于测试的命令',
                'detail_des': '测试用命令\n'
                              '没有什么用'
            },
            {
                ......
            },
        ],
        'menu_template': 'default'
    }
)
```

**注：如下格式依然可以加载菜单，但无三级菜单**

```python
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name='测试插件',
    description='测试',
    usage='/test'
)
```

## 如何使用插件

### 初次使用

1. 加载插件后先启动bot，会在bot.py目录下生成menu_config文件夹
2. 修改menu_config/config.json 中 "default"的值为任一字体的路径（不要有反斜杠）</br>字体格式为[PIL.ImageFont.truetype](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html?highlight=truetype#PIL.ImageFont.truetype)所支持的字体
3. 保存config.json后重启bot即可使用菜单

> 以下示例均为默认模板 字体：等线 常规

### 获取所有已加载插件的菜单[一级菜单]

指令：菜单

返回：所有已加载插件信息图片

效果：

```qq
菜单
```

![一级菜单](https://github.com/hamo-reid/nonenot_plugin_PicMenu/blob/main/show_pic/menuL1.jpg)

### 获取插件指令菜单[二级菜单]

指令：菜单 [插件名]/[一级菜单中插件序号]

返回：插件所有功能简要信息图片

效果示例：

```qq
菜单 1
菜单 测试插件
菜单 测试
```

**无menu_data键值**

![二级菜单(无menu_data)](https://github.com/hamo-reid/nonenot_plugin_PicMenu/blob/main/show_pic/menuL2_2.jpg)

**有menu_data键值**

![二级菜单(有menu_data)](https://github.com/hamo-reid/nonenot_plugin_PicMenu/blob/main/show_pic/menuL2.jpg)

### 返回指令信息

指令：菜单 [插件名]/[一级菜单序号] [指令]/[二级菜单序号]

返回：查询某一功能的详细描述

效果示例：
```
菜单 1 1
菜单 测试插件 1
菜单 测试 1
菜单 1 测试
```

![三级菜单](https://github.com/hamo-reid/nonenot_plugin_PicMenu/blob/main/show_pic/menuL3.jpg)

---

## 菜单高级信息

menu_info 中brief_des和detail_des可以实现高级效果

**Example:**

```python
from nonebot.plugin importPluginMetadata

__plugin_meta__ = PluginMetadata(
    name='怪插件',
    description='很奇怪',
    usage='怪',
    extra={
        'menu_data': [
            {
                'func': '恶臭',
                'trigger_method': 'on_cmd',
                'trigger_condition': '/恶臭',
                'brief_des': '<ft color=green>哼哼哼</ft>',
                'detail_des': '<ft size=40>哼哼哼</ft><ft color=red>啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊</ft>'
            },
            {
                ......
            },
        ],
        'menu_template': 'default'
    }
)
```

效果展示:

![高级信息1](https://github.com/hamo-reid/nonenot_plugin_PicMenu/blob/main/show_pic/menuA1.jpg)

![高级信息2](https://github.com/hamo-reid/nonenot_plugin_PicMenu/blob/main/show_pic/menuA2.jpg)

其中支持高级信息的数据:

- PluginMetadata.usage
- brief_des
- detail_des

高级信息可支持的用法见源码nonebot_plugin_PicMenu.img_tool中multi_text方法
