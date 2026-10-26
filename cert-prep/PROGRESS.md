# Exam prep — progress and handoff

Read this file and `TEACHING_STYLE.md` first when resuming in a new session.
Repo: `scar77-git/Action_recognition`, branch `claude/aws-ai-cert-prep-rpargp`, folder `cert-prep/`.

## Learner
- Senior software engineer, 3 years (Java, Python, PL/SQL), basic cloud/DevOps, no AI work experience.
- 3–4 h/day on weekdays, more on work-from-home days and weekends.
- Wants a demanding but caring professor: explain every term, examples, diagrams, pause after each part.

## Exams
| Exam | Date | Notes |
|---|---|---|
| AWS Certified Generative AI Developer – Professional (AIP-C01) | **Mon 9 Nov 2026, 1:30–4:40 PM IST** (190 min) | Study until 10 AM on exam day. ESL +30 declined. |
| Microsoft AI-103 (Azure AI Apps and Agents Developer Associate) | Sat 28 Nov 2026 | Live (not beta). Plan after 9 Nov. |
| Microsoft AI-500 (Multi-Agent AI Solutions Expert) | December 2026 | After AI-103 (prerequisite path). |

## Account constraints
- Bedrock Agents Classic blocked (maintenance mode, new account) → use Converse API / AgentCore / Strands.
- Bedrock on-demand TPM quota = 0 → console labs that need no model; code labs can use the Anthropic API key
  (learner's own machine, never pasted in chat).

## Rules agreed
- Every day ends with a PDF note in `notes/` named `Day_N_<date>_<Topic>.pdf`, built by `tools/dayNN.py`
  with `tools/notelib.py`. Include task numbers, concepts, lab, graded quiz, mistakes, glossary.
- After every session also update `tools/tracker.py` (DAYS, DOMAINS, ASSESSMENTS, LAB_BACKLOG, OVERALL, LAST_UPDATED)
  and rebuild `notes/Progress_Tracker.pdf` (landscape), then send it.
- Add one or two lines to `JOURNEY.md` after each session (milestones, obstacles, scores) — raw material for
  the learner's LinkedIn post and YouTube video.
- Quiz / warm-up questions only after the whole day's lesson and lab.
- Practice-set answer keys are never committed before the learner answers (keep the generator out of the repo).

## Done
| Day | Date | Official tasks | Result |
|---|---|---|---|
| 1 RAG + Knowledge Bases | 13 Oct | 1.4, 1.5 | Lab done |
| 2 Agents + tool calling | 14 Oct | 2.1 (A) | Quiz 5/5; lab pending (quota) |
| 3 Strands, Agent Squad, MCP, AgentCore, Step Functions | 15 Oct | 2.1 (B) | Labs pending |
| Practice Set 1 (30 Q) | 23 Oct | 1.3–1.5, 2.1, 2.4, 3.1, 3.2, 4.3, 5.1 | **26/30 (87%)**; concept score 28/30 |
| 4 Security and data privacy | 24 Oct | 3.2 | Quiz 4.25/5; lab studied, not run |
| Glossary Days 1–4 | 24 Oct | — | 137 terms |
| 5 Models and inference (new teaching style, 3 parts) | 25 Oct | 1.2, 2.4, 2.2 | Quiz **8/8**; lab pending (console-only steps in PDF) |

Coverage of exam guide ≈ 45%.

## Mistakes log (review every morning)
- DynamoDB is NOT a KB vector store (OpenSearch Serverless, Aurora pgvector, Neptune Analytics, S3 Vectors, Pinecone, MongoDB Atlas, Redis).
- Tool results → toolResult blocks in ONE role "user" message (matching toolUseId); never in the system prompt.
- Custom logic between retrieval and generation → Retrieve + Converse (not RetrieveAndGenerate, not an agent).
- Step Functions Express max 5 min; Standard up to 1 year; approval timeout → TimeoutSeconds/HeartbeatSeconds + Catch States.Timeout.
- Grounding (answer faithful to sources → Guardrails contextual grounding) vs filtering (who sees which docs → metadata filter at retrieval).
- Exact names: KB "data source" (not data store); "Amazon Bedrock Flows"; endpoint "bedrock-agent-runtime".
- KMS AccessDenied on KB sync → key policy must allow the KB role kms:Decrypt.
- Top-p = cumulative probability threshold (top-k = fixed count). Temperature → consistency; grounding → correctness.
- Batch inference (managed file job, hours, ~50% cheaper) vs async SQS (user waiting, on-demand price).
- Habit: read every option to the last word; flag look-alike options.

## Syllabus and coverage
- Official skill list: `reference/AWS_AIP-C01_All_Exam_Tasks_and_Skills.pdf` (5 domains, 20 tasks, 98 skills).
- Plan every lesson from the skill statements, not task titles. Track status in `tools/skills.py`
  (Y / P / N per skill) and rebuild `notes/Skill_Coverage_Matrix.pdf` after each session.
- 26 Oct check: 16 covered, 40 partly, 42 not yet → weighted skill coverage 36%.

## Remaining plan (AWS) — revised 26 Oct after the skill check
| Date | Session | Skills / tasks |
|---|---|---|
| Mon 26 Oct | Routing mini-lesson ✓ (checks pending), then **gap lesson** | 1.2.2–1.2.4, 1.4.1–1.4.3, 1.5.2, 1.5.5, 2.1.3–2.1.7, 2.2.2, 2.4.2–2.4.3 |
| Tue 27 | Day 6 (from Part 1): Guardrails, prompt injection, Responsible AI | 3.1, 3.4 |
| Wed 28 | Day 7 Prompt engineering + design | 1.6, 1.1, 2.1.2, (5.2.3, 5.2.5) |
| Thu 29 | Day 8 Data pipelines + enterprise integration | 1.3, 2.3 |
| Fri 30 | Day 9 App patterns + dev tools + governance | 2.5, 3.3 |
| Sat 31 | Day 10 Cost + performance | 4.1, 4.2 |
| Sun 1 Nov | Day 11 Monitoring + troubleshooting | 4.3, 5.2 |
| Mon 2 | Day 12 Evaluation + Practice Set 2 | 5.1 |
| Tue 3 | Full mock 1 (1:30 PM, 190 min) | all |
| Wed 4 | Weak areas | |
| Thu 5 | Full mock 2 | all |
| Fri 6 | Weak areas + Practice Set 3 + final cheat sheet | |
| Sat 7 | Full mock 3 + review | all |
| Sun 8 | Light review only | |
| Mon 9 | Skim until 10 AM → exam 1:30 PM | |

Readiness rule: mocks ≥75% ready; 65–75% focus weak tasks; <65% by 3 Nov → discuss rescheduling.

## Next action
Teach the **gap lesson** (skills missed inside tasks 1.2, 1.4, 1.5, 2.1, 2.2, 2.4) in 3 parts with pauses; Day 6 has NOT started — teach it from Part 1 (a Part 1 draft was posted on 26 Oct but not studied).
