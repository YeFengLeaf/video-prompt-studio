---
id: base/doc
layer: base
useWhen: 纪录/非虚构/口播/访谈/科普演示，需要可信而非戏剧化
duration: 每条 10–30s
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 纪录 / 非虚构 · 基础模板

## 结构

1. **可见状态**：把"他很焦虑"换成"他反复看表、手指敲桌"
2. **空间准确**：谁在哪、镜头从哪看
3. **信息源**：旁白/访谈/字幕，标明谁说的
4. **不虚构**：没拍到的人、没发生的结论不能补

## 提示词骨架

```text
{{style_anchor}}（纪实、自然光、克制调色）。
{{subject}}在{{real_location}}，{{observable_state}}。
0–{{t1}}s：{{establishing_shot}}，{{camera_note}}。
{{t1}}–{{t2}}s：{{observed_action}}。
{{t2}}–{{duration}}s：{{detail_or_reaction}}。
镜头：{{shot_size}}，{{angle}}，{{lens}}，{{camera_move}}。
声音：{{ambience}}；{{sfx}}；{{voiceover_or_interview}}。
约束：不添加未出现的人物、地点或结论。
```

## 填写规则

- 状态词必须可观察；"专家认为"要能对应到具体说话人。
- 访谈镜头：正对/侧 45°，眼睛看镜头外；别让被访者盯着镜头（除非设计如此）。
- 旁白与画面不要互相复述；画面给证据，旁白给背景。
- 数据/图表类：生成期留干净区域，数字后期叠。

## 常见失败

| 失败 | 原因 | 改法 |
|---|---|---|
| 像摆拍 | 动作太"演" | 改成日常小动作 |
| 事实被补 | 模型自己加人/加结论 | 明确"不添加未出现…" |
| 口播嘴型崩 | 台词太长 | 拆条 + 正脸近景 |
