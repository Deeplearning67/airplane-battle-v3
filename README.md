# 🛩️ 飞机大战 Airplane Battle v3.0 - Chapter Boss Edition

<div align="center">

**经典竖版街机射击游戏 · 章节Boss版**
**Classic Vertical Arcade Shooter · Chapter Boss Edition**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0-red.svg)]()

</div>

---

## 📖 简介 / About

**飞机大战 v3.0** 是基于 Pygame 的经典竖版街机射击游戏终极版本，包含完整的 **5章章节系统** 和 **章节专属Boss战**。

**Airplane Battle v3.0** is the ultimate edition of the classic vertical arcade shooter, featuring a complete **5-chapter system** with **unique bosses per chapter**.

---

## ✨ 核心特色 / Features

| 功能 Feature | 描述 Description |
|------------|----------------|
| **5章完整章节** | 每章独立配色、敌机造型、Boss设计 |
| **5个章节Boss** | 每章独特Boss，密集弹幕，多阶段攻击 |
| **章节进度** | 击败Boss进入下一章，第5章通关 |
| **9种道具系统** | 火力/生命/护盾/磁铁/冰冻等 |
| **Top 10排行榜** | JSON持久化，含章节记录 |
| **v2.3稳定性修复** | Surface缓存、异常保护、内存优化 |

---

## 🗺️ 章节设计 / Chapters

### 第一章 · 红色尖兵 (Chapter 1: Red Sentinel)
- **触发距离**: 3000m
- **敌人配色**: 红色系
- **Boss: 红色尖兵** — HP:80 — 十字交叉弹幕 + 扇形弹幕
- **难度**: ⭐⭐

### 第二章 · 紫色利刃 (Chapter 2: Purple Blade)
- **触发距离**: 6000m
- **敌人配色**: 紫色系
- **Boss: 紫色利刃** — HP:150 — 旋转螺旋弹幕 + 环形弹幕
- **难度**: ⭐⭐⭐

### 第三章 · 棕色重甲 (Chapter 3: Brown Fortress)
- **触发距离**: 10000m
- **敌人配色**: 棕色系
- **Boss: 棕色重甲** — HP:250 — 3方向散射 + 宽幅扇形弹幕
- **难度**: ⭐⭐⭐⭐

### 第四章 · 绿色精英 (Chapter 4: Green Elite)
- **触发距离**: 15000m
- **敌人配色**: 绿色系
- **Boss: 绿色精英** — HP:400 — 追踪弹 + 密集散布弹 + 横向弹幕
- **难度**: ⭐⭐⭐⭐⭐

### 第五章 · 黄金终焉 (Chapter 5: Golden Nemesis)
- **触发距离**: 22000m
- **敌人配色**: 金色系
- **Boss: 黄金终焉** — HP:600 — 全屏乱射 + 环形弹幕 + 激光预警弹幕
- **难度**: ⭐⭐⭐⭐⭐⭐

---

## 🚀 快速开始 / Quick Start

### 环境要求 / Requirements
```
Python 3.8+
Pygame >= 2.0.0
```

### 安装 / Installation
```bash
# Windows
pip install pygame

# 或一键安装依赖
pip install -r requirements.txt
```

### 运行 / Run
```bash
# 直接运行
python airplane_battle3.py

# 或使用启动器（Windows）
双击 run.bat
```

---

## 🎮 操作说明 / Controls

| 按键 Key | 功能 Action |
|----------|------------|
| `← → ↑ ↓` 或 `W A S D` | 移动飞机 Move |
| `空格 Space` | 发射子弹（长按连发）Fire (hold) |
| `B` | 使用全屏炸弹 Use Bomb |
| `P` 或 `ESC` | 暂停/继续 Pause/Resume |
| `R` | 重新开始（游戏结束时）Restart |
| `M` | 返回菜单（游戏结束时）Menu |
| `L` | 查看排行榜 Leaderboard |
| `鼠标左键` | 菜单按钮点击 Menu click |

---

## 🎯 Boss弹幕设计 / Boss Patterns

```
Chapter 1 Boss (红色尖兵):
  阶段0: 十字交叉 (0°/90°/180°/270°) 弹幕
  阶段1: 宽幅扇形弹幕 (7发)

Chapter 2 Boss (紫色利刃):
  阶段0: 旋转双螺旋弹幕 (每8帧发射)
  阶段1: 12发环形弹幕 + 螺旋弹幕叠加

Chapter 3 Boss (棕色重甲):
  阶段0: 3方向散射弹幕
  阶段1: 宽幅扇形弹幕 + 3方向叠加

Chapter 4 Boss (绿色精英):
  阶段0: 追踪弹 + 9发散布弹
  阶段1: 追踪弹 + 5发横向弹幕 + 散布弹叠加

Chapter 5 Boss (黄金终焉):
  阶段0: 3连随机弹幕 + 16发环形弹幕
  阶段1: 快速激光预警弹幕 + 环形弹幕叠加
```

---

## 📊 排行榜 / Leaderboard

排行榜包含以下字段（JSON格式）：
```json
{
  "entries": [{
    "name": "PILOT",
    "score": 30000,
    "distance": 25.4,
    "kills": 120,
    "chapter": 5,
    "date": "2026-04-14"
  }]
}
```

> ⚠️ `leaderboard3.json` 为游戏自动生成，已加入 `.gitignore`。

---

## 🛠️ 技术细节 / Technical Details

| 项目 Item | 规格 Spec |
|-----------|-----------|
| 渲染 Engine | Pygame SDL2 |
| 帧率 FPS | 60 FPS |
| 分辨率 Resolution | 540×780 (竖屏 Portrait) |
| 代码行数 Lines | ~2500 行单文件 |
| 图形 Graphics | 100% 程序化绘制 (Zero External Assets) |

### 性能优化 / Performance
- ✅ Surface 预缓存（陨石旋转/HUD背景/护盾效果）
- ✅ 粒子数量上限（150粒子+80尾迹）
- ✅ 全局异常保护主循环
- ✅ Bullet.update 方法注入（支持Boss自定义弹幕）

---

## 📜 版本历史 / Changelog

### v3.0 Chapter Boss (当前版本 / Current)
- ✅ 5章完整章节系统
- ✅ 每章专属Boss（密集弹幕设计）
- ✅ 章节进度追踪（第几章/通关）
- ✅ 排行榜增加章节字段
- ✅ Boss血量：80→150→250→400→600（逐章递增）
- ✅ Boss入场警告动画
- ✅ 章节通关动画

### v2.3 Stability
- ✅ emoji字体崩溃修复
- ✅ 玩家死亡后HUD安全访问
- ✅ PowerUp.apply引用修复
- ✅ 陨石旋转缓存限制

---

## 📁 项目结构 / Project Structure

```
airplanebattle3.0/
├── airplane_battle3.py   # 主游戏源码 (~2500行)
├── README.md             # 说明文档（本文件）
├── requirements.txt      # 依赖列表
├── run.bat               # Windows一键启动
├── LICENSE               # MIT协议
├── leaderboard3.json     # 排行榜（自动生成）
└── screenshots/          # 游戏截图
    └── (placeholder)
```

---

## 🛡️ 安全说明

本游戏为纯本地运行的游戏程序，无任何网络通信或数据外传行为。
排行榜数据存储在本地 `leaderboard3.json` 文件中。

---

<div align="center">

**作者 / Author**: 阿爪 🦞 | AZhua
**日期 / Date**: 2026.04
**许可 / License**: [MIT](LICENSE)

⭐ 如果喜欢，欢迎 Star！⭐

</div>
