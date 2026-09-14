"""
懂你意思 skill - 端到端 demo（模拟 16 专家 Delphi + NGT）

直接运行：
    python demo.py "帮我优化一下简历"

输出模拟的多轮投票 + 最终追问。
"""

import sys
import os
import random
from pathlib import Path

# 添加 scripts 目录到 path 以便 import expert_panel
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))
os.chdir(str(SCRIPTS_DIR))

# 用 importlib 兜底
import importlib.util
spec = importlib.util.spec_from_file_location(
    "expert_panel", str(SCRIPTS_DIR / "expert-panel.py")
)
expert_panel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(expert_panel)

get_all_experts = expert_panel.get_all_experts
format_vote_prompt = expert_panel.format_vote_prompt
format_ngt_prompt = expert_panel.format_ngt_prompt
aggregate_round = expert_panel.aggregate_round
run_ngt_vote = expert_panel.run_ngt_vote


# 模拟 LLM 调用：每位专家的"角色扮演"投票（伪随机但有立场的回答）
SIMULATED_VOTES = {
    "ISTJ": {"interpretation": "字面是'优化简历'", "intent": "让简历内容/排版更好", "confidence": 70, "evidence": "优化=改善，最直接解读"},
    "ISFJ": {"interpretation": "用户希望被认可", "intent": "获得一份能让用户自信投出去的简历", "confidence": 75, "evidence": "简历优化背后是用户的自我呈现焦虑"},
    "INFJ": {"interpretation": "表面说优化，深层想改变职业轨迹", "intent": "通过简历改写获得心仪岗位的面试机会", "confidence": 80, "evidence": "简历是求职的入场券，用户希望突破现状"},
    "INTJ": {"interpretation": "系统性问题", "intent": "重构简历定位以匹配长期职业目标", "confidence": 78, "evidence": "临时优化不如战略重构"},
    "ISTP": {"interpretation": "工具问题", "intent": "用 AI 工具快速生成一份 ATS 友好的简历", "confidence": 72, "evidence": "现在的简历优化基本都是 AI 工具活"},
    "ISFP": {"interpretation": "美感问题", "intent": "让简历排版更美观专业", "confidence": 60, "evidence": "优化包含视觉层面"},
    "INFP": {"interpretation": "价值表达", "intent": "让简历真实呈现用户的价值观和个人故事", "confidence": 70, "evidence": "好的简历不是堆砌，是讲自己的故事"},
    "INTP": {"interpretation": "逻辑问题", "intent": "梳理简历逻辑结构，让信息层次清晰", "confidence": 75, "evidence": "很多简历逻辑混乱，重点不突出"},
    "ESTP": {"interpretation": "时机问题", "intent": "快速优化，赶在下次投递前完成", "confidence": 85, "evidence": "用户在赶时间，所以强调速度"},
    "ESFP": {"interpretation": "观众问题", "intent": "让简历在 HR 眼中更出彩", "confidence": 65, "evidence": "简历是给 HR 看的"},
    "ENFP": {"interpretation": "可能性问题", "intent": "探索多种简历方向，找到最适合用户的", "confidence": 68, "evidence": "优化有多种方向，先探索再聚焦"},
    "ENTP": {"interpretation": "质疑问题", "intent": "挑战用户'优化简历'的预设——是不是该先想清楚要投什么？", "confidence": 72, "evidence": "盲目优化不如先定目标"},
    "ESTJ": {"interpretation": "执行问题", "intent": "按标准流程优化（基本信息/工作经历/技能）", "confidence": 70, "evidence": "简历有固定结构"},
    "ESFJ": {"interpretation": "和谐问题", "intent": "让简历对所有读者（HR/Leader/同事）都友好", "confidence": 65, "evidence": "简历会被多方看到"},
    "ENFJ": {"interpretation": "成长问题", "intent": "让简历体现用户的成长潜力", "confidence": 73, "evidence": "简历不只是过去，更是未来"},
    "ENTJ": {"interpretation": "战略问题", "intent": "简历对齐用户未来 3 年的职业目标", "confidence": 75, "evidence": "简历应服务于战略目标"},
}


SIMULATED_QUESTIONS = {
    "ISTJ": "你打算投递什么类型的岗位？（技术岗/管理岗/学术岗）",
    "ISFJ": "这份简历主要给谁看？（HR / 技术 Leader / 朋友推荐）",
    "INFJ": "你内心最希望这份简历帮你实现什么？",
    "INTJ": "你的 3 年职业目标是什么？",
    "ISTP": "现在用什么工具写简历？（Word / Markdown / 在线工具）",
    "ISFP": "你希望简历的视觉风格是？（简洁/创意/正式）",
    "INFP": "你希望简历传递的核心价值观是什么？",
    "INTP": "简历的核心逻辑主线应该是什么？",
    "ESTP": "你下次投递截止日期是什么时候？",
    "ESFP": "你最希望 HR 看完后记住你哪一点？",
    "ENFP": "除了工作，你有什么特别的经历想突出？",
    "ENTP": "你确定要'优化'，不是'重写'或'转行'？",
    "ESTJ": "你计划投递多少家公司？",
    "ESFJ": "你的同事/朋友会怎么看这份简历？",
    "ENFJ": "这份简历能激励你 5 年后成为什么样的人？",
    "ENTJ": "你的简历服务的最终战略目标是什么？",
}


def simulate_vote(expert: dict, round_num: int, prev_votes: list) -> dict:
    """模拟单个专家投票（带随机性 + 受上一轮影响）"""
    base = SIMULATED_VOTES.get(expert["mbti"], {})
    vote = {
        "index": expert["index"],
        "mbti": expert["mbti"],
        "interpretation": base.get("interpretation", ""),
        "intent": base.get("intent", ""),
        "confidence": base.get("confidence", 50),
        "evidence": base.get("evidence", ""),
    }

    # Round 2+：受上一轮影响，可能调整置信度
    if round_num > 1 and prev_votes:
        # 50% 概率跟随多数派
        if random.random() < 0.3:
            majority_intent = max(
                set(v["intent"] for v in prev_votes),
                key=lambda i: sum(1 for v in prev_votes if v["intent"] == i),
            )
            if vote["intent"] != majority_intent:
                vote["intent"] = majority_intent
                vote["confidence"] = min(95, vote["confidence"] + 10)

    return vote


def simulate_ngt_question(expert: dict) -> str:
    """模拟 NGT 阶段专家写下追问"""
    return SIMULATED_QUESTIONS.get(expert["mbti"], f"请专家 {expert['index']} 补充追问")


def run_demo(user_instruction: str):
    """运行完整 demo"""
    print("=" * 70)
    print(f"用户指令: \"{user_instruction}\"")
    print("=" * 70)

    # 先评估是否模糊
    vague_signals = ["帮我", "我想要", "能不能", "优化", "整理", "修改", "做一下", "搞一下"]
    is_vague = any(s in user_instruction for s in vague_signals) or len(user_instruction) < 20
    print(f"\n模糊度评估: {'模糊（启动投票）' if is_vague else '清晰（无需投票）'}")

    if not is_vague:
        print("\n指令清晰，直接按字面执行。")
        return

    experts = get_all_experts()
    print(f"\n启动 {len(experts)} 位 MBTI 专家进行 Delphi 投票...")

    all_round_votes = []
    final_intent = None

    # Round 1-3 (Delphi)
    for round_num in range(1, 4):
        print(f"\n{'─' * 70}")
        print(f"ROUND {round_num}")
        print(f"{'─' * 70}")

        prev_votes = all_round_votes[-1] if all_round_votes else None
        votes = [simulate_vote(e, round_num, prev_votes) for e in experts]
        all_round_votes.append(votes)

        # 输出每位专家的判断
        for v in votes[:5]:  # 只显示前 5 位
            print(f"[{v['index']:2d}-{v['mbti']}] {v['intent']} (置信度 {v['confidence']})")

        # 统计
        result = aggregate_round(votes)
        print(f"\n📊 统计: 共识度={result['consensus_level']}, 平均置信度={result['average_confidence']:.0f}")

        # 简化：显示意图分布
        for intent, count in sorted(result["intent_distribution"].items(), key=lambda x: -x[1])[:3]:
            print(f"  • {intent}: {count} 票")

        if result["consensus_level"] in ("strong", "weak"):
            final_intent = max(result["intent_distribution"], key=result["intent_distribution"].get)
            break

    if not final_intent:
        final_intent = max(result["intent_distribution"], key=result["intent_distribution"].get)

    # NGT 阶段
    print(f"\n{'═' * 70}")
    print(f"NGT 阶段（决定追问问题）")
    print(f"{'═' * 70}")

    expert_questions = []
    for e in experts:
        q_text = simulate_ngt_question(e)
        expert_questions.append({"index": e["index"], "question": q_text, "mbti": e["mbti"]})

    # 输出所有问题
    print("\n【阶段 1+2: 静默写下 + 轮流分享】")
    for q in expert_questions:
        print(f"  [{q['index']:2d}-{q['mbti']}] {q['question']}")

    # 投票
    ngt_result = run_ngt_vote(expert_questions)
    print(f"\n【阶段 3: 集体投票结果】")
    for idx, count in sorted(ngt_result["tally"].items(), key=lambda x: -x[1])[:5]:
        print(f"  问题[{idx}] {expert_questions[idx-1]['question']}: {count} 票")

    winner_q = expert_questions[ngt_result["winner_index"] - 1]
    print(f"\n⭐ 最高票（{ngt_result['tally'][ngt_result['winner_index']]} 票）: [{winner_q['mbti']}] {winner_q['question']}")

    # 最终输出
    print(f"\n{'═' * 70}")
    print("最终输出（给用户）")
    print(f"{'═' * 70}")
    print(f"\n# 🎯 懂你意思 — 多轮分析结果")
    print(f"\n## 你的指令\n> {user_instruction}")
    print(f"\n## 我们达成的共识")
    print(f"**最可能的意图**: {final_intent}")
    print(f"**置信度**: {result['average_confidence']:.0f}/100")
    print(f"\n## 一个追问")
    print(f"> {winner_q['question']}")
    print(f"\n**确认后我会按这个理解执行。**")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        instruction = " ".join(sys.argv[1:])
    else:
        instruction = "帮我优化一下简历"
    run_demo(instruction)
