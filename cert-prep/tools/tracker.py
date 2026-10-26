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
LAST_UPDATED = "Monday 26 Oct 2026 (after Day 5)"

# day, date, official tasks, added %, total %, status, score, lab, confidence (topic mastery for that day)
DAYS = [
    ("1. RAG + Knowledge Bases", "Tue 13 Oct", "1.4, 1.5 (+ parts of 1.3, 3.1, 5.1)", "+12%", "12%", "✓ Done",
     "Warm-up 3.5/5", "✓ Done", "75% — misses: supported vector stores, Retrieve vs RetrieveAndGenerate"),
    ("2. Agents + tool calling", "Wed 14 Oct", "2.1 part A (+ parts of 2.4)", "+5%", "17%", "✓ Done",
     "Quiz 5/5", "Pending (quota)", "85% — agent loop well understood"),
    ("3. Strands, Agent Squad, MCP, AgentCore", "Thu 15 Oct", "2.1 part B (+ parts of 4.3, 3.2)", "+5%", "22%",
     "✓ Done", "Via Practice Set 1", "Pending (quota)", "80% — theory strong, no hands-on yet"),
    ("Practice Set 1 (30 Q)", "Fri 23 Oct", "Days 1–3 (+ parts of 5.2)", "+3%", "25%", "✓ Done",
     "<b>26/30 (87%)</b>", "—", "87% — 2 of 4 misses were reading errors"),
    ("4. Security and data privacy", "Sat 24 Oct", "3.2", "+3%", "28%", "✓ Done", "Quiz 4.25/5",
     "Studied, not run", "80% — exact names (bedrock-agent-runtime, kms:Decrypt)"),
    ("5. Models and inference", "Sun 25 Oct", "1.2, 2.4, 2.2", "+14%", "42%", "✓ Done", "Quiz <b>8/8</b>",
     "To do later", "85% — new teaching style; lab not yet run"),
    ("6. Guardrails + Responsible AI", "Mon 26 Oct", "3.1, 3.4", "+8%", "50%", "Next", "—", "—", "—"),
    ("7. Prompt engineering + design", "Tue 27 Oct", "1.6, 1.1", "+9%", "59%", "Planned", "—", "—", "—"),
    ("8. Pipelines + integration + dev tools", "Wed 28 Oct", "1.3, 2.3, 2.5", "+14%", "73%", "Planned", "—", "—", "—"),
    ("9. Governance and compliance", "Thu 29 Oct", "3.3", "+5%", "78%", "Planned", "—", "—", "—"),
    ("10. Cost + performance", "Fri 30 Oct", "4.1, 4.2", "+7%", "85%", "Planned", "—", "—", "—"),
    ("11. Monitoring + evaluation + troubleshooting", "Sat 31 Oct", "4.3, 5.1, 5.2 + Practice Set 2", "+10%", "95%",
     "Planned", "—", "—", "—"),
    ("Mocks + reviews", "1–8 Nov", "Gaps found by mocks", "+5%", "100%", "Planned", "—", "—", "—"),
]

# domain, weight, coverage so far, confidence on what's covered, note
DOMAINS = [
    ("1. FM integration, data management, compliance", "31%", "~49%", "80%",
     "1.4, 1.5, 1.2 done; 1.1, 1.3, 1.6 to come (Days 7–8)"),
    ("2. Implementation and integration", "26%", "~55%", "85%", "2.1, 2.2, 2.4 done; 2.3, 2.5 on Day 8"),
    ("3. AI safety, security, governance", "20%", "~29%", "80%", "3.2 done; 3.1, 3.4 Day 6; 3.3 Day 9"),
    ("4. Operational efficiency and optimisation", "12%", "~15%", "—", "Mostly Days 10–11"),
    ("5. Testing, validation, troubleshooting", "11%", "~25%", "75%", "Mostly Day 11"),
]

# assessment, date, score, target
ASSESSMENTS = [
    ("Practice Set 1 (Days 1–3, 30 Q)", "23 Oct", "26/30 = 87%", "≥ 75%", "✓ Above target"),
    ("Practice Set 2 (Days 4–11 + 5 from Days 1–3)", "31 Oct", "—", "≥ 75%", "Planned"),
    ("Full mock 1 (75 Q, 190 min, 1:30 PM)", "1 Nov", "—", "≥ 75%", "Planned"),
    ("Full mock 2", "3 Nov", "—", "≥ 75%", "Planned"),
    ("Practice Set 3 (weakest tasks)", "4 Nov", "—", "≥ 75%", "Planned"),
    ("Full mock 3", "5 Nov", "—", "≥ 75%", "Planned"),
]

LAB_BACKLOG = [
    "Day 2 — Converse API tool loop (needs model quota or the Anthropic API key).",
    "Day 3 — Strands single + supervisor agents (code); AgentCore console lab Parts A–E.",
    "Day 4 — Security console lab, at least Part A (IAM Policy Simulator) and Part G (Guardrail PII).",
    "Day 5 — Console lab, start with Part B (request the TPM quota increase).",
]

OVERALL = ("<b>Overall confidence on topics covered so far: ~83%.</b> Coverage of the exam guide: <b>~42%</b>. "
           "Strongest: agents and tools (2.1), models and inference (1.2, 2.2, 2.4). Watch: exact service names and "
           "limits, and reading every option to the end. Biggest risk: no hands-on labs since Day 1.")

n = Note(OUT, "Progress Tracker — AWS AIP-C01",
         f"Last updated: <b>{LAST_UPDATED}</b> &nbsp;·&nbsp; Exam: <b>Mon 9 Nov 2026, 1:30 PM IST</b> "
         "&nbsp;·&nbsp; Then Microsoft AI-103 on Sat 28 Nov", wide=True)
n.callout("Where we stand", OVERALL, "ok")

n.story.append(Paragraph("1. Day-by-day progress", H1_SPLIT))
n.table(["Day", "Date", "Official tasks", "+ Added", "Total", "Status", "Score", "Lab", "Confidence"],
        [list(d) for d in DAYS], [0.17, 0.07, 0.15, 0.06, 0.05, 0.07, 0.1, 0.1, 0.23])
n.p("<b>Coverage</b> = share of the official exam guide studied (domain weights split equally across tasks; a studied "
    "task counts as ~85% covered — mocks fill the rest). <b>Confidence</b> = my estimate of how well you'd answer real "
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
n.p("<b>Day 6 — Guardrails and Responsible AI (Tasks 3.1, 3.4)</b>, three parts with pauses, then lab, quiz and PDF.")

n.build()
print(os.path.abspath(OUT))
