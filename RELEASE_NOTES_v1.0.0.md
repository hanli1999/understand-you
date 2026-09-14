# Understand You v1.0.0 — 16 MBTI 专家德尔菲投票

## 🎉 首个稳定版本

`understand-you` 是一个 Claude Code skill，专门处理**模糊、多义、不清楚自己真正想要什么**的用户指令。

通过召集 **16 位 MBTI 人格虚拟专家**组成评审团，进行多轮德尔菲投票 + NGT 名义群体法共同决策，最终给用户一个精准的追问问题。

## ✨ 主要特性

- 🎭 **16 位 MBTI 专家** — ISTJ → ENTJ 全覆盖，每个都有独特关注焦点
- 🗳️ **Delphi 多轮投票** — 3-5 轮匿名迭代，逐步收敛共识
- 👥 **NGT 共同决策追问** — 16 人只有 1 次共同追问机会，由集体投票决定问什么
- 🔄 **自动收敛判断** — 强共识(≥12) / 弱共识(9-11) / 分裂(≤8) 三档
- 📊 **完整输出模板** — 模型看详细过程，用户看简洁结果

## 📦 安装

```bash
git clone https://github.com/hanli1999/understand-you.git ~/.claude/skills/understand-you
```

## 🚀 使用

直接说模糊指令即可触发：

```
帮我优化一下简历
我想做一个项目
整理一下我这段时间的工作
```

或显式调用：

```
/understand-you
```

## 🧪 测试

```bash
cd scripts
python demo.py "帮我优化一下简历"
```

输出完整的多轮投票过程 + 最终追问。

## 🏗️ 工作流

1. Phase 0: 接收用户指令
2. Phase 1-3: Delphi 多轮投票（3-5 轮）
3. Phase 4: NGT 名义群体法决定追问
4. 输出：共识结论 + 置信度 + 一个追问问题

## 📝 文件结构

```
understand-you/
├── SKILL.md                  # 主文档
├── README.md                 # 本文件
├── LICENSE                   # MIT
├── references/
│   ├── mbti-profiles.md      # 16 人格详细画像
│   └── delphi-template.md    # Delphi + NGT 输出模板
├── scripts/
│   ├── expert-panel.py       # 16 专家 + 投票引擎
│   └── demo.py               # 端到端 demo
└── evals/
    └── evals.json            # 6 个测试用例
```

## 🤝 贡献

欢迎 Issue 和 PR！

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)
