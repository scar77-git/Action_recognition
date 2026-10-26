"""Practice Set 2 answer PDF: graded against the learner's answers, every option explained."""
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from notelib import S, Note  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

HERE = os.path.dirname(__file__)
KEY = os.path.join(HERE, "practice02_key.json")
OUT = os.path.join(HERE, "..", "notes", "Practice_Set_2_2026-10-26_Days_1-5_and_Gap_Answers.pdf")

MY = {1: "A", 2: "B", 3: "C", 4: "A", 5: "BC", 6: "D", 7: "A", 8: "C", 9: "BC", 10: "B", 11: "C", 12: "B",
      13: "CDF", 14: "B", 15: "D", 16: "B", 17: "D", 18: "ACDE", 19: "A", 20: "A", 21: "C", 22: "D", 23: "A",
      24: "D", 25: "A", 26: "C", 27: "D", 28: "C", 29: "ADF", 30: "D", 31: "C", 32: "BC", 33: "A", 34: "C",
      35: "A", 36: "C", 37: "B", 38: "B", 39: "ABE", 40: "D", 41: "A", 42: "C", 43: "D", 44: "BC", 45: "BCDE"}
GUESSES = {8, 19}
TYPE = {"MC": "Multiple choice", "TWO": "Select TWO", "THREE": "Select THREE", "ALL": "Select ALL (extra-hard)"}
DOMAIN = {"1": "1. FM integration, data, compliance", "2": "2. Implementation and integration",
          "3": "3. Safety, security, governance", "4": "4. Operational efficiency", "5": "5. Testing and troubleshooting"}

key = {int(k): v for k, v in json.load(open(KEY)).items()}
res, by_dom, by_type, by_diff = {}, defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0])
for i, v in key.items():
    ok = sorted(MY[i]) == sorted(v["answer"])
    res[i] = ok
    for d, k2 in ((by_dom, DOMAIN[v["skill"][0]]), (by_type, TYPE[v["type"]]),
                  (by_diff, "Hard" if v["difficulty"] == "H" else "Medium")):
        d[k2][0] += ok
        d[k2][1] += 1
score = sum(res.values())
pct = round(100 * score / len(key))

n = Note(OUT, "Practice Set 2 — Results and Answers",
         f"Monday 26 Oct 2026 &nbsp;·&nbsp; Score: <b>{score} / {len(key)} ({pct}%)</b> &nbsp;·&nbsp; Target ≥ 75% "
         "&nbsp;·&nbsp; Strict all-or-nothing grading on multiple response")
n.callout("Verdict",
          f"<b>{score}/{len(key)} = {pct}%</b> on a set that was 60% hard, with exam-style options and no hints — well above "
          "the 75% target. Both guesses were tested: one right (Q19), one wrong (Q8). Both Select THREE and two of the three "
          "Select ALL questions were fully correct. The four misses share one pattern: choosing an option that "
          "solves <i>part</i> of the requirement (cost but not quality, content but not the right mechanism, access but "
          "not consistency, retry vs fix).", "ok")

n.h1("1. Score breakdown")
rows = [[k2, f"{a} / {b}", f"{round(100 * a / b)}%"] for k2, (a, b) in sorted(by_dom.items())]
n.table(["Exam domain", "Score", "%"], rows, [0.6, 0.2, 0.2])
rows = [[k2, f"{a} / {b}", f"{round(100 * a / b)}%"] for k2, (a, b) in by_type.items()]
n.table(["Question type", "Score", "%"], rows, [0.6, 0.2, 0.2])
rows = [[k2, f"{a} / {b}", f"{round(100 * a / b)}%"] for k2, (a, b) in by_diff.items()]
n.table(["Difficulty", "Score", "%"], rows, [0.6, 0.2, 0.2])

n.h1("2. Mistakes log — the four misses")
n.table(["Q", "Skill", "Your answer", "Correct", "Rule to remember"], [
    ["8 (G)", "2.2.3", "C — distil one small model for everything", "B — small model first, escalate on failed validation",
     "When quality on the <b>hard 20%</b> must not drop, keep a path to the large model: <b>cascading</b>. Distillation "
     "alone trades away the hardest cases."],
    ["9", "2.4.4", "B, C — Intelligent Prompt Routing + Choice state", "C, D — classify step + Choice state",
     "Intelligent Prompt Routing chooses between models <b>in one family</b> by predicted quality. Routing by "
     "<b>business category</b> needs a <b>classification step</b> feeding a Choice state."],
    ["23", "1.5.6", "A — direct OpenSearch REST access per team", "B — retrieval tool behind an MCP server",
     "'Different frameworks + consistent auth + consistent format' → <b>one standard interface (MCP)</b>. Direct access "
     "works but gives each team its own auth and parsing."],
    ["45", "5.2.2", "B, C, D, E", "B, D",
     "<b>Fix, don't retry</b>: ValidationException (bad request) and AccessDeniedException (permissions). "
     "<b>Retry with backoff</b>: Throttling, ServiceUnavailable, ModelNotReady — they are temporary."],
], [0.07, 0.07, 0.27, 0.27, 0.32])

n.h1("3. Feedback")
n.bullets([
    "<b>Strongest areas</b>: security and privacy (all correct), vector stores at scale, safeguards (Select THREE "
    "fully correct), resilience and model lifecycle — the gap lesson clearly landed.",
    "<b>Pattern behind the misses</b>: each wrong choice met <i>one</i> requirement but not <i>all</i>. Before answering, "
    "list every requirement in the stem (e.g. 'cut cost' <b>and</b> 'no quality loss on complex') and strike any option "
    "that fails one.",
    "<b>Select ALL</b>: judge each option on its own against the question — Q45 needed 'is this error temporary?' for "
    "each line.",
    "<b>Guess calibration</b>: you marked 2 guesses and got 1 right — honest flagging; keep doing it.",
])

n.page_break()
n.h1("4. Every question explained")
for i in sorted(key):
    v = key[i]
    mark = "✓" if res[i] else "✗"
    g = " (guess)" if i in GUESSES else ""
    n.h2(f"Question {i} · Skill {v['skill']} · {TYPE[v['type']]} · {mark} you: {', '.join(MY[i])}{g} · correct: "
         f"{', '.join(v['answer'])}")
    n.p(v["stem"])
    for letter, text, ok, why in v["options"]:
        tag = "<b>✓ CORRECT</b>" if ok else "✗"
        picked = " <i>(your choice)</i>" if letter in MY[i] else ""
        n.story.append(Paragraph(f"<b>{letter}.</b> {text}{picked}<br/>{tag} — {why}", S["bullet"]))
    n.space(6)
n.build()
print(os.path.abspath(OUT), score, pct, dict(by_dom))
