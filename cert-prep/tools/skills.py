"""Skill Coverage Matrix — every official AIP-C01 skill checked against what has been taught.

Status: Y = covered, P = partly covered, N = not covered yet. Update after every session.
"""
import os
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(__file__))
from notelib import S, Note  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes", "Skill_Coverage_Matrix.pdf")
LAST_UPDATED = "Monday 26 Oct 2026 (after the gap lesson; Day 6 not started)"
H1_SPLIT = ParagraphStyle("h1split", parent=S["h1"], keepWithNext=0)

DOMAINS = OrderedDict([
    ("1", ("Foundation Model Integration, Data Management, and Compliance", 31)),
    ("2", ("Implementation and Integration", 26)),
    ("3", ("AI Safety, Security, and Governance", 20)),
    ("4", ("Operational Efficiency and Optimization", 12)),
    ("5", ("Testing, Validation, and Troubleshooting", 11)),
])

# (skill, what it asks for, status, where taught, gap / plan)
SKILLS = [
    # ---- Task 1.1 Analyze requirements and design GenAI solutions
    ("1.1.1", "Architectures aligned to business needs (FMs, integration patterns, deployment)", "P",
     "D1 RAG vs fine-tuning; D2 agent vs workflow; D5 deployment options", "End-to-end design method → Day 7"),
    ("1.1.2", "Proofs of concept on Bedrock to validate feasibility, performance, value", "N", "—", "Day 7"),
    ("1.1.3", "Standard components; Well-Architected Framework + Generative AI Lens", "N", "—", "Day 7"),
    # ---- Task 1.2 Select and configure FMs
    ("1.2.1", "Assess and choose FMs (benchmarks, capabilities, limitations)", "Y",
     "D5 Part 1 (criteria, model evaluation)", "—"),
    ("1.2.2", "Switch models/providers without code changes (Lambda, API Gateway, AppConfig)", "Y", "D5 Converse API; routing lesson (AppConfig map); Gap lesson 26 Oct", "—"),
    ("1.2.3", "Resilience: Step Functions circuit breaker, CRIS, cross-Region, graceful degradation", "Y", "D5 cross-region inference, fallbacks; Gap lesson 26 Oct", "—"),
    ("1.2.4", "Customisation lifecycle: SageMaker deploy, LoRA/adapters, Model Registry, pipelines, rollback, retire", "Y", "D5 Part 3 (fine-tuning, CPT, distillation, Custom Model Import); Gap lesson 26 Oct", "—"),
    # ---- Task 1.3 Data validation and processing pipelines
    ("1.3.1", "Data validation (Glue Data Quality, Data Wrangler, Lambda, CloudWatch metrics)", "N", "—", "Day 8"),
    ("1.3.2", "Multimodal processing (Bedrock multimodal, SageMaker Processing, Transcribe)", "P",
     "D1 parsing (BDA, Textract); D5 multimodal models", "Day 8"),
    ("1.3.3", "Format inputs per model (Bedrock JSON, SageMaker payloads, conversation format)", "P",
     "D2 Converse messages; D5 InvokeModel vs Converse, batch JSONL", "Day 8"),
    ("1.3.4", "Improve input quality (Bedrock reformatting, Comprehend entities, Lambda normalisation)", "N", "—", "Day 8"),
    # ---- Task 1.4 Vector stores
    ("1.4.1", "Vector architectures (KB hierarchical, OpenSearch Neural plugin, RDS+S3, DynamoDB for metadata)", "Y", "D1 KB + vector stores; Gap lesson 26 Oct", "—"),
    ("1.4.2", "Metadata frameworks (S3 metadata timestamps, authorship attributes, domain tags)", "Y", "D1 metadata filtering; PS1 Q3; Gap lesson 26 Oct", "—"),
    ("1.4.3", "Performance at scale (OpenSearch sharding, multi-index, hierarchical indexing)", "Y", "Gap lesson 26 Oct", "—"),
    ("1.4.4", "Integration with document systems, wikis (connectors)", "Y", "D1 KB data source connectors", "—"),
    ("1.4.5", "Keep vector stores current (incremental, change detection, sync, scheduled refresh)", "Y",
     "D1 sync jobs; PS1 Q5", "—"),
    # ---- Task 1.5 Retrieval mechanisms
    ("1.5.1", "Document segmentation (Bedrock chunking, Lambda fixed-size, hierarchical)", "Y", "D1; PS1 Q16", "—"),
    ("1.5.2", "Embedding choice (Titan dimensions, domain fit, Lambda batch embeddings)", "Y", "D1 embeddings; PS1 Q20; Gap lesson 26 Oct", "—"),
    ("1.5.3", "Vector search (OpenSearch, Aurora pgvector, KB managed store)", "Y", "D1; PS1 Q2", "—"),
    ("1.5.4", "Advanced search (hybrid, rerankers)", "Y", "D1; PS1 Q1", "—"),
    ("1.5.5", "Query handling (expansion, decomposition, Step Functions transformation)", "Y", "D1 query decomposition; Gap lesson 26 Oct", "—"),
    ("1.5.6", "Consistent access (function calling for vector search, MCP clients, standard APIs)", "Y",
     "D2 tools; D3 MCP; PS1 Q17", "—"),
    # ---- Task 1.6 Prompt engineering and governance
    ("1.6.1", "Instruction frameworks (Prompt Management roles, Guardrails, templates)", "P",
     "D5 system prompts", "Day 7"),
    ("1.6.2", "Interactive systems (Step Functions clarification, Comprehend intent, DynamoDB history)", "N", "—", "Day 7"),
    ("1.6.3", "Prompt governance (parameterised templates, approvals, S3 repos, CloudTrail, Logs)", "N", "—", "Day 7"),
    ("1.6.4", "Prompt QA (Lambda output checks, Step Functions edge cases, CloudWatch regression)", "N", "—", "Day 7"),
    ("1.6.5", "Iterative refinement (structured inputs, output specs, chain-of-thought, feedback loops)", "N", "—", "Day 7"),
    ("1.6.6", "Complex prompt systems (Prompt Flows chains, branching, reusable components)", "N", "—", "Day 7"),
    # ---- Task 2.1 Agentic AI
    ("2.1.1", "Autonomous systems with memory/state (Strands, Agent Squad, MCP)", "Y", "D2, D3; PS1", "—"),
    ("2.1.2", "Structured reasoning (Step Functions ReAct, chain-of-thought)", "P", "D2 ReAct; D3 Step Functions",
     "Day 7 (chain-of-thought)"),
    ("2.1.3", "Safeguarded workflows (stopping conditions, Lambda timeouts, IAM boundaries, circuit breakers)", "Y", "D3 Step Functions; PS1 Q29; Gap lesson 26 Oct", "—"),
    ("2.1.4", "Model coordination (specialised FMs, ensembles, selection frameworks)", "Y", "D3 supervisor/router; routing lesson; Gap lesson 26 Oct", "—"),
    ("2.1.5", "Human collaboration (Step Functions approvals, API Gateway feedback)", "Y", "D3 waitForTaskToken; PS1 Q10, Q29; Gap lesson 26 Oct", "—"),
    ("2.1.6", "Reliable tools (Strands custom behaviours, function definitions, Lambda validation)", "Y", "D2 tool schemas, toolResult errors; PS1 Q21; Gap lesson 26 Oct", "—"),
    ("2.1.7", "MCP servers: Lambda (stateless, light) vs ECS (complex); client libraries", "Y", "D3 MCP; Gap lesson 26 Oct", "—"),
    # ---- Task 2.2 Deployment
    ("2.2.1", "Deploy per need (Lambda on-demand, Provisioned Throughput, SageMaker hybrid)", "Y", "D5 Part 3", "—"),
    ("2.2.2", "LLM-specific deployment (containers, GPU memory, model loading)", "Y", "Gap lesson 26 Oct", "—"),
    ("2.2.3", "Optimised deployment (smaller models, cascading)", "Y", "D5 distillation; routing lesson", "—"),
    # ---- Task 2.3 Enterprise integration
    ("2.3.1", "Enterprise connectivity (legacy APIs, event-driven, data sync)", "N", "—", "Day 8"),
    ("2.3.2", "Add GenAI to apps (API Gateway microservices, Lambda webhooks, EventBridge)", "N", "—", "Day 8"),
    ("2.3.3", "Secure access (identity federation, RBAC, least privilege)", "P", "D4 IAM/SCP; D3 Identity", "Day 8"),
    ("2.3.4", "Cross-environment compliance (Outposts, Wavelength, secure routing)", "N", "—", "Day 8"),
    ("2.3.5", "CI/CD + GenAI gateway (CodePipeline, CodeBuild, tests, rollback, central layer)", "N", "—", "Day 8"),
    # ---- Task 2.4 FM API integrations
    ("2.4.1", "Sync/async interaction (Bedrock APIs, SDKs + SQS, API Gateway validation)", "Y", "D5 Part 2", "—"),
    ("2.4.2", "Real-time (streaming APIs, WebSockets / server-sent events, chunked transfer)", "Y", "D5 streaming; Gap lesson 26 Oct", "—"),
    ("2.4.3", "Resilience (SDK backoff, API Gateway rate limiting, fallback, X-Ray)", "Y", "D5 backoff, fallback; Gap lesson 26 Oct", "—"),
    ("2.4.4", "Model routing (static, Step Functions content-based, metrics, API Gateway)", "Y",
     "Routing mini-lesson (26 Oct)", "—"),
    # ---- Task 2.5 App integration and dev tools
    ("2.5.1", "FM API interfaces (streaming via API Gateway, token limits, retries)", "P", "D5 Part 2", "Day 9"),
    ("2.5.2", "Accessible interfaces (Amplify UI, OpenAPI-first, Prompt Flows no-code)", "N", "—", "Day 9"),
    ("2.5.3", "Business enhancements (Lambda CRM, Step Functions doc processing, BDA)", "N", "—", "Day 9"),
    ("2.5.4", "Developer productivity (Amazon Q Developer)", "N", "—", "Day 9"),
    ("2.5.5", "Advanced apps (Strands, Agent Squad, Step Functions patterns, prompt chaining)", "P", "D3", "Day 9"),
    ("2.5.6", "Troubleshooting (Logs Insights, X-Ray, Q Developer)", "N", "—", "Day 9 / Day 11"),
    # ---- Task 3.1 Safety controls
    ("3.1.1", "Input safety (Guardrails, custom moderation with Step Functions/Lambda)", "N", "—", "Day 6"),
    ("3.1.2", "Output safety (Guardrails, toxicity evaluations, text-to-SQL determinism)", "N", "—", "Day 6"),
    ("3.1.3", "Reduce hallucinations (KB grounding, confidence scoring, JSON Schema outputs)", "P",
     "D1 grounding; D5 Part 1 Q&A", "Day 6"),
    ("3.1.4", "Defence in depth (Comprehend pre-filter, Guardrails, Lambda post-check, API filtering)", "N", "—", "Day 6"),
    ("3.1.5", "Threat detection (prompt injection, jailbreaks, sanitisation, adversarial testing)", "N", "—", "Day 6"),
    # ---- Task 3.2 Data security
    ("3.2.1", "Protected environments (VPC endpoints, IAM, Lake Formation, CloudWatch)", "Y", "D4", "—"),
    ("3.2.2", "Privacy (Comprehend, Macie, Bedrock privacy, Guardrails, S3 Lifecycle)", "Y", "D4", "—"),
    ("3.2.3", "Privacy with utility (masking, anonymisation, PII detection)", "Y", "D4", "—"),
    # ---- Task 3.3 Governance
    ("3.3.1", "Compliance (model cards, Glue lineage, source tagging, decision logs)", "N", "—", "Day 9"),
    ("3.3.2", "Data source tracking (Glue Data Catalog, attribution tags, CloudTrail)", "N", "D4 CloudTrail preview", "Day 9"),
    ("3.3.3", "Organisational governance frameworks", "N", "—", "Day 9"),
    ("3.3.4", "Continuous governance (misuse/drift/bias detection, alerting, redaction, logging)", "N", "—", "Day 9"),
    # ---- Task 3.4 Responsible AI
    ("3.4.1", "Transparency (reasoning displays, confidence metrics, source attribution, agent tracing)", "P",
     "D1 citations; D2 trace", "Day 6"),
    ("3.4.2", "Fairness (fairness metrics, Prompt Management A/B, LLM-as-a-judge)", "N", "—", "Day 6"),
    ("3.4.3", "Policy compliance (Guardrails, model cards, Lambda compliance checks)", "N", "—", "Day 6"),
    # ---- Task 4.1 Cost
    ("4.1.1", "Token efficiency (estimation, context pruning, response limits, compression)", "P",
     "D5 max tokens, RAG to shrink input", "Day 10"),
    ("4.1.2", "Cost-effective selection (tiered usage, price-performance)", "P", "D5; routing lesson", "Day 10"),
    ("4.1.3", "Utilisation and throughput (batching, capacity planning, PT optimisation)", "P", "D5 Part 3", "Day 10"),
    ("4.1.4", "Caching (semantic, fingerprinting, edge, request hashing, prompt caching)", "N", "—", "Day 10"),
    # ---- Task 4.2 Performance
    ("4.2.1", "Responsiveness (pre-computation, latency-optimised models, parallel, streaming)", "P",
     "D5 streaming; PS1 Q30", "Day 10"),
    ("4.2.2", "Retrieval performance (index optimisation, query preprocessing, hybrid scoring)", "P", "D1 hybrid", "Day 10"),
    ("4.2.3", "Throughput (token processing, batch inference, concurrency)", "P", "D5 batch", "Day 10"),
    ("4.2.4", "Model-specific tuning (parameters, A/B tests, temperature/top-k/top-p)", "Y", "D5 Part 1", "—"),
    ("4.2.5", "Resource allocation (capacity planning, utilisation monitoring, auto-scaling)", "N", "—", "Day 10"),
    ("4.2.6", "System performance (API profiling, vector query optimisation, latency reduction)", "N", "—", "Day 10"),
    # ---- Task 4.3 Monitoring
    ("4.3.1", "Holistic observability (operational, tracing, business dashboards)", "P", "D3 Observability", "Day 11"),
    ("4.3.2", "GenAI KPIs (token usage, hallucination rate, drift, invocation logs, cost anomalies)", "P",
     "D4 invocation logging", "Day 11"),
    ("4.3.3", "Actionable insights (dashboards, compliance monitoring, forensic audit)", "N", "—", "Day 11"),
    ("4.3.4", "Tool performance (call patterns, tool-calling observability, baselines)", "P", "D3 Observability", "Day 11"),
    ("4.3.5", "Vector store operations (monitoring, index optimisation, data quality)", "N", "—", "Day 11"),
    ("4.3.6", "GenAI failure modes (golden datasets, output diffing, reasoning path tracing)", "N", "—", "Day 11"),
    # ---- Task 5.1 Evaluation
    ("5.1.1", "Quality metrics (relevance, factual accuracy, consistency, fluency)", "P", "D1 RAG metrics", "Day 12"),
    ("5.1.2", "Systematic evaluation (Bedrock evaluations, A/B, canary, cost-performance)", "P",
     "D5 model evaluation", "Day 12"),
    ("5.1.3", "User-centred evaluation (feedback, ratings, annotation)", "N", "—", "Day 12"),
    ("5.1.4", "QA processes (continuous evaluation, regression tests, quality gates)", "N", "—", "Day 12"),
    ("5.1.5", "Multi-perspective assessment (RAG eval, LLM-as-a-judge, human feedback)", "P",
     "D1; D5; PS1 Q19", "Day 12"),
    ("5.1.6", "Retrieval quality testing (relevance scoring, context matching, latency)", "P", "D1 metrics", "Day 12"),
    ("5.1.7", "Agent performance (task completion, tool effectiveness, agent evaluations)", "N", "—", "Day 12"),
    ("5.1.8", "Reporting to stakeholders (visualisations, automated reports)", "N", "—", "Day 12"),
    ("5.1.9", "Deployment validation (synthetic workflows, hallucination/semantic drift checks)", "N", "—", "Day 12"),
    # ---- Task 5.2 Troubleshooting
    ("5.2.1", "Content handling (context overflow, dynamic chunking, truncation analysis)", "P",
     "D5 ValidationException, max_tokens", "Day 11"),
    ("5.2.2", "Integration issues (error logging, request validation, response analysis)", "P",
     "D5 error table; D4 KMS/IAM errors", "Day 11"),
    ("5.2.3", "Prompt problems (testing frameworks, version comparison, refinement)", "N", "—", "Day 7 / Day 11"),
    ("5.2.4", "Retrieval issues (relevance, embedding diagnostics, drift, chunking fixes)", "P",
     "D1; PS1 Q20 embedding mismatch", "Day 11"),
    ("5.2.5", "Prompt maintenance (template testing, Logs, X-Ray, schema validation)", "N", "—", "Day 7 / Day 11"),
]

MARK = {"Y": "✓ Covered", "P": "½ Partly", "N": "✗ Not yet"}
SCORE = {"Y": 1.0, "P": 0.5, "N": 0.0}

# ---------------------------------------------------------------- summary numbers
per_domain = OrderedDict((d, {"Y": 0, "P": 0, "N": 0}) for d in DOMAINS)
for sid, *_rest in SKILLS:
    per_domain[sid.split(".")[0]][_rest[1]] += 1
weighted = 0.0
domain_rows = []
for d, (name, weight) in DOMAINS.items():
    c = per_domain[d]
    total = sum(c.values())
    cov = (c["Y"] + 0.5 * c["P"]) / total
    weighted += weight * cov
    domain_rows.append([f"{d}. {name}", f"{weight}%", str(total), str(c["Y"]), str(c["P"]), str(c["N"]),
                        f"{round(100 * cov)}%"])
totals = {k: sum(per_domain[d][k] for d in DOMAINS) for k in "YPN"}

n = Note(OUT, "Skill Coverage Matrix — AWS AIP-C01",
         f"Last updated: <b>{LAST_UPDATED}</b> &nbsp;·&nbsp; Source: official exam guide — 5 domains, 20 tasks, "
         f"{len(SKILLS)} skills", wide=True)
n.callout("Summary",
          f"<b>{totals['Y']} skills covered, {totals['P']} partly covered, {totals['N']} not yet covered</b> "
          f"(of {len(SKILLS)}). Weighted skill coverage (covered = 1, partly = ½, by domain weight): "
          f"<b>{round(weighted)}%</b> — a little below the earlier task-level estimate (~42%), because studied tasks still "
          "contain uncovered skills. This skill-level figure is the one to trust. Gaps inside already-studied tasks are "
          "closed in the gap lesson; the rest are assigned to Days 6–12.", "ok")

n.h1("1. Coverage by domain")
n.table(["Domain", "Weight", "Skills", "Covered", "Partly", "Not yet", "Coverage"], domain_rows,
        [0.46, 0.08, 0.08, 0.09, 0.09, 0.09, 0.11])

n.story.append(Paragraph("2. Every skill", H1_SPLIT))
rows = [[sid, what, MARK[st], where, gap] for sid, what, st, where, gap in SKILLS]
n.table(["Skill", "What it asks for", "Status", "Where taught", "Gap / plan"], rows,
        [0.06, 0.4, 0.09, 0.24, 0.21])
n.build()
print(os.path.abspath(OUT), totals, round(weighted, 1))
