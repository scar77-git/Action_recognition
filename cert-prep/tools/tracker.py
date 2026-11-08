"""Progress tracker PDF — update the data below after every session, then run this script."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import S, Note  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

# Tables here are long; let them start right under their heading instead of jumping to a new page.
H1_SPLIT = ParagraphStyle("h1split", parent=S["h1"], keepWithNext=0)

OUT = os.path.join(os.path.dirname(__file__), "..", "notes", "Progress_Tracker.pdf")
LAST_UPDATED = "Sunday 8 Nov 2026 (End Game Day — all 98 skills taught)"

# day, date, official tasks, added %, total %, status, score, lab, confidence (topic mastery for that day)
DAYS = [
    ("1. RAG + Knowledge Bases", "Tue 13 Oct", "1.4, 1.5 (+ parts of 1.3, 3.1, 5.1)", "+11%", "11%", "✓ Done",
     "Warm-up 3.5/5", "✓ Done", "75% — misses: supported vector stores, Retrieve vs RetrieveAndGenerate"),
    ("2. Agents + tool calling", "Wed 14 Oct", "2.1 part A (+ parts of 2.4)", "+4%", "15%", "✓ Done",
     "Quiz 5/5", "Pending (quota)", "85% — agent loop well understood"),
    ("3. Strands, Agent Squad, MCP, AgentCore", "Thu 15 Oct", "2.1 part B (+ parts of 4.3, 3.2)", "+4%", "19%",
     "✓ Done", "Via Practice Set 1", "Pending (quota)", "80% — theory strong, no hands-on yet"),
    ("Practice Set 1 (30 Q)", "Fri 23 Oct", "Days 1–3 (+ parts of 5.2)", "+2%", "21%", "✓ Done",
     "<b>26/30 (87%)</b>", "—", "87% — 2 of 4 misses were reading errors"),
    ("4. Security and data privacy", "Sat 24 Oct", "3.2", "+4%", "25%", "✓ Done", "Quiz 4.25/5",
     "Studied, not run", "80% — exact names (bedrock-agent-runtime, kms:Decrypt)"),
    ("5. Models and inference", "Sun 25 Oct", "1.2, 2.4, 2.2", "+10%", "35%", "✓ Done", "Quiz <b>8/8</b>",
     "To do later", "85% — new teaching style; lab not yet run"),
    ("Routing mini-lesson (Skill 2.4.4)", "Mon 26 Oct", "2.4.4", "+2%", "37%", "✓ Read",
     "Checks pending", "—", "—"),
    ("Gap lesson (skills missed in studied tasks)", "Mon 26 Oct", "1.2.2–1.2.4, 1.4.1–1.4.3, 1.5.2, 1.5.5, "
     "2.1.3–2.1.7, 2.2.2, 2.4.2–2.4.3", "+10%", "47%", "✓ Done", "Quiz <b>12/12</b> (1 guess)", "—", "85% — strong; review replicas vs primary shards"),
    ("Practice Set 2 (45 Q)", "Mon 26 Oct", "Days 1–5 + gap", "—", "47%", "✓ Done", "<b>41/45 (91%)</b>", "—",
     "89% on hard questions; misses = partial-requirement options"),
    ("6. Guardrails + Responsible AI", "27–29 Oct", "3.1, 3.4", "+9%", "56%", "✓ Done", "Quiz <b>12/12</b>", "—",
     "90% — all hard questions correct"),
    ("7–8. Cost + performance + governance (self-study PDF)", "Fri 30 Oct", "4.1, 4.2, 3.3", "+10%", "66%", "✓ PDF",
     "Quiz <b>8/12</b> (67%)", "—", "70% — self-study; revise caching, cost math, decision logs"),
    ("9. Prompt engineering + design (Theo prof 2)", "30 Oct – 8 Nov", "1.6, 1.1, 2.1.2, 5.2.3, 5.2.5", "+11%",
     "77%", "✓ Done", "Quiz <b>8/10</b> (80%)", "Skipped (exam eve)",
     "80% — revise X-Ray vs invocation logs; map every finding in multi-fix stems"),
    ("End Game Day (Theo prof 2): data pipelines, integration, CI/CD, dev tools, monitoring, evaluation, troubleshooting",
     "Sun 8 Nov", "1.3, 2.3, 2.5, 4.3, 5.1, 5.2.1/5.2.2/5.2.4", "+23%", "100%", "✓ Done", "Quiz <b>20/20</b>",
     "—", "88% — taught fast on exam eve; strong quiz, little time to consolidate"),
    ("Mocks 1–3", "—", "All", "—", "—", "Not taken", "—", "—", "—"),
]

# domain, weight, coverage so far, confidence on what's covered, note
DOMAINS = [
    ("1. FM integration, data management, compliance", "31%", "100% (28 of 28 skills)", "85%",
     "1.3 on End Game Day"),
    ("2. Implementation and integration", "26%", "100% (25 of 25)", "85%", "2.3 / 2.5 on End Game Day"),
    ("3. AI safety, security, governance", "20%", "100% (15 ✓ of 15)", "85%", "Complete"),
    ("4. Operational efficiency and optimisation", "12%", "100% (16 of 16)", "78%",
     "Days 7–8 quiz 67%; 4.3 monitoring End Game 100%"),
    ("5. Testing, validation, troubleshooting", "11%", "100% (14 of 14)", "85%",
     "5.1 / 5.2 End Game Day"),
]

# assessment, date, score, target
ASSESSMENTS = [
    ("Practice Set 1 (Days 1–3, 30 Q)", "23 Oct", "26/30 = 87%", "≥ 75%", "✓ Above target"),
    ("Gap-lesson quiz (12 Q, exam-style options)", "26 Oct", "12/12 = 100%", "≥ 75%", "✓ Above target"),
    ("Day 6 quiz (12 Q, 7 hard)", "29 Oct", "12/12 = 100%", "≥ 75%", "✓ Above target"),
    ("Days 7–8 quiz (self-study, 12 Q)", "30 Oct", "8/12 = 67%", "≥ 75%", "✗ Below — revise"),
    ("Practice Set 2 (Days 1–5 + gap, 45 Q, 60% hard)", "26 Oct", "41/45 = 91%", "≥ 75%", "✓ Above target"),
    ("Day 9 quiz (10 Q, 6 hard, incl. Select ALL)", "8 Nov", "8/10 = 80%", "≥ 75%", "✓ Above target"),
    ("End Game quiz (20 Q, 12 hard, incl. Select ALL)", "8 Nov", "20/20 = 100%", "≥ 75%", "✓ Above target"),
    ("Full mocks 1–3", "—", "—", "≥ 75%", "Not taken; learner doing external practice papers 8–9 Nov"),
]

LAB_BACKLOG = [
    "Day 2 — Converse API tool loop (needs model quota or the Anthropic API key).",
    "Day 3 — Strands single + supervisor agents (code); AgentCore console lab Parts A–E.",
    "Day 4 — Security console lab, at least Part A (IAM Policy Simulator) and Part G (Guardrail PII).",
    "Day 5 — Console lab, start with Part B (request the TPM quota increase).",
]

OVERALL = ("<b>All 98 official skills taught (100% skill coverage).</b> Assessments: Practice Set 1 87%, Practice "
           "Set 2 91%, Day 6 100%, Days 7–8 67%, Day 9 80%, End Game 100%. Estimated confidence ~85%. Risks: no full "
           "timed mock, few hands-on labs, End Game topics learned on exam eve. Final review material: "
           "Final_Exam_Cheat_Sheet_2026-11-08.pdf (decision rules, look-alike pairs, trick cues, mistakes, glossary).")

n = Note(OUT, "Progress Tracker — AWS AIP-C01",
         f"Last updated: <b>{LAST_UPDATED}</b> &nbsp;·&nbsp; Exam: <b>Mon 9 Nov 2026, 1:30 PM IST</b> "
         "&nbsp;·&nbsp; Then Microsoft AI-103 on Sat 28 Nov", wide=True)
n.callout("Where we stand", OVERALL, "ok")

n.story.append(Paragraph("1. Day-by-day progress", H1_SPLIT))
n.table(["Day", "Date", "Official tasks", "+ Added", "Total", "Status", "Score", "Lab", "Confidence"],
        [list(d) for d in DAYS], [0.17, 0.07, 0.15, 0.06, 0.05, 0.07, 0.1, 0.1, 0.23])
n.p("<b>Coverage</b> = skill-level coverage of the official guide (98 skills; covered = 1, partly = ½, weighted by "
    "domain). Projected values for planned days. <b>Confidence</b> = my estimate of how well you'd answer real "
    "exam questions on that day's topics, based on your quiz and practice results.")

n.h1("2. Coverage and confidence by exam domain")
n.table(["Domain", "Exam weight", "Covered", "Confidence", "Notes"], [list(d) for d in DOMAINS],
        [0.32, 0.1, 0.1, 0.1, 0.38])

n.h1("3. Practice sets and mock exams")
n.table(["Assessment", "Date", "Score", "Target", "Status"], [list(a) for a in ASSESSMENTS],
        [0.4, 0.1, 0.18, 0.12, 0.2])
n.p("Readiness rule: mocks ≥ 75% → ready; 65–75% → focus on weakest tasks; below 65% by 3 Nov → discuss rescheduling.")

n.h1("4. Lab backlog")
n.bullets(LAB_BACKLOG)

n.h1("5. Next session")
n.p("<b>Exam: Mon 9 Nov, 1:30 PM IST.</b> Learner's plan: review all PDFs (2 h) → cheat sheet + glossary (1 h) → "
    "AWS Skill Builder / Tutorials Dojo practice questions and our practice sets until 12:30 PM. In the exam: answer "
    "every question, flag and return, list each requirement and strike options that fail any one.")

n.build()
print(os.path.abspath(OUT))
