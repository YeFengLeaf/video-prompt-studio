---
id: styles/style-lock
layer: styles
useWhen: 需要把全片摄影基调锁死为一段固定不变的英文口令时；每个镜头粘贴在开头，全片不换
models: all
---

# STYLE LOCK 壳

> 结构来源：`references/08_知识库融合.md` §1（方法论 M1，已去绑定）。证据等级 C 级（项目内约定，未核实当前模型表现）。
> 用法：三个要素（导演 / 胶片 / 工艺）按题材替换，不得照抄示例壳当通用默认值。换镜头换段，LOCK 不换。

```text
[STYLE LOCK]
Shot on {{film_stock}} film stock + analog film grain visible +
practical light only + {{director}} cinematography + {{director}} painterly
desaturation + photochemical film texture + slight halation + organic film noise
+ heavy atmospheric haze + dust particles + film print look not digital cinema +
photorealistic film still aesthetic + NOT 3D render.
```

## 填写规则

- `{{film_stock}}`：写胶片型号，如 `35mm Kodak Vision3 500T`；不要只写「胶片感」。
- `{{director}}`：写一位导演名（风格坐标），前后两次须为同一人；不要堆三位以上导演。
- `{{process}}`（如需）：化学工艺/后期工艺，如 `photochemical film texture`；没有就不写，不要凑。
- 壳内必须保留 `NOT 3D render` 防跑偏句；写实段落滑向 3D 质感时先查壳有没有被改掉。
- 与画质基线句并用时不得重复堆叠同义画质词（见 `references/09_去AI感策略库.md` 类别 1）。

## 失败风险

- 形容词堆叠（cinematic / 8K / 超写实并列）会把画面推糊：风格词拆四层按需取用，见 `references/09_去AI感策略库.md` 类别 1。
- 一镜一个型号：胶片型号须与 STYLE LOCK 一致，不得一镜换一个。

## 禁止

- 禁止把示例壳（Kodak Vision3 500T / Christopher Doyle / Wong Kar-wai）不经替换直接当通用默认值。
- 禁止在壳里写剧情、角色名、台词——壳只锁摄影基调。
- 禁止删 `NOT 3D render` 后声称「已锁风格」。
