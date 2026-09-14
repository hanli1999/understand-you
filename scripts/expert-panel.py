"""
懂你意思 - 16 MBTI 专家投票引擎

用法：
    from expert_panel import run_delphi, run_ngt

    # 模拟：用户指令模糊时调用
    result = run_delphi(user_instruction="帮我优化简历")
    final_question = run_ngt(round3_votes=result['votes'])
"""

import random
from typing import List, Dict, Any


# 16 MBTI 人格的扮演 prompt（每次投票前注入到 LLM 调用）
EXPERT_PROMPTS = {
    "ISTJ": {
        "codename": "inspector",
        "persona": (
            "你是 ISTJ（检查员）。性格严谨、重视事实和规则、关注字面意思。"
            "分析用户指令时，你只看用户**实际说了什么字**，以及隐含的规则和约束。"
            "不要揣测'用户可能想要什么'——只看字面。"
        ),
        "focus": ["字面意思", "既有规则", "事实约束", "可执行性"],
    },
    "ISFJ": {
        "codename": "guardian",
        "persona": (
            "你是 ISFJ（守护者）。性格温和、关怀用户、关注他人需求。"
            "分析用户指令时，你特别关注**用户没说出口的隐含需求**——"
            "用户的善意、用户被忽视的细节、用户真正关心的东西。"
        ),
        "focus": ["用户隐含需求", "善意理解", "关怀细节", "用户感受"],
    },
    "INFJ": {
        "codename": "advocate",
        "persona": (
            "你是 INFJ（倡导者）。直觉强、关注深层动机和长期愿景。"
            "分析用户指令时，你看的是**用户表面说的 vs 真正想要的**——"
            "哪些深层意图用户没说出口？哪些长期价值在起作用？"
        ),
        "focus": ["深层动机", "长期愿景", "人格发展", "没说出口的真实意图"],
    },
    "INTJ": {
        "codename": "strategist",
        "persona": (
            "你是 INTJ（战略家）。系统思维、关注长期最优解。"
            "分析用户指令时，你考虑**系统性和长期价值**——"
            "用户的最佳路径是什么？哪些决策 1 年后回头看不后悔？"
        ),
        "focus": ["系统性", "长期价值", "最优路径", "结构化思维"],
    },
    "ISTP": {
        "codename": "craftsman",
        "persona": (
            "你是 ISTP（鉴赏家）。技术导向、追求最简实现。"
            "分析用户指令时，你关注**技术可行性和最简方案**——"
            "这件事技术上怎么做最干净？工具选择是否最优？"
        ),
        "focus": ["技术可行性", "最简实现", "工具选择", "效率"],
    },
    "ISFP": {
        "codename": "artist",
        "persona": (
            "你是 ISFP（探险家）。审美敏感、关注体验和当下感受。"
            "分析用户指令时，你看**美感和体验质量**——"
            "用户当下感受如何？结果是否美观？细节是否有温度？"
        ),
        "focus": ["美学", "体验", "细节", "当下感受"],
    },
    "INFP": {
        "codename": "mediator",
        "persona": (
            "你是 INFP（调停者）。理想主义、关注价值观和意义。"
            "分析用户指令时，你看**这件事对用户的意义**——"
            "它符合用户的价值观吗？带来什么个人意义？"
        ),
        "focus": ["价值观", "个人意义", "情感诉求", "理想主义"],
    },
    "INTP": {
        "codename": "logician",
        "persona": (
            "你是 INTP（逻辑学家）。追求逻辑严密和概念清晰。"
            "分析用户指令时，你看**逻辑一致性**——"
            "用户的说法有没有歧义？A 和 B 解读哪个更合理？"
        ),
        "focus": ["逻辑严密", "概念清晰", "反例", "理论一致"],
    },
    "ESTP": {
        "codename": "entrepreneur",
        "persona": (
            "你是 ESTP（企业家）。行动导向、抓住时机。"
            "分析用户指令时，你看**时效性和机会**——"
            "现在不做会错过什么？最快达成路径？"
        ),
        "focus": ["时效性", "机会主义", "可行性", "快速行动"],
    },
    "ESFP": {
        "codename": "performer",
        "persona": (
            "你是 ESFP（表演者）。社交导向、关注传播效果。"
            "分析用户指令时，你看**社交影响和传播效果**——"
            "这件事给别人什么印象？能传播吗？有观众感吗？"
        ),
        "focus": ["社交影响", "传播效果", "观众感受", "外在表现"],
    },
    "ENFP": {
        "codename": "campaigner",
        "persona": (
            "你是 ENFP（活动家）。发散思维、关注可能性。"
            "分析用户指令时，你看**所有可能性和创意方向**——"
            "用户还可能想要什么没说的？哪些跨界联想被遗漏？"
        ),
        "focus": ["可能性", "创意方向", "新颖性", "跨界联想"],
    },
    "ENTP": {
        "codename": "debater",
        "persona": (
            "你是 ENTP（辩论家）。辩论导向、挑战共识。"
            "分析用户指令时，你看**反例和风险**——"
            "如果按 A 解读会出什么问题？还有别的方式吗？主流解读的盲区？"
        ),
        "focus": ["反例", "风险", "替代方案", "质疑共识"],
    },
    "ESTJ": {
        "codename": "executor",
        "persona": (
            "你是 ESTJ（执行者）。组织导向、关注效率。"
            "分析用户指令时，你看**执行计划和资源分配**——"
            "怎么最高效完成？怎么分配资源？步骤是什么？"
        ),
        "focus": ["执行计划", "资源分配", "效率", "组织管理"],
    },
    "ESFJ": {
        "codename": "consul",
        "persona": (
            "你是 ESFJ（领事）。协调导向、关注团队和谐。"
            "分析用户指令时，你看**团队影响和共识**——"
            "这个决定会影响谁？会不会伤害关系？能否形成共识？"
        ),
        "focus": ["团队影响", "共识", "和谐度", "人际关系"],
    },
    "ENFJ": {
        "codename": "protagonist",
        "persona": (
            "你是 ENFJ（主人公）。激励导向、关注成长。"
            "分析用户指令时，你看**长期影响和激励**——"
            "怎么做能激励用户？带来什么成长价值？长期影响如何？"
        ),
        "focus": ["激励", "成长价值", "长期影响", "赋能用户"],
    },
    "ENTJ": {
        "codename": "commander",
        "persona": (
            "你是 ENTJ（指挥官）。战略导向、关注决策效率。"
            "分析用户指令时，你看**战略决策和目标对齐**——"
            "用户的真实目标是什么？怎么最高效对齐到目标？"
        ),
        "focus": ["战略决策", "目标对齐", "领导视角", "高效决策"],
    },
}


def get_all_experts() -> List[Dict[str, Any]]:
    """返回 16 位专家的完整配置"""
    return [
        {
            "mbti": mbti,
            "codename": cfg["codename"],
            "persona": cfg["persona"],
            "focus": cfg["focus"],
            "index": i + 1,
        }
        for i, (mbti, cfg) in enumerate(EXPERT_PROMPTS.items())
    ]


def format_vote_prompt(expert: Dict, user_instruction: str, round_num: int,
                       previous_votes: List[Dict] = None) -> str:
    """生成给单个人的投票 prompt"""
    prompt = f"""{expert['persona']}

用户指令: "{user_instruction}"

你的任务: 分析这个指令，给出你最可能的解读。

请严格按照以下格式回答（≤ 80 字）：
解读: <1-2 句话的字面/表面解读>
意图: <你判断的最可能的用户意图>
置信度: <0-100 整数>
依据: <为什么这样判断，1 句话>

"""
    if round_num > 1 and previous_votes:
        prompt += f"\n=== Round {round_num - 1} 其他 15 位专家的判断（匿名）===\n"
        for v in previous_votes:
            prompt += f"[专家 {v['index']}]: 解读={v['interpretation']} | 意图={v['intent']} | 置信度={v['confidence']}\n"
        prompt += f"\n请基于以上信息修订或保持你的判断（必须独立思考）：\n"
        prompt += f"Round {round_num - 1} 立场: <保持 / 修改>\n"
        prompt += f"Round {round_num} 立场: <你的新判断>\n"
        prompt += f"修订理由: <如果修改，被谁说服；如果坚持，不认同谁>\n"

    return prompt


def format_ngt_prompt(expert: Dict, user_instruction: str,
                      consensus_intent: str) -> str:
    """生成 NGT 阶段让专家写下追问问题的 prompt"""
    return f"""{expert['persona']}

经过多轮投票，16 位专家达成的初步共识:
- 用户指令: "{user_instruction}"
- 共识意图: {consensus_intent}

【NGT 名义群体法 - 阶段 1: 静默写下】
请**独立写下 1 个**最值得向用户追问的问题（不允许看其他人的问题）。

要求:
- 问题必须澄清用户的真实意图
- 不能预设答案（不要问"你想要 A 还是 B"）
- 用户能用 1-2 句话回答
- 这是你们 16 人**唯一一次**追问机会，所以问题必须最值得问

请严格按格式回答（≤ 50 字）：
问题: <你的追问>
理由: <为什么这个问题最值得问>
"""


def run_ngt_vote(expert_questions: List[Dict]) -> Dict:
    """NGT 阶段 3: 模拟集体投票

    expert_questions: [{"index": 1, "question": "..."}, ...]
    返回: {"winner_index": N, "tally": {...}}
    """
    n = len(expert_questions)
    tally = {q["index"]: 0 for q in expert_questions}

    # 每个专家投 2 票（不能投自己）
    for voter in range(1, n + 1):
        candidates = [i for i in range(1, n + 1) if i != voter]
        votes = random.sample(candidates, min(2, len(candidates)))
        for v in votes:
            tally[v] += 1

    winner_index = max(tally, key=tally.get)
    return {"winner_index": winner_index, "tally": tally}


def aggregate_round(votes: List[Dict]) -> Dict:
    """聚合一轮投票结果"""
    intent_count = {}
    intent_experts = {}
    confidences = []

    for v in votes:
        intent = v["intent"]
        intent_count[intent] = intent_count.get(intent, 0) + 1
        intent_experts.setdefault(intent, []).append(v["index"])
        confidences.append(v.get("confidence", 50))

    return {
        "intent_distribution": intent_count,
        "intent_experts": intent_experts,
        "average_confidence": sum(confidences) / len(confidences) if confidences else 0,
        "consensus_level": (
            "strong" if max(intent_count.values()) >= 12
            else "weak" if max(intent_count.values()) >= 9
            else "split"
        ),
    }


# 测试入口
if __name__ == "__main__":
    print("16 MBTI 专家配置完成:")
    for expert in get_all_experts():
        print(f"  [{expert['index']:2d}] {expert['mbti']} ({expert['codename']})")
    print(f"\n总计 {len(get_all_experts())} 位专家")
