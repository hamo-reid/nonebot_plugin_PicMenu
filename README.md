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

- 使用PluginMetadata或JSON加载数据
- 所有信息以图片方式呈现
- 共三级菜单，依次显示插件总表、插件功能总表、功能详情
- 查询时插件名和功能支持模糊匹配
- 可更换菜单样式模板[目前仅有默认模板]

## [更新记录](https://github.com/hamo-reid/nonenot_plugin_PicMenu/blob/main/History.md)

## 如何添加菜单

### 1. 从代码中添加菜单

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

### 2.从json文件添加菜单

1. 装载插件后需启动一次bot
2. 在bot.py目录下生成的menu_config/menus中编写json文件
3. json文件名格式如下: [需配置菜单的插件名].json
4. json内格式如下

```json
{
    "name": "菜单中显示的插件名",
    "description": "描述",
    "usage": "用法",
    "funcs": [
        {
            "func": "功能名",
            "trigger_method": "触发方式",
            "trigger_condition": "触发条件",
            "brief_des": "简述",
            "detail_des": "详细"
        },
        //同上
        ...
    ]
}
```

**注:** 

1. funcs为非必填项
2. 对于使用pip或nb-cli下载的插件名为其包名，本地加载的为 文件/文件夹 名

## 如何使用插件

### 初次使用

1. 加载插件后先启动bot，会在bot.py目录下生成menu_config文件夹
2. 修改menu_config/config.json 中 "default"的值为任一字体的路径（不要有反斜杠）</br>字体格式为[PIL.ImageFont.truetype](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html?highlight=truetype#PIL.ImageFont.truetype)所支持的字体
3. 保存config.json后重启bot即可使用菜单

### 菜单开关

切换菜单开启或关闭，命令如下：

```qq
菜单开关
```

仅有`SUPERUSER`和`ADMIN`拥有权限

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

## 菜单富文本

menu_info 中brief_des和detail_des可以实现部分富文本效果

**Example:**

```python
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name='演示插件',
    description='演示',
    usage='无',
    extra={
        'menu_data': [
            {
                'func': '演示',
                'trigger_method': '......',
                'trigger_condition': '......',
                'brief_des': '演示用',
                'detail_des': '<ft size=20>这是一个演示</ft>\n'
                              '<ft size=20 color=red>这是一个演示</ft>\n'
                              '<ft size=20 color=(0,0,255)>这是一个演示</ft>\n'
                              '这是一个<ft size=40>演示</ft>\n'
            }
        ],
        'menu_template': 'default'
    }
)
```

效果展示:

![富文本信息1](https://github.com/hamo-reid/nonenot_plugin_PicMenu/blob/main/show_pic/menuA1.jpg)

其中支持富文本的数据:

- PluginMetadata.usage
- brief_des
- detail_des

富文本可支持的用法见源码nonebot_plugin_PicMenu.img_tool中multi_text方法
