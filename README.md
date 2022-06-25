<div align="center">

# nonebot-plugin-menu
### Nonebot2 插件菜单插件

<img src="https://img.shields.io/badge/python-3.7.3+-blue?style=for-the-badge" alt="python">
 
<img src="https://img.shields.io/badge/tested_python-3.8.5-blue?style=for-the-badge" alt="python">

<img src="https://img.shields.io/static/v1?label=Nonebot&message=2.0.0%2Dbeta.3&color=red&style=for-the-badge" alt="nonebot">
 
</div>


---

> 当前版本仅能下载源码手动加载

## 特性
- 所有信息以图片方式呈现
- 查询时插件名和指令支持模糊匹配
- 可更换菜单样式模板[目前仅有默认模板]

## 需要安装的第三方库

```cmd
python -m pip install pillow==8.0.1
python -m pip install fuzzywuzzy==0.18.0
```

## 开发者添加菜单

### 从代码加载
参考代码
```python
# 假设本地加载的插件名为"nonebot_plugin_menu"
menu_manager = require("nonebot_plugin_menu").menu_manager
menu_dict = {
    "name": "测试插件",
    "description": "测试用插件",
    "cmds": [
        {
            "cmd": "测试",
            "type": "on_cmd",
            "brief_description": "用于测试的命令",
            "detail_description": "这个命令用于测试，实际没什么用"
        },
    ]
}
menu_manager.load_from_code(menu_info_path)
```
直接从字典加载

### 从json加载

#### 参考代码
```python
from pathlib import Path
# 假设本地加载的插件名为"nonebot_plugin_menu"
menu_manager = require("nonebot_plugin_menu").menu_manager
menu_info_path = Path(__file__).parent / 'menu.json'
menu_manager.load_from_json(menu_info_path)
```
menu.json中存放菜单数据

#### json格式
```json
{
    "name": "测试插件",
    "description": "测试用插件",
    "cmds": [
        {
            "cmd": "测试",
            "type": "on_cmd",
            "brief_description": "用于测试的命令",
            "detail_description": "这个命令用于测试，实际没什么用"
        }
    ]
}
```

## 如何使用

### 获取所有已加载插件的菜单[一级菜单]
指令：[指令头]菜单 | 菜单

返回：所有已加载插件信息图片

### 获取插件指令菜单[二级菜单]
指令：[指令头]菜单 [插件名]/[一级菜单中插件序号]

返回：插件所有命令简要信息图片

### 返回指令信息
指令：[指令头]菜单 [插件名]/[一级菜单序号] [指令]/[二级菜单序号]

返回：指令详细信息图片
