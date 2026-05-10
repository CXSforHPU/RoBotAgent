---
name: mbot-guide
description: "当需要调用机械臂相关功能时，请一定先查看mbot-guide技能。"
---

# 机械臂控制技能

## 功能介绍

本技能控制 MBot 机器人的机械臂执行各类任务，包括移动、识别、分类、放置、定位、游戏互动等。

- **机械臂控制工具** (`mbot_motion`)：控制机械臂运动与任务执行

## 使用前必读

1. **语言解析**:将语言中复杂务分割为多个任务，并返回一个任务列表
2. **服务调用**:任务列表进行单独发布，并等待服务返回结果

---

## 一、机械臂控制（mbot_motion）

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | string | 是 | 操作类型（move/recognize/sort/place/position/game/calibration/list） |
| `command` | string | 是 | 具体命令名称，见下方映射表 |
| `data1` | integer | 否 | 附加参数1（默认 0） |
| `data2` | integer | 否 | 附加参数2（默认 0） |

### 操作类型与命令映射

#### move — 移动

| command | 含义 |
|---------|------|
| `move_left` | 向左 |
| `move_right` | 向右 |
| `move_up` | 向上 |
| `move_down` | 向下 |
| `move_forward` | 向前 |
| `move_backward` | 向后 |

```
# 示例：向前移动
mbot_motion(action="move")
```

#### recognize — 识别

| command | 含义 |
|---------|------|
| `color_recognition` | 颜色识别 |
| `shape_recognition` | 形状识别 |
| `qrcode_recognition` | 二维码识别 |
| `drug_identification` | 药品识别 |
| `garbage_identification` | 垃圾识别 |
| `characters_identification` | 字符识别 |

```
# 示例：识别颜色
mbot_motion(action="recognize", command="color_recognition")
```


#### sort — 分类

| command | 含义 |
|---------|------|
| `color_sorting` | 颜色分拣 |
| `shape_sorting` | 形状分拣 |
| `qrcode_sorting` | 二维码分拣 |
| `drug_sorting` | 药品分拣 |
| `garbage_sorting` | 垃圾分拣 |
| `characters_sorting` | 字符分拣 |

```
#示例 药品分拣
mbot_motion(action="sort", command="drug_sorting")
```


#### place — 放置

| command | 含义 |
|---------|------|
| `place_in_warehouse_1` | 放入仓库 1 号位 |
| `place_in_warehouse_2` | 放入仓库 2 号位 |
| `place_in_warehouse_3` | 放入仓库 3 号位 |
| `place_in_warehouse_4` | 放入仓库 4 号位 |

```
# 示例：放入仓库 2 号位
mbot_motion(action="place", command="place_in_warehouse_2")
```

#### position — 定位

| command | 含义 |
|---------|------|
| `go_home` | 回到 home 位置 |
| `go_sorting_position` | 移动到分拣位置 |
| `go_camera_position` | 移动到摄像头位置 |


```
#示例 回到 home 位置
mbot_motion(action="position", command="go_home")
```


#### game — 游戏

| command | 含义 |
|---------|------|
| `face_tracking` | 人脸追踪 |
| `guessing_fists_game` | 猜拳游戏 |
| `stacking_game` | 叠叠乐游戏 |

```
# 示例：人脸追踪
mbot_motion(action="game", command="face_tracking")
```

#### calibration — 校准

| command | 含义 |
|---------|------|
| `color_calibration` | 颜色校准 |

#### list — 列出所有可用命令

```
mbot_motion(action="list")
```

## 二、典型多复杂任务分解

1. 先颜色识别再颜色分拣：
```
mbot_motion(action="recognize", command="color_recognition")
mbot_motion(action="sort", command="color_sorting")
```
2. 先形状识别再形状分拣：
```
mbot_motion(action="recognize", command="shape_recognition")
mbot_motion(action="sort", command="shape_sorting")
```
3. 先二维码识别再二维码分拣：
```
mbot_motion(action="recognize", command="qrcode_recognition")
mbot_motion(action="sort", command="qrcode_sorting")
```
4. 先药品识别再药品分拣：
```
mbot_motion(action="recognize", command="drug_identification")
mbot_motion(action="sort", command="drug_sorting")
```


## 四、注意事项

1. 忽视传感器数据