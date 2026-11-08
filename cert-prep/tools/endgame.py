"""End Game Day note: every remaining skill (1.3, 2.3, 2.5, 4.3, 5.1, 5.2.1/5.2.2/5.2.4)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import Note  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "End_Game_Day_2026-11-08_All_Remaining_Skills.pdf")

n = Note(OUT, "End Game Day — All Remaining Skills",
         "Sun 8 Nov 2026 (exam eve) &nbsp;·&nbsp; Taught by Theo prof 2 &nbsp;·&nbsp; Skills <b>1.3.1–1.3.4</b>, "
         "<b>2.3.1–2.3.5</b>, <b>2.5.1–2.5.6</b>, <b>4.3.1–4.3.6</b>, <b>5.1.1–5.1.9</b>, <b>5.2.1, 5.2.2, 5.2.4</b> "
         "&nbsp;·&nbsp; After today all 98 official skills have been taught")
n.callout("Today in one paragraph",
          "Check and shape data <b>before</b> it reaches a model (Glue Data Quality, Data Wrangler, Lambda checks, "
          "Textract/Transcribe/BDA, Comprehend, query rewriting, the Converse format). Bolt GenAI onto existing systems "
          "with <b>adapters, events and webhooks</b>, secure it with <b>federation, RBAC/ABAC and metadata filters</b>, "
          "keep regulated data in place with <b>Outposts / Wavelength / PrivateLink</b>, and ship through <b>CI/CD with "
          "GenAI tests and a central gateway</b>. Monitor four layers (operational, FM usage, quality, business) plus "
          "tracing and audit, and evaluate with <b>several metrics, several judges and several moments</b>.", "ok")

n.h1("Where to buy reliable practice exams")
n.bullets([
    "<b>AWS Skill Builder</b> (skillbuilder.aws) — search 'AIP-C01': official practice question set and official "
    "practice exam. Written by AWS; start here.",
    "<b>Tutorials Dojo</b> (portal.tutorialsdojo.com) — AIP-C01 practice exams (~$14.99, timed + review modes, "
    "explanations) and a free 30-question sampler.",
    "<b>Udemy</b> — many AIP-C01 practice courses of uneven quality; only recent, highly rated ones.",
    "Avoid 'exam dump' sites: often wrong, and using them breaks the AWS Certification Agreement.",
])

# ------------------------------------------------------------ Part 1
n.h1("Part 1 — Data pipelines, input quality, input troubleshooting")
n.code(" RAW DATA (S3: PDFs, CSVs, recordings, images)\n"
       "   | S3 event / EventBridge\n"
       " 1 VALIDATE --bad--> s3://.../quarantine/ + metric RejectedDocs + alarm\n"
       " 2 CONVERT  multimodal -> text/structured (Textract, Transcribe, BDA, SageMaker Processing)\n"
       " 3 IMPROVE  normalise, enrich, reformat (Lambda, Comprehend, Bedrock)\n"
       " 4 FORMAT   for the target (Converse messages, JSONL batch, endpoint payload)\n"
       "   -> KB sync / fine-tuning dataset / batch inference")
n.h2("Data validation (1.3.1)")
n.table(["Tool", "What it is", "Exam cue"], [
    ["AWS Glue Data Quality", "Rules in DQDL (Completeness, Uniqueness, ColumnLength…) on Catalog tables or in Glue "
     "jobs; results to CloudWatch / EventBridge to stop the pipeline", "Tabular data at scale, rule-based, no custom code"],
    ["SageMaker Data Wrangler", "Visual data prep; Data Quality and Insights report (missing, duplicates, outliers, "
     "imbalance)", "Data scientists preparing a training / fine-tuning set visually"],
    ["Lambda checks", "Per-file custom checks (parseable, language, size, PII) → quarantine prefix",
     "Rules not enough; per-document logic"],
    ["CloudWatch metrics", "ValidDocs / RejectedDocs / QualityScore + alarm", "Turn validation into monitoring"],
], [0.22, 0.48, 0.3])
n.p("<i>Example:</i> 30% of nightly product descriptions arrive empty → Completeness rule fails → job stops before "
    "the KB sync → the chatbot never answers 'no information available'.")
n.h2("Multimodal processing (1.3.2)")
n.table(["Input", "Service"], [
    ["Scanned docs, forms, tables", "Amazon Textract (OCR + key-value pairs + tables)"],
    ["Speech: calls, meetings", "Amazon Transcribe (timestamps, speaker diarization, custom vocabulary, PII redaction)"],
    ["Mixed docs/images/audio/video → your schema", "Bedrock Data Automation (blueprints); also a KB parser"],
    ["Understand images/video with an FM", "Bedrock multimodal models (Claude image input, Amazon Nova)"],
    ["Search images by meaning", "Titan Multimodal Embeddings"],
    ["Custom heavy preprocessing at scale", "SageMaker Processing jobs (your container, managed batch compute)"],
], [0.42, 0.58])
n.h2("Formatting inputs (1.3.3)")
n.bullets([
    "<b>Converse</b>: one format for all models — messages [{role user|assistant, content blocks}], starts with user, "
    "alternates; system prompt in the separate <i>system</i> field.",
    "<b>InvokeModel</b>: model-specific JSON body (Anthropic anthropic_version + messages; Titan inputText…) → "
    "switching model by changing modelId alone gives ValidationException.",
    "<b>SageMaker endpoint</b>: whatever the container expects, e.g. {\"inputs\": …, \"parameters\": …} + ContentType.",
    "<b>Batch inference</b>: JSONL, one {\"recordId\", \"modelInput\"} per line.",
])
n.h2("Improving input quality (1.3.4)")
n.bullets([
    "<b>Lambda normalisation</b>: strip HTML, fix encoding, unify dates/units, remove boilerplate, de-duplicate.",
    "<b>Comprehend</b>: entities → chunk metadata; dominant language → routing / Translate; PII → mask before storage.",
    "<b>Bedrock reformatting</b>: small model fixes spelling, rewrites follow-ups into <b>standalone questions</b>, "
    "decomposes multi-part questions, converts free text to structure.",
])
n.h2("Troubleshooting content handling (5.2.1)")
n.table(["Symptom", "Cause", "Fix"], [
    ["ValidationException: input too long", "Context window exceeded", "Trim/summarise history, fewer/smaller chunks, "
     "compress, larger-context model"],
    ["Stops mid-sentence, stopReason max_tokens", "Output limit", "Raise maxTokens, shorter format, continue call"],
    ["Long-doc summary ignores the end", "Truncation / lost middle", "Map-reduce summarisation"],
    ["Chunks very uneven", "One chunk size for everything", "Dynamic chunking per document type"],
], [0.32, 0.25, 0.43])
n.h2("Troubleshooting FM integration (5.2.2)")
n.p("Structured error logs (request ID, model ID, Region, error, tokens); <b>API Gateway request validation</b> rejects "
    "bad requests before paying for Lambda/Bedrock; always read <b>stopReason</b> (end_turn, max_tokens, tool_use, "
    "guardrail_intervened, content_filtered).")
n.table(["Error", "Action"], [
    ["ValidationException", "Fix the request (shape, length) — don't retry"],
    ["AccessDeniedException", "Fix IAM / enable model access / KMS key policy"],
    ["ResourceNotFoundException", "Wrong model ID or Region (or use an inference profile)"],
    ["ThrottlingException", "Backoff + jitter; quota increase; cross-Region inference"],
    ["ModelTimeout / ServiceUnavailable / ModelNotReady", "Retry"],
], [0.45, 0.55])
n.h2("Troubleshooting retrieval (5.2.4)")
n.p("First call <b>Retrieve</b> alone: right chunks but wrong answer → prompt/grounding problem; wrong chunks → "
    "retrieval problem.")
n.table(["Symptom", "Fix"], [
    ["All scores low after a model change", "Same embedding model for docs and queries; re-embed everything"],
    ["Exact codes / SKUs missed", "Hybrid search"],
    ["Right doc, chunk lacks context; tables split", "Larger chunks, overlap, hierarchical chunking, parse tables whole"],
    ["Answer drowned in noise", "Smaller / semantic chunks"],
    ["Relevant chunk ranked low", "Reranker (or higher top-k then rerank)"],
    ["New documents never appear", "Ingestion job statistics / failure reasons; sync after uploads"],
    ["Quality declines over months", "Drift: monitor retrieval scores and 'no answer' rate; refresh content"],
    ["Slow at scale", "HNSW tuning, more OCUs/capacity, metadata filters"],
], [0.45, 0.55])

# ------------------------------------------------------------ Part 2
n.h1("Part 2 — Enterprise integration, CI/CD, gateway, interfaces, dev tools")
n.h2("Enterprise connectivity (2.3.1)")
n.code(" GenAI app/agent -> API Gateway (REST, auth, throttling)\n"
       "                 -> Lambda ADAPTER (JSON <-> SOAP/XML)\n"
       "                 -> VPN / Direct Connect -> legacy system on-premises   (+ SQS buffer for fragile systems)")
n.bullets([
    "<b>Event-driven loose coupling</b>: EventBridge rules route business events (TicketCreated) to GenAI Lambdas.",
    "<b>Data sync</b>: SaaS → S3 with <b>AppFlow</b>; databases continuously with <b>DMS CDC</b>; sources → KB with "
    "data source connectors and <b>StartIngestionJob</b> triggered by change events.",
])
n.h2("Adding GenAI to existing apps (2.3.2)")
n.code(" Sync:     App -> API Gateway (/summarise) -> Lambda -> Bedrock -> response\n"
       " Webhook:  Sender -> API GW/Lambda (verify signature, 200 OK fast) -> SQS -> worker Lambda -> Bedrock\n"
       " Events:   CRM 'CaseClosed' -> EventBridge rule -> Lambda -> Bedrock summary -> CRM")
n.h2("Secure access (2.3.3)")
n.bullets([
    "Federation: <b>IAM Identity Center</b> (workforce SSO), <b>Cognito</b> user pools (sign-in, tokens) + identity "
    "pools (temporary AWS credentials), <b>API Gateway authorizers</b> (Cognito / Lambda).",
    "RBAC for models (InvokeModel only on approved ARNs) and data (<b>group claim → KB metadata filter</b>); ABAC with tags.",
    "Least privilege: resource-level ARNs, condition keys, SCP deny for unapproved models, VPC endpoints.",
])
n.h2("Cross-environment compliance (2.3.4)")
n.table(["Service", "Use when"], [
    ["AWS Outposts (AWS racks in your data centre)", "Data must stay on premises; low latency to on-prem systems; "
     "self-hosted open models (Bedrock is a Region service)"],
    ["AWS Wavelength (AWS compute in 5G telecom networks)", "Ultra-low latency to mobile/edge devices"],
    ["AWS Local Zones", "Low latency to a metro area without own hardware"],
    ["Direct Connect / VPN + PrivateLink + Transit Gateway", "Private routing between on-prem and Bedrock"],
    ["Geographic cross-Region inference profile + SCP Region deny", "Residency within a geography in the cloud"],
], [0.45, 0.55])
n.h2("CI/CD and the GenAI gateway (2.3.5)")
n.code(" push -> CodePipeline\n"
       "   CodeBuild: build + unit tests | security scans | GenAI tests (prompt regression, guardrail attack prompts,\n"
       "              schema checks, cost/latency budget)\n"
       "   manual approval (prod) -> deploy (CloudFormation/CDK) -> CodeDeploy canary on Lambda alias\n"
       "   -> CloudWatch alarm -> AUTOMATIC ROLLBACK      (prompts/flows: move version pointer/alias back)\n\n"
       " Teams -> GenAI GATEWAY (API Gateway + Lambda/ECS): auth, per-team usage plans, approved-model routing/fallback,\n"
       "          central guardrails + PII masking, logging, token metering, cost per team -> Bedrock / other providers")
n.h2("Interfaces and developer tools (2.5.1–2.5.6)")
n.bullets([
    "<b>2.5.1</b> Streaming: ConverseStream → WebSocket API or SSE / response streaming. API Gateway integration "
    "timeout 29 s by default → stream or go async (job ID + SQS). Token budgets; SDK standard/adaptive retries, "
    "backoff + jitter, fallback model.",
    "<b>2.5.2</b> <b>Amplify</b> (declarative UI components incl. AI chat, hosting); <b>OpenAPI-first</b> contracts "
    "(API Gateway import, SDKs, agent tool schemas); <b>Bedrock Flows</b> no-code builder.",
    "<b>2.5.3</b> Lambda + CRM (summarise history, draft reply, write back); Step Functions document processing "
    "(BDA/Textract → classify → Choice on confidence → human task token → store); <b>BDA blueprints</b>.",
    "<b>2.5.4</b> <b>Amazon Q Developer</b>: generate/refactor code, API suggestions, unit tests, security scans, "
    "performance tips, agentic multi-file changes. (Q Business = employee assistant over company data.)",
    "<b>2.5.5</b> Strands, Agent Squad, Step Functions agent patterns, Bedrock prompt chaining (recap).",
    "<b>2.5.6</b> Logs Insights over prompts/responses; X-Ray across FM calls; Q Developer for GenAI error patterns.",
])

# ------------------------------------------------------------ Part 3
n.h1("Part 3 — Monitoring and observability (Task 4.3)")
n.code(" 4 BUSINESS     deflection, CSAT, conversions, cost per resolved case   (is it worth it?)\n"
       " 3 QUALITY      hallucination rate, relevance, ratings, drift           (is it RIGHT?)  GenAI-specific\n"
       " 2 FM USAGE     tokens, cost, guardrail blocks, stopReason mix          (how is it used?) GenAI-specific\n"
       " 1 OPERATIONAL  latency, errors, throttles                              (is it UP?)\n"
       "   + TRACING (X-Ray / OpenTelemetry, AgentCore Observability) + AUDIT (CloudTrail, invocation logs)")
n.table(["Skill", "Key points"], [
    ["4.3.1 Holistic", "AWS/Bedrock metrics (Invocations, InvocationLatency, Client/ServerErrors, Throttles, "
     "Input/OutputTokenCount); X-Ray performance tracing; invocation logs + AgentCore traces for FM interactions; "
     "business custom metrics on CloudWatch dashboards / QuickSight."],
    ["4.3.2 KPIs", "Token usage, prompt effectiveness (pass rate per version), hallucination rate (grounding / judge "
     "on samples), quality, response drift. <b>CloudWatch anomaly detection</b> for time-varying bursts; "
     "<b>Cost Anomaly Detection</b> for unusual spend; invocation logs for detail; benchmarks per version."],
    ["4.3.3 Insights", "Dashboards; <b>AWS Config</b> compliance rules + Security Hub; forensics with CloudTrail / "
     "<b>CloudTrail Lake</b> SQL, invocation logs in <b>S3 Object Lock</b>, correlation IDs; user interaction and "
     "behaviour-pattern tracking (refusal, guardrail-intervention rate, length, topics)."],
    ["4.3.4 Tools", "Call patterns, per-tool latency/errors, tool-calling and multi-agent hand-off traces, usage "
     "baselines → anomaly alarms (loops)."],
    ["4.3.5 Vector store", "Latency, request rate, indexing latency, OCUs; scheduled index optimisation (HNSW "
     "ef_search, segment merge, pgvector VACUUM/ANALYZE/reindex, full re-index after embedding change); data quality "
     "(ingestion statistics, duplicates, stale and orphaned vectors)."],
    ["4.3.6 Failure modes", "Golden datasets → hallucinations/regressions; output diffing (semantic similarity) → "
     "inconsistency/drift; reasoning path tracing → logic errors; pipeline: logs → S3 → Athena / Firehose → "
     "OpenSearch, Lambda judge on samples → CloudWatch metrics."],
], [0.18, 0.82])

# ------------------------------------------------------------ Part 4
n.h1("Part 4 — Evaluation (Task 5.1)")
n.code(" WHAT: relevance, correctness, faithfulness, completeness, consistency, fluency, harm, retrieval, agent\n"
       " WHO:  code (exact checks, BLEU/ROUGE/BERTScore) | LLM-as-a-judge | humans (users, annotators)\n"
       " WHEN: design (choose) | CI/CD (quality gate) | rollout (A/B, canary, shadow) | production (continuous)")
n.table(["Skill", "Key points"], [
    ["5.1.1 Metrics", "Relevance, factual accuracy, faithfulness, completeness, consistency, fluency, harmfulness. "
     "BLEU/ROUGE = word overlap; BERTScore = meaning."],
    ["5.1.2 Systematic", "<b>Bedrock Evaluations</b>: automatic, LLM-as-a-judge, human; bring your own responses; "
     "compare jobs. A/B = compare (business outcomes); canary = safe rollout; multi-model; token efficiency, "
     "latency-to-quality, cost per success."],
    ["5.1.3 User-centred", "Thumbs, stars, comments linked to response IDs; implicit signals (rephrase, regenerate, "
     "escalate); annotation with SageMaker Ground Truth / A2I / Bedrock human eval → new golden cases."],
    ["5.1.4 QA process", "Scheduled continuous evaluation in production; regression tests on every change; "
     "automated quality gates that fail deployments."],
    ["5.1.5 Multi-perspective", "RAG evaluation + LLM-as-a-judge (calibrated, different judge model) + human sample."],
    ["5.1.6 Retrieval", "Context relevance, context coverage; hit rate / recall@k, precision@k, MRR; Retrieve "
     "latency p50/p95. KB evaluation: retrieve-only or retrieve-and-generate (faithfulness, citation precision/coverage)."],
    ["5.1.7 Agents", "Task completion rate, tool selection/argument correctness, steps/tokens/cost per task, reasoning "
     "quality from traces; managed agent evaluation on scenario sets incl. edge cases."],
    ["5.1.8 Reporting", "QuickSight (business), CloudWatch dashboards (ops), Athena over results; scheduled Lambda "
     "reports via SNS/SES; model comparison charts; match the audience."],
    ["5.1.9 Deployment validation", "CloudWatch Synthetics canaries running scripted conversations; hallucination and "
     "<b>semantic drift</b> vs baseline; consistency checks; <b>shadow testing</b> (no user impact); canary with "
     "automatic rollback."],
], [0.2, 0.8])

# ------------------------------------------------------------ Quiz
n.h1("End Game quiz — 20 / 20 (100%)")
n.table(["Q", "Level", "Skill", "Answer", "Why (and the trap)"], [
    ["1", "Hard", "1.3.1", "C ✓", "Glue Data Quality (DQDL) + EventBridge halt. Lambda = custom code; Data Wrangler = manual."],
    ["2", "Medium", "1.3.2", "B ✓", "One managed service, many file types, defined schema → BDA blueprints."],
    ["3", "Hard", "1.3.3", "B, D ✓", "Converse = one format; roles must alternate starting with user. Retrying a ValidationException never helps."],
    ["4", "Hard", "1.3.4", "D ✓", "Follow-ups lack context → rewrite to standalone question; index untouched."],
    ["5", "Medium", "5.2.1", "C ✓", "max_tokens with small input = output limit, not context window."],
    ["6", "Hard", "5.2.4", "A, D ✓", "Codes → hybrid search; query/doc embedding mismatch → re-embed with one model."],
    ["7", "Medium", "2.3.1", "D ✓", "Throttled API Gateway + adapter over private link; nightly copy isn't current."],
    ["8", "Hard", "2.3.2", "B, E ✓", "Acknowledge within 5 s, do the 10–30 s work asynchronously."],
    ["9", "Hard", "2.3.3", "C ✓", "Federation + department claim → metadata filter; prompts and guardrails don't enforce access."],
    ["10", "Medium", "2.3.4", "A ✓", "Data must stay in the factory → Outposts with a self-hosted model."],
    ["11", "Hard", "2.3.5", "B, D, F ✓", "Gateway + per-team cost attribution + CI/CD with canary rollback."],
    ["12", "Medium", "2.5.1", "D ✓", "Streaming fixes both the 29 s timeout and the perceived wait."],
    ["13", "Medium", "2.5.2/2.5.4", "B, D ✓", "Amplify UI for the front-end; Q Developer for code work (not Q Business)."],
    ["14", "Hard", "2.5.3", "A ✓", "Two-day human wait → Standard workflow + task token; Express max 5 min."],
    ["15", "Hard", "4.3.2", "C, E ✓", "Time-varying metric → anomaly detection; unusual spend → Cost Anomaly Detection."],
    ["16", "Medium", "4.3.3", "C ✓", "Exact response + tamper-proof for 7 years → invocation logs in S3 Object Lock."],
    ["17", "Hard", "4.3.4/4.3.6", "C, E ✓", "Cost up, answers fine → tool-call baselines (loops); wrong conclusion → reasoning traces."],
    ["18", "Hard", "5.1.2/5.1.9", "A, E ✓", "No user impact → shadow; gradual + rollback → canary with alarms."],
    ["19", "Medium", "5.1.6", "A ✓", "KB evaluation retrieve-only: context relevance + coverage."],
    ["20", "Hard", "5.1.3–5.1.5", "B, D, E, F ✓", "Judge for scale, experts for tone, users for learning, gate for deployments."],
], [0.04, 0.08, 0.1, 0.12, 0.66])

n.h1("Glossary — new terms")
n.table(["Term", "Meaning"], [
    ["AWS Glue Data Quality / DQDL", "Rule-based data checks in Glue / the rule language (Completeness, Uniqueness…)."],
    ["SageMaker Data Wrangler", "Visual data preparation with a data quality and insights report."],
    ["Quarantine prefix", "S3 location where invalid files are moved for review."],
    ["Multimodal", "Data beyond plain text: images, scans, audio, video."],
    ["Amazon Textract", "OCR service extracting text, key-value pairs and tables from documents."],
    ["OCR (Optical Character Recognition)", "Reading text from images."],
    ["Amazon Transcribe", "Speech-to-text with diarization, custom vocabulary and PII redaction."],
    ["Speaker diarization", "Labelling who spoke when in a recording."],
    ["Bedrock Data Automation (BDA) / blueprint", "Managed extraction from documents and media / your field schema for it."],
    ["SageMaker Processing job", "Managed batch compute running your own preprocessing container."],
    ["Titan Multimodal Embeddings", "Embedding model placing images and text in one vector space."],
    ["JSONL", "File with one JSON object per line (batch inference input)."],
    ["Query rewriting / decomposition", "Turning a follow-up into a standalone question / splitting a complex question."],
    ["Map-reduce summarisation", "Summarise chunks separately, then summarise the summaries."],
    ["Dynamic chunking", "Choosing chunking strategy and size per document type."],
    ["API Gateway request validation", "Schema checks that reject malformed requests before the backend runs."],
    ["Adapter (Lambda)", "Translator between a modern JSON API and a legacy protocol such as SOAP."],
    ["Direct Connect / Site-to-Site VPN", "Dedicated private line / encrypted tunnel between on-premises and AWS."],
    ["Loose coupling", "Systems interact through events, so each can change or fail independently."],
    ["Amazon EventBridge", "Event bus routing events to targets by rules."],
    ["Amazon AppFlow", "Managed no-code data transfer from SaaS apps to AWS."],
    ["AWS DMS / CDC", "Database Migration Service / Change Data Capture streaming only changed rows."],
    ["Webhook", "HTTP callback a third-party system sends when an event happens."],
    ["IAM Identity Center", "Workforce single sign-on to AWS accounts and roles."],
    ["Amazon Cognito user / identity pool", "App user sign-in and tokens / exchange for temporary AWS credentials."],
    ["Lambda authorizer", "Custom token check protecting an API Gateway API."],
    ["RBAC / ABAC", "Access by role / access by attributes such as tags."],
    ["AWS Outposts", "AWS-managed racks running AWS services in your own data centre."],
    ["AWS Wavelength", "AWS compute inside telecom 5G networks for ultra-low latency."],
    ["AWS Local Zones", "Small AWS sites near large cities."],
    ["Transit Gateway", "Hub connecting many VPCs and on-premises networks."],
    ["CI/CD", "Continuous Integration / Continuous Delivery: automated build, test, deploy."],
    ["CodePipeline / CodeBuild / CodeDeploy", "Pipeline orchestration / build and test runs / gradual deploys with rollback."],
    ["GenAI gateway", "Central layer all apps use to reach models: auth, quotas, routing, guardrails, logging, cost."],
    ["Usage plan", "API Gateway per-client throttling and quota tied to API keys."],
    ["SSE (Server-Sent Events)", "One-way server-to-browser stream over HTTP."],
    ["AWS Amplify / Amplify UI", "Front-end framework and hosting / declarative ready-made UI components."],
    ["OpenAPI specification", "Machine-readable API contract used for API-first development."],
    ["Amazon Q Developer", "AI coding assistant: generate, refactor, test, explain, optimise code."],
    ["Amazon Q Business", "Enterprise assistant answering employees from company data."],
    ["KPI", "Key Performance Indicator."],
    ["CloudWatch anomaly detection", "Learned expected band for a metric; alarm when outside it."],
    ["AWS Cost Anomaly Detection", "Billing feature alerting on unusual spend patterns."],
    ["AWS Config", "Continuous checks of resource configuration against rules."],
    ["CloudTrail Lake", "Queryable (SQL) store of CloudTrail audit events."],
    ["S3 Object Lock (WORM)", "Write once, read many: objects can't be changed or deleted for a period."],
    ["Correlation ID", "Request ID carried through every log line to trace one request end to end."],
    ["Output diffing", "Comparing outputs for the same input across runs or versions."],
    ["Reasoning path tracing", "Inspecting each reasoning/tool step to find where logic fails."],
    ["BLEU / ROUGE / BERTScore", "Word-overlap metrics / meaning-based similarity metric."],
    ["Faithfulness", "Every claim in the answer is supported by the provided context."],
    ["A/B test / canary / shadow test", "Compare configs on split users / small % rollout / mirror traffic without "
     "showing results."],
    ["SageMaker Ground Truth / Amazon A2I", "Labelling workforce service / human review loops."],
    ["Quality gate", "Pipeline step that fails a deployment below quality thresholds."],
    ["Context relevance / context coverage", "Retrieved chunks are relevant / contain the needed information."],
    ["Hit rate (recall@k) / precision@k / MRR", "Right chunk in top k / share of top k relevant / rewards rank 1."],
    ["Task completion rate", "Share of agent tasks fully and correctly finished."],
    ["CloudWatch Synthetics canary", "Scheduled script acting as a synthetic user against an endpoint."],
    ["Semantic drift", "Answers' meaning shifting versus a baseline for the same questions."],
], [0.36, 0.64])

n.callout("Next", "Read the Final Exam Cheat Sheet (decision rules, trick cues, mistakes, consolidated glossary), then "
          "practice questions until 12:30 PM. Exam 1:30 PM IST.")
n.build()
print(os.path.abspath(OUT))
