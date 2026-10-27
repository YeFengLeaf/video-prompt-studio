---
id: styles/cinematic-realism
layer: styles
useWhen: 写实电影感、剧情短片、品牌片、需要可信物理
duration: 任意
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 风格壳 · 写实电影感

## 视觉规则

- **光**：一个主光源（窗/灯/天光）+ 一个补光；有方向、有明暗比。
- **色**：低饱和、统一色温；不用"电影级调色"这种空词。
- **材质**：皮肤有纹理但不磨皮；布料有重量；金属有反射。
- **景深**：中近景浅景深，全景深景深；不要每镜都虚化。
- **运动**：手持只用于紧张段；稳定器用于展示段。

## 提示词壳

```text
写实电影摄影，{{time_of_day}}，{{light_source}}为主光源，{{light_quality}}，
低饱和{{palette}}，{{film_texture}}，{{lens_feel}}。
{{subject}}在{{setting}}，{{action}}。
```

## 禁止

- `masterpiece, 8k, ultra detailed, best quality` 这类噪音词
- 同时写"柔光"和"硬光"
- 每镜都写"浅景深"
- 用"电影感""高级感"代替具体光向与材质

## 迁移点

- 从写实风格切到非写实：删掉 `film_texture`、`lens_feel`，换成材质锁。
- 广告产品镜头：把 `{{lens_feel}}` 换成微距 + 控制反光。
