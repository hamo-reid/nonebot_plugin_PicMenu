# 更新记录

## 2022/8/5 v0.1.6

**bug_fix:**

- 修复无menu_data插件内部名称为plugin.name的错误

## 2022/7/21 v0.1.5

**bug_fix:**

- 修复gocq断线重连后导致菜单信息重复加载的错误  感谢[@jasmineamber](https://github.com/jasmineamber)
- 修复无menu_data插件的插件名为Plugin.name而非PluginMenudata.name的错误
- 防止因插件名过长导致超出图片宽度

**add:**

- 为一、二级菜单添加表头
- 添加菜单开关，控制是否开启菜单

## 2022/7/8  v0.1.4

**bug_fix:**

- 修复无menu_data插件的插件名加载错误导致菜单无法生成的bug

**optimize:**

- 优化usage在菜单中的展示效果

## 2022/7/7  v0.1.3.2

**bug_fix:**

- 修复三级菜单长文本显示不全的问题

## 2022/7/2  v0.1.2

**add:**

- 对PluginMetadata中无menu_data键值对的插件适配菜单
- 添加加载插件菜单信息的log
