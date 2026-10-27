# 方言骨架 · Wan2.2

> 来源：`references/03_模型适配.md` §12.4（外包调研 REC_20261022_055–058）。骨架文件：只复述档案，不新增参数。证据等级 A（官方仓库 README）。开源推理口径；ComfyUI / Diffusers 集成参数名一致但入口不同。
>
> G7 复核注（2026-10-27）：TI2V-5B 的 5 秒 720P@24fps、`1280*704`/`704*1280`、I2V 尺寸随输入图已在官方模型卡证实；A14B 的 `1280*720`、S2V-14B 的 `1024*704` 及 prompt extension 细节未逐项打开，维持原值，见 `references/03_模型适配.md` §14。

## 档案

- 任务：T2V / I2V / TI2V / S2V（A14B 与 TI2V-5B 尺寸规则不同，055，A）
- 尺寸：T2V/I2V-A14B `1280*720`；TI2V-5B 固定 `1280*704` 或 `704*1280`；I2V 的 `--size` 为画面面积、比例随输入图；S2V-14B `1024*704`；24fps（055，A）
- 参考输入：输入图（I2V）；prompt extension 可纯靠图片扩写（`--prompt ''`，056，A）
- 音频：视任务（本批证据未记录，标未核实）
- 引用语法：自然语言正文；参数走命令行（开源推理）
- 参数位置：提示词外（命令行参数）

## 结构顺序

```text
自然语言提示词正文（可经 prompt extension 扩写）
+ 命令行：--task / --size / --ckpt_dir / --offload_model / --convert_model_dtype / --t5_cpu（按需）
```

## 写法规则

- prompt extension 二选一：`--prompt_extend_method 'dashscope'`（需 API key，key 只从环境变量读，永不写入输出文件；T2V 用 qwen-plus，I2V 用 qwen-vl-max）或 `--prompt_extend_method 'local_qwen'`（本地 Qwen2.5-14B/7B/3B-Instruct 做 T2V，Qwen2.5-VL-7B/3B-Instruct 做 I2V）；`--prompt_extend_target_lang 'zh'`（056）。
- 显存：14B 单卡 ≥80GB；降显存组合 `--offload_model True --convert_model_dtype --t5_cpu`；多卡 FSDP + DeepSpeed Ulysses；TI2V-5B 单卡 24GB 可跑（057）。
- 禁忌：Wan-Animate 任务保持基线权重，不挂 Wan2.2 系 LoRA；replacement 模式可用 `--use_relighting_lora` 官方指定重光照 LoRA（058）。

## 骨架模板

```text
提示词正文：{{主体}} {{动作}}，{{场景}}，{{光照/氛围}}。

命令行（示例，按任务改）：
python generate.py --task t2v-A14B --size 1280*720 --ckpt_dir ./Wan2.2-T2V-A14B --offload_model True --convert_model_dtype --prompt "{{提示词正文}}"
```

## 未核实清单

- 音频能力；ComfyUI / Diffusers 入口的具体参数名（与命令行一致但入口不同，055）；HF 模型卡国内直连可用性。
