# Journey log — raw material for the LinkedIn post / YouTube video

Story beats recorded as they happen. Add one or two lines after every session.

## The challenge
- 13 Oct 2026: decided to take AWS Certified Generative AI Developer – Professional (AIP-C01), a hard
  Professional-level exam, with ~4 weeks to prepare, while working full time (3–4 h/day).
- Background: senior software engineer (Java, Python, PL/SQL), no professional AI experience.
- Originally planned two exams (AWS + Microsoft AI-500) in the same window; re-planned to one exam at a time
  after learning AI-500 was in beta (delayed scores) and needed a prerequisite → AI-103 on 28 Nov.

## The method (learning with Claude as a professor)
- Day-by-day syllabus mapped to the 18 official exam-guide tasks, coverage tracked in %.
- Each day: lesson → lab → quiz → PDF note with mistakes log; answer keys hidden until answered.
- Progress Tracker PDF with confidence per day and per exam domain, updated after every session.
- Everything versioned in git — the commit history is the timeline.

## Obstacles and how they were handled
- Day 2: Amazon Bedrock Agents was in maintenance mode for new accounts → switched to the Converse API
  tool loop and AgentCore, which are also exam topics.
- Bedrock model quota of 0 on the new account → console-only labs that need no model; quota increase requested.
- Day 4: feedback that lessons were too dense (abbreviations, tables) → teaching style changed from Day 5:
  plain-English explanations, examples, diagrams, pauses after each part, glossary per day.

## Milestones
| Date | Milestone |
|---|---|
| 13 Oct | Day 1 — RAG and Knowledge Bases, first lab completed |
| 23 Oct | Practice Set 1: 26/30 (87%) on Days 1–3 |
| 24 Oct | Exam booked: Mon 9 Nov, 1:30 PM IST |
| 25 Oct | Day 5 in the new teaching style — quiz 8/8 |
| 26 Oct | Learner spotted a missing skill (2.4.4 model routing) → checked all 98 official skills; coverage was 37%, not ~42%. Built a Skill Coverage Matrix and a gap lesson; coverage now 47%. |
| 26 Oct | Gap-lesson quiz 12/12 after two quiz versions were withdrawn (answers leaked via input suggestions, then via bold formatting) — learner insisted on harder, plausible options. |
| 26 Oct | Practice Set 2 (45 questions, 60% hard, official formats incl. Select THREE / Select ALL): **41/45 (91%)**. |
| 29 Oct | Day 6 (guardrails, prompt injection, responsible AI) after a work break — quiz 12/12; coverage 56%. |
| 30 Oct | No internet at the learner's end → combined Days 7–8 (cost, performance, governance) into an offline self-study PDF with check questions and a quiz; coverage 66%. |
| 30 Oct | Days 7–8 self-study quiz: 8/12 (67%) — first score below target; self-study without a taught lesson showed. |
| 8 Nov | Day 9 (prompt engineering, prompt governance, solution design) with a new professor session ("Theo prof 2") on the eve of the exam — quiz 8/10 (80%); coverage 77%. Learner asked how the Well-Architected GenAI Lens relates to standard components — answered with a Java/SonarQube vs shared-library analogy. |
| 8 Nov | **End Game Day**: the learner refused to stop at 77% the evening before the exam — 33 remaining skills in four parts, then a 20-question quiz scored **20/20**. All 98 official skills taught; a final cheat sheet (decision rules, look-alike pairs, trick cues, mistakes, 353-term glossary) built for the last review. |
| 9 Nov | Exam morning: learner asked for a 65-question whole-syllabus mock (Hard / Very hard, Select ONE / TWO / THREE / ALL) with explanations and why every other option is wrong under each question. |
