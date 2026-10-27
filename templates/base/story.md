---
id: base/story
layer: base
useWhen: 有剧本、梗概或可拍摄的故事，要拆成 1–3 条视频
duration: 每条 8–30s
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 剧情短片 · 基础模板

## 结构（按顺序填，不跳步）

1. **风格锚**：一句材质/摄影基调（不堆形容词）
2. **主体锚**：谁 + 最小外观（只写输入里有的，或标"待补"）
3. **初始状态**：人物在哪、在做什么、空间关系
4. **三个节拍**：建立 → 变化 → 落点；一节拍一动作
5. **镜头**：每拍一个景别/机位/运镜
6. **光**：一个主光源 + 一个补光逻辑
7. **声**：环境底噪 + 动作音 + 台词/静场
8. **收束**：最后画面停在哪

## 提示词骨架

```text
{{style_anchor}}。
{{subject_anchor}}在{{setting}}，{{initial_state}}。
0–{{t1}}s：{{beat_establish}}。
{{t1}}–{{t2}}s：{{beat_change}}。
{{t2}}–{{duration}}s：{{beat_landing}}。
镜头：{{shot_size}}，{{angle}}，{{lens}}，{{camera_move}}（{{move_path}}）。
光线：{{light_source}}，{{light_quality}}。
声音：{{ambience}}；{{sfx}}；{{dialogue_block}}。
收束：{{ending_state}}。
```

## 填写规则

- `{{beat_*}}` 必须是**可观察动作**，不写"她意识到""气氛变得"。
- 三个节拍的时间加起来 = `{{duration}}`；允许最后一拍多留 0.5–1s 给反应。
- `{{camera_move}}` 只写一个；路径写"从…到…"。
- `{{dialogue_block}}` 没有台词就写"无对白"。
- 非写实题材先换 `templates/styles/` 的风格锚，再填动作。

## 常见失败

| 失败 | 原因 | 改法 |
|---|---|---|
| 动作做一半停了 | 缺落点 | 补 `{{ending_state}}` |
| 人物漂移 | 外观描述太长/矛盾 | 缩短主体锚，交给素材图 |
| 节奏赶 | 三拍塞了五个动作 | 减事件，不加快运镜 |
| 画面空 | 没有前景/环境信息 | 补一个环境细节 |
