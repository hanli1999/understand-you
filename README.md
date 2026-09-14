# Understand You — 16 MBTI 专家德尔菲投票 skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 当用户给出的指令**模糊、多义、不清楚自己真正想要什么**时，召集 **16 位 MBTI 人格虚拟专家**组成评审团，通过 **多轮德尔菲法（Delphi Method）**反复匿名投票逐步收敛，最终用 **名义群体法（NGT）** 共同决策**一个最值得问的追问问题**。

## ✨ 特性

- 🎭 **16 位 MBTI 人格** — 每个专家都有独特的关注焦点和判断风格
- 🗳️ **多轮德尔菲投票** — 3-5 轮匿名迭代，逐步收敛共识
- 👥 **名义群体法追问** — 16 人共同决定 1 个最值得问的问题（每人只有 1 次追问机会）
- 🔄 **自动收敛判断** — 强共识(≥12) / 弱共识(9-11) / 分裂(≤8) 三档
- 📊 **完整的输出模板** — 给模型看的详细过程 + 给用户看的简洁结果

## 🚀 快速使用

### 触发 skill

直接在 Claude Code 中说模糊指令即可：

```
帮我优化一下简历
我想做一个项目
整理一下我这段时间的工作
```

Claude 会自动调用 `understand-you` skill，启动 16 专家 Delphi 投票流程。

### 显式调用

```
/understand-you
```

### 跑 demo

```bash
cd scripts
python demo.py "帮我优化一下简历"
```

输出完整的多轮投票过程 + 最终追问。

## 🏗️ 工作流

```
Phase 0: 接收用户指令
       ↓
Phase 1: Delphi Round 1（16 专家独立分析）
       ↓
Phase 2: Delphi Round 2（看到他人意见后修订）
       ↓
Phase 3: Delphi Round 3（趋向收敛）
       ↓
Phase N: 直到达成共识（最多 5 轮）
       ↓
Phase N+1: NGT 名义群体法（决定追问问题）
       ↓
输出: 共识结论 + 置信度 + 一个追问问题
```

## 🎭 16 MBTI 专家

| 类型 | 代号 | 关注焦点 |
|------|------|----------|
| **ISTJ** | inspector | 字面意思、规则、约束 |
| **ISFJ** | guardian | 用户隐含需求、善意理解 |
| **INFJ** | advocate | 深层动机、没说出口的真实意图 |
| **INTJ** | strategist | 系统性、长期价值、最优路径 |
| **ISTP** | craftsman | 技术可行性、最简实现 |
| **ISFP** | artist | 美学、体验、即时感受 |
| **INFP** | mediator | 价值观、个人意义 |
| **INTP** | logician | 逻辑严密、概念清晰 |
| **ESTP** | entrepreneur | 时效性、机会主义 |
| **ESFP** | performer | 社交影响、传播效果 |
| **ENFP** | campaigner | 发散可能性、创意方向 |
| **ENTP** | debater | 反例、风险、替代方案 |
| **ESTJ** | executor | 执行计划、资源分配 |
| **ESFJ** | consul | 团队影响、共识、和谐 |
| **ENFJ** | protagonist | 长期影响、激励、成长 |
| **ENTJ** | commander | 战略决策、目标对齐 |

每个专家都有完整的 persona prompt（见 `references/mbti-profiles.md`）。

## 📦 文件结构

```
understand-you/
├── SKILL.md                          # 主文档
├── README.md                         # 本文件
├── LICENSE                           # MIT 协议
├── references/
│   ├── mbti-profiles.md              # 16 人格详细画像
│   └── delphi-template.md            # Delphi + NGT 输出模板
├── scripts/
│   ├── expert-panel.py               # 16 专家配置 + 投票引擎
│   └── demo.py                       # 端到端 demo
└── evals/
    └── evals.json                    # 6 个测试用例
```

## 🔬 技术原理

### Delphi Method（德尔菲法）

- **匿名性**：专家之间不知道谁是谁
- **迭代性**：每轮能看到上一轮统计
- **收敛性**：每轮输出更聚焦
- **少数派保护**：少数意见必须记录

### Nominal Group Technique（名义群体法）

1. 静默写下（独立、不公开）
2. 轮流分享（不讨论）
3. 集体投票（每人 2 票，不能投自己）
4. 得票最高者作为最终追问

## 🧪 测试用例

见 `evals/evals.json`：

| # | 测试指令 | 预期行为 |
|---|---|---|
| 1 | 帮我优化一下简历 | 触发，3+ 阵营分化 |
| 2 | 我想做一个项目 | 触发，多解读 |
| 3 | 帮我写一份总结 | 触发，多场景解读 |
| 4 | 把这段代码改一下 | 触发，缺信息追问 |
| 5 | 你好 | **不触发**（指令清晰） |
| 6 | 我想要一个工具... | 触发，多维度追问 |

## 🤝 贡献

欢迎提 Issue 和 PR！

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- Delphi Method: RAND Corporation (1960s)
- Nominal Group Technique: Delbecq & Van de Ven (1971)
- MBTI: Isabel Briggs Myers & Katharine Cook Briggs
