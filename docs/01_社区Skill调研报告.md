# 社区 AI 视频提示词 Skill 调研报告

- 调研日期：2026-10-20（Asia/Shanghai）
- 调研人：skill-architect
- 样本：GitHub 搜索结果中筛 12 个，深读 7 个，补充对照 3 个
- 方法：GitHub REST API 查元数据 → 无 blob 浅克隆 + 稀疏检出（只取文本文件）→ 程序化提取文件树/SKILL.md 分节/占位符统计 → 定点精读 → 抓 issue/PR
- 证据分级：沿用本库 `提示词产品/知识资产准入门禁_v0.1.md` 的 E0–E5

> **本报告的红线**：所有结论都对应到具体仓库、文件路径与行号；star 数、推送时间是 2026-10-20 API 实测；没有安装运行过的，不写成"实测可用"。

---

## 1. 调研渠道与可用性

| 渠道 | 实测 | 本次用法 |
|---|---|---|
| `api.github.com` | 200 | 搜索、元数据、文件树、issue |
| `github.com` + `git clone` | 200 | 无 blob 浅克隆 + 稀疏检出 |
| `raw.githubusercontent.com` | 超时 | 放弃；改用 API contents / git 对象 |
| `docs.claude.com` / `claude.com` | 200 | 规范交叉核对（未作为主要证据） |
| `skillsmp.com` / `smithery.ai` / `clawhub.ai` | 200 | 分发形态参考 |
| `google.com` / `reddit.com` / `x.com` | 超时 | 未使用，不编造这些平台的反馈 |
| `bilibili.com` / `juejin.cn` / `cn.bing.com` | 200 | 中文社区补充 |

搜索词与结果量：`seedance+skill` 1025 个仓库；`seedance+in:name` 2001 个；`video+prompt+in:name+skill` 48 个；`kling+prompt+skill` 55 个。

**关于"Seedance 2.0 skill os"**：用 `seedance+skill+os`（7 条）与 `"skill os"+in:name`（140 条）均未找到同名仓库；`"skill os"` 类最高星是 `ynulihao/AgentSkillOS`（617★），与视频无关。最接近"Skill OS"形态的是下表 S1（29 个子技能 + 路由 + 门禁）。

---

## 2. 样本总表（API 实测）

| # | 仓库 | ★ | 最近推送 | 许可 | 检出文本 | SKILL.md | 入口形态 |
|---|---|---:|---|---|---:|---:|---|
| S1 | [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0) | 7844 | 10-03 | MIT | 225 | 29 | 套件 + 路由 |
| S2 | [dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill) | 4358 | 09-19 | MIT | 5 | 2 | 单文件手册（双语） |
| S3 | [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) | 3114 | 10-20 | MIT | 356 | 12 | 流水线套件 + 状态文件 |
| S4 | [liangdabiao/Seedance2-Storyboard-Generator](https://github.com/liangdabiao/Seedance2-Storyboard-Generator) | 2632 | 09-21 | 无 | 93 | 1 | 单技能 + references |
| S5 | [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance) | 2174 | 10-20 | MIT | 154 | 15 | 市场 + 题材技能矩阵 |
| S6 | [Square-Zero-Labs/video-prompting-skill](https://github.com/Square-Zero-Labs/video-prompting-skill) | 185 | 08-25 | Apache-2.0 | 19 | 1 | 单入口 + 每模型参考 |
| S7 | [CyberJ0605/cinematic-video-prompt-engineer-skill](https://github.com/CyberJ0605/cinematic-video-prompt-engineer-skill) | 131 | 10-15 | MIT | 19 | 1 | 单文件 44KB + 参考库 |
| A1 | [songguoxs/seedance-prompt-skill](https://github.com/songguoxs/seedance-prompt-skill) | 2945 | 02-12 | 无 | 3 | 1 | 单技能 23KB |
| A2 | [OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill) | 767 | 09-27 | MIT | — | 32 子技能 | 子技能矩阵 |
| A3 | [ZeroLu/awesome-seedance](https://github.com/ZeroLu/awesome-seedance) | 2758 | 10-20 | MIT | — | 0 | 资源集合（非 Skill） |

> 「检出文本」= 稀疏检出后实际取得的文本文件数（md/json/yaml/txt）；仓库总文件数（含图片/视频/SVG）见各节"规模"。两者不是一回事。

---

## 3. 七个深读样本

### S1 Emily2040/seedance-2.0 —— "Skill OS"形态的极限样本

**规模**：343 个文件（稀疏检出 225 个文本文件）、29 个 `SKILL.md`、根 `SKILL.md` 154 行/29.5KB；`version: 6.7.0`；CI 有 `validate-skills.yml`。

**信息架构**（`SKILL.md:17-153`）
- 根技能只做四件事：路由、查事实、保护引用、保持提示词紧凑。
- 九个 H2：`Soul` / `Agent Trust Boundary` / `Fast Lane` / `Director's Read Gate` / `Operating Loop` / `Authority Order` / `Sequence Gate` / `Load Map`。
- `Operating Loop` 13 步（intake → source gate → professional gate → sequence gate → mode gate → capability check → reference authority → multilingual → safety → direction → prompt build → quality pass → repair loop）。
- `Load Map` 35 行"情境 → 加载哪些文件"，是渐进披露的极端版本。
- 子技能按关注点拆：camera / motion / lighting / audio / characters / continuation / antislop / filter / copyright / interview / sequence / troubleshoot / examples-zh/ja/ko…

**提示词策略**
- `Director's Read` 强制先做"导演读解"（戏剧功能、可见载体、被压制的行为、不可转移的细节），再编译成提示词。
- 参考权威按维度分配：每个 target × dimension 只能有一个 owner（`SKILL.md:65`）。
- 物理规则：不把"非自愿结果"写成终点（衣角被门夹住、滑倒、洒出），模型会把它演成主动行为（`SKILL.md:70`）。

**工程实现**
- 每个运行时链接都是相对 Markdown 链接，静态校验保证不越出技能目录。
- 有 `validation/`、`schemas/`、`evals/`、`data/`，CI 校验。
- `agents/openai.yaml` 提供跨客户端适配。

**用户体验**
- `Fast Lane`（`SKILL.md:31-40`）明确承认"大多数请求只是一条短片"，跳过全套门禁；一旦出现 IP/真人/品牌/平台事实问题立即升级。
- `Authority Order`（`SKILL.md:75-95`）9 层冲突裁决，并要求说明"牺牲了什么"。
- 诚实规则："Never state or imply that you viewed…"（`SKILL.md:52`）。

**优点**
1. 把"默认走快路、出问题才升级"写成了制度，而不是口号。
2. 冲突裁决顺序可直接复用：安全 > 已核实边界 > 用户硬约束 > 素材契约 > 连续性 > 物理 > 镜头 > 风格 > 自身默认。
3. 状态与谱系（`project_id`/`clip_id`、accepted state overrides planned state）适合多集生产。
4. 对"没看过就不能说看过"的坚持，正是多数视频 Skill 缺的诚实底线。

**缺陷**
1. **入口认知负担过大**：154 行路由 + 35 行 Load Map + 13 步循环，单条用户读完已经失去耐心。
2. Fast Lane 仍要求先加载 `Director's Read`，快路并不真的"快"。
3. 29 个子技能 + 大量 references，维护成本极高；版本号 6.7.0 说明仍在高频重构。
4. 没有面向单条用户的确定性校验脚本（至少根目录未见）。

**可借鉴**
- Fast Lane 的判定条件与升级信号。
- Authority Order 的分层与"说明牺牲"。
- Load Map 的"情境 → 文件"写法（我们会压缩到 9 行）。
- 参考权威"每维度一个 owner"。

**不借**
- 29 子技能矩阵、13 步全量门禁、对单条用户的门禁前置。

---

### S2 dexhunter/seedance2-skill —— 单文件手册的最佳实践

**规模**：8 个文件；`SKILL.md` 378 行/15.7KB，`zh/SKILL.md` 17.9KB；MIT。

**信息架构**（`SKILL.md` 12 个 H2）
`System Constraints` → `Core Syntax: The @ Reference System` → `Prompt Structure Blueprint` → `Camera Language Reference` → `Capability-Specific Prompt Patterns`（10 种）→ `Style and Quality Modifiers` → `Workflow` → `Common Mistakes` → `Example Prompt Templates`（4 个）→ `Interaction Instructions`。

**提示词策略**
- 约束表硬编码平台边界：图 ≤9、视频 ≤3（单条 2–15s）、音频 ≤3、合计 ≤12；输出 4–15s、480p–720p；禁止真人脸（`SKILL.md:14-31`）。
- `@` 引用按用途给 13 种句式（首帧/尾帧/角色/场景/运镜/动作/特效/节奏/音色/BGM/音效/服装/产品）（`SKILL.md:46-70`）。
- 结构公式：主体 + 场景 + 动作 + 运镜 + 时间分段 + 转场 + 声音 + 风格（`SKILL.md:74-93`）。
- 10 种能力模式：一致性、运镜复刻、特效复刻、延长、编辑、卡点、对白、一镜到底、电商、科普（`SKILL.md:135-260`）。

**工程实现**
- 无脚本、无状态、无校验；纯 Markdown。
- 双语（英/中）各自完整，不是机翻。

**用户体验**
- `Interaction Instructions` 仍是"先问类型/素材 → 再起草 → 解释 → 给变体"（`SKILL.md:369-378`），2 个问题起步。
- 模板是**完整 prompt**（产品广告 15s、短剧 15s、舞蹈 13s、风景 15s），复制即用，但不能组合。

**优点**
1. 约束表 + `@` 职责表是同类里最清楚的，读完就能写。
2. 按"能力"而不是按"题材"组织模式，覆盖率高。
3. 常见错误 7 条（模糊引用、冲突指令、超载、漏 `@`、忽略音频、忘记时长、真人脸）直击失败点。
4. 双语单文件，分发成本最低。

**缺陷**
1. 只是手册：无状态、无素材作用域、无自检、无多模型。
2. 交互仍要求用户先报素材清单；对"只有一句话"的用户不友好。
3. 平台数字没有来源与时效标注，平台改版即过期。
4. 模板不可组合，10 种模式之间没有拼装规则。

**可借鉴**
- 约束表 + `@` 职责表 + 能力模式 + 错误清单。
- 极简单文件入口（我们保留入口轻量，但把深度放进 references）。

**不借**
- 把完整 prompt 当模板；无来源的数字写成确定事实。

---

### S3 zenstory-ai/drama-skills —— 流水线 + 文件状态 + 规则分级

**规模**：561 个文件（稀疏检出 356 个文本文件）、12 个 `SKILL.md`；`skills/short-drama` 是路由，另有 develop / write / assets / image-prompts / storyboard / video-prompts / produce / edit / review / novel-analyze；`maintainers/skills/short-drama-knowhow` 单独放置。

**信息架构**
- **creator-first 五文档**：每集维护 `剧本.md`、`视觉设定.md`、`分镜.md`、`图片提示词.md`、`视频提示词.md`，不建并行结构化真相（`skills/short-drama/SKILL.md:11-15`）。
- 路由表把"用户要做什么"映射到唯一 owner（`SKILL.md:17-32`）。
- `.agents/notes/` 记录架构决策；`.clawhub/` 是分发清单；`tests/` + `evaluations/` 是验证层。

**提示词策略**
- 规则四级（`.agents/notes/implemented/architecture/2026-07-16-rule-tiers-and-script-boundary.md`）：
  - `structural_invariant`：本地可证明的矛盾，校验器可阻断；
  - `reviewed_invariant`：语义义务，由 reviewer 引用证据判定；
  - `craft_default`：通常有帮助，创作者说明理由即可覆盖；
  - `taste_option`：表达选择，不得单独阻断。
- 脚本只做确定性工作，不把创作判断写成规则代码。
- 明确反对：用固定字数/比例/数量配方当质量门槛；用关键词/正则匹配创作语义。

**工程实现**
- `project_tool.py init/publish/accept/set-authority/export`，JSONL 决策记录 + 权威字段。
- `dashboard_server.py` 本地创作台（Python 标准库 + 原生前端）。
- `export` 附 `manifest.json` + `checksums.sha256`，且 `asserts_approval` 恒为 false（`SKILL.md:159-160`）。
- 技能自包含：改动只落在自己目录，跨技能按名字路由。

**用户体验**
- "只有真实创作分叉才询问；不要拿 schema、目录、事务或检查器询问创作者"（`SKILL.md:47`）——本次调研里最好的一条交互原则。
- 遇到缺参考图时给三条路，而不是只给"生成图/文生视频"两个选项（`SKILL.md:52-55`）。
- 初始化命令较重（`init --title ...`），对纯文本用户有门槛。

**优点**
1. 文件即状态，跨会话可续；产物所有权清楚。
2. 规则四级是防止"审美法条化"的成熟方案，可直接迁移。
3. 交互原则克制且具体。
4. 导出不冒充审批，诚实度最高。

**缺陷**
1. 极重：561 文件、Python 工具、Dashboard、JSONL 决策链；单条创作者用不上。
2. 安装与运行门槛高（脚本、Python 版本、ClawHub）。
3. 中文长文档为主，英文入口较弱。

**可借鉴**
- 五文档状态 → 我们压缩成 4 个文件（brief/decisions/continuity/plan）。
- 规则四级 + 脚本边界。
- "只问真实分叉"。
- 导出快照不等于审批。

**不借**
- Dashboard、project_tool 全套、JSONL 决策链。

---

### S4 liangdabiao/Seedance2-Storyboard-Generator —— 中文本土化最强，但交互最重

**规模**：112 个文件（稀疏检出 93 个文本文件）；`SKILL.md` 475 行/20.8KB；`references/` 5 篇（Seedance 手册 23.9KB、优化分镜、声音设计、好剧本、故事转视频脚本）；6 个完整项目样例（林冲/聂风/项链/鲁智深/司马光/岳阳楼记/崖山海战）。

**信息架构**
- 核心工作流"文-资-视-剪"（`SKILL.md:10-20`）。
- 剧本格式：`△` 镜头描述、对白、OS/VO、闪回、字幕（`SKILL.md:115-120`）。
- 资产编号 C/S/P（角色/场景/道具），每个角色多角度。
- 分镜表列：分镜号 | 景别 | 镜头运动 | 画面内容 | 台词 | 预估时长 | 分镜出图提示词（`SKILL.md:403-405`）。
- 输出清单 6 项（剧本/角色资产/场景资产/道具资产/分镜提示词/集数衔接）（`SKILL.md:436-445`）。

**提示词策略**
- 分镜规则 9 条：文学描写转可拍摄镜头、每镜 2–5s、每集 13–15s、景别变化、动作用 `→`、对白标声音来源、正反打、空镜转场、只写明确音效（`SKILL.md:407-417`）。
- 质量自检分格式/内容/技术三类（`SKILL.md:449-472`）。
- 尾帧描述用于集间衔接。

**工程实现**
- 纯 Markdown + references；无脚本、无校验、无状态机。
- 无 LICENSE 文件 → 不能直接复用其文案。

**用户体验**
- 第 2 步就要问 5 个参数：视觉风格、时长、平台画幅、基调、核心梗（`SKILL.md:40-50`）。
- 固定 2–5s/镜、13–15s/集、3–7 镜/集，属于把经验写成硬规则。

**优点**
1. 中文短剧生产语汇最完整（△、OS/VO、尾帧、集间衔接）。
2. 资产编号与分镜表列可以直接被生产团队使用。
3. 6 个完整项目样例，比空模板有说服力。
4. 自检分三类，可操作。

**缺陷**
1. 5 个前置问题 + 固定镜数/时长，与"3 轮内出包"直接冲突。
2. 无脚本、无参数表、无多模型。
3. 无许可，不能复制文案。

**issue 证据**（这是本次最有价值的一手反馈）
- #1「Seedanc2.0在哪里用啊？」——用户不知道在哪个平台跑（`2026-02-26`）。
- #6「流程方面的问题」——用户问"有没有一键式的体验"，作者答"是手动"（`2026-04-01`）。
- #7「生成的视频呢？看下质量如何」——作者只能给 B 站主页（`2026-04-22`）。

→ 三条都指向同一个缺口：**Skill 只交付文本，不交付"能跑起来的路径 + 可核对的证据"**。

**可借鉴**
- 资产编号 C/S/P、分镜表列、尾帧衔接、自检三类、样例驱动。

**不借**
- 5 问前置、固定镜数/时长、无来源的经验数字。

---

### S5 LearnPrompt/awesome-seedance —— 证据驱动 + 题材矩阵

**规模**：193 个文件（稀疏检出 154 个文本文件）、15 个 `SKILL.md`；`README.md` 136KB（中/日/英三份）；`.claude-plugin/marketplace.json`；`agents/skills/seedance-*` 按题材拆（3D 卡通、汽车、史诗奇幻、时尚、美食 ASMR、游戏 UI 直播、恐怖悬疑、梗图喜剧、宠物、生产工作流、提示词库、复古 DV、运动极限、分镜九宫格、旅行城市漫步）。

**信息架构**
- 两类技能：**题材技能**（useWhen 命中具体片子类型）+ **生产工作流**（端到端）。
- `seedance-production-workflow/SKILL.md` 43 行：Route → Prepare → Generate and inspect → Finish。
- 状态机：`planned` / `assets-ready` / `submitted` / `generated` / `reviewed`；"Never call a prompt or an unrun storyboard a completed video"（`SKILL.md:8`）。
- 要求写 `brief.md`、`reference-map.md`、`plan.json`，并有 `scripts/validate_plan.py` 检查时长/顺序/缺引用（`SKILL.md:25-29`）。

**提示词策略**
- `seedance-prompt-library/SKILL.md`：模板带 `useWhen` / `structure` / `guidance` / `pitfalls`；"空块就是提示词变笼统的地方"（`SKILL.md:16`）；没有匹配模板就明说，不强套（`SKILL.md:14`）。
- 输出：成品 prompt + 用了哪个模板 + 案例链接（`SKILL.md:20-24`）。
- 语言跟随用户；模板双语。

**工程实现**
- `data/style-library.json` + `scripts/generate-skill-reference.mjs` 生成参考文件，不手改。
- `validate_plan.py` 是本次 7 个样本里唯一的"计划校验脚本"。
- `evaluations/`、`submissions/`、PR 模板。

**用户体验**
- 先识别"要什么类型的镜头"，只在真正歧义时问（"产品视频"可能是广告环绕也可能是 UGC 测评）。
- 题材技能让用户按"我要拍什么"选，而不是按"我要填什么"选。

**优点**
1. 证据链最完整：案例可追溯到原帖，有跨模型复测记录。
2. 模板四字段（useWhen/structure/guidance/pitfalls）是可组合模板的正确形态。
3. 状态机 + "不把提示词说成视频"直接可借。
4. 有唯一的计划校验脚本，说明作者知道"结构要能机器验"。

**缺陷**
1. 15 个题材技能是"分发"而非"统一管线"，跨题材项目仍要人工搬。
2. `prompt-library` 依赖外部站点数据，离线不可用。
3. README 136KB，入口信息过载。
4. 单条用户仍要先选题材。

**可借鉴**
- 模板四字段；状态机；案例与模板分离；输出带"用了哪个模板"。

**不借**
- 15 个题材并列；依赖外部站点。

---

### S6 Square-Zero-Labs/video-prompting-skill —— 多模型适配的最佳结构

**规模**：26 个文件（稀疏检出 19 个文本文件）；`video-prompting/SKILL.md` 109 行/7.9KB；`references/models/` 下 10 个模型目录：Ovi、Veo 3/3.1、Wan 2.2、Wan Animate 2、Seedance 2.0、Seedance 2.5、MiniMax H3、LTX-2、LTX-2.3、LTX-2.5；各模型目录下有 `prompting.md`，部分附 `example_prompts/`。

**信息架构**
- 一个入口 + 两个索引：`Model Index`（模型 → 文件）、`Workflow Index`（角色设定图工作流）。
- 加新模型 = 建 `references/models/<model>/prompting.md` + 在索引加一行（`SKILL.md:35`）。
- 明确"这个文件是入口：路由、问最少的问题、按格式起草"（`SKILL.md:16`）。

**提示词策略**
- 全局规则：**不把模型名/版本/时长/画幅/分辨率/参数名写进最终提示词**，除非该模型的 schema 明确要求时间码（`SKILL.md:43`）。
- 时长只作内部规划；参数单独一行；i2v 把图当视觉锚，只写变化（`SKILL.md:44-46`）。
- 输出默认只给最终 prompt 文本，单行；MiniMax H3 / Seedance 2.5 / LTX-2.5 是有理由的例外（`SKILL.md:99-104`）。
- 推荐"能装下动作的最短时长"，不默认拉满（`SKILL.md:60`、`:73`）。

**工程实现**
- 无脚本、无状态、无自检；纯参考库。
- 10 个模型文件中有 9 个带官方来源链接（Ovi 的 `prompting.md` 没有）；抽查的 Seedance 2.0（火山引擎）、Seedance 2.5（官方页 + fal/Dreamina）、Veo（Google Cloud）、H3（HuggingFace）均带链接。

**用户体验**
- 先问模型（或给支持列表），再确认输入模式（t2v/i2v/keyframe/reference/edit/extend）。
- 用户没给模型时必须问，这是无法默认的硬信息。
- 输出极简，不解释，适合熟练用户。

**优点**
1. 多模型适配的目录结构最干净，可直接作为我们的模型层骨架。
2. 参数外置规则统一，避免"把平台参数写进内容"的常见错误。
3. 每个模型有官方来源，证据意识强。
4. "最短可行时长"反行业默认，正确。

**缺陷**
1. 只做 prompt，不做故事结构、资产挂图、自检、状态。
2. 依赖用户知道模型名；新手门槛高。
3. 10 个模型深度不均（H3 23KB，Ovi 可能很薄）。
4. 没有"故事层/执行层分离"的验收方法。

**可借鉴**
- Model Index + 每模型方言文件；参数外置；最短可行时长；输出极简。
- 官方来源链接的写法。

**不借**
- "只做 prompt"的定位（我们要生产包）。

---

### S7 CyberJ0605/cinematic-video-prompt-engineer-skill —— 交互克制与执行门禁

**规模**：27 个文件（稀疏检出 19 个文本文件）；`cinematic-video-prompt-engineer/SKILL.md` 317 行/44.6KB；references 含运镜库 14KB、追车覆盖、续写工作流、导演模块、风格模式、参考图优先工作流、竖屏适配；`PROMPT_VERSION.md` 37KB；4 个 demo mp4。

**信息架构**
- `Execution Decisions and Agent Capabilities` → `Continuity and Director Delivery Gate` → `Default Workflow` → `Execution Gates and Failure Recovery` → `Duration Rules` → `When to Ask Questions` → `Output Format` → `Cinematic Translation Rules` → `Anti-Patterns` → `Safety`。
- 参考库按"任务证据 → 读哪节"路由（`SKILL.md:264-278`）。

**提示词策略**
- **何时问**：只在"故事基础未解决"时问一句；明确不问道具/镜头/灯光/声音/微表情（`SKILL.md:196-204`）。这是本次调研最接近"3 轮契约"的设计。
- 执行门禁表：触发条件 → 第一反应 → 仍不行怎么办（`SKILL.md:161-178`）。
- 时长规则：按可播放内容定时长，单条上限 30s；字符上限 1300（≤15s）/2400（16–24s）/3000（25–30s）；关键台词至少提前 1–2 秒结束留反应（`SKILL.md:182-194`）。
- 输出 workshop 模式：`【剧情诊断】→【电影化改写策略】→【最终视频提示词】`（`SKILL.md:216-232`）。
- 反模式 12 条：逐句分镜、把多个转折塞进 30s、堆运镜、跨镜重置、默认生成所有参考图、用"电影感"代替具体光向等（`SKILL.md:284-300`）。
- 参考图与计划不符时，**以可见图为准**，不静默继承计划（`SKILL.md:174`）。

**工程实现**
- 无脚本；靠长文档 + 参考库。
- demo 视频 55MB，仓库偏重。

**用户体验**
- 输出先给诊断，用户可在"看片前"纠正理解，减少返工。
- 44KB 单文件一次加载偏重。

**优点**
1. "只问故事基础"的克制，是 3 轮契约的直接证据。
2. 执行门禁表把"失败时怎么办"写成了可执行分支。
3. 时长/字符预算具体，且有"留反应时间"这种专业细节。
4. 反模式清单质量高。

**缺陷**
1. 单模型为主（提 Kling/Seedance/Veo，但无分模型方言表）。
2. 44KB 单文件，上下文成本高。
3. 无自动校验；诊断与成品混在一个输出里。

**可借鉴**
- "只问故事基础"；执行门禁表；时长/字符预算；反模式；"以可见图为准"。

**不借**
- 44KB 单文件；无脚本。

---

## 4. 三个补充样本

| 样本 | 结构 | 值得记的一点 | 问题 |
|---|---|---|---|
| A1 songguoxs（2945★） | 单 `SKILL.md` 580 行/23.7KB，`@图片1` 官方命名，三种输出模式（简单/完整/超长） | 中文平台细节最细；输出模式按复杂度分层 | 必问时长；一次给 2–3 个版本，选择过载；无自检 |
| A2 OSideMedia（767★） | 32 个子技能 | 子技能覆盖广，按平台/风格拆 | 碎片化，无统一管线；维护成本高 |
| A3 ZeroLu/awesome-seedance（2758★） | 资源集合，无 `SKILL.md` | 证明"收藏型"需求极大 | 是库不是 Skill；不可执行 |

---

## 5. 横向对比矩阵

| 维度 | S1 Emily | S2 dexhunter | S3 zenstory | S4 liangdabiao | S5 LearnPrompt | S6 Square-Zero | S7 CyberJ | 本项目目标 |
|---|---|---|---|---|---|---|---|---|
| 入口形态 | 29 子技能 + 路由 | 单文件 | 流水线套件 | 单技能 | 15 题材技能 | 单入口 + 模型库 | 单文件 44KB | **单入口 + 按需引用** |
| 首次出结果轮次 | 多（门禁前置） | 2 问后 | 多阶段 | 5 问后 | 1–2 问 | 1 问（模型） | 0–1 问 | **≤3 轮，通常 1 问** |
| 状态/续写 | 有（sequence state） | 无 | 有（文件系统） | 无 | 有（plan.json） | 无 | 无 | 有（4 文件，仅 Full Lane） |
| 多模型 | 仅 Seedance 线 | 仅 Seedance | 少量（H3/Seedance/Wan 方言） | 仅 Seedance | 仅 Seedance | **10 模型** | 多模型提及 | **6 方言 + 索引** |
| 素材作用域 | 有（authority） | 有（@ 角色） | 有（REF 绑定） | 有（C/S/P） | 有（reference-map） | 弱 | 有（参考图优先） | 有（职责 + 作用镜头） |
| 确定性校验 | 静态链接校验 | 无 | 有（脚本） | 无 | `validate_plan.py` | 无 | 无 | **有（3 脚本）** |
| 证据/来源 | 强（静态校验/诚实规则） | 弱（无来源） | 中（决策笔记） | 弱 | **强（案例可追溯）** | 强（官方链接） | 中 | **强（证据等级列）** |
| 许可 | MIT | MIT | MIT | 无 | MIT | Apache-2.0 | MIT | MIT |

---

## 6. 五条关键结论

### 6.1 社区分成两派，中间地带是空的

- **单文件手册派**（S2、A1）：易读、易分发，但没有状态、没有自检、没有多模型。
- **套件派**（S1、S3、S5）：完整、可维护，但重到普通创作者用不起。
- **中间地带**——"一个入口 + 3 轮出包 + 按需加载 + 确定性自检 + 多模型方言"——本次 7 个样本里没有一个同时做到。这是本项目的生态位。

### 6.2 真正被采用的交互设计是"少问、快出"

正向证据：
- S1 `Fast Lane`：大多数请求只是一条短片，不要跑全套门禁。
- S7 `When to Ask Questions`：只问故事基础，技术细节自己补。
- S3：只有真实创作分叉才问，不拿 schema/目录问创作者。

反向证据：
- S4 第 2 步问 5 个参数；A1 必问时长；两者都要求用户先做专业决策。
- S1 的 Fast Lane 仍要先加载 `Director's Read`，说明"快路"很容易被自己的门禁吃掉。

→ **3 轮契约不是我们的发明，是把社区最好的三条做法合并成硬约束。**

### 6.3 多模型适配的正确结构是"索引 + 方言文件"

S6 用 10 个 `references/models/<model>/prompting.md` + 一行索引解决多模型；S3 用 MiniMax/Seedance/Wan 方言文件；S4/A1 则被单模型锁死。

→ 我们采用"Model Index + 每模型方言 + 全局参数外置规则"，并额外加一条 S6 没做的：**故事层/执行层分离的验收**（换模型只允许改五处）。

### 6.4 证据与真实性是稀缺品

- S5 把 840+ 案例追溯到原帖，并做跨模型复测；S6 每个模型文件带官方链接；S1 明说"没看过不许说看过"；S3 导出 `asserts_approval=false`。
- 其余项目普遍：平台数字无来源、无时效、把作者经验写成硬规则（S4 的 2–5s/镜、13–15s/集）。

→ 我们把"证据等级"做进输出合同的参数表（A/B/C/D），未核实项必须显示。

### 6.5 最普遍的工程缺口是"确定性自检"

7 个深读样本里，只有 S5 有 `validate_plan.py`、S3 有完整脚本层；其余全是"靠模型自觉"。

→ 我们的三个脚本（模板、生产包、自测）是差异化重点，而且只守 `structural_invariant`，不碰审美。

---

## 7. 用户真实痛点（来自 issue，不来自 README）

| 证据 | 原话 | 痛点 | 我们的对应 |
|---|---|---|---|
| S4 #1 | "Seedanc2.0在哪里用啊？一搜索跳出来好多" | 平台/版本混乱，不知道在哪跑 | 参数节写"入口/平台"，不确定就标未核实；第 1 轮问模型 |
| S4 #6 | "需要手动拷贝素材去 nanobanana 生图，然后再手动去 seedance 创建任务吗？有一键式的体验吗" | 流程断裂，手动搬运 | 生产包直接给"素材清单 + 本条槽位 + 参数"，减少搬运；但不承诺全自动 |
| S4 #7 | "生成的视频呢？看下质量如何" | 看不到成品证据 | 样例明确标 synthetic；不拿文本 PASS 冒充成片质量；风险节写最可能失败点 |
| S1 规则 | "Never state or imply that you viewed…" | 模型假装看过素材 | 硬边界第 4 条 |
| S3 原则 | "不要拿 schema、目录、事务或检查器询问创作者" | 把工程问题甩给用户 | 硬禁问题清单 |

---

## 8. 对本项目的迁移决策

### 8.1 借（注明来源）

| 借什么 | 来自 | 落地位置 |
|---|---|---|
| Fast Lane + 升级信号 | S1 | `SKILL.md` §3、`references/00_交互协议.md` §1 |
| 权威顺序（9 层） | S1 | `references/00_交互协议.md` §7 |
| Load Map（压缩到 9 行） | S1 | `SKILL.md` §7 |
| "没看过不许说看过" | S1 | `SKILL.md` §0 |
| 约束表 + `@` 职责表 | S2 | `references/03_模型适配.md`、`04_素材与引用.md` |
| 能力模式（一致性/运镜/延长/编辑/对白/一镜） | S2 | `templates/shots/`、`references/01_输入路由.md` |
| 五文档状态（压缩为 4 文件） | S3 | `references/00_交互协议.md` §4 |
| 规则四级 + 脚本边界 | S3 | `references/06_质量与自检.md` §1 |
| "只问真实分叉" | S3 | `references/00_交互协议.md` §8 |
| 导出不冒充审批 | S3 | `references/06_质量与自检.md` §7 |
| 资产编号 C/S/P 思路 | S4 | `references/04_素材与引用.md` §4（改为 A/S 两级） |
| 分镜表列 + 尾帧衔接 | S4 | `references/07_输出合同.md` §2 |
| 自检分格式/内容/技术 | S4 | `references/06_质量与自检.md` §2–3 |
| 模板四字段 | S5 | `templates/*` 的 frontmatter + 正文 |
| 状态机 + 不把提示词说成视频 | S5 | `references/00_交互协议.md` §4 |
| Model Index + 每模型方言 | S6 | `references/03_模型适配.md` §2 |
| 参数外置 + 最短可行时长 | S6 | `references/03_模型适配.md` §1、§9 |
| "只问故事基础" | S7 | `SKILL.md` §2 |
| 执行门禁表 | S7 | `references/06_质量与自检.md` §4 |
| 时长/字符预算 + 留反应 | S7 | `references/02_镜头语言.md` §6、`05_声音与台词.md` §2 |
| 反模式清单 | S7 | `references/02_镜头语言.md` §10、`06` §4 |

### 8.2 不借

- 29 个子技能矩阵、13 步全量门禁（S1）：对单条用户过重。
- Dashboard、project_tool、JSONL 决策链（S3）：安装门槛高于收益。
- 15 个题材技能并列（S5）：跨题材项目仍要人工搬。
- 完整 prompt 当模板（S2/S4）：不可组合，且容易变成复制文案。
- 固定 2–5s/镜、13–15s/集、3–7 镜/集（S4）：把经验写成硬规则。
- 一次给 2–3 个风格版本（A1）：选择过载，且稀释"一个可执行方案"。
- 5 问前置（S4）、必问时长（A1）：与 3 轮契约冲突。

### 8.3 自创（差异化）

1. **3 轮硬契约**：第 1 轮 ≤3 问且带默认值；第 2 轮固定 8 节；第 3 轮只改点名单元。
2. **8 节输出合同**：决策摘要 / 事实层 / 分镜表 / 提示词 / 素材挂图 / 参数 / 自检 / 风险。
3. **参数表带证据等级**（A/B/C/D），把"未核实"变成一等公民。
4. **故事层/执行层分离的换模型验收**：事实层与分镜表逐字不变，只改五处。
5. **确定性脚本只守结构不变量**：模板占位符、时间轴、台词进出、引用语法隔离、参数泄漏。
6. **反"审美法条化"**：`taste_option` 永不阻断交付；关键词表不当质量门槛。

---

## 9. 调研限制（必须照实说）

1. **没有安装运行任何一个样本**：结论来自代码/文档阅读与 API 数据，不代表实际生成效果。
2. **没有读完所有文件**：S1 343 个、S3 561 个文件（分别核对 225/356 个文本文件）只做了结构摘要与定点精读。
3. **star 数不等于质量**：A3 是资源集合（2758★）却不可执行；S6 只有 185★ 但结构最干净。
4. **issue 样本很少**：7 个仓库里只有 S4 有实质吐槽；不能据此推断整个社区。
5. **平台数字会过期**：所有时长/分辨率/参考数都应在平台改版后重核。
6. **未使用 Google/Reddit/X**：这些渠道本机不可达，报告中没有任何来自它们的"社区反馈"。

---

## 10. 证据索引（抽查用）

| 结论 | 证据位置 | 日期 |
|---|---|---|
| Fast Lane / Authority Order / Load Map | `S1 SKILL.md:31-40, 75-95, 115-153` | 2026-10-03 推送 |
| 约束表 / @ 职责 / 能力模式 | `S2 SKILL.md:14-31, 46-70, 135-260` | 2026-09-19 推送 |
| 五文档 / 只问真实分叉 / 规则四级 | `S3 skills/short-drama/SKILL.md:11-15, 47`；`.agents/notes/.../2026-07-16-rule-tiers...md` | 2026-10-20 推送 |
| 5 问 / 固定镜数 / issue 吐槽 | `S4 SKILL.md:40-50, 407-417`；issues #1/#6/#7 | 2026-09-21 推送 |
| 状态机 / 模板四字段 / validate_plan | `S5 agents/skills/seedance-production-workflow/SKILL.md:8, 25-29`；`seedance-prompt-library/SKILL.md:14-24` | 2026-10-20 推送 |
| Model Index / 参数外置 | `S6 video-prompting/SKILL.md:18-46, 99-104` | 2026-08-25 推送 |
| 只问故事基础 / 门禁表 / 时长预算 | `S7 cinematic-video-prompt-engineer/SKILL.md:161-204` | 2026-10-15 推送 |

> 仓库快照保存在 `_harvest/skill_research/`（稀疏检出，只含文本文件）；原始克隆不进入交付物。
