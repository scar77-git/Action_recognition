"""Days 7–8 (self-study PDF): Cost and performance (4.1, 4.2) and Governance (3.3)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import S, Note  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Day_7-8_2026-10-30_Cost_Performance_Governance.pdf")

n = Note(OUT, "Days 7–8 — Cost, Performance and Governance",
         "Self-study edition, 30 Oct 2026 &nbsp;·&nbsp; Skills <b>4.1.1–4.1.4</b>, <b>4.2.1–4.2.6</b>, "
         "<b>3.3.1–3.3.4</b> &nbsp;·&nbsp; Exam: Mon 9 Nov, 1:30 PM IST")
n.callout("How to use this PDF offline",
          "Read one part at a time. After each part, answer its check questions on paper. At the end, take the 12-question "
          "quiz (25 minutes, no notes) and send your answers when you're back online — the answers and explanations will "
          "be added then. Skim the glossary first if any term is unfamiliar.", "ok")

# ======================================================== PART 1
n.h1("Part 1 — Cutting costs (Task 4.1)")
n.p("On-demand Bedrock bills per input token and per output token, so cost depends on how many tokens you send, how "
    "many you get back, and how many calls you make.")
n.code(" cost = (input tokens x input price) + (output tokens x output price)   per call\n"
       "      x number of calls\n"
       " Levers: (1) fewer/cheaper tokens  (2) cheaper model per call  (3) fewer calls (caching)\n"
       "         (4) cheaper capacity (batch / Provisioned Throughput)")
n.h2("1.1 Token efficiency (4.1.1)")
n.bullets([
    "<b>Measure first</b>: every Converse response includes usage (inputTokens, outputTokens). Log it per request and "
    "per feature as CloudWatch metrics to see which feature costs what. Estimate big prompts beforehand with token "
    "counting (supported models).",
    "<b>Context window optimisation</b>: send only the top relevant chunks, not whole documents; drop instructions that "
    "don't apply.",
    "<b>Context pruning</b> for long chats — you pay for the whole history on every call: sliding window (last N turns), "
    "summarise older turns, drop stale tool outputs.",
    "<b>Prompt compression</b>: same meaning, fewer tokens — remove repetition, fewer/shorter few-shot examples.",
    "<b>Response size controls</b>: output tokens cost more — sensible max tokens per feature, concise formats "
    "('max 3 bullets'), JSON with only the needed fields.",
])
n.code(" Turn 30 WITHOUT pruning: [system] + [29 old turns ~12,000 tokens] + [new question]   <- paid every call\n"
       " Turn 30 WITH pruning:    [system] + [summary of turns 1-25 ~300 tokens] + [last 4 turns] + [question]")
n.p("<b>Example</b>: a support bot at 9,000 input tokens per turn drops to 2,500 with top-5 chunks + a history summary, "
    "and to 1,800 with a compressed system prompt — about 80% less input cost.")
n.h2("1.2 Cost-effective model selection (4.1.2)")
n.p("Compare <b>cost per successful task</b>, not price per token — a cheap model that often fails and triggers retries "
    "or escalation can cost more.")
n.code(" Model A: $0.002/request, 95% success                         -> ~$0.0021 per success\n"
       " Model B: $0.0008/request, 60% success (+ escalate failures to A) -> 0.0008 + 0.4 x 0.002 = $0.0016")
n.bullets(["Tiered usage by complexity: routing and cascading (gap lesson).",
           "Balance cost against quality with evaluation: cheapest model that meets the quality bar.",
           "Efficient patterns: batch inference (~50% cheaper) for non-urgent work; caching."])
n.h2("1.3 Throughput and capacity (4.1.3)")
n.bullets([
    "<b>Batching</b>: batch inference jobs; or group many small items in one prompt (classify 20 short reviews in one "
    "call returning a JSON list) so instructions are paid for once.",
    "<b>Capacity planning</b>: needed TPM ≈ peak requests per minute × average tokens per request "
    "(e.g. 300 × 2,000 = 600,000 TPM) — compare with quotas or plan Provisioned Throughput.",
    "<b>Utilisation monitoring</b>: Bedrock CloudWatch metrics — Invocations, InputTokenCount, OutputTokenCount, "
    "InvocationLatency, InvocationThrottles.",
    "<b>Auto-scaling</b> for self-hosted models on SageMaker AI: scale on load; keep a warm minimum (slow model loading).",
    "<b>Provisioned Throughput optimisation</b>: buy for the steady baseline only, send bursts to on-demand or "
    "cross-Region inference; commit only when usage is stable; monitor utilisation.",
])
n.h2("1.4 Caching — the cheapest call is the one you don't make (4.1.4)")
n.code(" request -> (1) edge cache (CloudFront)      identical public response?      -> return instantly\n"
       "         -> (2) exact-match cache (hash)     same normalised prompt + params? -> stored answer\n"
       "         -> (3) semantic cache (embeddings)  SIMILAR question answered?       -> stored answer\n"
       "         -> (4) model call + PROMPT CACHING  reuse processed static prefix    -> cheaper, faster")
n.bullets([
    "<b>Prompt caching</b> (Bedrock): mark a cache checkpoint after a long static prefix (system prompt, document, tool "
    "definitions); later calls reuse it — cached input tokens are discounted and responses start faster. The cache lasts "
    "minutes and refreshes on use. Put static content first, the user's question last — earlier changes break the cache. "
    "Example: the same 30-page contract sent with every question.",
    "<b>Exact-match cache</b> (deterministic request hashing / result fingerprinting): normalise the request, hash it, "
    "look it up in ElastiCache or DynamoDB; best with temperature 0.",
    "<b>Semantic cache</b>: embed the question, search previously answered questions (ElastiCache vector search or "
    "OpenSearch); above a similarity threshold, return the cached answer. Too low a threshold returns wrong answers to "
    "merely similar-looking questions.",
    "<b>Edge caching</b> with CloudFront for public, identical, non-personal responses.",
    "<b>Cautions</b>: never serve one user's personalised or PII answer to another (user/tenant in the key, or don't "
    "cache); set a TTL; invalidate on data changes (e.g. after a KB sync).",
])
n.h2("Part 1 check questions (answer on paper)")
n.numbered(["Why can a cheaper model end up costing more overall?",
            "A legal assistant sends the same 50-page contract with every question. Which feature cuts cost, and where "
            "should the user's question go in the prompt?",
            "What is the risk of a semantic cache with a low similarity threshold?"])

# ======================================================== PART 2
n.h1("Part 2 — Making it fast (Task 4.2)")
n.p("Where the time goes in one LLM call: a short wait before the first token (TTFT, grows with input size), then "
    "generation, which takes time <b>per output token</b>. That's why output length is the biggest latency lever.")
n.code(" |--- network ---|--- read prompt (TTFT) ---|--- generate token, token, token ... ---|\n"
       "                   more input = longer        more OUTPUT tokens = proportionally longer")
n.h2("2.1 Responsive systems (4.2.1)")
n.bullets([
    "<b>Pre-computation for predictable queries</b>: generate answers ahead of time (nightly) for the top questions, "
    "daily summaries or product descriptions, store them, serve instantly.",
    "<b>Latency-optimised models</b>: Bedrock offers a latency-optimised inference option for some models in some Regions "
    "(a performance setting on the call) for time-sensitive apps; otherwise choose smaller, faster models.",
    "<b>Parallel requests</b>: run independent sub-tasks concurrently (Step Functions Parallel or Map states, async SDK "
    "calls) — total time ≈ the slowest call, not the sum.",
    "<b>Response streaming</b>: improves perceived latency (time to first token).",
    "<b>Performance benchmarking</b>: measure TTFT, tokens per second, p50/p95/p99 latency under realistic load before "
    "choosing a model or configuration.",
])
n.code(" Sequential: [summary 4s] -> [risks 4s] -> [actions 4s] = 12 s\n"
       " Parallel:   [summary 4s]\n"
       "             [risks   4s]  -> merge -> ~4-5 s\n"
       "             [actions 4s]")
n.h2("2.2 Retrieval performance (4.2.2)")
n.bullets([
    "<b>Index optimisation</b>: ANN settings (HNSW, ef_search), shards and replicas, vector quantisation, per-domain "
    "indexes (gap lesson).",
    "<b>Query preprocessing</b>: rewrite/expand, apply metadata filters first so the vector search covers less data.",
    "<b>Hybrid search with custom scoring</b>: weight keyword vs vector results and boost by fields such as recency or "
    "document type (e.g. newer policies rank higher).",
])
n.h2("2.3 Throughput (4.2.3)")
n.bullets([
    "<b>Token processing optimisation</b>: shorter prompts and outputs fit more requests within the same TPM quota.",
    "<b>Batch inference</b> for bulk work.",
    "<b>Concurrent invocation management</b>: cap concurrency so you stay within quotas — SQS-driven workers, Lambda "
    "reserved concurrency as a ceiling, token-bucket style rate limiting, retries with jitter to avoid synchronized "
    "retry storms.",
])
n.h2("2.4 Model-specific tuning (4.2.4) — recap")
n.p("Parameters per use case (Day 5): low temperature for extraction/classification, higher for creative work; top-p / "
    "top-k to narrow choices; max tokens per feature. Use A/B tests to prove a change improves quality or latency.")
n.h2("2.5 Resource allocation (4.2.5)")
n.bullets([
    "<b>Capacity planning for token processing</b>: profile each feature's input vs output tokens (summarisation is "
    "input-heavy; drafting is output-heavy) and plan quotas or model units from that.",
    "<b>Utilisation monitoring of prompt and completion patterns</b>: watch InputTokenCount vs OutputTokenCount trends "
    "to spot prompt bloat or runaway answer length.",
    "<b>Auto-scaling tuned for GenAI traffic</b> (self-hosted): scale on concurrency or invocations, not CPU; scheduled "
    "scaling before known peaks; warm minimum because large models load slowly.",
])
n.h2("2.6 System performance (4.2.6)")
n.bullets([
    "<b>API call profiling</b>: break each call into TTFT vs generation time and trace across services with X-Ray to "
    "find the slow hop.",
    "<b>Vector query optimisation</b>: filter first, keep k (number of results) small, avoid returning huge payloads.",
    "<b>LLM latency reduction</b>: shorter outputs (biggest lever), smaller or distilled models, prompt caching (faster "
    "start for long static prefixes), streaming, latency-optimised inference, same-Region calls.",
    "<b>Efficient service communication</b>: avoid long chains of synchronous hops; use async/event-driven steps; reuse "
    "SDK clients and connections instead of creating them per request.",
])
n.h2("Part 2 check questions")
n.numbered(["Why does capping output length usually reduce latency more than shortening the input?",
            "A report needs a summary, a risk list and an action list, each from a separate model call. How do you cut "
            "total time?",
            "Your Lambda functions call Bedrock and burst to thousands of concurrent calls, causing throttling. Name two "
            "ways to manage concurrency."])

# ======================================================== PART 3
n.h1("Part 3 — Governance and compliance (Task 3.3)")
n.p("Governance answers four questions an auditor or regulator will ask: <b>What does this model do and not do?</b> "
    "<b>Where did its data come from?</b> <b>Who approved it and who is accountable?</b> <b>How do we know it is still "
    "behaving?</b>")
n.h2("3.1 Compliance frameworks (3.3.1)")
n.bullets([
    "<b>Programmatic model cards</b> with SageMaker AI: create and update model cards through the API/SDK inside your "
    "pipeline, so intended use, training data, evaluation results and limitations are recorded automatically for every "
    "version (not hand-written once and forgotten).",
    "<b>Automatic data lineage with AWS Glue</b>: Glue jobs and the Glue Data Catalog record which sources fed which "
    "datasets (and SageMaker lineage tracking links data, training jobs and models) — answers 'where did this come from?'",
    "<b>Metadata tagging for source attribution</b>: tag documents and chunks with source system, owner, date, "
    "classification — so every answer can be traced to its sources.",
    "<b>Decision logs in CloudWatch Logs</b>: for each important answer log the request, retrieved sources, model and "
    "guardrail versions, output and resulting decision — a complete record for audits.",
])
n.h2("3.2 Data source tracking (3.3.2)")
n.bullets([
    "<b>Register sources in the Glue Data Catalog</b> (one inventory of datasets, schemas, owners).",
    "<b>Attribution in generated content</b>: citations and source IDs from metadata attached to answers.",
    "<b>CloudTrail</b> for audit logging of who accessed or changed data, models and guardrails.",
])
n.code(" Source systems -> Glue Data Catalog (registered, owner, schema) -> pipeline (lineage recorded)\n"
       "   -> KB chunks tagged {source, owner, date} -> answer with citations -> decision log (CloudWatch Logs)\n"
       "   -> every API action recorded by CloudTrail")
n.h2("3.3 Organisational governance (3.3.3)")
n.p("A governance framework aligns AI work with company policy, regulation and responsible-AI principles:")
n.bullets([
    "Roles and accountability: an AI governance board or review group; named owners per model and use case.",
    "Risk assessment per use case before build and before launch (impact, data sensitivity, failure modes).",
    "Approval workflow for models and prompts (e.g. Model Registry approval status; prompt version approval).",
    "Standards enforced technically: approved-model list via SCPs/IAM, mandatory guardrails, logging and encryption "
    "baselines checked by AWS Config rules.",
    "Evidence for audits: AWS Audit Manager can collect evidence continuously against frameworks (including a generative "
    "AI best-practices framework).",
    "Documentation and review cadence: model cards, periodic re-evaluation.",
])
n.h2("3.4 Continuous monitoring and advanced controls (3.3.4)")
n.bullets([
    "<b>Automated misuse detection</b>: alarms on guardrail intervention rates, unusual usage per user or API key.",
    "<b>Drift detection</b>: track quality and grounding scores, response length and topics over time; for self-hosted "
    "models SageMaker Model Monitor detects data and model quality drift.",
    "<b>Bias drift monitoring</b>: fairness metrics tracked over time (SageMaker Clarify with Model Monitor for bias "
    "drift on hosted models).",
    "<b>Automated alerting and remediation</b>: CloudWatch alarm → EventBridge → Lambda or Systems Manager automation "
    "(roll back a model version, disable a feature flag, open a ticket).",
    "<b>Token-level redaction</b>: mask PII in prompts, responses and logs (Guardrails masking, Comprehend) so logs "
    "remain usable without exposing data.",
    "<b>Response logging</b>: model invocation logging, encrypted with KMS, retention via lifecycle rules.",
    "<b>AI output policy filters</b>: guardrails enforcing output policies.",
])
n.code(" metric/alarm (drift, misuse, bias gap) -> EventBridge rule -> Lambda / SSM Automation\n"
       "      -> roll back model version | flip AppConfig flag off | notify + open ticket")
n.h2("Part 3 check questions")
n.numbered(["An auditor asks which source documents and which model version produced a specific answer last March. "
            "What must you have been logging?",
            "Why create model cards programmatically in the pipeline instead of writing them by hand?",
            "Grounding scores fall steadily over two weeks after a data change. Describe an automated detect-and-respond "
            "chain."])

# ======================================================== rules
n.h1("Decision rules — Days 7–8")
n.numbered([
    "Find costly features → log token usage per feature; long chats → context pruning; big inputs → relevant chunks + "
    "compression; output cost → max tokens + concise formats.",
    "Compare models by cost per successful task; tiered usage via routing/cascading.",
    "Many tiny calls → group items per prompt or batch inference; plan TPM = peak requests × tokens.",
    "Provisioned Throughput for the steady baseline only; monitor utilisation.",
    "Same long prefix each call → prompt caching (static first). Identical requests → exact-match cache. Similar "
    "questions → semantic cache with a careful threshold. Public identical pages → CloudFront. Never cache personal "
    "answers across users; TTL + invalidation.",
    "Predictable queries → pre-compute. Time-critical → latency-optimised or smaller model + streaming. Independent "
    "sub-tasks → parallel calls.",
    "Slow retrieval → filter first, tune ANN/index, hybrid scoring with boosts.",
    "Throttling under bursts → cap concurrency (SQS workers, reserved concurrency), backoff with jitter.",
    "Latency → shorten outputs first; profile TTFT vs generation; X-Ray across hops; reuse clients.",
    "Model documentation → programmatic SageMaker model cards; lineage → Glue / Data Catalog; attribution → metadata "
    "tags + citations; audit → CloudTrail + decision logs in CloudWatch Logs.",
    "Organisational governance → roles, risk assessment, approvals, enforced standards (SCP, Config), Audit Manager evidence.",
    "Continuous governance → drift, bias-drift and misuse alarms → EventBridge → automated remediation; redact PII in logs.",
])

# ======================================================== quiz
n.page_break()
n.h1("Quiz — 12 questions (25 minutes, answers added when you send yours)")
QUIZ = [
    ("A support assistant's monthly cost doubled. Conversations are long, and every call resends the full history. "
     "Users say answer quality is fine. What should the team do first?",
     ["Switch to a larger model so that fewer follow-up questions are needed",
      "Purchase Provisioned Throughput sized to the current token volume",
      "Raise the maximum output tokens so that each answer covers more follow-up questions",
      "Keep the recent turns verbatim and replace older turns with a short running summary"]),
    ("A legal team asks many questions about the same 60-page contract within a session. Each call includes the full "
     "contract followed by the question. What reduces cost and latency with the least change?",
     ["Move the question before the contract so that the model reads it first",
      "Store the contract in a knowledge base and retrieve the whole contract on every call",
      "Place the contract first with a cache checkpoint after it, and put the question last",
      "Summarise the contract once and send only the summary with each question"]),
    ("An internal help desk receives thousands of reworded versions of the same twenty questions each day. Answers "
     "aren't personalised and change only when policies are updated. What avoids most model calls safely? (Select TWO.)",
     ["Hash each question's exact text and return a stored answer only on identical text",
      "Embed each question and return a stored answer when a previous question is sufficiently similar",
      "Lower the similarity threshold as far as possible so that more questions match",
      "Clear the stored answers whenever the policy knowledge base is re-synced",
      "Cache answers at the edge with CloudFront using each user's session cookie as the key"]),
    ("Model A costs $0.004 per request with 96% task success. Model B costs $0.0015 with 70% success; failures are "
     "re-run on Model A. Which statement is correct?",
     ["Model A is cheaper per successful task because it rarely fails",
      "Model B with escalation costs about $0.0027 per request, which is cheaper than Model A",
      "Both cost the same because failures cancel out the price difference",
      "Model B is always cheaper because its price per request is lower"]),
    ("A dashboard shows the same morning market summary to 50,000 employees. It currently calls the model for every page "
     "view. What should the team do?",
     ["Generate the summary once each morning, store it, and serve the stored copy",
      "Use streaming so that each employee sees the summary appear faster",
      "Switch to a latency-optimised model for every page view",
      "Add a semantic cache keyed on each employee's ID"]),
    ("A report needs three independent model outputs (summary, risks, actions), each taking about 5 seconds. Users wait "
     "15 seconds. What should the team do?",
     ["Combine all three instructions into one longer prompt with a larger output limit",
      "Switch the three calls to batch inference",
      "Increase the Lambda memory of the function that makes the calls",
      "Run the three calls concurrently, for example with a Step Functions Parallel state, then merge the results"]),
    ("Thousands of Lambda invocations call Bedrock at once during a nightly job, causing throttling and failed records. "
     "The job has several hours to finish. Which approach fits best?",
     ["Increase Lambda reserved concurrency to the maximum so that the job finishes sooner",
      "Retry every failure immediately without delay until it succeeds",
      "Feed records through an SQS queue processed by a capped number of workers, with backoff and jitter on throttles",
      "Purchase Provisioned Throughput for the full peak of the nightly burst"]),
    ("A chat app's p95 latency is high. Traces show the time is mostly spent generating long answers, while users read "
     "only the first few paragraphs. What is the most effective fix?",
     ["Cap answer length with a lower max tokens and an instruction for concise answers",
      "Add replicas to the vector index",
      "Increase the number of retrieved chunks",
      "Move the application to a Region farther from users but with more capacity"]),
    ("Auditors require, for any answer from the last year, the sources used, the model and guardrail versions, and the "
     "decision taken. What should the team implement?",
     ["CloudTrail management events for the Bedrock account",
      "A model card updated quarterly",
      "Monthly LLM-as-a-judge evaluations",
      "Structured decision logs in CloudWatch Logs per answer, with source IDs from document metadata"]),
    ("A company retrains a model weekly and wants its documentation (intended use, data, evaluation results, limitations) "
     "always current for every version without manual effort. What should it do?",
     ["Write a model card by hand at the first release and link it from every later version",
      "Create SageMaker model cards through the API as a step in the training pipeline",
      "Store the training notebooks in S3 as the documentation",
      "Enable CloudTrail data events on the training bucket"]),
    ("A company must prove where every dataset used by its GenAI pipelines came from and how it was transformed. What "
     "should it use?",
     ["Amazon Macie discovery jobs on the source buckets",
      "S3 Lifecycle rules on the raw data bucket",
      "AWS Glue Data Catalog registration with lineage tracked by its Glue jobs",
      "Bedrock model invocation logging"]),
    ("After a data change, grounding scores drop steadily, and the company wants this detected and contained without "
     "waiting for humans. Which combination should it use? (Select THREE.)",
     ["Publish grounding scores as CloudWatch metrics with an alarm on a sustained drop",
      "A quarterly manual review of a sample of answers",
      "An EventBridge rule that reacts to the alarm",
      "Raising the guardrail grounding threshold to its maximum permanently",
      "A Lambda or Systems Manager automation that rolls back to the previous data or model version or disables the feature flag",
      "Model invocation logging alone"]),
]
for i, (stem, opts) in enumerate(QUIZ, 1):
    n.h2(f"Question {i}")
    n.p(stem)
    for j, o in enumerate(opts):
        n.story.append(Paragraph(f"<b>{'ABCDEF'[j]}.</b> {o}", S["bullet"]))
    n.space(4)

n.h1("Glossary — new terms")
n.table(["Term", "Meaning"], [
    ["Token usage / token counting", "Input/output token counts returned per call; estimating tokens before sending."],
    ["Context pruning / sliding window", "Dropping or summarising old conversation turns to cut tokens."],
    ["Prompt compression", "Same instructions in fewer tokens."],
    ["Cost per successful task", "Total cost including failures, retries and escalations divided by successes."],
    ["Capacity planning", "Estimating needed tokens/requests per minute from peak traffic."],
    ["Bedrock CloudWatch metrics", "Invocations, InputTokenCount, OutputTokenCount, InvocationLatency, InvocationThrottles."],
    ["Prompt caching / cache checkpoint", "Reusing a processed static prompt prefix; the marker after the cached part."],
    ["Exact-match cache / request hashing / fingerprint", "Cache keyed by a hash of the normalised request."],
    ["Semantic cache", "Cache matched by embedding similarity of questions."],
    ["TTL / cache invalidation", "Time-to-live for cached items / removing them when data changes."],
    ["Pre-computation", "Generating answers ahead of time for predictable requests."],
    ["Latency-optimised inference", "Bedrock option for faster responses on supported models/Regions."],
    ["TTFT / tokens per second", "Time to first token / generation speed."],
    ["p50 / p95 / p99", "Latency percentiles (median, 95th, 99th)."],
    ["Parallel / Map state", "Step Functions states running branches or items concurrently."],
    ["Concurrency control / reserved concurrency", "Capping simultaneous calls; Lambda's per-function concurrency setting."],
    ["Custom scoring / boosting", "Adjusting search ranking by weights or fields such as recency."],
    ["Programmatic model card", "Model card created/updated by code in a pipeline."],
    ["Data lineage", "Record of where data came from and how it was transformed."],
    ["AWS Glue Data Catalog", "Central inventory of datasets and schemas."],
    ["Decision log", "Per-answer record of inputs, sources, versions, output and decision."],
    ["AWS Config / AWS Audit Manager", "Configuration compliance rules / continuous audit evidence collection."],
    ["SageMaker Model Monitor", "Detects data, quality and bias drift for hosted models."],
    ["Drift / bias drift", "Gradual change in data or behaviour / in fairness metrics over time."],
    ["Automated remediation", "Alarm → EventBridge → Lambda/SSM action without human delay."],
    ["Token-level redaction", "Masking individual sensitive tokens (PII) in text and logs."],
], [0.38, 0.62])
n.build()
print(os.path.abspath(OUT))
