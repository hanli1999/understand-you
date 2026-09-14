# 🎉 开源了！understand-you — 16 MBTI 专家帮你"懂你意思"

你有没有过这种体验：让 AI 帮你做件事，结果它做出来的完全不是你想要的，但你又说不出哪里不对？

**根本原因：你的指令模糊，但你自己都没意识到。**

我做了个 Claude Code skill 专门解决这个：

🔗 https://github.com/hanli1999/understand-you

---

## 🧠 它怎么工作

你说一句话（比如"帮我优化一下简历"），它会：

1. **召集 16 位 MBTI 人格虚拟专家**（ISTJ 检查员 → ENTJ 指挥官，覆盖所有思维风格）
2. **多轮德尔菲法投票**（3-5 轮，每轮看到他人意见后修订，独立思考）
3. **NGT 名义群体法决定追问**（16 人集体投票决定**最值得问的一个问题**）
4. **最后只问你 1 个问题**——这个问题是 16 人共同决策出来的，不是 AI 猜的

---

## 💡 为什么有效？

**普通 AI**："你说啥我做啥，猜错了是你的问题"
**understand-you**："我们有分歧，让我问你 1 个问题——这个问题是 16 个不同人格的 AI 经过几轮辩论投票出来的"

**例子**：你说"我想做一个项目"
- 16 位专家会分裂成：创业项目 / AI 项目 / 研究项目 / 兴趣项目 / 转行准备...
- 多轮投票后，会发现关键分歧：**"这个项目是为了工作、兴趣、还是学习？"**
- 16 人投票决定问你这个问题——不是你猜，是 16 人投票

---

## 🚀 用法

```bash
# 安装
git clone https://github.com/hanli1999/understand-you.git ~/.claude/skills/understand-you

# 使用
# 方式 1: 直接说模糊指令
"帮我优化一下简历"

# 方式 2: 显式调用
/understand-you
```

---

## 🎭 16 MBTI 专家

ISTJ (检查员) | ISFJ (守护者) | INFJ (倡导者) | INTJ (战略家)
ISTP (鉴赏家) | ISFP (探险家) | INFP (调停者) | INTP (逻辑学家)
ESTP (企业家) | ESFP (表演者) | ENFP (活动家) | ENTP (辩论家)
ESTJ (执行者) | ESFJ (领事) | ENFJ (主人公) | ENTJ (指挥官)

每个专家都有自己的关注焦点（比如 ISTJ 看字面，INTJ 看长期价值，ENTP 专挑刺），保证投票有真正的分歧。

---

## 🛠️ 技术栈

- **Delphi Method**（1960s RAND）— 匿名 + 迭代 + 收敛
- **Nominal Group Technique**（1971 Delbecq & Van de Ven）— 静默 + 轮流 + 投票
- **MBTI**（Myers-Briggs）— 16 种思维风格

不是 AI 拍脑袋，是群体决策科学 + 心理学的正经方法。

---

## 📦 完全开源

- ⭐ MIT License
- 📝 完整文档
- 🧪 6 个测试用例
- 🎬 端到端 demo 脚本

欢迎 Issue / PR / Star ⭐

**GitHub**: https://github.com/hanli1999/understand-you

---

#ClaudeCode #Skill #OpenSource #AI #MBTI #DelphiMethod #群体智能 #多智能体

---

## 💬 用法 demo（完整流程）

```
用户: 帮我优化一下简历

(understand-you skill 启动)

Round 1: 16 专家独立投票
- [ISTJ]: 优化=改善内容/排版
- [INFJ]: 深层是想拿心仪岗位面试
- [INTJ]: 应该重构定位匹配长期目标
- [ENTP]: 你确定要优化不是重写吗？
- ... (16 人投票)

Round 2: 看到他人意见后修订
(出现阵营分化: "标准流程派" vs "战略重构派" vs "时间紧迫派")

Round 3: 收敛 (弱共识: 9 票同意"按标准流程优化")

NGT 阶段: 决定追问
- [ISTJ]: 你要投递什么类型岗位？
- [INTP]: 简历的核心逻辑主线应该是什么？  ← 5 票 ⭐
- [ENFJ]: 这份简历能激励你成为什么样的人？  ← 5 票
- [ESTP]: 你下次投递截止日期？  ← 3 票
...

最终追问: "简历的核心逻辑主线应该是什么？"
```

这就是它和普通 AI 的区别——**16 种思维风格的真实辩论，不是猜。**
