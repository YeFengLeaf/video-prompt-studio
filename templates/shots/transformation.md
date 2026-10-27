---
id: shots/transformation
layer: shots
useWhen: 变身、材质变化、昼夜转换、时间流逝、形态过渡
duration: 3–8s
models: [seedance-2.0, seedance-2.5, veo, minimax-h3, kling, generic]
---

# 镜头模式 · 变身 / 过渡

## 何时用

- 角色变身、换装、老化；
- 产品形态变化（固态→液态）；
- 昼夜/季节转换；
- 两个空间之间的过渡。

## 结构

1. **变化前**：明确初始状态（颜色、形状、材质）
2. **触发**：什么引起变化（光、触碰、时间）
3. **中间态**：至少一个可观察的过渡形态
4. **变化后**：明确终态

## 提示词骨架

```text
{{subject}}从{{state_before}}开始，{{trigger}}。
{{t_mid}}s：{{intermediate_state}}（可见的过渡形态）。
{{t_end}}s：完成变为{{state_after}}。
镜头：{{shot_size}}，{{angle}}，{{camera_move}}。
光线：{{light_change}}。
声音：{{transition_sfx}}。
约束：变化过程连续，不跳变；不出现额外主体。
```

## 参数建议

- 变化过程至少占 1/2 时长；不要 0.5 秒完成。
- 中间态越具体越稳：`皮肤先出现裂纹，再透出金属光泽`。
- 一次只变一个维度（形/色/材质），多变会糊。

## 失败风险

| 风险 | 改法 |
|---|---|
| 直接跳变 | 补中间态与时间点 |
| 变成别的东西 | 写"保持{{identity_feature}}不变" |
| 画面闪烁 | 减少同时变化的元素 |
| 过渡像特效 | 写成材质/光的连续变化 |
