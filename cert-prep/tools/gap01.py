"""Gap lesson note: skills missed inside already-studied tasks (1.2, 1.4, 1.5, 2.1, 2.2, 2.4) + routing (2.4.4)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import Note  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Gap_Lesson_2026-10-26_Resilience_Scale_Safeguards.pdf")

n = Note(OUT, "Gap Lesson — Resilience, Scale and Safeguards",
         "Monday 26 Oct 2026 &nbsp;·&nbsp; Closes skills missed inside studied tasks: <b>1.2.2–1.2.4, 1.4.1–1.4.3, "
         "1.5.2, 1.5.5, 2.1.3–2.1.7, 2.2.2, 2.4.2–2.4.4</b> &nbsp;·&nbsp; Exam: Mon 9 Nov, 1:30 PM IST")

n.callout("Why this lesson exists",
          "On 26 Oct we checked all 98 official skills against what had been taught. Several skills inside 'finished' "
          "tasks were missing. This lesson closes them: model routing, switching models without code changes, "
          "resilience (circuit breakers, graceful degradation), the custom-model lifecycle, LLM hosting, vector search "
          "at scale, query handling, agent safeguards, MCP hosting, streaming to browsers, API rate limiting and "
          "tracing.", "ok")

# =============================================================== routing
n.h1("Routing mini-lesson — Skill 2.4.4: intelligent model routing")
n.p("Real applications receive mixed requests: some easy, some hard. Sending everything to a large model wastes "
    "money; sending everything to a small one gives poor answers on hard requests. <b>Model routing</b> chooses the "
    "model per request — the cheapest one that can handle it well.")
n.code("                         +--> small, cheap model     (easy / short requests)\n"
       " request --> ROUTER -----+--> code-specialised model (programming questions)\n"
       "                         +--> large, capable model   (complex reasoning)")
n.h2("① Static routing in application code")
n.p("Fixed rules decide the model from something known in advance (feature, endpoint, customer tier), usually a "
    "configuration map. Better practice: keep the map in <b>AWS AppConfig</b> or <b>Systems Manager Parameter Store</b> "
    "so a feature can move to another model without redeploying. Example: premium customers → large model, free tier "
    "→ small model. Simple and predictable, but blind to request content.")
n.code('MODEL_FOR_FEATURE = {"faq_answer": "amazon.nova-micro-v1:0", "email_summary": "amazon.nova-lite-v1:0",\n'
       '                     "contract_review": "<large model ID>"}\n'
       "model_id = MODEL_FOR_FEATURE[feature]   # with Converse, only modelId changes")
n.h2("② Content-based routing with AWS Step Functions")
n.code(" request -> [Classify: small model or Comprehend -> 'code' | 'legal' | 'general']\n"
       "           -> [Choice state]\n"
       "                'code'    -> Bedrock InvokeModel: code-specialised model\n"
       "                'legal'   -> Bedrock InvokeModel: large reasoning model (+ legal KB)\n"
       "                'general' -> Bedrock InvokeModel: small general model\n"
       "           -> [Return / store answer]  (built-in retries, execution history = audit trail)")
n.p("Exam cue: 'route by request content to specialised FMs, auditable' → Step Functions classify + Choice.")
n.h2("③ Routing based on metrics")
n.bullets([
    "<b>Amazon Bedrock Intelligent Prompt Routing</b> (managed): call a <b>prompt router</b> instead of a model; per prompt "
    "it predicts which model in a family gives good-enough quality and sends it to the cheaper one when quality is "
    "about equal. Exam cue: 'automatically pick the most cost-effective model in a family per prompt, least effort'.",
    "<b>Your own metrics-based router</b> using CloudWatch latency/error/throttle/cost metrics: <b>fallback</b> on "
    "throttling or latency spikes; <b>weighted A/B</b> (90% current, 10% candidate); <b>cascading</b> (small model "
    "first, escalate to large if the answer fails a quality check).",
])
n.h2("④ API Gateway with request transformations")
n.p("Route at the API layer: <b>path-based routes</b> (/v1/summarise vs /v1/analyse), and <b>mapping templates</b> that "
    "rewrite the request (insert the model ID, reshape the body) based on path, a header such as x-tier: premium, or a "
    "<b>stage variable</b>. Clients never need to know which model is used.")
n.table(["Scenario", "Choose"], [
    ["Fixed model per feature or tier; simplest", "Static routing (config map / AppConfig)"],
    ["Route by request content, auditable", "Step Functions: classify → Choice → model"],
    ["Cheaper model in a family per prompt, least effort", "Bedrock Intelligent Prompt Routing"],
    ["Switch on latency/errors/throttling; A/B; escalate on low quality", "Metrics-based routing (fallback, weighted, cascade)"],
    ["Routing by path/header/stage, invisible to clients", "API Gateway with request transformations"],
], [0.6, 0.4])

# =============================================================== part A
n.h1("Part A — Resilience and the model lifecycle")
n.h2("A1. Switching models without code changes (Skill 1.2.2)")
n.p("Even a one-line code change means edit, test and redeploy. During an incident you need minutes. Keep the model "
    "choice in configuration: <b>AWS AppConfig</b> stores settings and <b>feature flags</b> your app reads at runtime "
    "(the AppConfig Lambda extension caches them). Changes can be <b>validated</b>, rolled out <b>gradually</b> "
    "(e.g. 10% first) and <b>rolled back automatically</b> when a CloudWatch alarm fires. API Gateway stage variables "
    "can switch at the API layer.")
n.code("        +------------- AWS AppConfig -------------+\n"
       '        | "summariser_model": "amazon.nova-lite-v1:0" |  <- ops team edits this\n'
       '        | "fallback_model":   "amazon.nova-micro-v1:0"|\n'
       "        +----------------------+------------------+\n"
       "                               | read (cached) at runtime\n"
       " User -> API Gateway -> Lambda +--> Bedrock Converse(modelId = value from AppConfig)")
n.h2("A2. Resilient AI systems (Skill 1.2.3)")
n.p("<b>① Circuit breaker</b> — stop calling a failing service for a while and use an alternative; it <b>fails fast</b> "
    "instead of making every user wait for timeouts, and avoids piling load on the failing service.")
n.code("            failures exceed threshold (e.g. 5 in 1 minute)\n"
       "   [CLOSED: normal] ------------------------------------> [OPEN: skip model, use fallback]\n"
       "         ^  test call succeeds                                   | after cool-down (e.g. 60 s)\n"
       "         +------------------ [HALF-OPEN: try ONE request] <------+\n"
       "                              test fails -> back to OPEN")
n.p("On AWS: <b>Step Functions</b> checks circuit state stored in <b>DynamoDB</b>; OPEN → fallback branch; CLOSED → call "
    "the model and record failures.")
n.bullets([
    "<b>② Cross-region inference</b> also covers <b>models not available in your Region</b>: the profile routes to a "
    "Region where the model exists.",
    "<b>③ Cross-Region deployment</b> of the whole app (Lambda, API Gateway, KB in two Regions) with <b>Route 53 failover</b>.",
    "<b>④ Graceful degradation</b>: reduced but useful service instead of errors — smaller fallback model, cached "
    "answers, a clear 'AI answers delayed' message, answering without RAG plus a warning, skipping a failing tool.",
])
n.h2("A3. Custom model lifecycle (Skill 1.2.4)")
n.p("<b>LoRA (Low-Rank Adaptation)</b> is a <b>parameter-efficient fine-tuning (PEFT)</b> technique: freeze the base model "
    "and train small <b>adapters</b>. Training is cheaper and faster, adapters are megabytes, and one base model on one "
    "SageMaker endpoint can serve many adapters.")
n.code(" FULL FINE-TUNING: [7B model - ALL weights changed] -> new ~14 GB copy per use case\n"
       " LoRA:             [7B base model - FROZEN, shared] + [adapter A 20 MB] (legal)\n"
       "                                                    + [adapter B 20 MB] (medical)\n"
       "                                                    + [adapter C 20 MB] (support)")
n.p("<b>SageMaker Model Registry</b> stores every model version with an approval status (Pending / Approved / Rejected). "
    "An automated pipeline (<b>SageMaker Pipelines</b> or <b>AWS CodePipeline</b>, triggered via EventBridge) deploys only "
    "Approved versions; rollback = redeploy the previous approved version.")
n.code(" Train v3 -> register (PendingManualApproval) -> reviewer/tests approve -> Approved\n"
       "          -> EventBridge event -> deployment pipeline deploys v3")
n.bullets([
    "<b>Deployment guardrails</b> on SageMaker endpoints: <b>blue/green</b> (old and new side by side), <b>canary</b> "
    "(small slice first), <b>linear</b> (equal steps), <b>auto-rollback</b> when a CloudWatch alarm fires.",
    "<b>Retiring models</b>: Bedrock models move <b>Active → Legacy → End-of-Life</b>; after EOL calls fail. Track dates, "
    "evaluate the replacement early, switch via configuration, canary, keep rollback until proven.",
])
n.h2("A4. What makes deploying LLMs different (Skill 2.2.2)")
n.p("<b>GPU memory ≈ parameters × bytes per parameter</b>, plus the <b>KV cache</b> (working memory per conversation, "
    "growing with context length and concurrent users).")
n.table(["Precision", "Bytes / parameter", "13B model", "70B model"], [
    ["32-bit", "4", "52 GB", "280 GB"], ["16-bit (usual)", "2", "<b>26 GB</b>", "140 GB"],
    ["8-bit", "1", "13 GB", "70 GB"], ["4-bit", "0.5", "6.5 GB", "35 GB"],
], [0.3, 0.25, 0.22, 0.23])
n.bullets([
    "<b>Quantisation</b> (8/4-bit) shrinks memory 2–4× with a small quality loss; <b>tensor parallelism</b> splits a model "
    "across several GPUs.",
    "<b>Containers</b>: <b>Large Model Inference (LMI)</b> containers (vLLM, TensorRT-LLM) or Hugging Face <b>Text "
    "Generation Inference (TGI)</b> handle batching, streaming, quantisation, multi-GPU.",
    "<b>Model loading</b> from S3 can take minutes — hurts auto-scaling; keep warm instances, pre-cache artefacts, use "
    "smaller/quantised models.",
    "If Bedrock offers the model, Bedrock handles all of this — usually the 'least operational overhead' answer.",
])

# =============================================================== part B
n.h1("Part B — Vector stores at scale and query handling")
n.h2("B1. More vector architectures (Skill 1.4.1)")
n.bullets([
    "<b>OpenSearch Service + neural plugin</b>: OpenSearch itself calls an embedding model (e.g. Bedrock via a "
    "connector) at ingest and query time; you send text. 'Topic-based segmentation' = topic-specific indexes.",
    "<b>RDS / Aurora PostgreSQL + pgvector with S3 documents</b>: documents in S3; chunks, embeddings and metadata in "
    "SQL — join vectors with business data.",
    "<b>DynamoDB alongside a vector DB</b>: DynamoDB holds metadata/records (fast ID lookup); OpenSearch does similarity "
    "search; zero-ETL sync. DynamoDB is still <b>not</b> a vector store.",
])
n.code(" WITHOUT neural plugin: code -> Bedrock (embed) -> vector -> code -> OpenSearch\n"
       " WITH neural plugin:    code -> OpenSearch -> (OpenSearch calls Bedrock to embed) -> store/search\n"
       " DynamoDB pairing:      query -> OpenSearch (vector search) -> top IDs -> DynamoDB (fetch records)")
n.h2("B2. Metadata frameworks (Skill 1.4.2)")
n.code(" s3://kb-docs/refund-policy.pdf\n"
       " s3://kb-docs/refund-policy.pdf.metadata.json\n"
       ' {"metadataAttributes": {"department": "finance", "doc_type": "policy", "author": "j.smith",\n'
       '                         "effective_date": 20261001, "region": "EU"}}')
n.bullets([
    "Filter at retrieval (equals, greater-than, in-list, starts-with): department = finance AND effective_date ≥ 20260101.",
    "Outdated answers → effective_date / version attribute + filter, or remove superseded documents and re-sync.",
    "Return author/date with answers for transparency; domain tags keep searches in the right content type.",
])
n.h2("B3. Vector search at scale (Skill 1.4.3)")
n.p("<b>Shards</b> are pieces of one index spread across nodes. A query goes to <b>all</b> shards at once (scatter), each "
    "returns its best matches, and results are merged (gather) — speed comes from <b>parallelism</b>, not early exit. "
    "<b>Replicas</b> are copies of shards: they <b>serve reads</b> (more throughput) and <b>survive node failure</b>.")
n.code(" query --> sent to ALL shards at once\n"
       "           node 1: shard 1 -> its top 10 --+\n"
       "           node 2: shard 2 -> its top 10 --+--> merged -> overall top 10\n"
       "           node 3: shard 3 -> its top 10 --+")
n.bullets([
    "<b>Multi-index per domain</b> (legal, HR, product): smaller, faster, domain-specific settings/embeddings.",
    "<b>Hierarchical indexing</b>: search document summaries first, then chunks within the top documents.",
    "ANN algorithms (e.g. <b>HNSW</b>) trade recall vs latency (e.g. ef_search); <b>vector quantisation</b> cuts memory.",
])
n.h2("B4. Embedding dimensions and batching (Skill 1.5.2)")
n.table(["More dimensions (1024)", "Fewer dimensions (256)"], [
    ["More nuance, usually slightly better retrieval", "4× less storage, faster search, cheaper"],
    ["Bigger index, more memory, higher cost", "Slightly less precise"],
], [0.5, 0.5])
n.p("Decide by evaluating retrieval quality on your queries; consider domain fit and modality (Titan Multimodal "
    "Embeddings for images). Load millions of documents with <b>batch embedding generation</b> (parallel Lambda from "
    "S3/SQS, or batch inference). Queries and documents must use the same embedding model.")
n.h2("B5. Query handling (Skill 1.5.5)")
n.code(' Expansion:     "laptop won\'t charge" -> + "battery not charging", "power adapter fault" -> search all -> merge\n'
       " HyDE:          FM writes a hypothetical answer -> search with it\n"
       ' Decomposition: "Compare refund and shipping of Basic vs Premium" -> 4 sub-queries -> combine\n'
       ' Rewriting:     "And for premium?" -> "What is the refund window for the Premium plan?"')
n.p("Step Functions pipeline: [Rewrite (FM)] → [Decompose / expand] → [<b>Map state</b>: retrieve each sub-query in "
    "parallel] → [Merge + rerank] → [Generate].")
n.h2("B6. How Bedrock offers query handling")
n.table(["Technique", "Built into Knowledge Bases?", "How"], [
    ["Query decomposition", "Yes", "RetrieveAndGenerate query transformation type QUERY_DECOMPOSITION"],
    ["Follow-up questions", "Yes", "Pass the sessionId from the previous RetrieveAndGenerate call"],
    ["Reranking", "Yes", "Reranking configuration with a Bedrock rerank model"],
    ["Hybrid vs semantic", "Yes", "Search type setting (overrideSearchType)"],
    ["Metadata filter — explicit", "Yes", "Pass a filter"],
    ["Metadata filter — implicit", "Yes", "A model builds the filter from the question using attribute descriptions"],
    ["Query expansion / HyDE", "No single switch", "Bedrock model call to rephrase, then Retrieve each and merge"],
    ["Custom multi-step pipelines", "Build it", "Step Functions around the Retrieve API (Map state)"],
], [0.25, 0.2, 0.55])
n.code('''bedrock_agent_runtime.retrieve_and_generate(
    input={"text": "Compare refund and shipping for Basic vs Premium"},
    sessionId=previous_session_id,                                   # follow-ups keep context
    retrieveAndGenerateConfiguration={"type": "KNOWLEDGE_BASE", "knowledgeBaseConfiguration": {
        "knowledgeBaseId": "KB123", "modelArn": "<model ARN>",
        "orchestrationConfiguration": {"queryTransformationConfiguration": {"type": "QUERY_DECOMPOSITION"}},
        "retrievalConfiguration": {"vectorSearchConfiguration": {
            "numberOfResults": 10, "overrideSearchType": "HYBRID",
            "filter": {"equals": {"key": "department", "value": "finance"}}}}}})''')

# =============================================================== part C
n.h1("Part C — Agent safeguards, MCP hosting, streaming, rate limiting, tracing")
n.h2("C1. Safeguarded agent workflows (Skill 2.1.3)")
n.code(" [Call model] -> [Choice: tool?] -> [Run tool] -> [Increment counter] -> [Choice: counter < 10 AND budget left?]\n"
       "      ^------------------------------------- yes ------------------------------+\n"
       "                                             no -> [Stop: best answer + 'limit reached' / escalate]")
n.bullets([
    "<b>Stopping conditions</b>: max iterations, token/cost budget (+ CloudWatch billing alarm), total time, "
    "'same tool failed 3 times'.",
    "<b>Timeouts</b>: per-tool Lambda timeout; Step Functions TimeoutSeconds on states and the workflow.",
    "<b>IAM boundaries</b>: least privilege per tool role; <b>permission boundaries</b> cap the maximum a role can get — "
    "limits damage if a prompt injection manipulates the agent.",
    "<b>Circuit breakers</b> for failing tools.",
])
n.h2("C2. Coordinating multiple models (Skill 2.1.4)")
n.code("                 +--> Model A --> answer A --+\n"
       " question -------+--> Model B --> answer B --+--> AGGREGATION --> final answer\n"
       "                 +--> Model C --> answer C --+")
n.p("Aggregation: <b>majority vote</b> (classification), <b>judge model</b> (LLM-as-a-judge picks best), <b>merge</b> "
    "complementary parts, <b>confidence-based</b> (disagreement → human review). Worth it for high-stakes accuracy; "
    "costs ~3× latency and money. A 'model selection framework' = routing logic.")
n.h2("C3. Humans in the loop (Skill 2.1.5)")
n.code(" User clicks thumbs up/down (+ comment) -> API Gateway POST /feedback -> Lambda -> DynamoDB\n"
       "   store request ID, prompt, answer, model version, rating -> dashboards, bad-answer review, eval datasets")
n.p("Human augmentation: send low-confidence or disputed outputs to people; <b>Amazon Augmented AI (A2I)</b> manages "
    "human review workflows. Approvals: Step Functions waitForTaskToken (Day 3).")
n.h2("C4. Reliable tool integrations (Skill 2.1.6)")
n.code('''{"name": "refund_order",
 "description": "Refunds an order. Only for orders in DELIVERED status, within 30 days.",
 "inputSchema": {"json": {"type": "object",
   "properties": {"order_id": {"type": "string", "pattern": "^ORD-[0-9]{6}$"},
                  "reason":   {"type": "string", "enum": ["damaged", "late", "wrong_item"]},
                  "amount":   {"type": "number", "minimum": 0, "maximum": 5000}},
   "required": ["order_id", "reason"]}}}''')
n.bullets([
    "Strict schemas (types, required, enum, pattern, min/max) prevent bad calls.",
    "<b>Validate again in Lambda</b> — never trust model-generated parameters; return clear toolResult errors.",
    "Retries with backoff for temporary failures; <b>idempotent</b> actions (unique request ID so a retry doesn't "
    "refund twice).",
    "Strands lets you customise behaviour around tool calls (logging, validation, approvals).",
])
n.h2("C5. Hosting MCP servers (Skill 2.1.7)")
n.table(["", "AWS Lambda", "Amazon ECS (often Fargate)"], [
    ["Best for", "Stateless, lightweight, quick tools", "Complex, stateful, long-running tools; heavy dependencies"],
    ["Examples", "Weather, order status, currency", "Persistent DB connection pools, browser automation, long streams"],
    ["Scaling / cost", "Scales to zero; pay per call", "Runs continuously; you size containers"],
    ["Limits", "15-minute max; no state between calls", "No time limit; keeps state in memory"],
], [0.16, 0.4, 0.44])
n.p("Use <b>MCP client libraries</b> (built into Strands) so every tool is called the same way; AgentCore Gateway can "
    "front Lambda functions as MCP tools.")
n.h2("C6. Real-time streaming to the browser (Skill 2.4.2)")
n.code(" Browser <=== WebSocket (stays open) ===> API Gateway WebSocket API -> Lambda -> Bedrock ConverseStream\n"
       "         <-- token <-- token <-- token <--- Lambda posts each chunk to the connection")
n.table(["Option", "What it is", "Use when"], [
    ["WebSockets (API Gateway WebSocket API)", "Persistent two-way connection", "Interactive chat, interruptions, two-way"],
    ["Server-sent events / Lambda response streaming", "One-way stream over HTTP", "Just stream the answer to the user"],
    ["API Gateway chunked transfer encoding", "HTTP response sent in pieces", "REST-style APIs streaming tokens"],
], [0.32, 0.3, 0.38])
n.h2("C7. Rate limiting and tracing (Skill 2.4.3)")
n.code(" Abusive client --> API Gateway: usage-plan limit reached -> 429   (Bedrock quota protected)\n"
       " Normal users   --> API Gateway --> Lambda --> Bedrock  OK\n\n"
       " X-Ray trace for request abc123 (total 12.1 s)\n"
       "   API Gateway 0.05 s | Lambda 12.0 s -> KB Retrieve 0.4 s, Bedrock call 11.4 s  <- bottleneck")
n.bullets([
    "<b>API Gateway throttling</b>: rate and burst limits per API/stage/method; <b>usage plans with API keys</b> give "
    "per-client quotas; excess gets HTTP 429 before reaching Bedrock.",
    "<b>AWS X-Ray</b>: traces each request across services with timings and a service map — find the slow step.",
])

# =============================================================== rules
n.h1("Decision rules — gap lesson")
n.numbered([
    "Switch models without code change/redeploy → <b>AppConfig</b> (+ Lambda/API Gateway), gradual rollout, alarm rollback.",
    "Stop hammering a failing model → <b>circuit breaker</b> (Step Functions + DynamoDB).",
    "Model not in your Region → <b>cross-region inference</b>; Region outage → <b>multi-Region + Route 53 failover</b>.",
    "Reduced service instead of errors → <b>graceful degradation</b>.",
    "Many cheap variants of one model → <b>LoRA adapters</b> on a shared base endpoint.",
    "Govern custom models → <b>Model Registry</b> + pipeline; safe rollout → <b>blue/green, canary, linear + auto-rollback</b>.",
    "Model nearing end-of-life → evaluate, switch via config, canary, retire.",
    "Self-hosting a big LLM → GPU memory sizing, <b>quantisation</b>, <b>tensor parallelism</b>, <b>LMI/TGI</b> containers.",
    "OpenSearch embeds automatically → <b>neural plugin</b>; vectors + SQL joins → <b>pgvector</b>; DynamoDB = metadata only.",
    "Latest version / department / author → <b>.metadata.json + filters</b> (explicit or implicit).",
    "Slow huge index → <b>shards</b> (parallel), <b>replicas</b> (throughput, availability), multi-index, hierarchical.",
    "Cheaper vector search → fewer dimensions or vector quantisation; millions of docs → batch embedding.",
    "Vague → expansion; multi-part → decomposition; follow-ups → rewriting / sessionId; least effort → KB built-ins.",
    "Runaway agents → stopping conditions + budgets; slow tools → timeouts; manipulation → least-privilege IAM.",
    "High-stakes accuracy → ensemble + aggregation; ratings → API Gateway → Lambda → DynamoDB; review → A2I.",
    "Bad tool params → strict schema + Lambda validation + clear errors + idempotency.",
    "Light MCP tools → Lambda; complex/stateful/long → ECS (Fargate).",
    "Two-way chat → WebSockets; one-way stream → SSE / chunked transfer; backend → Bedrock streaming.",
    "One client exhausting capacity → <b>API Gateway throttling + usage plans</b>; find slow service → <b>X-Ray</b>.",
    "Model routing → static config, Step Functions content-based, Intelligent Prompt Routing, metrics, API Gateway.",
])

# =============================================================== checks
n.h1("Your part checks — graded")
n.table(["Part", "Your answers", "Feedback"], [
    ["A", "Circuit breaker vs retries; LoRA for 15 variants; 13B GPU memory",
     "✓ ✓ — circuit breakers also fail fast; LoRA saves storage and needs one shared endpoint. Memory: 13B × 2 bytes "
     "= <b>26 GB</b> + KV cache (worked through together)."],
    ["B", "Latest-version fix; shards vs replicas; follow-up questions",
     "✓ ½ ✓ — shards don't stop early: all shards are searched in parallel and merged; replicas also add read "
     "throughput."],
    ["C", "Runaway agent safeguards; MCP host for 30-min stateful tool; WebSockets vs SSE",
     "✓ ✓ ✓ — add token/cost budgets with billing alarms; Lambda's 15-minute limit rules it out."],
], [0.07, 0.38, 0.55])

n.h1("Mistakes and learnings")
n.table(["Point", "Correction"], [
    ["Shards 'stop early when a match is found'", "All shards are searched in parallel (scatter-gather); speed = parallelism."],
    ["GPU memory sizing unknown", "Memory ≈ parameters × bytes per parameter (16-bit = 2 bytes) + KV cache."],
    ["DynamoDB in RAG designs", "Valid only for metadata/records next to a vector DB — never as the vector store."],
], [0.38, 0.62])

n.h1("Glossary — new terms")
n.table(["Term", "Meaning"], [
    ["Model routing", "Choosing the model per request to balance cost and quality."],
    ["AWS AppConfig / feature flag", "Service for runtime settings; a flag is an on/off or value read while the app runs."],
    ["Systems Manager Parameter Store", "AWS store for configuration values and secrets."],
    ["Stage variable", "Per-stage setting in API Gateway (e.g. dev vs prod)."],
    ["Mapping template", "API Gateway rule that transforms requests/responses."],
    ["Intelligent Prompt Routing", "Bedrock feature routing each prompt to the cheaper adequate model in a family."],
    ["Cascading", "Try a small model first; escalate to a larger one if quality checks fail."],
    ["Circuit breaker (closed/open/half-open)", "Stops calls to a failing service, uses a fallback, tests recovery."],
    ["Graceful degradation", "Reduced but useful service instead of errors."],
    ["Route 53 failover", "DNS routing that sends users to a healthy Region."],
    ["LoRA / PEFT / adapter", "Parameter-efficient fine-tuning: train small adapters on a frozen base model."],
    ["SageMaker Model Registry", "Catalogue of model versions with approval status."],
    ["SageMaker Pipelines / CodePipeline", "Automated ML / CI-CD pipelines."],
    ["Blue/green, canary, linear", "Deployment strategies shifting traffic gradually; auto-rollback on alarms."],
    ["Active / Legacy / End-of-Life", "Bedrock model lifecycle stages."],
    ["KV cache", "GPU working memory per conversation; grows with context and users."],
    ["Quantisation", "Storing weights/vectors with fewer bits to save memory."],
    ["Tensor parallelism", "Splitting one model across several GPUs."],
    ["LMI / TGI containers", "Large Model Inference and Text Generation Inference serving containers."],
    ["OpenSearch neural plugin", "OpenSearch calls an embedding model itself at ingest and query time."],
    ["Zero-ETL integration", "Managed sync between services without pipeline code (e.g. DynamoDB → OpenSearch)."],
    ["Sidecar .metadata.json", "File next to a KB document holding its metadata attributes."],
    ["Implicit filtering", "A model builds metadata filters from the user's question."],
    ["Shard / replica", "Piece of an index on a node / copy of a shard for reads and availability."],
    ["ANN / HNSW / ef_search", "Approximate nearest-neighbour search; HNSW algorithm; recall-vs-latency setting."],
    ["Query expansion / HyDE", "Search with rephrasings / with a hypothetical answer."],
    ["Query decomposition / rewriting", "Split multi-part questions / make follow-ups standalone."],
    ["Map state", "Step Functions state running a step for every item, in parallel."],
    ["Stopping condition", "Limit that ends an agent loop (iterations, budget, time)."],
    ["Permission boundary", "IAM feature capping the maximum permissions a role can have."],
    ["Ensemble / aggregation", "Several models answer; combine by vote, judge, merge."],
    ["Amazon A2I (Augmented AI)", "Managed human review workflows for ML outputs."],
    ["Idempotent", "Repeating a request has the same effect as doing it once."],
    ["WebSocket API", "API Gateway persistent two-way connections."],
    ["Server-sent events (SSE)", "One-way server-to-browser stream over HTTP."],
    ["Chunked transfer encoding", "HTTP response sent in pieces."],
    ["Lambda response streaming", "Lambda sends its response progressively (e.g. via function URLs)."],
    ["Usage plan / API key", "API Gateway per-client quotas and throttling."],
    ["AWS X-Ray / service map", "Distributed tracing with per-step timings; diagram of services."],
], [0.36, 0.64])

n.callout("Next", "Gap-lesson quiz (new questions), then Day 6 — Guardrails and Responsible AI — from Part 1.")
n.build()
print(os.path.abspath(OUT))
