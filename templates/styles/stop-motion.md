---
id: styles/stop-motion
layer: styles
useWhen: 定格动画、黏土、模型、手作感
duration: 任意
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 风格壳 · 定格动画

## 视觉规则

- **材质**：黏土指纹、模型接缝、布料毛边；不磨皮。
- **运动**：逐帧位移，轻微抖动；"一拍二"的顿挫。
- **光**：棚拍式侧光，有明确阴影；不写自然光。
- **景**：微缩布景，景深较深（模型要看清）。
- **色**：手工上色感，允许不均。

## 提示词壳

```text
定格动画，{{material}}模型，可见指纹与接缝，
微缩布景，{{light_direction}}棚拍侧光，{{palette}}手工上色。
{{subject}}在{{setting}}，{{action}}。
运动：逐帧、轻微抖动、{{frame_rate_note}}。
```

## 禁止

- 丝滑稳定器运动
- 写实皮肤/真实毛发
- 数字磨皮与光追高光
- 快速运镜（定格经不起快摇）

## 迁移点

- 动作分解成"每 0.2–0.3 秒一个姿势"，比写"流畅"有效。
- 转场用"手入画/换景片"，符合 hand-made 逻辑。
