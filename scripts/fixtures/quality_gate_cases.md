# 质量门禁测试用例（20 条）

> 预期分级（EXPECTED）为本文件作者的人工判断，**写于运行 `quality_gate.py` 之前**，未按脚本输出倒推调整。门禁规则见 `scripts/quality_gate.py` 文首。分级口径：BLOCKED = 缺 STYLE LOCK / 参数泄漏 / 锚定职责冲突 / ≥3 个情绪形容词；WARN = 对抗覆盖 ≤3 类、或引用无职责词、或 1–2 个情绪形容词；PASS = 覆盖 ≥4 类且无上述问题。
>
> 格式：`<!-- CASE N EXPECTED=TIER -->` + 一个 ` ```text ` 提示词块。`--cases` 模式按此格式解析。

<!-- CASE 01 EXPECTED=PASS -->
```text
STYLE LOCK：冷白招牌主光，湿地面反光，纪实摄影质感。
女孩站在便利店门口，@Image1 负责女孩身份与雨衣，不得传递背景。
0–5s：她停在门左侧，脚步按节拍放慢。光影跟随光源变化，地面有淡淡投影。
手部特写：FACS 单元素微表情，嘴角单侧轻扬。皮肤写实独立 Pass，纹理词加密度。
Dialogue:
女孩："最后一张了。"
声音：雨声底噪。后期：字幕后期加。
```

<!-- CASE 02 EXPECTED=BLOCKED -->
```text
一个女孩在雨夜的便利店门口，把车票折成纸鹤，放进捐款箱。
镜头慢慢推近，光线很美，氛围感人。
```

<!-- CASE 03 EXPECTED=BLOCKED -->
```text
STYLE LOCK：冷白招牌主光。
女孩把车票折成纸鹤。生成 1080p、16:9 的视频，画质清晰。
@Image1 负责女孩身份。
```

<!-- CASE 04 EXPECTED=BLOCKED -->
```text
STYLE LOCK：暖调室内。
The girl looks happy, then sad, then excited, smiling broadly at the camera the whole time.
```

<!-- CASE 05 EXPECTED=WARN -->
```text
STYLE LOCK：冷白招牌主光。
女孩停在门左侧，动作按节拍数写。光影跟随光源变化。
@Image1 负责女孩身份。后期：字幕后期加。
她看起来 sad，低头折纸鹤。
```

<!-- CASE 06 EXPECTED=BLOCKED -->
```text
STYLE LOCK：冷白招牌主光。
参考：@Image1 负责女孩身份；@Image1 负责背景光线。
女孩把车票折成纸鹤。
```

<!-- CASE 07 EXPECTED=WARN -->
```text
STYLE LOCK：冷白招牌主光。
女孩站在门口，参考 @Image1。镜头缓推，光影自然。
```

<!-- CASE 08 EXPECTED=WARN -->
```text
STYLE LOCK：冷白招牌主光。
动作按节拍数写，情绪写成时间弧。光影跟随光源变化，地面有淡淡投影。
```

<!-- CASE 09 EXPECTED=WARN -->
```text
STYLE LOCK：电影感。
cinematic, film grain, bokeh, anamorphic, 8K 超写实，梦幻光晕，极致唯美。
女孩在雨中回头，画面唯美动人。
```

<!-- CASE 10 EXPECTED=PASS -->
```text
STYLE LOCK：冷白招牌主光，湿地面反光。
Dialogue:
女孩："最后一张了。"
男孩："留着吧。"
台词按短句分轮，标点即呼吸，一镜只容一两轮短句。
动作按节拍数写。光影跟随光源变化。@Image1 负责女孩身份。
```

<!-- CASE 11 EXPECTED=WARN -->
```text
STYLE LOCK：冷白招牌主光。
不要动，没有雨，不要有任何人走动，画面里不要出现车。
女孩站在门口不动。
```

<!-- CASE 12 EXPECTED=PASS -->
```text
STYLE LOCK：冷白招牌主光。
正面状态描述：女孩静止站立，相机随后缓推。动作按节拍数写。
光影跟随光源变化。@Image1 负责女孩身份。后期：字幕后期加。
```

<!-- CASE 13 EXPECTED=WARN -->
```text
STYLE LOCK：冷白招牌主光。
后期：饱和降 10%，颗粒叠加透明度 5%。剪辑：只用前 2 秒稳定段，字幕后期加。
```

<!-- CASE 14 EXPECTED=BLOCKED -->
```text
STYLE LOCK：冷白招牌主光。
女孩把车票折成纸鹤，生成 10 秒 4K 视频。
```

<!-- CASE 15 EXPECTED=PASS -->
```text
STYLE LOCK：冷白招牌主光。
0–5s：女孩走到店门口停下，动作按节拍数写。
5–10s：手部特写折纸鹤，FACS 单元素微表情。
10–15s：纸鹤落入捐款箱，光影跟随光源变化。
@Image1 负责女孩身份。后期：字幕后期加。
```

<!-- CASE 16 EXPECTED=PASS -->
```text
STYLE LOCK：冷白招牌主光，湿地面反光。
@Image1 负责女孩身份与雨衣，不得传递背景。
动作按节拍数写，情绪写成时间弧。光影跟随光源变化。
Dialogue：女孩："最后一张了。"标点即呼吸。
后期：字幕后期加，饱和降 10%。
```

<!-- CASE 17 EXPECTED=WARN -->
```text
STYLE LOCK：冷白招牌主光。
他很悲伤地笑了，低头折纸鹤。动作按节拍数写。
光影跟随光源变化。@Image1 负责女孩身份。后期：字幕后期加。
```

<!-- CASE 18 EXPECTED=PASS -->
```text
STYLE LOCK：冷白招牌主光。
把电影感拆四层按需取用，虚化词配主体保护，分步叠加测试。
动作翻译成生物力学，情绪写成时间弧，动作按节拍数写，减词降载。
FACS 单元素微表情，皮肤写实独立 Pass，纹理词加密度。
空泛否定改正面状态描述，负面清单只保留具体 artifact。
Dialogue：女孩："最后一张了。"标点即呼吸，短句分轮，口型对齐。
光线从画面左侧照进来，光影跟随光源变化，重量词写实。
给素材补来源身份，参考图限定作用域，character sheet 保一致，@Image1 负责女孩身份，不得传递背景。
后期：饱和降 10%，颗粒叠加；剪辑：字幕后期加，混编真实素材。
```

<!-- CASE 19 EXPECTED=BLOCKED -->
```text
女孩在雨夜便利店门口折纸鹤，生成 4K 超清视频，画面极致唯美。
```

<!-- CASE 20 EXPECTED=PASS -->
```text
STYLE LOCK：冷白招牌主光。
@Element1 负责女孩身份，不得传递背景。
动作按节拍数写。光影跟随光源变化。
Dialogue：女孩："最后一张了。"后期：字幕后期加。
```
