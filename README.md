# Video Prompt Studio（视频提示词工作台）

> 一句话创意 / 一段剧本 → **3 轮内**拿到能直接粘贴进视频模型的生产包。
> 不是提示词收藏夹，也不是视频生成器。
>
> 状态：**v1.0.1-beta 预发布**（2026-10-27 发布；外部手测 G6 与平台参数复核 G7 仍未完成，不能称为 GA）。

- 支持方言：Seedance 2.0 / 2.5、Veo 3 / 3.1、MiniMax H3、Kling 4.0、Runway Gen-3、Pika 2.5、Wan2.2、LTX-2/2.3（Sora 2 仅历史口径）、通用
- 交付物：8 节 Markdown 生产包（决策摘要 / 事实层 / 分镜表 / 提示词 / 素材挂图 / 参数 / 自检 / 风险）
- 自带校验：模板、时间轴、台词保真、引用语法隔离、参数泄漏、占位符保真

---

## 它解决什么

社区里两类 Skill 各有硬伤：

| 类型 | 代表 | 问题 |
|---|---|---|
| 单文件手册 | dexhunter、songguoxs | 无状态、无自检、单模型、模板不可组合 |
| 大套件 | Emily2040、zenstory-ai | 29 个子技能 / 561 个文件，单条创作者用不起 |

本 Skill 取中间路线：

1. **3 轮硬契约**——第 1 轮最多 3 个问题且都带默认值；第 2 轮出完整包；第 3 轮只改点名单元。
2. **故事层 / 执行层分离**——换模型时事实层与分镜表逐字不变，只重编译执行层五处。
3. **证据等级进参数表**——A/B/C/D 四档；`C` 级必须写"未核实"，不许包装成官方事实。
4. **脚本只守结构不变量**——审美判断不写成规则，`taste_option` 永不阻断交付。

---

## 发布包与校验和

最新发布是 **v1.0.1-beta** 预发布（GitHub Release，2026-10-27），资产为 `video-prompt-studio-v1.0.1-beta.zip`（230,270 B）。当前 Release 资产只有 zip，没有附 `SHA256SUMS`；仓库根目录的 [`SHA256SUMS`](SHA256SUMS) 提供该 zip 的 SHA-256：

```text
00240eb3d1914d52724142cde2f87260074ab0f8d8e7f46db1192da3fd38f5ea  video-prompt-studio-v1.0.1-beta.zip
```

下载 zip 后放在同一目录校验：

```bash
# macOS / Linux
shasum -a 256 -c SHA256SUMS
# Windows PowerShell
Get-FileHash .\video-prompt-studio-v1.0.1-beta.zip -Algorithm SHA256
```

> Release 说明里写的“同目录 SHA256SUMS”目前没有作为 Release 资产上传；下次发布应把本文件一并上传。不要把它当成已随 Release 提供的文件。

> **已发布 zip 的内容限制（2026-11-19 实测）**：`v1.0.1-beta` 资产由提交 `d18fae6` 打包，包内 `README.md` / `CHANGELOG.md` 仍是旧口径（README 标“v1.0.0 发布候选”，安装命令写 `视频提示词Skill`），包内 `scripts/quality_gate.py --cases` 也是旧版：20 例中 19/20 一致，且 mismatch 返回 0。仓库当前分支已修复这些文档与门禁问题；要按本 README 安装和校验，请用 `git clone` 取当前分支，或等待经批准后重新打包的 Release。不要在旧 zip 内直接照做下节的 20/20 校验。

---

## 安装

```bash
# 1) 取得目录（二选一）
git clone https://github.com/YeFengLeaf/video-prompt-studio.git
# 或解压 Release zip：macOS 系统 unzip 对中文文件名可能失败，用 ditto
# ditto -x -k video-prompt-studio-v1.0.1-beta.zip .
# Linux / Windows 可用 unzip video-prompt-studio-v1.0.1-beta.zip

# 2) 安装到客户端（在 video-prompt-studio 的上一级执行）
cp -r video-prompt-studio ~/.claude/skills/video-prompt-studio

# 或作为项目内技能
cp -r video-prompt-studio <project>/.claude/skills/video-prompt-studio
```

没有安装机制时，直接把 `SKILL.md` 贴进对话，或让 Agent 读这个目录。

**目录名必须与 frontmatter 的 `name` 一致**（`video-prompt-studio`）；发行包顶层目录已经是 `video-prompt-studio`，安装时不要改成旧文档里的 `视频提示词Skill`。部分客户端按目录名索引技能。

依赖：无。脚本只用 Python 标准库（3.9+）。

---

## 快速开始

### 场景 1：只有一句话

```text
你：拍一个雨夜女孩把车票折成纸鹤的 15 秒短片，无台词。
我：（按默认 Seedance 2.0 / 16:9 / 15s 直接出包，或最多问 3 个带默认值的问题）
```

产出：`assets/examples/01_single_story/output.md` 这种 8 节包。

### 场景 2：有剧本对白

```text
你：这段剧本改成 30 秒，台词别动：夜，废弃仓库。男人提灯站在门口，女人被绑在椅子上。
    女人：你到底要把我带到哪里去？
    男人：到了你就知道。
```

产出：`assets/examples/03_script_dialogue/output.md`。

### 场景 3：换模型

```text
你：这条换成 MiniMax H3。
我：只改执行层（结构、引用语法、时间码、参数位置），事实层与分镜表不动；
    给出 output-minimax.md，并说明哪五处变了。
```

产出：`assets/examples/04_model_switch/output-minimax.md`。

---

## 目录

```text
video-prompt-studio/
├── SKILL.md                 入口（3 轮契约 / 路由 / 8 节合同 / 硬边界）
├── references/              按需加载的 11 篇规则 + 方言骨架（10 个模型骨架）
├── templates/               18 个可组合模板（base / styles / shots）
├── assets/
│   ├── examples/            6 组可复现样例
│   └── schemas/             请求 / 计划 / 生产包 JSON Schema
├── scripts/                 6 个确定性校验脚本 + tests/ 回归测试
└── docs/                    调研 / 差距 / 使用验证 / 质检 / 发布计划 / 外部手测协议
```

---

## 校验

以下命令和结果（20/20、mismatch 非零退出）针对**当前仓库分支**；已发布的 `v1.0.1-beta` zip 内是旧脚本，实测 19/20 且 mismatch 退出 0，不能用于复现本节结果。差异见上节“已发布 zip 的内容限制”。

```bash
cd video-prompt-studio
# Windows 建议加 -X utf8；脚本只用标准库
python -X utf8 scripts/check_templates.py                 # 18 个模板 + 229 个占位符
python -X utf8 scripts/check_package.py output.md --model seedance-2.0
python -X utf8 scripts/selftest.py                        # 20 项回归
python -X utf8 scripts/quality_gate.py --cases scripts/fixtures/quality_gate_cases.md  # 20/20，mismatch 非零退出
python -X utf8 scripts/tests/test_quality_gate_exit.py    # 质量门禁退出码回归
```

示例：`check_package.py` 输出

```text
S-01  PASS 8 节齐全
S-02  PASS 3 镜，从 0s 连续排到 15.0s
S-03  PASS 分镜合计 15.0s ≈ 标称 15s
...
汇总：PASS 14 · WARN 0 · FAIL 0
```

退出码：`0` 无 FAIL / `1` 有 FAIL / `2` 文件错误。

---

## 设计来源（只抽结构，不复制文案）

| 来源 | 借了什么 |
|---|---|
| [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0) | Fast Lane、权威顺序、"没看过不许说看过" |
| [dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill) | 约束表、`@` 职责表、能力模式、错误清单 |
| [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | 文件状态、规则四级、只问真实分叉、导出不冒充审批 |
| [liangdabiao/Seedance2-Storyboard-Generator](https://github.com/liangdabiao/Seedance2-Storyboard-Generator) | 资产编号、分镜表列、尾帧衔接 |
| [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance) | 模板四字段、状态机、证据与案例分离 |
| [Square-Zero-Labs/video-prompting-skill](https://github.com/Square-Zero-Labs/video-prompting-skill) | Model Index、参数外置、最短可行时长 |
| [CyberJ0605/cinematic-video-prompt-engineer-skill](https://github.com/CyberJ0605/cinematic-video-prompt-engineer-skill) | 只问故事基础、执行门禁、时长预算、反模式 |

详细对照见 `docs/01_社区Skill调研报告.md`。

---

## 边界（照实说）

- **不生成**图片/视频，不调用付费接口，不上传素材。
- 平台参数来自公开文档与社区转引，**没有逐台实测**；平台改版后需重核。
- 脚本 PASS 只证明文本层结构自洽，**不证明成片好看**。
- 样例是 synthetic 输入，不是真实成片复现。
- Kling 4.0 参数已按官方 4.0 用户指南核实（页面标注 2026-11-04；本库 2026-11-19 复核，值未变）；旧版参数未核实，出包前先确认版本。Runway Gen-3 全表未在官方 Gen-3 文档页复核，已降为 C/未核实；Pika 2.5 全表未在官方页复核，维持 B 转引；Sora 2 API 已关闭（历史口径）。

---

## License

MIT。第三方项目的结构借鉴已在 `docs/01` 标注；未复制任何原始提示词或文案。
