---
id: base/mv
layer: base
useWhen: 歌词/MV/音乐短片，有段落但无精确音频参考
duration: 每条 8–20s
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 歌词 / MV · 基础模板

## 结构

1. **段落**：主歌 / 副歌 / 桥段 / 重复段
2. **视觉母题**：每段一个可重复的视觉元素
3. **节拍**：按段落组织，不按歌词逐句
4. **重复处理**：重复段复用镜头语言，不重复同一画面

## 提示词骨架

```text
{{style_anchor}}。
{{section_name}}（{{estimated_duration}}s，节奏为估计）。
0–{{t1}}s：{{motif_shot}}。
{{t1}}–{{t2}}s：{{performance_or_action}}。
{{t2}}–{{duration}}s：{{motif_variation}}。
镜头：{{shot_size}}，{{angle}}，{{camera_move}}。
光线：{{light_source}}。
声音：{{music_style}}；{{ambience}}；{{vocal_note}}。
```

## 填写规则

- **没有音频文件时，节奏只能标"估计"**；不许写"BPM 128"或"检测到 4/4 拍"。
- 歌词逐字保留，标 `（歌词）`，不当作动作指令。
- 重复段：同一母题换景别/换光/换运动方向，不要原样复制。
- 音乐只写风格、乐器、进入/退出点；不写歌名。

## 常见失败

| 失败 | 原因 | 改法 |
|---|---|---|
| 像幻灯片 | 每句一镜 | 按段落分，一段 1–2 镜 |
| 节奏对不上 | 声称检测了 BPM | 改标"估计"，让用户提供音频 |
| 重复段无聊 | 原样复制 | 换景别或运动方向 |
| 歌词被唱错 | 让模型"唱"歌词 | 歌词只作字幕/人声参考，另测口型 |
