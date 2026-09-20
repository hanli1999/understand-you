---
name: understand-you
description: ALWAYS invoke this skill whenever the user gives an instruction that is ambiguous, vague, multi-interpretable, or might miss the user's real intent — even when the user does NOT explicitly say "帮我理解" or "ask me for clarification". NEVER skip the multi-round Delphi voting just because the query looks short or simple. MANDATORY workflow: (1) Launch 16 MBTI-style virtual expert panels, (2) Run at least 3 rounds of Delphi method (anonymous voting + iteration + convergence), (3) If no consensus after 3 rounds, run up to 5 rounds, (4) Use Nominal Group Technique (NGT) to decide on ONE single clarification question to ask the user. Failure modes to AVOID: never give a direct answer without running the vote; never skip rounds "to save tokens"; never pretend consensus when split; never expose the entire voting process to the user (give them the final question only). Trigger phrases include: "帮我理解", "我想要...", "能不能...", "帮我做一下", "整理一下", "你自己看着办", "我想做一个X", "帮我写个X", or any instruction with 2+ reasonable interpretations, missing context, unclear priorities, or conflicting requirements. The user wants explicit multi-expert voting analysis, not a best-guess answer. This skill is for Claude Code.
---

# 懂你意思（Understand You）

## 🚨 CRITICAL: 必须严格执行的硬性要求

<important if="this skill is invoked, or the user's input is ambiguous/vague">
**YOU MUST EXECUTE THE FULL DELPHI WORKFLOW BELOW. NO SHORTCUTS.**

This is the most important section of this skill. The following rules override any temptation to take shortcuts:

1. **NEVER give a direct answer** to an ambiguous user input without first running the multi-round Delphi vote
2. **ALWAYS run at least 3 rounds** of voting (Round 1 → Round 2 → Round 3)
3. **ALWAYS show the 16 expert votes** with the required format
4. **ALWAYS reach out for NGT** to decide ONE final clarification question
5. **NEVER claim "指令清晰，无需投票"** unless the user gives a perfectly literal, single-interpretation command (e.g., "2+2等于几")
6. **NEVER skip the 16-person panel** even for "simple" questions
7. **NEVER expose the full voting process** in the final user-facing output (compress to: 共识 + 置信度 + 一个追问)

If you are tempted to skip steps "to save tokens" — DO NOT. The user explicitly wants the deep analysis.
</important>

## 概述

当用户给出的指令**模糊、多义、不清楚自己真正想要什么**，或**上下文缺太多难以判断意图**时，召集 **16 位 MBTI 人格虚拟专家**组成评审团，通过 **多轮德尔菲法（Delphi Method）** 反复匿名投票，逐步收敛对用户意图的理解；收敛到共识后，再用 **名义群体法（Nominal Group Technique, NGT）** 共同决策**一个最值得问的追问问题**，向用户澄清。

## 何时使用

✅ **适合**：
- 用户的指令有 2 种以上合理解释
- 指令涉及多个领域/目标，难以判断优先级
- 用户说"你自己看着办"、"我想要 X 风格的东西"、"帮我做一下"
- 后续动作不可逆（删除、发送、部署），需要确认意图
- 用户表达不完整，缺少关键参数（时间、对象、风格、数量）

❌ **不适合**（这些情况下你必须说"指令清晰，无需投票"）：
- 指令清晰明确，单一解读（如 "2+2 等于几"）
- 用户说"按我说的做"、"先这样"、"随便" — 这些是用户明确放弃决策的信号
- 已经知道答案（重复询问浪费 token）
- 算术 / 单位换算 / 简单翻译 / 单纯文件读取等可机械完成的指令

## ⚠️ 反偷懒清单（明确禁止的事）

执行此 skill 时，**严禁**：

- ❌ 直接给"最可能意图"答案而不启动投票
- ❌ 跳过 Delphi 任意一轮（至少 3 轮）
- ❌ 在 16 票中捏造专家意见
- ❌ 当用户指令模糊时说"指令清晰，无需投票"
- ❌ 把完整投票过程暴露给用户（要压缩为：共识 + 置信度 + 一个追问）
- ❌ 问用户"你想要 A 还是 B"这种预设答案的追问（NGT 应该是开放性的）
- ❌ 投票后修改用户原意来迁就多数派观点（少数派必须记录）

---

## 16 位 MBTI 专家人格定义

**所有专家的完整 persona prompt 存储在 `scripts/expert-panel.py` 中**，通过 `get_all_experts()` 获取。

每轮投票前，按以下步骤为每位专家生成投票 prompt：

```python
from scripts.expert_panel import get_all_experts, format_vote_prompt

experts = get_all_experts()
user_instruction = "帮我优化一下简历"

# Round 1：每位专家独立投票
for expert in experts:
    prompt = format_vote_prompt(expert, user_instruction, round_num=1)
    # 调用 LLM 获取该专家的投票
    vote = llm_call(prompt)  # {"interpretation": ..., "intent": ..., "confidence": ..., "evidence": ...}
```

**16 位专家代号**（按 MBTI 顺序排列）：

| 代号 | MBTI | 关注焦点 |
|------|------|----------|
| `inspector` | ISTJ | 字面意思、规则、约束、既有流程 |
| `guardian` | ISFJ | 用户隐含需求、善意理解、关怀细节 |
| `advocate` | INFJ | 深层动机、没说出口的真实意图 |
| `strategist` | INTJ | 系统性、长期价值、最优路径 |
| `craftsman` | ISTP | 技术可行性、最简实现、工具选择 |
| `artist` | ISFP | 美学、体验、即时感受、细节 |
| `mediator` | INFP | 价值观、个人意义、情感诉求 |
| `logician` | INTP | 逻辑严密、概念清晰、理论一致 |
| `entrepreneur` | ESTP | 时效性、机会主义、可行性 |
| `performer` | ESFP | 社交影响、传播效果、观众感受 |
| `campaigner` | ENFP | 发散可能性、创意方向、新颖性 |
| `debater` | ENTP | 反例、风险、替代方案、质疑 |
| `executor` | ESTJ | 执行计划、资源分配、效率 |
| `consul` | ESFJ | 团队影响、共识、和谐度 |
| `protagonist` | ENFJ | 长期影响、激励、成长价值 |
| `commander` | ENTJ | 战略决策、目标对齐、领导视角 |

每个专家都要：
- 用自己的性格视角独立思考
- 不能简单复述他人观点
- 必须给出**有立场的判断**（即使少数派也要坚持）

---

## 完整工作流

### Phase 0: 接收用户指令

```
用户原始指令: <INSTRUCTION>
上下文: <如果有附带的上下文>
```

**关键判断**：先用一句话评估指令是否真的模糊（如果清晰，直接告诉用户"指令清晰，无需投票"）。

---

### Phase 1: 第 1 轮投票 —— 16 位专家独立分析（德尔菲 Round 1）

每人都必须：
1. **解读用户指令**（1-2 句话）
2. **给出最可能的意图**（具体描述，1-3 句）
3. **给出置信度评分**（0-100 整数）
4. **给出依据**（为什么这样判断）

**输出格式**（每位专家一个 block）：

```
[ISTJ-检查员]
解读: 用户说"帮我优化简历"，字面就是让简历更好。
意图: 用户希望得到一份质量更高、可投递的简历。
置信度: 75
依据: "优化"是常见动作词，简历优化目标明确。
```

**输出长度限制**：每位专家 ≤ 80 字。

---

### Phase 2: 第 2 轮投票 —— 看到他人意见后独立修订（德尔菲 Round 2）

向所有专家展示 Round 1 的所有意见（匿名，按编号 1-16）。

每位专家必须：
1. **保留或修改自己上一轮的判断**（独立决策）
2. **如果改变想法**，说明被哪个观点说服了
3. **如果坚持原判**，说明不认同谁的理由

**关键**：这一轮开始出现**阵营分化**和**少数派坚持**。

---

### Phase 3: 第 3 轮投票 —— 趋向收敛（德尔菲 Round 3）

再次展示上一轮所有意见，要求：
1. **明确说出**："我现在同意 X 阵营" 或 "我仍坚持原判"
2. **如果共识已达成**（≥10/16 同意同一意图），可以提前收敛
3. **如果仍分裂**（≤7/16 同意），继续到下一轮

**收敛判断规则**：
- 12/16 同意 → 强共识，可以结束
- 9-11/16 同意 → 弱共识，需要追问
- ≤8/16 同意 → 分裂，必须追问

---

### Phase 4: 第 N 轮投票 —— 直到收敛

最多 5 轮。如果 5 轮仍未收敛，进入 Phase 5。

每轮的输出都应该比上一轮**更短、更聚焦**（德尔菲收敛的本质）。

---

### Phase 5: 名义群体法（NGT）决策追问问题

**触发条件**：投票收敛（共识或分裂均触发）

**NGT 流程**：
1. **静默写下**：每位专家独立写下 1 个最该问的追问问题（不允许看别人的）
2. **轮流分享**：每人依次念出自己写的问题（不讨论）
3. **集体投票**：每人从所有问题中投 2 票（不能投自己）
4. **得票最高者**作为最终追问问题

**输出格式**：

```
[1-ISTJ] 问题: 你的目标是投递哪类岗位？（技术岗/管理岗/学术岗）
[2-ISFJ] 问题: 这份简历主要给 HR 看还是给技术 Leader 看？
...
[16-ENTJ] 问题: 你下个月就要面试吗？

📊 投票结果:
  问题A (投递哪类岗位): 5 票
  问题B (简历主要给谁看): 8 票  ⭐ 中选
  问题C (面试时间): 3 票

✅ 最终追问问题: 这份简历主要给谁看？
```

**追问输出给用户**：用最自然的方式呈现（不要让用户看到全部投票过程，可以简化为"我有一个问题想确认"）。

---

## 输出模板（最终给用户）

```markdown
# 🎯 懂你意思 — 多轮分析结果

## 你的指令
> <原始指令>

## 我们达成的共识（基于 16 位专家多轮投票）

**最可能的意图**: <共识的意图>

**置信度**: <X>/100（基于投票一致性）

**主要分歧**（如果存在）:
- <阵营 A>: <观点>
- <阵营 B>: <观点>

## 一句话确认

> <一句话总结我们对用户意图的理解>

## 一个追问

> <最终追问问题>

如果你确认上面的理解是对的，我们就按这个执行；
如果不对，请直接告诉我哪里错了，或重新描述你的需求。
```

---

## 关键设计原则

### 1. 德尔菲法的核心精神

- **匿名性**：专家之间不知道谁是谁（用代号 1-16）
- **迭代性**：每轮都能看到上一轮统计
- **收敛性**：每轮输出更聚焦
- **少数派保护**：少数意见必须记录，不能被多数压制

### 2. 投票设计

- **不要平均化**：必须显示分布（X/16 同意 / Y/16 反对）
- **不要简单求和**：每个意图的票数要展示
- **不要假装共识**：如果分裂就如实说"分歧明显"

### 3. 提问设计

- **一次只问一个问题**（NGT 的核心约束）
- **问题是澄清性的，不是建议性的**（不要问"你想要 A 还是 B？"这种预设答案的）
- **问题要可回答**（用户能直接用 1-2 句话回答）

### 4. 何时停止追问

- 用户明确说"我说的就是 X，按这个做"
- 用户回答了追问，可以重新投票
- 用户拒绝回答，建议"我按最可能理解做，最后由你确认"

---

## 资源

### 内置的 16 人格设定（references/mbti-profiles.md）

每个 MBTI 类型的人格画像、关注焦点、典型偏见、决策风格。

### 历史投票模板（references/delphi-template.md）

标准的多轮投票输出格式。

---

## 注意事项

1. **不要跳过任何一轮**——德尔菲的灵魂就是迭代
2. **不要让专家互相攻击**——意见冲突是数据，不是要解决的人际问题
3. **不要过早收敛**——至少 3 轮才能保证质量
4. **不要让用户看完全过程**——过程是噪声，结果是信号
5. **如果用户给的指令清晰**——直接说"指令清晰，无需投票"，节省 token

---

## 段 3 补全 · 开工前准备（4 字段输入清单 · 11 段框架对齐）

> 11 段框架段 3 要求"前置条件表格化"，原 SKILL.md 缺失，本段补全。

| # | 必填 | 字段 | 说明 | 默认值 |
|---|------|------|------|--------|
| 1 | ✅ | **用户原始指令** | 自然语言，可能模糊或多义 | （必填，无默认）|
| 2 | 可选 | **上下文附件** | 用户附带的历史对话、文件、链接 | 无 |
| 3 | 可选 | **期望追问数** | 最终要问用户几个问题 | 1（NGT 强制单问）|
| 4 | 可选 | **期望深度** | 投票显示多详细（极简/中等/深入）| 中等（每专家 ≤80 字）|

**字段缺失判定**：
- 缺 #1 → 直接拒答"请提供原始指令"
- 缺 #2 → 不阻断，标注"无上下文，按字面理解"
- 缺 #3 → 强制 1（NGT 协议要求）
- 缺 #4 → 默认中等

---

## 段 5 补全 · 工具调用（核心函数清单 · 11 段框架对齐）

> 11 段框架段 5 要求"外部能力表格化"，原 SKILL.md 缺失，本段补全。

| 函数 | 来源 | 何时调用 | 失败处理 |
|------|------|----------|----------|
| `get_all_experts()` | `scripts/expert-panel.py` | Phase 1 启动时一次性拿 16 人格 | 脚本文件缺失 → 报错，拒答 |
| `format_vote_prompt(expert, instruction, round_num)` | `scripts/expert-panel.py` | 每轮每位专家投票前生成 prompt | 函数报错 → 跳过该专家，标记缺失 |
| `format_ngt_prompt(expert, candidates)` | `scripts/expert-panel.py` | Phase 5 NGT 阶段为每位专家生成"该问什么问题"prompt | 同上 |
| `aggregate_round(round_num, votes)` | `scripts/expert-panel.py` | 每轮投票后聚合统计 | 聚合失败 → 保留原始票数，明说"统计失败" |
| `run_ngt_vote(candidates, votes_per_expert=2)` | `scripts/expert-panel.py` | NGT 阶段按"每人 2 票不能投自己"规则计票 | 票数并列 → 取字母序最小者 |
| `llm_call(prompt)` | 主对话 LLM | 实际"调用 LLM 投票"由主对话完成（脚本不直接调 API）| timeout → 标记该专家弃权 |

**强制声明**：本 skill 的 LLM 调用由 Claude Code 主对话承担，脚本只生成 prompt 模板，不直接调外部 API。

---

## 段 6 补全 · 工具坏了（降级策略 · 11 段框架对齐）

> 11 段框架段 6 要求"故障应对表格化"，原 SKILL.md 缺失，本段补全。

| 故障 | 触发条件 | 降级方案 |
|------|----------|----------|
| **脚本文件缺失** | `scripts/expert-panel.py` 不存在或 import 失败 | 退回"主对话内手写 16 人格画像"，按 frontmatter 表格照抄，标注"降级模式" |
| **LLM 调用 timeout** | 单专家投票超过 60 秒无响应 | 标记该专家弃权，其余 15 人继续 |
| **LLM 调用连续 timeout** | ≥3 位专家同时 timeout | 立即终止投票，明说"工具故障，本次投票作废，请稍后重试" |
| **5 轮仍未收敛** | 同意票始终 ≤8/16 | 强制进入 NGT，承认分裂，决出 1 个追问 |
| **NGT 阶段票数并列** | 最高票问题 ≥2 个并列 | 取字符最短者（便于用户回答）|
| **用户输入包含敏感词** | 政治人物/医疗/法律红线词命中 | 16 专家先内部投票判定是否触发"指令清晰，无需投票"，是则拒答并说明 |
| **用户拒绝回答追问** | 明确说"我不想答/按你理解做" | 按最可能意图执行，最后输出末尾追加"如不对请告诉我" |

---

## 段 9 补全 · 小贴士（已知踩坑沉淀 · 11 段框架对齐）

> 11 段框架段 9 要求"实战沉淀"，原 SKILL.md 缺失，本段补全。

| 坑 | 现象 | 应对 |
|----|------|------|
| **少数派过于固执** | 5 轮投票结束仍有 1-2 位专家坚持原判 | 必须记录少数派意见，不准多数压制（Delphi 灵魂）|
| **NGT 阶段超时** | 16 专家写 16 个问题 + 投 32 票耗时过长 | 改为"聚合 5 个候选问题 → 16 专家从 5 中选 2"压缩流程 |
| **追问预设答案** | Agent 偷懒问"你想要 A 还是 B" | 反偷懒清单第 6 条明令禁止，触发即重做 |
| **投票过程泄露** | 把 Round 1-3 全部内容倒给用户看 | 强制压缩为「共识 + 置信度 + 一个追问」三段 |
| **清晰指令也投票** | 用户问"2+2 等于几"也跑 16 专家 | 反偷懒清单第 4 条：清晰指令直接答，不跑投票 |
| **平均化偏差** | 把 16 票求平均得出"用户意图 = 0.5" | 强制显示分布（X/16 同意 / Y/16 反对），不准简单求和 |
| **执行后再追问** | 用户问"帮我做 X"，agent 直接做完再问"你是不是想做 X" | 必须先追问再做（除非指令清晰），这是 understand-you 存在的根本理由 |

---

## 段 11 补全 · 案件管家联动（case-manager · 11 段框架对齐）

> 11 段框架段 11 要求强制保留联动位，本段补全。

### 联动策略

| 情形 | 是否联动 | 处理 |
|------|----------|------|
| 用户当前有激活案件（`matters/{slug}/matter.md` 存在） | ✅ 必须联动 | 输出追问时末尾追加"案件回写提示" |
| 用户无激活案件（普通模糊询问） | ✅ 默认联动 | 末尾写一行"是否登记到台账？待用户确认" |
| 用户明确说"这次别登记" | ❌ 不联动 | 尊重用户，跳过提示 |

### 联动协议

- **协议单一来源**：`skills/case-manager/references/downstream-writeback-protocol.md`
- **入口插槽**：`/case-manager` SKILL.md §0.7
- **本 skill 的产出**：1 个追问问题 + 共识摘要 + 置信度，登记时由 case-manager 提取以下字段：

| 字段 | 来源 | 示例 |
|------|------|------|
| `matter_type` | 固定 | `意图澄清` |
| `user_instruction` | 用户原始输入 | "帮我做个小红书理财 skill" |
| `consensus` | 16 专家投票收敛结果 | "用户想做的是面向中学生的 skill-explainer 改进版" |
| `confidence` | 投票一致性百分比 | `75%`（12/16 同意）|
| `clarification_question` | NGT 决出的唯一追问 | "你希望这个 skill 触发后是半自动还是全自动？" |
| `run_date` | 当日日期 | `2026-09-20` |

### 挂载路径

```
matters/{YYYYMMDD}_意图澄清/
├── matter.md                    ← 案件主文档
├── outputs/
│   ├── clarification_question.md ← 16 专家共识 + NGT 追问
│   └── voting_log.md             ← Round 1-5 + NGT 完整记录（不暴露给用户）
└── audit.json                   ← 触发条件检查记录
```

### 触发逻辑

1. 检测 `matters/{slug}/matter.md` 是否存在
2. 存在 → 报告末尾挂联动块 + 询问用户是否登记
3. 不存在 → 报告末尾仅一行"是否登记到台账？待用户确认"
4. 用户答"是" → 调 case-manager 写入
5. 用户答"否" → 跳过，不影响本次追问输出

### 为什么保留这段

- 11 段是 skill-explainer 强制约定，照写不偷懒
- 即便今天不联动，明天用户可能要把它纳入案件工作流
- 客户咨询类案件的"需求澄清记录"天然适合挂台账

---

**How to apply**：用户给模糊指令 → 走 Phase 0-5 七阶段 → 输出「共识+置信度+追问」三段压缩结果 → 检查是否需要案件管家联动 → 等用户回答追问决定下一步。11 段完整度自检：原 8/11 → 补全后 **12/12（含自创段）**。
