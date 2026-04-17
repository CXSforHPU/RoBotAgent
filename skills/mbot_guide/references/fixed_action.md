# 机械臂固定动作指令集（完整版）
## 文档说明
本文档包含机械臂**回到原点**、**四大仓库定位**、**夹爪开合**、**安全停机**等标准化固定动作指令，所有指令采用统一JSON格式，可直接下发执行，time统一设置为0.5秒保证运动平稳，适用于自动化抓取、归位、仓储定位场景。

---

## 一、基础归位动作
### 1. 回到机械臂原点（标准初始姿态）
```json
{
    "action": "set_joint",
    "joint_name": "joint1",
    "angle": 0,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint2",
    "angle": -45,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint3",
    "angle": -90,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint4",
    "angle": -90,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint5",
    "angle": 0,
    "time": 0.5
}
{
    "action": "set_gripper",
    "angle": 0,
    "time": 0.5
}
```

---

## 二、仓储定位动作
### 2. 仓库一 定位姿态
```json
{
    "action": "set_joint",
    "joint_name": "joint1",
    "angle": -44,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint2",
    "angle": -21,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint3",
    "angle": -90,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint4",
    "angle": -90,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint5",
    "angle": 0,
    "time": 0.5
}
{
    "action": "set_gripper",
    "angle": 0,
    "time": 0.5
}
```

### 3. 仓库二 定位姿态
```json
{
    "action": "set_joint",
    "joint_name": "joint1",
    "angle": -16,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint2",
    "angle": -37,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint3",
    "angle": -102,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint4",
    "angle": -98,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint5",
    "angle": 0,
    "time": 0.5
}
{
    "action": "set_gripper",
    "angle": 0,
    "time": 0.5
}
```

### 4. 仓库三 定位姿态
```json
{
    "action": "set_joint",
    "joint_name": "joint1",
    "angle": 16,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint2",
    "angle": -37,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint3",
    "angle": -102,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint4",
    "angle": -98,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint5",
    "angle": 0,
    "time": 0.5
}
{
    "action": "set_gripper",
    "angle": 0,
    "time": 0.5
}
```

### 5. 仓库四 定位姿态
```json
{
    "action": "set_joint",
    "joint_name": "joint1",
    "angle": 36,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint2",
    "angle": -5,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint3",
    "angle": -78,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint4",
    "angle": -98,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint5",
    "angle": 0,
    "time": 0.5
}
{
    "action": "set_gripper",
    "angle": 0,
    "time": 0.5
}
```

---

## 三、扩展实用动作（新增完善）
### 6. 夹爪完全张开（取物专用）
```json
{
    "action": "set_gripper",
    "angle": 0,
    "time": 0.5
}
```

### 7. 夹爪完全闭合（抓物专用）
```json
{
    "action": "set_gripper",
    "angle": -90,
    "time": 0.5
}
```

### 8. 紧急安全停机姿态（断电/故障保护）
```json
{
    "action": "set_joint",
    "joint_name": "joint1",
    "angle": 0,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint2",
    "angle": -45,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint3",
    "angle": -90,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint4",
    "angle": -90,
    "time": 0.5
}
{
    "action": "set_joint",
    "joint_name": "joint5",
    "angle": 0,
    "time": 0.5
}
{
    "action": "set_gripper",
    "angle": 0,
    "time": 0.5
}
```

---

## 四、使用规范
1. **执行顺序**：所有动作按JSON从上到下依次执行，关节动作完成后再执行夹爪动作
2. **时间参数**：默认`time=0.5s`，高速动作可改为`0.3s`，精密动作可改为`1s`
3. **角度范围**：所有关节/夹爪角度限制在 **-125° ~ 125°**
4. **场景建议**：
   - 抓取流程：原点 → 仓库定位 → 夹爪张开 → 抓取 → 夹爪闭合 → 回到原点
   - 故障处理：直接执行**紧急安全停机姿态**