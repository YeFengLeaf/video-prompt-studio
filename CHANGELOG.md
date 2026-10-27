# Changelog

本文件记录 `video-prompt-studio` 的版本变更。格式参考 Keep a Changelog；版本号语义化。

## [1.0.1-dev] - Unreleased（2026-10-27，开发中，未发布）

Batch A（P0 修复）与 Batch B（入口瘦身与样例扩充）均已提交到工作副本，未打包、未发布。

### Added

- 内容安全硬边界（`SKILL.md` §0 第 4 条）：真人 / 未成年人 / IP / 品牌的拒绝与通用化替代规则。
- 无代码人工对账清单（`references/06_质量与自检.md` §8）：无 shell 时按 S-01…S-14 逐项人工核对，并在自检节写明「脚本未跑」，不得谎报脚本结果。
- 审稿模式与降级分支（`SKILL.md` §1）：用户说"审一下"时只输出问题清单与最小改动建议；输入严重不足时按默认值出「草案」，不得编造必须保留的事实。
- Fast Lane 精简合同（`SKILL.md` §3）：单条、非专业、无 IP/真人/品牌风险时不建项目状态，8 节仍齐全，第 7 节无 shell 时必须披露「脚本未跑」。
- 外部手测记录表（`docs/06_外部手测记录表.md`）：仅为 G6 协议与空白记录表，尚未执行，见下文 Pending。
- 样例 2 组：`assets/examples/05_kling/`（Kling 方言，参数标 C 级未核实）与 `assets/examples/06_generic/`（通用方言，参数标 D 级按平台填写）；两组输出均 `check_package.py` 14 PASS / 0 FAIL。
- 自测负向用例 2 项（`scripts/selftest.py`）：MiniMax H3 时间码不豁免 S-08 语法隔离、Seedance 2.5 分镜合计与标称时长不一致报 S-03；自测由 13 项增至 17 项，全部通过。

### Changed

- 入口瘦身：`SKILL.md` 由 223 行减至 135 行（Batch A 之后）；§6 模型参数表细节只保留在 `references/03_模型适配.md`，§10 失败症状表只保留在 `references/06_质量与自检.md` §4，入口只留指针与规则；章节编号未变，交叉引用未断。
- Kling 表述统一为实验性、未核实：`SKILL.md` frontmatter 与 §6、`docs/05_发布计划_v1.0.md` 的发布文案；Kling 参数在样例中标 C 级「未核实」，须按平台复核。
- 参数核验日期规则（`SKILL.md` §4 第 6 节）：核验日期填 `references/03_模型适配.md` 的核验日期，超过 30 天写「需复核」，不得当作现行事实。
- 样例计数 4 组 → 6 组（`SKILL.md`、`README.md` 正文与 `说明.md` 的样例表；`docs/05_发布计划_v1.0.md` 仅发布文案 1 行已改，门禁表与质量指标仍为 v1.0.0 历史记录，未改）。

### Batch C（复核后修复，2026-10-27；两模型复核均报 P0，已逐项修）

- R-12 内容安全复核项（`references/06_质量与自检.md` §3、§8）：真人授权 / 未成年人 / IP / 品牌进入复核与人工对账；审稿第一步固定为安全筛查（`references/00_交互协议.md` §9）。
- 审稿模式合同例外（`references/07_输出合同.md` §1、S-01 备注）：审稿输出为两段式，不适用 8 节齐全要求；事实层加「真人授权」记录行；台词表分隔行列数修正为 6 列。
- 新样例结论改为「草案（待素材 / 待确认）」，§5 加素材待提供状态说明，分镜表改为每镜一个主动作并补 R-11/R-12 自检行；通用样例核验日期统一填「未核实」。
- 版本与口径统一：`SKILL.md` frontmatter `1.0.1-dev`；`README.md` 回归 17 项；`说明.md` 当前状态行更新；本条样例计数口径修正为实际改动范围；`docs/06` 方言覆盖改为建议项，不计入 G6 判定。
- Lane 判据（`SKILL.md` §3、`references/00_交互协议.md` §4）：有第三方验收 / 客户交付 / 需回滚证据或合规审查的，一律走 Full Lane 建项目状态。

### 知识库并入（2026-10-27，未发布；决策 D2）

- Added：`references/08_知识库融合.md`（方法论 M1–M10 已去绑定、STYLE LOCK 壳结构、单项目方法卡通用规则摘要）；`references/09_去AI感策略库.md`（八类缺陷对抗词、面部去 AI 感、物理正确性八条）；`references/10_自动化设计注记.md`（VideoGenCLI 架构，设计文档、未实现）；`references/方言骨架/` 10 个模型骨架（只复述档案，不新增参数）。
- Added：`references/02` 追加光线与氛围、自查清单、长度与拆条、电影语言常识、站位行格式；`references/04` 追加首帧六条门槛、多图分工协议、资产命名规范、人物一致性（视觉身份证/方案对比/seed-recipe）；`references/05` 追加台词去 AI 感（14 条禁用词、5 维身份矩阵）与声音一致性（音色身份证、方案对比、克隆纪律）；`references/00` 追加七阶段状态机；`references/06` 追加失败归档流程。
- Added：`references/03` 扩展为 11 模型总表（新增 Runway Gen-3、Pika 2.5、Sora 2 历史口径、Wan2.2、LTX-2/2.3 五档档案）+ 转换引擎五步 + 切换验收三条 + G7 复核记录补遗；方言骨架与总表逐值一致。
- Added：`scripts/check_switch.py`（切换验收）、`scripts/quality_gate.py`（质量门禁，`scripts/fixtures/quality_gate_cases.md` 20 例，一致率 19/20，case 09 已知未调）、`scripts/dialect_converter.py`（故事核逐字保留，未填参数一律 `[UNVERIFIED: to fill in]`；Kling/Veo/MiniMax/Sora 档案已按 G7 更正，Kling 改为 4.0 A 级 `@Element1`）；`templates/styles/style-lock.md`（STYLE LOCK 壳模板）；`selftest.py` 增至 20 项，全部通过。
- Changed：Kling 表述由「实验性、未核实」更正为 Kling 4.0 已核实（A 级，官方 4.0 用户指南，2026-10-27 复核）：`SKILL.md` frontmatter 与 §6、`README.md`、`说明.md`；`docs/05_发布计划_v1.0.md` 为 v1.0.0 历史记录，未改。`SKILL.md` 入口 135 行 → 143 行（≤150 行）。
- Changed：示例说话人去绑定：`references/05` 的示例名替换为通用占位「角色A」；`说明.md` 的本地源目录绝对路径泛化。
- Excluded（未并入）：融合映射表、调研记录 JSON、采集管线代码、失败案例原文、单项目方法卡原文、源项目专用壳 02–05；采集管线仅在 `references/10` 留一条未实现注记。

### Pending（仍未完成，不得声称已做）

- 外部手测（G6）：`docs/06_外部手测记录表.md` 仅为协议，截至 2026-10-27 尚未执行，无任何手测记录，G6 未通过。
- 平台参数复核（G7）：部分完成——Seedance / Veo / MiniMax H3 / Kling 4.0 / Sora 停用状态已按官方文档复核（见 `references/03` §11/§14）；Runway Gen-3、Pika 2.5 等 6 项未确认，G7 未通过。

## [1.0.0] - 2026-10-20

### Added

- 入口 `SKILL.md`：3 轮契约、输入路由、8 节输出合同、四条规则分级、模型方言速查、按需加载表、失败修复表、真实性边界。
- `references/` 8 篇：交互协议、输入路由、镜头语言、模型适配、素材与引用、声音与台词、质量与自检、输出合同。
- `templates/` 17 个：5 个 base（剧情/广告/MV/纪录/非写实）、6 个 styles（写实/水墨/赛博/纸艺/动漫/定格）、6 个 shots（建立/正反打/跟拍/一镜/产品环绕/变身）。
- `assets/examples/` 4 组：一句话创意、Veo 产品广告、剧本对白、换模型（MiniMax H3）。
- `assets/schemas/` 3 个：请求、项目计划、生产包 JSON Schema。
- `scripts/` 3 个：`check_package.py`（S-01…S-14）、`check_templates.py`、`selftest.py`。
- `docs/` 3 篇：社区 Skill 调研报告、差距分析与改造方案、使用与验证。

### Fixed（发布前质检，2026-10-20）

- 修复 `check_package.py` 多段包误判：S-02 现在按段分组，各段从 0s 独立核对。
- 修复同一素材被引用多次时 S-07 误报（改为统计不同引用 token）。
- 修复块外占位符漏检：S-10 现在检查第 1–6 节，不再只看提示词块。
- 修复错误作用镜头只警告：引用不存在的镜号现在 FAIL；空范围仍为 WARN。
- 修复 5 列台词表被跳过：没有「结论」列也能识别台词并核对逐字进出。
- 新增分镜表表头校验，列错位时直接 FAIL，不再静默误判。
- 补齐 `LICENSE` 与 `assets/schemas/plan.schema.json`（原 `references/00` 的引用为断链）。
- 修正 Veo 时长表述（原“8s 级”无来源，改为“按平台，本库未记录上限”）。
- 文档命令统一为 `python -X utf8`，并注明在 Skill 根目录执行。

### Design notes（哪些来自社区、哪些是自创）

**借来的结构**

- Fast Lane、权威顺序、"没看过不许说看过" ← Emily2040/seedance-2.0。
- 约束表、`@` 职责表、能力模式 ← dexhunter/seedance2-skill。
- 文件状态、规则四级、只问真实分叉 ← zenstory-ai/drama-skills。
- 资产编号、分镜表列、尾帧衔接 ← liangdabiao/Seedance2-Storyboard-Generator。
- 模板四字段、状态机、证据与案例分离 ← LearnPrompt/awesome-seedance。
- Model Index、参数外置、最短可行时长 ← Square-Zero-Labs/video-prompting-skill。
- 只问故事基础、执行门禁、时长预算、反模式 ← CyberJ0605/cinematic-video-prompt-engineer-skill。

**自创**

- 3 轮硬契约 + 第 3 轮"只改点名单元"的补丁协议。
- 8 节固定输出合同（决策摘要 / 事实层 / 分镜表 / 提示词 / 素材挂图 / 参数 / 自检 / 风险）。
- 参数表内嵌证据等级 A/B/C/D。
- 故事层 / 执行层分离的换模型验收（事实与分镜逐字不变）。
- 只守 `structural_invariant` 的确定性脚本；`taste_option` 永不阻断。

### Known limits

- 平台参数未逐台实测；Seedance 2.0/2.5 上限、Veo 时长、Kling 语法均需按平台复核。
- 情绪、口型、物理、材质只能人工看片判断。
- 样例为 synthetic，不是真实成片复现。
- 多集/序列只提供状态文件约定，未提供自动化工具。

### Verification

- `python -X utf8 scripts/selftest.py`：13/13 通过（含 5 项 QC 回归）。
- 17 个模板、223 个占位符全部保真。
- 4 个样例 `check_package.py` 均 14 PASS / 0 FAIL。
- 负向测试：Veo 校验 Seedance 包报 S-08；残留 `{{}}` 报 S-10；多段/重复引用/错误镜号各有回归。
