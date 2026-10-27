---
id: shots/tracking
layer: shots
useWhen: 人物移动、追逐、穿行空间、展示环境
duration: 3–10s
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 镜头模式 · 跟拍 / 移动镜头

## 何时用

- 人物从 A 走到 B，空间信息在移动中揭示；
- 追逐、逃跑、赶路；
- 产品/人物入场。

## 结构

1. **起点**：机位在哪、拍到什么
2. **路径**：跟谁、经过什么、速度
3. **终点**：停在哪、最后画面

## 提示词骨架

```text
{{subject}}从{{start_point}}向{{end_point}}{{movement}}。
镜头从{{camera_start}}开始，{{tracking_type}}跟随，
经过{{landmark}}，在{{camera_end}}停住。
{{shot_size}}，{{lens}}，{{speed_note}}。
声音：{{ambience}}；{{footstep_or_whoosh}}。
```

## 参数建议

- 焦段 24–35mm（广角跟拍稳定）；主体保持画面中偏一侧。
- 速度写"匀速/渐快/急停"，不写"很有动感"。
- 一次跟拍只揭示 1–2 个新信息点。

## 失败风险

| 风险 | 改法 |
|---|---|
| 主体出画 | 写"保持在画面中偏左" |
| 背景穿帮 | 减少经过的地标 |
| 像航拍 | 明确机位高度（手持/稳定器/车载） |
| 速度不匀 | 写"匀速"或"渐快" |
