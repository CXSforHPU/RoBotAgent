---
name: monster_hunter_world_guide
description: "当用户涉及到有关怪物猎人世界的话题，包括游戏基本信息，游戏数据接口，游戏控制接口，如何启动游戏、关闭游戏等，请查阅此文档"
---

# 怪物猎人世界指南



## 游戏基本信息

无



## 游戏数据接口

可以通过HTTP接口获取当前游戏画面，用户分析游戏状态



### 游戏画面API

`GET {{monster-hunter-world-server-url}}/monster_hunter_world/screen`

#### 参数

无

#### 返回内容

当前游戏画面的截图（JPEG图像）

用途：

- 分析游戏状态

#### 规则

每次需要判断游戏状态时，必须重新调用**游戏画面API**来获取最新的游戏画面



## 游戏控制接口

### 启动游戏API

通过HTTP接口来打开游戏

`GET {{monster-hunter-world-server-url}}/monster_hunter_world/start`

#### 参数

无

#### 返回内容

无



### Xbox360按钮点击API

可以通过HTTP接口模拟 **Xbox360** 手柄按钮点击操作

`GET {{monster-hunter-world-server-url}}/xbox360/click_button/{button_name}`

#### 参数

`button_name`：Xbox360 手柄按钮名称

#### 可用按钮

- START
- BACK
- A（确定）
- B（返回）
- X
- Y
- UP
- DOWN
- LEFT
- RIGHT
- LB
- RB
- LS
- RS

#### 示例

按下 A 键

```
GET {{monster-hunter-world-server-url}}/xbox360/click_button/A
```

#### 返回内容

无



## 启动游戏参考文档

用户需要启动游戏时，查看文档: `{{skills-path}}/{{skill-name}}/references/start-game.md`



## 关闭游戏参考文档

用户需要关闭游戏时，查看文档:`{{skills-path}}/{{skill-name}}/references/close-game.md`
