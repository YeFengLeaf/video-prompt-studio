---
id: shots/establishing
layer: shots
useWhen: 开场、换场、交代空间、需要观众先知道"在哪"
duration: 3–6s
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 镜头模式 · 建立镜头

## 何时用

- 一条视频的开头；
- 场景切换；
- 观众需要先理解空间关系，后面的动作才看得懂。

## 结构

1. 空间全貌（景别：全景/远景）
2. 一个可识别的地标或光源
3. 人物入画或已在画面中（二选一，不要都做）
4. 镜头只做一个动作：固定 / 缓推 / 缓拉

## 提示词骨架

```text
{{setting}}全貌，{{landmark}}，{{light_source}}。
{{subject}}在画面{{position}}，{{state}}。
镜头：{{shot_size}}，{{angle}}，{{lens}}，{{camera_move}}（{{move_path}}）。
声音：{{ambience}}。
```

## 参数建议

- 焦段 24–35mm；景深偏深（看得清空间）。
- 时长 3–6s；超过 6s 必须有新信息进入。

## 失败风险

| 风险 | 改法 |
|---|---|
| 空镜无信息 | 加一个地标/光源/人物动作 |
| 与下一镜空间矛盾 | 在建立镜里写清人物方位 |
| 运镜太多 | 只留固定或缓推 |
