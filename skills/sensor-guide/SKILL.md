---
name: sensor-guide
description: "当需要调用传感器相关功能时，请一定先查看sensor-guide技能。"
---

# 传感器数据获取技能

## 调用方法
```python
sensor_get(action="xxx")
```

---

## 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|--------|
| `action` | string | 是 | 取值：`get_data` / `get_status` |

---

## 1. action = get_data（获取实时环境数据）
**功能**：获取电池、温湿度、气压、光照、空气质量、超声波状态  
**调用**：
```python
sensor_get(action="get_data")
```

**返回示例**：
```
传感器实时数据：
  电池电压：7.4 V
  环境温度：25.3 ℃
  环境湿度：60.2 %RH
  大气压强：101.3 kPa
  光照强度：500 Lux
  空气质量1：50
  空气质量2：30
  超声波1：检测到障碍物
  超声波2：无障碍物
  超声波3：无障碍物
  超声波4：无障碍物
```

---

## 2. action = get_status（获取节点运行状态）
**功能**：获取传感器节点运行、数据、话题、更新时间  
**调用**：
```python
sensor_get(action="get_status")
```

**返回示例**：
```
传感器节点状态：
  节点状态：运行中
  数据状态：有数据
  订阅话题：/sensor/data
  最后更新时间：0.5s
```

---

### 总结
- 两个核心指令：`get_data` 拿环境数据、`get_status` 查节点状态
- 统一调用函数：`sensor_get(action="...")`
- 返回格式为结构化文本，可直接解析或展示使用