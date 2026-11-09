"""Full Mock 1 — 65 questions across the whole AIP-C01 syllabus.

Builds two PDFs from the question bank in mock_q1..mock_q5:
  * Questions only (timed practice)
  * Questions with the answer, explanation and why-each-other-option-is-wrong directly below each question
"""
import os
import random
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from notelib import S, Note  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402
import mock_q1, mock_q2, mock_q3, mock_q4, mock_q5  # noqa: E402,E401

NOTES = os.path.join(os.path.dirname(__file__), "..", "notes")
OUT_Q = os.path.join(NOTES, "Full_Mock_1_2026-11-09_65Q_Questions.pdf")
OUT_A = os.path.join(NOTES, "Full_Mock_1_2026-11-09_65Q_With_Answers.pdf")

KIND = {
    "single": ("Single answer", 4, (1, 1), "(Choose ONE.)"),
    "two": ("Select TWO", 5, (2, 2), "(Select TWO.)"),
    "three": ("Select THREE", 6, (3, 3), "(Select THREE.)"),
    "all": ("Select ALL", 6, (2, 4), "(Select ALL that apply — extra-hard practice format: 2 to 4 options are "
                                     "correct.)"),
}
DOMAINS = {"1": "Domain 1 — FM integration, data, compliance", "2": "Domain 2 — Implementation and integration",
           "3": "Domain 3 — Safety, security, governance", "4": "Domain 4 — Efficiency and optimisation",
           "5": "Domain 5 — Testing, validation, troubleshooting"}

bank = mock_q1.QS + mock_q2.QS + mock_q3.QS + mock_q4.QS + mock_q5.QS


def check(q, i):
    label, n_opts, (lo, hi), _ = KIND[q["kind"]]
    letters = "ABCDEFG"[:len(q["opts"])]
    assert len(q["opts"]) == n_opts, (i, "option count")
    assert lo <= len(q["ans"]) <= hi and set(q["ans"]) <= set(letters), (i, "answer count")
    assert set(q["wrong"]) == set(letters) - set(q["ans"]), (i, "wrong-option explanations")
    text = " ".join(q["stem"] + q["opts"] + [q["why"]] + list(q["wrong"].values()))
    assert not re.search(r"&(?!amp;|lt;|gt;)", text), (i, "unescaped ampersand")


for i, q in enumerate(bank):
    check(q, i)
assert len(bank) == 65, len(bank)

# Mix domains like the real exam; fixed seed so the numbering never changes between builds.
order = list(range(len(bank)))
random.Random(9112026).shuffle(order)
qs = [bank[i] for i in order]
for q in qs:
    q["level"] = "Very hard" if q["kind"] in ("three", "all") or q["skill"] == "4.1.2" else "Hard"


def add_question(n, num, q):
    label, _, _, instruction = KIND[q["kind"]]
    n.h2(f"Question {num} &nbsp;·&nbsp; {q['level']} &nbsp;·&nbsp; {label} &nbsp;·&nbsp; "
         f"Domain {q['dom']} · Skill {q['skill']}")
    for para in q["stem"]:
        # The type instruction is printed on its own line below, so drop any copy written into the stem.
        n.p(re.sub(r"\s*\(Select (TWO|THREE|ALL that apply)\.\)$", "", para))
    n.p(f"<i>{instruction}</i>")
    for letter, opt in zip("ABCDEFG", q["opts"]):
        n.story.append(Paragraph(opt, S["bullet"], bulletText=f"{letter}."))
    n.space(4)


def add_answer(n, q):
    n.callout(f"Answer: {', '.join(q['ans'])}", q["why"], "ok")
    n.p("<b>Why the other options are wrong</b>")
    n.bullets([f"<b>{k}.</b> {v}" for k, v in sorted(q["wrong"].items())])
    n.space(6)


intro = ("65 questions — the number of scored questions on the real exam — spread by exam weight: Domain 1 = 20, "
         "Domain 2 = 17, Domain 3 = 13, Domain 4 = 8, Domain 5 = 7. Every question is Hard or Very hard. Types: "
         "single answer (4 options), Select TWO (5), Select THREE (6) and Select ALL (6 options, 2–4 correct — "
         "extra-hard practice; the real exam always states the number). Scoring is all-or-nothing per question. "
         "Suggested time: 165 minutes (about 2.5 minutes per question).")

# ---------------------------------------------------------------- questions-only PDF
nq = Note(OUT_Q, "Full Mock 1 — 65 Questions (Whole Syllabus)",
          "Built by Theo prof 2 · Mon 9 Nov 2026 · Exam 1:30 PM IST · Answers in the 'With Answers' PDF")
nq.callout("How to use", intro + " Write your answers on paper, then check them against the With Answers PDF.")
for num, q in enumerate(qs, 1):
    add_question(nq, num, q)
nq.build()

# ---------------------------------------------------------------- with-answers PDF
na = Note(OUT_A, "Full Mock 1 — 65 Questions with Answers and Explanations",
          "Built by Theo prof 2 · Mon 9 Nov 2026 · Each answer, its explanation and why every other option is wrong "
          "appear directly below the question")
na.callout("How to use", intro + " Cover the green box with a sheet of paper, answer, then reveal.")
for num, q in enumerate(qs, 1):
    add_question(na, num, q)
    add_answer(na, q)

na.h1("Answer key at a glance")
na.table(["Q", "Level", "Type", "Domain", "Skill", "Answer"],
         [[str(num), q["level"], KIND[q["kind"]][0], q["dom"], q["skill"], ", ".join(q["ans"])]
          for num, q in enumerate(qs, 1)],
         [0.07, 0.15, 0.2, 0.12, 0.14, 0.32])
by_dom = Counter(q["dom"] for q in qs)
na.table(["Domain", "Questions", "Your score"], [[DOMAINS[d], str(by_dom[d]), "____ / " + str(by_dom[d])]
                                                 for d in sorted(by_dom)], [0.6, 0.2, 0.2])
na.p("Readiness rule: ≥ 75% (49 / 65) ready · 65–75% revise the weakest domain's cheat-sheet tables · below 65% → "
     "focus the remaining time on the decision-rule tables only.")
na.build()

letters = Counter(c for q in qs for c in q["ans"])
print(os.path.abspath(OUT_Q))
print(os.path.abspath(OUT_A))
print("kinds", Counter(q["kind"] for q in qs), "levels", Counter(q["level"] for q in qs))
print("domains", dict(sorted(by_dom.items())), "answer letters", dict(sorted(letters.items())))
