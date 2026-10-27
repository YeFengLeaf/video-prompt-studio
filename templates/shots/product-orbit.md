---
id: shots/product-orbit
layer: shots
useWhen: 产品展示、电商、360° 看外观、材质细节
duration: 4–10s
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 镜头模式 · 产品环绕 / 细节

## 何时用

- 需要看清产品外形与材质；
- 电商主图视频；
- 广告收束镜头。

## 结构

1. 产品静止在干净背景（或使用场景）
2. 一个环绕/推近动作
3. 材质细节（反光、纹理、接缝）
4. 收束：英雄机位 + 留白

## 提示词骨架

```text
产品：{{product_facts}}，静止于{{surface}}，背景{{background}}。
0–{{t1}}s：{{camera_move}}环绕，{{angle_range}}，突出{{feature_1}}。
{{t1}}–{{t2}}s：推近至{{detail_area}}，{{light_behavior}}，可见{{material_detail}}。
{{t2}}–{{duration}}s：回到{{hero_angle}}，画面{{negative_space}}留白。
光线：{{light_source}}，{{reflection_note}}。
声音：{{sfx}}；{{music_note}}。
约束：产品外形不变形、不替换；文字/logo 留后期。
```

## 参数建议

- 环绕角度写范围（`从左前 45° 到右前 45°`），不写"360°"（容易穿帮）。
- 微距细节用 85–100mm；环境反光要控制（黑旗/柔光）。
- 一条只讲一个卖点，多卖点拆条。

## 失败风险

| 风险 | 改法 |
|---|---|
| 产品变形 | 减少环绕角度，或改固定+转台 |
| 反光乱 | 写"柔光箱反射，无环境倒影" |
| logo 糊 | 留白后期叠 |
| 像图库 | 加一个使用场景或人手互动 |
