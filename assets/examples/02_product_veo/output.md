# 白瓷茶杯 · 视频提示词生产包

- 目标模型：Veo 3.1
- 交付形态：单条
- 生成日期：2026-10-20
- 包版本：v1

## 1. 决策摘要

**我替你定的**
- 时长 8s：四个短拍，够全貌 + 交互 + 细节 + 收束
- 画幅 16:9：产品横构图
- 景别策略：中景全貌 → 近景手部 → 微距釉面 → 中景收束
- 光线逻辑：左侧窗光为唯一主光源，柔光，木桌反光作补
- 声音方案：无对白；瓷杯轻碰木桌 + 安静室内底噪
- 语言：提示词用英文（Veo 对英文更稳），事实层保留中文

**仍未知的**
- 平台分辨率与单条时长上限（标 C，未核实）
- 杯子容量与工艺（用户未提供，不编）

**本轮未做**
- 没写产品图提示词
- 没做品牌文案（用户明确不要文字）

## 2. 事实层

- 产品：白瓷茶杯，青灰釉，杯口薄，无 logo
- 场景：木桌，左侧窗户
- 时间：清晨
- 道具：无
- 必须保留：产品外形与釉色不变；画面无文字

### 台词表

| 说话人 | 原文（逐字） | 语气 | 字数 | 预算秒数 | 结论 |
|---|---|---|---|---:|---:|---|
| — | 无对白 | — | 0 | 0 | 可执行 |

## 3. 分镜表

| 镜号 | 时间 | 景别 | 角度 | 焦段 | 运镜 | 主动作 | 台词 | 声音 | 入点 → 出点 |
|---|---|---|---|---|---|---|---|---|---|
| S01-01 | 0–2s | 中景 | 平视 | 50mm | 固定 | 茶杯静置，热气上升 | — | 安静室内底噪 | 桌面空 → 杯在画面右三分之一 |
| S01-02 | 2–4s | 近景 | 平视 | 85mm | 缓推 | 一只手把杯子端起 | — | 瓷杯离桌的轻响 | 杯在桌面 → 杯离桌 10cm |
| S01-03 | 4–6s | 特写 | 俯视 | 100mm | 固定 | 釉面与薄杯口在光下显出层次 | — | 无 | 杯口占满画面 → 保持 |
| S01-04 | 6–8s | 中景 | 平视 | 50mm | 缓拉 | 杯子被放回木桌 | — | 瓷杯落桌的轻碰 | 杯在手中 → 杯回到桌面 |

## 4. 提示词

```text
Cinematography: static medium shot, shallow depth of field, soft window light from the left.
Subject: a white porcelain teacup with pale celadon glaze and a very thin rim, no logo, from reference image 1.
Action: 0-2s the cup sits still on the table, steam rises slowly; 2-4s a hand lifts it gently; 4-6s a macro shot shows the glaze and the thin rim catching the light; 6-8s the cup is set back on the wooden table from reference image 2.
Context: a quiet wooden table, one window on the left, soft morning light, no other objects.
Style & Ambiance: Japanese ceramic still life, muted warm gray, restrained and quiet, no text.
SFX: the soft clink of porcelain touching wood.
Ambient noise: a quiet room, distant birds outside.
```

## 5. 素材与挂图

| 编号 | 素材 | 主职责 | 作用镜头 | 不得传递 | 本条槽位 |
|---|---|---|---|---|---|
| A01 | 白瓷杯产品图 | 外形 + 釉色 | 全部 | 背景、光线 | reference image 1 |
| A02 | 木桌场景图 | 空间 + 木纹 | S01-01~S01-04 | 产品 | reference image 2 |

## 6. 参数

| 项 | 值 | 证据等级 | 核验日期 | 说明 |
|---|---|---|---|---|
| 时长 | 8s | C | 未核实 | 按平台可调，未核实 |
| 画幅 | 16:9 | B | 2026-10-20 | 按平台 |
| 分辨率 | 1080p | C | 未核实 | 未核实 |
| 参考数 | 2 图 | C | 未核实 | Veo 参考入口按平台 |
| 音频 | 开 | A | 2026-10-20 | 支持对白/SFX/环境声 |
| 模式 | 文生视频 + 2 图参考 | C | 未核实 | 入口按平台 |

## 7. 自检

### 结构项（脚本）
- S-01 PASS · S-02 PASS · S-03 PASS（8s）· S-04 PASS · S-05 PASS（无台词）
- S-06 PASS · S-07 PASS（2 份资产 / 2 处引用）· S-08 PASS（Veo 不用 @ 语法）
- S-09 PASS（参数全在块外）· S-10 PASS · S-11 PASS · S-12 PASS · S-13 PASS · S-14 PASS

### 复核项（人）
- R-03 通过：杯与桌面职责分开
- R-06 需人工看成片：薄杯口在微距下的透光是否可信
- R-07 通过：没有混入"电影感/高级感"空词

### 结论
可交付（文本层）

## 8. 风险与下一步

- 最可能失败：微距镜头里杯口变形 → 把 S01-03 改成固定机位 + 更短时长
- 次可能失败：手部动作穿模 → 减少手指参与，只拍杯身被托起
- 第 3 轮建议先改：S01-02 的手部动作
- 未核实：Veo 单条时长上限、参考图入口
