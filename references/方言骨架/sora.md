# 方言骨架 · Sora 2

> 来源：`references/03_模型适配.md` §12.3（外包调研 REC_20261022_052–054）。骨架文件：只复述档案，不新增参数。证据等级 A（OpenAI 官方发布页）。时效口径（2026-10-27 更正）：Sora 产品已于 2026-04-26 停用，Videos API 已于 2026-09-24 关闭；本文件为**历史口径**，不得作为当前可用平台出包。API 实际分辨率仅 720p（720×1280 / 1280×720）。

## 档案

- 单条上限：示例档 5.0s（历史口径；产品已停用，054，A）
- 画幅/分辨率：示例写 4K；API 实际仅 720p（720×1280 / 1280×720，2026-10-27 官方页复核）；历史口径，不得编造（054，A）
- 参考输入：参考视频（V2V 兜底复杂因果物理，053，A）
- 音频：原生；Sound 段嵌入台词（054，A）
- 引用语法：自然语言分节（无 `@` 式语法）
- 参数位置：分节参数直接写进提示词（Format & Look 直接写时长/快门/画幅，054，A）

## 结构顺序（Sora 2 shot-list 分节）

```text
Primary Target & Visuals（动作先读、二读景观）
Format & Look（时长; 分辨率; 快门; 传感器/颗粒）
Lenses & Filtration
Grade / Palette（highlights / mids / shadows 分层）
Lighting & Atmosphere
Location & Framing
Sound（环境声 / 音乐 / 台词）
Optimized Shot List（1 shot / 时长 + 时间码）
```

## 写法规则

- v1 历史口径（052，A）：长段落电影场面描述，相机写成动作句（`The camera follows behind…` / `The camera rotates around…`），胶片/镜头参数直接嵌句。仅作历史参考，现行出包用 v2 分节式。
- 不写长串复合精确运镜轨迹，改用分镜单镜；左右方位改为相对动作关系描述；多实体场景加 `one/two` 数量约束（053）。
- 使用真人肖像"角色"功能需本人授权，注意肖像权与版权风险（054；安全边界同 Skill R-12）。

## 骨架模板

```text
Primary Target & Visuals: {{主体}} {{动作}}; {{景观二读}}.
Format & Look: {{时长}}; {{分辨率}}; {{快门}}; {{传感器/颗粒}}.
Lenses & Filtration: {{焦段/滤镜}}.
Grade / Palette: highlights {{...}}; mids {{...}}; shadows {{...}}.
Lighting & Atmosphere: {{光照与氛围}}.
Location & Framing: {{地点与构图}}.
Sound: {{环境声}}; {{台词（如有）}}.
Optimized Shot List: 1 shot / {{时长}}.
```

## 未核实清单

- 产品已停用（2026-04-26）且 Videos API 已关闭（2026-09-24）：本文件全部内容为历史口径，不得出包；展示示例原文未逐字打开发布页复核。
