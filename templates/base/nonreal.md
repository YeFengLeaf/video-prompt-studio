---
id: base/nonreal
layer: base
useWhen: 纸艺、水墨、定格、3D 卡通、插画动画等非写实方向
duration: 每条 6–20s
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 非写实动画 · 基础模板

## 结构

1. **材质锁**：这是什么做的（纸/墨/黏土/赛璐璐）
2. **运动规则**：顿挫、回弹、化开、逐帧
3. **工艺痕迹**：折痕、毛边、笔触、指纹
4. **禁止写实**：不写浅景深、胶片颗粒、真实皮肤

## 提示词骨架

```text
{{material_style}}。
{{subject}}由{{material_detail}}构成，{{craft_marks}}。
0–{{t1}}s：{{material_establish}}。
{{t1}}–{{t2}}s：{{motion_rule_action}}。
{{t2}}–{{duration}}s：{{material_landing}}。
镜头：{{shot_size}}，{{angle}}，{{camera_move}}（克制）。
运动规则：{{motion_rhythm}}。
声音：{{foley_material}}；{{ambience_or_silence}}。
约束：保持{{material_style}}，不写实化。
```

## 填写规则

- 材质词要具体：`宣纸纤维`、`折痕锐利`、`黏土指纹`，不写"高级质感"。
- 运动节奏写成可执行：`一拍二`、`每 0.2s 位移一次`、`墨迹连续扩散`。
- 声音也按材质写：纸的沙沙声、黏土的闷响，不是真实世界的音效。
- 需要风格壳时叠 `templates/styles/` 对应文件。

## 常见失败

| 失败 | 原因 | 改法 |
|---|---|---|
| 纸变塑料 | 材质描述不足 | 补纸纹、毛边、厚度 |
| 定格变丝滑 | 没写顿挫 | 写"逐帧、轻抖、一拍二" |
| 水墨变烟雾 | 用"特效"描述 | 写成宣纸上的连续渐变 |
| 画面太写实 | 混入摄影词 | 删浅景深/胶片/真实皮肤 |
