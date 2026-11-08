"""Final exam cheat sheet: strategy, decision rules, look-alike pairs, trick cues, mistakes, consolidated glossary.

The mistakes log is read from PROGRESS.md and the glossary is merged from every day's glossary table at build
time, so this sheet stays in sync with the other notes.
"""
import ast
import html
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import S, Note  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "notes", "Final_Exam_Cheat_Sheet_2026-11-08.pdf")
H1_SPLIT = ParagraphStyle("h1split", parent=S["h1"], keepWithNext=0)
GLOSSARY_SOURCES = ["glossary.py", "gap01.py", "day05.py", "day06.py", "day07_08.py", "day09.py", "endgame.py"]


def mistakes_from_progress():
    lines = open(os.path.join(HERE, "..", "PROGRESS.md"), encoding="utf-8").read().splitlines()
    start = lines.index("## Mistakes log (review every morning)") + 1
    out = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if line.startswith("- "):
            out.append(html.escape(line[2:], quote=False))
        elif line.startswith("  ") and out:
            out[-1] += " " + html.escape(line.strip(), quote=False)
    return out


def harvested_glossary():
    terms = {}
    for name in GLOSSARY_SOURCES:
        tree = ast.parse(open(os.path.join(HERE, name), encoding="utf-8").read())
        for node in tree.body:
            if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "SECTIONS":
                for _section, rows in ast.literal_eval(node.value):
                    for term, full, meaning, _example in rows:
                        label = term if full in ("—", "", term) else f"{term} ({full})"
                        terms.setdefault(term.split(" (")[0].strip().lower(), (label, meaning))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "table" and len(node.args) >= 2:
                try:
                    header, rows = ast.literal_eval(node.args[0]), ast.literal_eval(node.args[1])
                except ValueError:
                    continue
                if header == ["Term", "Meaning"]:
                    for term, meaning in rows:
                        terms.setdefault(term.split(" (")[0].strip().lower(), (term, meaning))
    return sorted(terms.values(), key=lambda t: t[0].lower())


n = Note(OUT, "Final Exam Cheat Sheet — AWS AIP-C01",
         "Exam: <b>Mon 9 Nov 2026, 1:30 PM IST</b> &nbsp;·&nbsp; Built by Theo prof 2 from Days 1–9, the gap lesson, "
         "End Game Day, both practice sets and every quiz &nbsp;·&nbsp; All 98 official skills taught")

# ------------------------------------------------------------ 1. strategy
n.h1("1. Exam-day strategy")
n.bullets([
    "Format: 75 questions (65 scored + unscored ones that look identical), multiple choice (1 of 4) and multiple "
    "response (2+ of 5–7, all-or-nothing). Scaled score 100–1000; professional exams usually pass at 750.",
    "<b>Answer every question</b> — blank = wrong, no penalty for guessing. Flag and move on after ~3 minutes.",
    "Pace: ~2.5 min per question → question 25 by ~2:35 PM, question 50 by ~3:40 PM, leave 15+ min to review flags.",
    "<b>List every requirement in the stem</b> (cost, latency, 'no code changes', 'least overhead', residency, "
    "audit…) and strike any option that fails even one.",
    "<b>Read every option to the last word</b> — look-alike options differ in one phrase (Express vs Standard, draft "
    "vs alias, CloudTrail vs invocation logs).",
    "Multi-finding stems: map each finding to an option before submitting; a missing fix makes the answer wrong.",
    "Wrong options are usually real AWS approaches that fail one requirement — ask 'which requirement does this miss?'",
])

# ------------------------------------------------------------ 2. decision rules
n.story.append(Paragraph("2. Decision rules by domain — 'stem says → answer'", H1_SPLIT))
n.h2("Domain 1 — FM integration, data, compliance (31%)")
n.table(["Stem says…", "Answer"], [
    ["Knowledge changes often / must cite sources", "RAG (Knowledge Base) + scheduled or event-driven sync"],
    ["Style, tone, format, domain behaviour", "Fine-tuning (labelled pairs); raw domain text → continued pre-training"],
    ["Small model must behave like a big one", "Distillation; trained elsewhere → Custom Model Import"],
    ["Most cost-effective model meeting quality", "Smallest adequate model, proven with Bedrock model evaluation"],
    ["Consistent output", "Low temperature; correctness → grounding; cut off → raise maxTokens"],
    ["Custom logic between retrieval and generation", "Retrieve + Converse (not RetrieveAndGenerate)"],
    ["Exact codes/IDs missed", "Hybrid search; right docs wrong order → reranker; context lost → hierarchical chunking"],
    ["Tables / complex PDFs parsed badly", "FM parsing or Bedrock Data Automation"],
    ["Relationships across entities", "GraphRAG (Neptune Analytics)"],
    ["Vector store options", "OpenSearch Serverless, Aurora pgvector, Neptune Analytics, S3 Vectors, Pinecone, "
     "MongoDB Atlas, Redis — never DynamoDB"],
    ["Vague / multi-part / follow-up questions", "Query expansion / decomposition / rewriting to standalone"],
    ["Rule-based data checks at scale, no code", "Glue Data Quality (DQDL) → EventBridge halt"],
    ["Visual dataset prep for training", "SageMaker Data Wrangler"],
    ["Many media types → one schema, managed", "Bedrock Data Automation; calls → Transcribe; scans → Textract; "
     "custom container → SageMaker Processing"],
    ["Switch models with one request format", "Converse API"],
    ["Persona/rules consistent across teams, change without redeploy", "Prompt Management versions referenced by ARN "
     "(pointer in AppConfig)"],
    ["Parser-safe structured output", "Tool schema + toolChoice + Lambda validation"],
    ["Prompt chain with branching inside Bedrock, low-code", "Bedrock Flows (alias + InvokeFlow)"],
    ["Missing details must be asked, long waits", "Step Functions Standard + .waitForTaskToken; history in DynamoDB"],
    ["New prompt must not reduce quality", "Golden set + Map state + Lambda checks + PassRate alarm gate"],
    ["Validate feasibility before investing", "PoC: measurable criteria first, on-demand, sample KB, evaluation jobs"],
    ["Consistent implementation across teams", "WA Tool + GenAI Lens → reusable CDK/CloudFormation via Service Catalog"],
], [0.45, 0.55])
n.h2("Domain 2 — Implementation and integration (26%)")
n.table(["Stem says…", "Answer"], [
    ["Fixed, known steps", "Workflow / Step Functions / Flows — not an agent"],
    ["Path depends on intermediate results", "Agent (ReAct loop with iteration cap)"],
    ["Full control of the tool loop", "Converse API with toolConfig; results as toolResult in a user message"],
    ["Framework-agnostic agent hosting, session isolation", "AgentCore Runtime"],
    ["Reuse tools across teams and frameworks", "MCP, often via AgentCore Gateway"],
    ["Act in third-party apps as the user", "AgentCore Identity (outbound OAuth)"],
    ["Remember users across sessions", "AgentCore Memory long-term"],
    ["Each request to one specialist / several combined", "Router (Agent Squad classifier) / supervisor"],
    ["Runaway agents", "Stopping conditions, iteration caps, timeouts, budgets, least-privilege IAM"],
    ["Stop hammering a failing model", "Circuit breaker (Step Functions + DynamoDB state)"],
    ["Switch model without redeploy", "AppConfig (+ gradual rollout, alarm rollback)"],
    ["Route by content to specialised FMs", "Classify step + Choice state; same family by quality → Intelligent Prompt Routing"],
    ["Throttling", "Backoff + jitter → cross-Region inference → SQS buffer → quota / Provisioned Throughput"],
    ["User waiting, feels slow", "Streaming (ConverseStream → WebSocket / SSE)"],
    ["API Gateway 504 at ~29 s", "Stream, or async: job ID + SQS + worker + stored result"],
    ["Huge non-urgent volume", "Batch inference (~50% cheaper)"],
    ["Legacy SOAP / fragile on-prem system", "API Gateway throttling + Lambda adapter + VPN/Direct Connect (+ SQS buffer)"],
    ["Webhook with short sender timeout", "Verify, enqueue, 200 fast; worker does the GenAI work"],
    ["Only documents the user may see", "Identity group claim → KB metadata filter"],
    ["Data must stay on premises / 5G edge latency", "Outposts / Wavelength"],
    ["Many teams: approved models, quotas, cost per team, swap providers", "GenAI gateway + usage plans + application "
     "inference profiles"],
    ["Ship GenAI changes safely", "CodePipeline + CodeBuild (prompt regression, guardrail, security tests) + "
     "CodeDeploy canary with alarm rollback"],
    ["Chat UI fast / API contract first / speed up developers", "Amplify UI / OpenAPI / Amazon Q Developer"],
], [0.45, 0.55])
n.h2("Domain 3 — Safety, security, governance (20%)")
n.table(["Stem says…", "Answer"], [
    ["Must always block, regardless of user input", "Guardrails (not the system prompt)"],
    ["A subject however worded / exact words", "Denied topic / word filter"],
    ["Answer must be supported by sources", "Contextual grounding (grounding + relevance thresholds)"],
    ["Provably consistent with written rules", "Automated Reasoning checks"],
    ["Same policies for non-Bedrock models", "ApplyGuardrail; only user text → input tagging"],
    ["Hidden instructions in documents/emails", "Indirect prompt injection: sanitise, check retrieved content, least "
     "privilege, human confirmation"],
    ["Find PII in S3 / redact in pipeline / mask at runtime", "Macie / Comprehend / Guardrails"],
    ["Column or row restrictions on lake data", "Lake Formation"],
    ["No public internet", "Interface VPC endpoints (bedrock-runtime, bedrock-agent-runtime)"],
    ["Restrict models for a team / whole org", "IAM with model ARNs / SCP deny"],
    ["Own and rotate keys; sync fails after enabling KMS", "Customer managed KMS key; key policy must allow the role"],
    ["Who did it / what text / why this answer", "CloudTrail / invocation logging / decision logs"],
    ["Must not change for N years", "S3 Object Lock (compliance mode)"],
    ["Fairness", "Per-group metrics + counterfactual tests; document limits in model cards"],
], [0.45, 0.55])
n.h2("Domain 4 — Efficiency and monitoring (12%)")
n.table(["Stem says…", "Answer"], [
    ["Same long prefix every call", "Prompt caching (static content first)"],
    ["Identical / reworded repeat questions", "Exact-match cache / semantic cache (invalidate on KB sync)"],
    ["Latency dominated by long answers", "Cap output length first"],
    ["Cost per team", "Application inference profiles + tags"],
    ["Steady guaranteed capacity / spiky", "Provisioned Throughput / on-demand (+ cross-Region inference)"],
    ["Metric varies by time of day", "CloudWatch anomaly detection"],
    ["Unexpected spend", "AWS Cost Anomaly Detection"],
    ["Which service in the chain is slow", "X-Ray"],
    ["Analyse prompts/responses at scale", "Logs Insights / Athena over invocation logs"],
    ["Agent cost up, answers fine", "Tool call baselines → loops"],
    ["Compliance drift (logging off, no guardrail)", "AWS Config rules"],
    ["Vector store slow / stale / deleted docs still found", "Index tuning, capacity, filters / sync deletions"],
], [0.45, 0.55])
n.h2("Domain 5 — Testing, validation, troubleshooting (11%)")
n.table(["Stem says…", "Answer"], [
    ["Pick a model with our own data, least effort", "Bedrock model evaluation job (automatic / LLM-as-a-judge / human)"],
    ["Is the retriever the problem?", "Retrieve alone; KB evaluation retrieve-only (context relevance, coverage)"],
    ["Validate on real traffic, no user impact", "Shadow testing"],
    ["Gradual release with automatic rollback", "Canary + alarms"],
    ["Compare business outcomes of two configs", "A/B test"],
    ["Broken flow when no users are active", "CloudWatch Synthetics canaries"],
    ["Meaning of answers changed after upgrade", "Semantic drift check vs baseline"],
    ["Same question, different answers", "Output diffing / consistency analysis (+ temperature)"],
    ["Right data, wrong conclusion", "Reasoning path tracing"],
    ["Block deployments that reduce quality", "Automated quality gate in the pipeline"],
    ["Scale + subjective tone + learn from users", "LLM-as-a-judge + human annotation sample + user feedback"],
    ["Wrong behaviour, latency normal", "Rendered prompt in invocation logs (Logs Insights)"],
    ["stopReason max_tokens, small input", "Raise maxTokens / shorter format"],
    ["ValidationException / AccessDenied", "Fix, don't retry; Throttling / ServiceUnavailable → retry"],
], [0.45, 0.55])

# ------------------------------------------------------------ 3. look-alikes
n.story.append(Paragraph("3. Look-alike pairs the exam uses to confuse you", H1_SPLIT))
n.table(["Pair", "The difference"], [
    ["Grounding vs filtering", "Answer true to sources (Guardrails) vs who may see which sources (metadata filter)"],
    ["CloudTrail vs invocation logs vs decision logs", "Who called which API vs exact prompt/response text vs why "
     "this answer (sources, versions)"],
    ["X-Ray vs Logs Insights", "Where time/errors occur across services vs what the content was"],
    ["Retrieve vs RetrieveAndGenerate", "Chunks only (custom logic after) vs managed retrieval + answer"],
    ["Step Functions Express vs Standard", "Max 5 minutes, high volume vs up to 1 year, waits, full history"],
    ["Batch inference vs async SQS vs StartAsyncInvoke", "Managed file job, hours, ~50% cheaper vs user waiting, "
     "on-demand price vs native async for slow media generation"],
    ["Provisioned Throughput vs cross-Region inference", "Guaranteed capacity, commitment vs more throughput, no extra cost"],
    ["Intelligent Prompt Routing vs content routing", "Within one model family by predicted quality vs classify + Choice"],
    ["Denied topics vs word filters", "Meaning vs exact words"],
    ["Contextual grounding vs Automated Reasoning", "Similarity to sources vs formal logic against rules"],
    ["Fine-tuning vs continued pre-training vs distillation", "Labelled pairs vs raw text vs teacher → student"],
    ["Prompt Management vs Flows/Agents lifecycle", "Versions only (pointer in config) vs versions + aliases"],
    ["Prompt caching vs exact cache vs semantic cache", "Reused prefix tokens vs identical request vs similar meaning"],
    ["Hybrid search vs reranker vs hierarchical chunking", "Exact terms vs ordering vs lost context"],
    ["Temperature vs top-p vs top-k", "Randomness vs cumulative probability threshold vs fixed count"],
    ["Router vs supervisor", "One specialist per request vs combining several"],
    ["Macie vs Comprehend vs Guardrails (PII)", "Find in S3 vs redact in pipeline vs mask/block at runtime"],
    ["Glue Data Quality vs Data Wrangler", "Automated rules in pipelines vs visual exploration"],
    ["BDA vs Textract vs SageMaker Processing", "Many media → schema vs document OCR vs custom container"],
    ["Outposts vs Wavelength vs Local Zones", "Your data centre vs 5G edge vs metro site"],
    ["Q Developer vs Q Business", "Developers' coding assistant vs employees' assistant over company data"],
    ["A/B vs canary vs shadow", "Compare outcomes vs safe gradual rollout vs no user impact"],
    ["Anomaly detection vs Cost Anomaly Detection vs Budgets", "Metric band vs unusual spend vs fixed amount"],
    ["Replicas vs shards", "Throughput + availability vs parallel capacity for big indexes"],
    ["Agent action group vs MCP / AgentCore Gateway", "Tools for one Bedrock agent vs tools shared across frameworks"],
], [0.38, 0.62])

# ------------------------------------------------------------ 4. trick cues
n.h1("4. Trick-question cues")
n.table(["Cue in the stem or option", "What it signals"], [
    ["'LEAST operational overhead'", "Managed feature (KB, Flows, Guardrails, BDA) beats custom Lambda/EC2 code"],
    ["'MOST cost-effective'", "Smallest adequate model, batch, caching, routing — not Provisioned Throughput by reflex"],
    ["'without code changes / redeploying'", "AppConfig, Prompt Management version pointer, aliases, gateway"],
    ["'always / regardless of input / enforce'", "Guardrails, IAM, SCP — never a prompt instruction"],
    ["'only the documents they are allowed to see'", "Metadata filter at retrieval from identity claims"],
    ["'exact text' vs 'who'", "Invocation logging vs CloudTrail"],
    ["'reworded' / 'similar questions'", "Semantic, not exact-match, cache"],
    ["'hours' / 'days' / 'human approval'", "Step Functions Standard + task token, not Express"],
    ["'no impact on users'", "Shadow testing"],
    ["'real-time' / 'user waiting'", "Streaming or synchronous; 'overnight' → batch"],
    ["Option fine-tunes for facts that change", "Wrong — RAG"],
    ["Option retries a ValidationException", "Wrong — fix the request"],
    ["Option puts security in the system prompt", "Wrong — Guardrails / IAM / filters"],
    ["Option uses DynamoDB as the vector store", "Wrong — metadata or history only"],
    ["'publish a wiki' / 'ask teams to' / 'review manually monthly'", "Wrong when consistency or automation is required"],
    ["Option correct but covers only part of the stem", "Wrong — your most common past error pattern"],
    ["Draft (agent, flow, prompt) used in production", "Wrong — versions/aliases"],
], [0.42, 0.58])

# ------------------------------------------------------------ 5. numbers and names
n.h1("5. Numbers and exact names")
n.bullets([
    "Step Functions Express ≤ 5 min; Standard ≤ 1 year. Lambda ≤ 15 min. API Gateway integration timeout 29 s default.",
    "Batch inference ≈ 50% cheaper than on-demand; input is JSONL (recordId + modelInput).",
    "KB 'data source' (not data store); endpoint <b>bedrock-agent-runtime</b> for Retrieve, InvokeAgent, InvokeFlow; "
    "<b>bedrock-runtime</b> for Converse / InvokeModel.",
    "'Amazon Bedrock Flows' (formerly Prompt Flows). Model lifecycle Active → Legacy → End-of-Life.",
    "Tool results: toolResult blocks in ONE role 'user' message with the matching toolUseId.",
    "stopReason values: end_turn, max_tokens, tool_use, guardrail_intervened, content_filtered.",
    "Bedrock CloudWatch metrics: Invocations, InvocationLatency, InvocationClientErrors, InvocationServerErrors, "
    "InvocationThrottles, InputTokenCount, OutputTokenCount.",
])

# ------------------------------------------------------------ 6. mistakes
n.h1("6. Your mistakes log — read this last tonight and first tomorrow")
n.bullets(mistakes_from_progress())

# ------------------------------------------------------------ 7. glossary
terms = harvested_glossary()
n.story.append(Paragraph(f"7. Consolidated glossary — {len(terms)} terms (all days, alphabetical)", H1_SPLIT))
n.table(["Term", "Meaning"], [[t, m] for t, m in terms], [0.34, 0.66])

n.callout("Last word", "You've covered all 98 skills. Trust the method: requirements list → strike failing options → "
          "managed, least-privilege, automated answer that satisfies every constraint. Good luck, 1:30 PM.", "ok")
n.build()
print(os.path.abspath(OUT), len(terms))
