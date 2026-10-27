# 方言骨架 · Runway Gen-3

> 来源：`references/03_模型适配.md` §12.1（外包调研 REC_20261022_041–046）。骨架文件：只复述档案，不新增参数。证据等级 A（官方资源页），REC_046 单项 C、未核实。公式以 Gen-4.5 验证为主，旧模型对复合运动词遵循度弱。
>
> G7 复核注（2026-10-27）：未找到 Gen-3 的官方文档页，本文件数值未在官方页复核，维持原等级；Gen-4/4.5 的数值不得用来证实 Gen-3，见 `references/03_模型适配.md` §14。

## 档案

- 单条：5 秒级短 clip 拼接（044，A）
- 画幅/分辨率：按平台（未在本批证据中记录确切值，不得编造）
- 参考输入：图/视频参考（面板交互）；Motion Brush 涂刷区域（045，A）
- 音频：视入口（本批证据未记录，标未核实）
- 引用语法：自然语言 + 面板（无 `@` 式语法）
- 参数位置：提示词外；面板参数不进提示词（043，A）

## 结构顺序

```text
[景别] + [角度] + [运动 + 方向 + 速度] + [主体与动作] + [镜头/光影] + [光照/氛围] + [揭示]
```

## 写法规则

- 每个运动词必须带速度或时长修饰；单镜只可靠执行一个运动，多段运动分镜拼接（041）。
- 静态镜头用官方锁定句：`The camera is entirely motionless for the duration of the scene, with movement only occurring from the subject.`（042）。
- 运动路径只保留一个真相源：面板管路径时 prompt 不写对立运镜词，只写风格、情绪与叙事目的（043）。
- 速度只用 slow / gradually / gently / steadily / deliberately；禁用 quickly / rapidly / fast / suddenly（044）。
- 总长 20–50 词；光照必须带方向 `from [direction]`；重量词 `Heavy [object] moves slowly` / `Light [object] drifts` / `With weight`（044）。
- Motion Brush 与 Camera Control 是两个通道，同区域避免重复指定（045）。
- Camera Motion 面板项（Pan/Tilt 等）：**未核实**（046，C，第三方教程，UI 可能已变）。

## 骨架模板

```text
{{景别}}, {{角度}}, {{速度}} {{运动}} over {{时长}}, on {{主体}} {{动作}}, {{焦段}} lens, {{光照方向}} lighting, {{氛围}}.
The {{运动}} reveals {{揭示}}.
Static lock（如需锁机）: The camera is entirely motionless for the duration of the scene, with movement only occurring from the subject.
```

## 未核实清单

- 画幅/分辨率确切档位；音频能力；Camera Motion 面板当前 UI 项（046）。
