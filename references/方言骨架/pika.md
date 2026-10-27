# 方言骨架 · Pika 2.5

> 来源：`references/03_模型适配.md` §12.2（外包调研 REC_20261022_047–051）。骨架文件：只复述档案，不新增参数。证据等级 B（官方转引）；页面域名（pikaslabs.com）未与 pika.ai 官方站交叉验证，全部数值以产品内实测为准。
>
> G7 复核注（2026-10-27）：未打开 Pika 官方文档页，本文件数值未在官方页复核，维持 B 级与 caveat，不得升级，见 `references/03_模型适配.md` §14。

## 档案

- 单条上限：时长档 5 / 10 / 15 / 20 / 25 秒（047，B）
- 画幅：7 种比例 16:9、9:16、1:1、4:5、5:4、3:2、2:3（047，B）
- 分辨率：Free 480p / Standard 720p / Pro Mode 1080p；24fps；MP4 (H.264)（047，B）
- 参考输入：参考图（跨镜头一致性复用同一张参考图与相近提示词结构，048，B）
- 音频：Pika 2.5 不生成音频（音频走 Pikaformance 专门模型，050，B）；Basic 免费档仅非商用
- 引用语法：自然语言；negative prompts 另列排错（048，B）
- 参数位置：提示词外（时长/分辨率/比例走产品档位）

## 结构顺序

```text
A [subject] [action] in [setting], [style/lighting], [camera move], [look], [resolution], [negative prompts]
```

## 写法规则

- 官方模板句式见上；negative prompts 常用：`no morphing, no extra limbs, no blurry faces`（048）。
- 每个 clip 只放一个主体（048）。
- 相机短语：`Slow dolly forward`、`Orbit clockwise 120°`、`Aerial drone shot`、`Slow pan right`、`Tilt down`、Bullet time（配 `no motion blur`）、`Tripod-stable`、`Rack focus`（049）。
- 画面一律 textless（字幕后期加）；避免极快运动与 whiplash 急摇；>25s 叙事多 clip 拼接（050）。
- Pikaframes：把生成末帧作为下一段 conditioning context，每扩展段约 +3–5 秒，最长 25 秒（051）。

## 骨架模板

```text
A {{主体}} {{动作}} in {{场景}}, {{光照/风格}}, {{相机短语}}, film look, {{分辨率档}}.
Negative prompts: no morphing, no extra limbs, no blurry faces.
```

## 未核实清单

- 域名归属（pikaslabs.com vs pika.ai）；渲染耗时与 Turbo 模式数值以产品内实测为准（047）。
