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
