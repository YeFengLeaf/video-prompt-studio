# 方言骨架 · MiniMax H3

> 来源：`references/03_模型适配.md` §6。骨架文件：只复述档案，不新增参数。证据等级 A（MiniMax 官方 GitHub 提示词 Skill，2026-10-27 复核；原"官方 HF 指南"说法已更正）。
>
> G7 复核注：三字段、五种模式、`<Picture 1>` 等标签、4–15 秒已在官方 Skill 正文证实；关键帧前缀句式出自该 Skill 的 `references/base-en.txt`，本次未逐字打开，见 `references/03_模型适配.md` §11。

## 档案

- 单条上限：4–15 秒（A，2026-10-27 官方复核）
- 画幅：按平台（A）
- 分辨率：按平台（A）
- 参考输入：图/视频/主体/音频参考（A）
- 音频：原生（A）
- 引用语法：`[Shot N]` + `<Picture 1>`（A）
- 参数位置：**部分必须在提示词内**（时间码）——唯一的"参数在提示词内"例外（A）

## 三字段（T2VA）

```text
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: ...
```

## 关键帧模式前缀

```text
I2VA: For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
FL2VA: How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark; Picture 2 (from Shot N) aligns with the S.SS-second mark.
L2VA: How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark.
```

## 时间码规则

- `[Shot 1]` 不写时间码，从风格与初始构图开始。
- 后续镜头：`[Shot 2] At 00:03.500, the camera cuts to…`
- 时间严格递增，两位小数，落在有效时长内。
- 只有"增加新主体/空间/状态/视角/时间"才切；小距离变化用运镜。

## 骨架模板

```text
integrated_multimodal_description: [Shot 1] {{风格与初始构图}} [Shot 2] At {{00:SS.mmm}}, {{新主体/空间/状态/视角/时间变化}} ...
overall_soundscape: {{环境声与动作音}}
non_diegetic_music: {{音乐/无}}
```
