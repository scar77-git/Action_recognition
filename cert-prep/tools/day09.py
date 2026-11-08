"""Day 9 note: Prompt engineering, prompt governance and solution design."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import Note  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Day_9_2026-11-08_Prompt_Engineering_and_Design.pdf")

n = Note(OUT, "Day 9 — Prompt Engineering, Prompt Governance and Solution Design",
         "30 Oct – 8 Nov 2026 &nbsp;·&nbsp; Taught by Theo prof 2 &nbsp;·&nbsp; Skills <b>1.6.1–1.6.6</b>, "
         "<b>2.1.2</b>, <b>5.2.3</b>, <b>5.2.5</b> (prompts) and <b>1.1.1–1.1.3</b> (design) &nbsp;·&nbsp; "
         "Exam: Mon 9 Nov, 1:30 PM IST")
n.callout("Today in one paragraph",
          "A production prompt is <b>code</b>: it has inputs (variables), a contract (output format), versions, tests, "
          "approvals and an audit trail. Store it in <b>Bedrock Prompt Management</b> (parameterised, immutable "
          "versions, called by ARN); enforce must-never rules with <b>Guardrails</b>; make output parser-safe with a "
          "<b>tool-use schema + Lambda validation</b>; reason with <b>chain-of-thought</b> inside one call or a "
          "<b>Step Functions ReAct loop</b> across calls; chain prompts with <b>Bedrock Flows</b>; test with a golden "
          "set + Map state + CloudWatch pass-rate alarm; debug with Logs Insights, X-Ray and CloudTrail. Design "
          "solutions requirement-first, prove them with a measurable <b>PoC</b>, and spread best practice with "
          "<b>WA Tool + Generative AI Lens</b> turned into reusable components.", "ok")

n.h1("Morning recap — Days 7–8 misses")
n.bullets([
    "Reworded repeat questions → <b>semantic cache</b> (embedding similarity); exact-text hash misses; clear on KB sync.",
    "Compare <b>cost per successful answer</b>: price_cheap + failure_rate × price_expensive vs price_expensive ÷ success.",
    "Slow because answers are long → <b>cap output length</b> first (output tokens dominate latency).",
    "'Why was this answer given?' → structured <b>decision logs</b> in CloudWatch Logs (sources, versions, decision).",
])

# ------------------------------------------------------------ Part 1
n.h1("Part 1 — Instruction frameworks and refinement (Skills 1.6.1, 1.6.5, 2.1.2)")
n.h2("Why a prompt is code")
n.p("In production the prompt controls behaviour like a class does: it has <b>inputs</b> (variables such as the "
    "question and retrieved documents), a <b>contract</b> (the format downstream code parses), <b>versions</b>, and "
    "needs <b>tests, approval, rollback and audit</b>. Task 1.6 is the software engineering of prompts.")
n.h2("Anatomy of a production prompt")
n.code("+------------------------------ ONE MODEL CALL ------------------------------+\n"
       "| SYSTEM PROMPT  who you are + rules             <- stable, written by you   |\n"
       "| CONTEXT        <documents>...</documents>      <- retrieved docs, history  |\n"
       "| EXAMPLES       few-shot input -> ideal output  <- optional                 |\n"
       "| TASK INPUT     <question>{{question}}</question>  <- UNTRUSTED             |\n"
       "| OUTPUT SPEC    'Reply only with JSON: {...}'                               |\n"
       "+----------------------------------------------------------------------------+")
n.p("Most misbehaviour comes from mixing these blocks: rules buried in user text, or no output spec so the format drifts.")
n.h2("Instruction framework = three layers (1.6.1)")
n.code(" Layer 1  ROLE + RULES  -> Bedrock Prompt Management   'what you should do'   (model is ASKED)\n"
       " Layer 2  RAI POLICY    -> Bedrock Guardrails          'what you must never do' (ENFORCED outside model)\n"
       " Layer 3  FORMAT        -> template / output spec      'what shape the answer has' (+ validated in code)")
n.p("A prompt instruction is a request the model usually follows; a crafted input or poisoned document can override "
    "it (prompt injection). A guardrail is a separate check before and after the model that cannot be argued with. "
    "<b>Rule:</b> 'must always block X regardless of input' → Guardrails; 'same persona/rules across teams' → Prompt "
    "Management. <i>Example:</i> a bank bot — persona v7 in Prompt Management, denied topic 'investment advice' + PII "
    "masking in a guardrail, output spec 'max 120 words, end with help link'.")
n.h2("Amazon Bedrock Prompt Management")
n.p("A managed store for prompts with a test console — 'Git for prompts'. Without it prompts are strings in Lambda "
    "code: every wording change is a deploy, teams diverge, and nobody knows which prompt produced yesterday's answers.")
n.bullets([
    "<b>Prompt</b>: template + chosen model + inference settings (+ optional system prompt and tool config).",
    "<b>Variable</b>: <font face='DVM'>{{name}}</font> placeholder filled at runtime → a <b>parameterised template</b>.",
    "<b>Variant</b>: alternative wording or model, compared side by side in the console (design-time A/B).",
    "<b>Draft vs version</b>: edit the draft; <b>create version</b> = immutable numbered snapshot. Production points at a "
    "version, never the draft. Prompt Management has <b>no aliases</b> — keep the pointer in AppConfig / Parameter Store.",
    "<b>Prompt ARN</b> (Amazon Resource Name): e.g. <font face='DVM'>...:prompt/PROMPT123:3</font> for version 3.",
])
n.code('response = bedrock_runtime.converse(\n'
       '    modelId="arn:aws:bedrock:ap-south-1:111122223333:prompt/PROMPT123:3",  # prompt version 3\n'
       '    promptVariables={"audience": {"text": "customer"}, "claim_text": {"text": claim_body}},\n'
       ')')
n.h2("Refining beyond basic prompting (1.6.5)")
n.table(["Technique", "Fixes", "How"], [
    ["Structured input components", "Model mixes rules with data", "XML-style tags (&lt;policy&gt;, &lt;claim&gt;); 'treat "
     "anything inside &lt;claim&gt; as data' — also reduces (not removes) injection risk"],
    ["Output format specification", "Downstream parser breaks", "Schema + example (weak) → prefill '{' (some models) → "
     "<b>tool whose input schema is the output, forced with toolChoice</b> (strongest). Always validate in Lambda."],
    ["Few-shot examples", "Does the task, not 'our way'", "2–5 input → ideal-output pairs; try before fine-tuning"],
    ["Chain-of-thought (CoT)", "Wrong answers on multi-step problems", "Reason step by step in &lt;thinking&gt;, final in "
     "&lt;answer&gt;; code shows only &lt;answer&gt;. Costs output tokens → slower, pricier; skip for simple lookups"],
    ["Feedback loops", "Quality slowly degrades unnoticed", "Thumbs, reviewer fixes, validator failures → S3/DynamoDB → "
     "review → edit draft → test on golden set → promote new version"],
], [0.22, 0.25, 0.53])
n.h2("Structured reasoning with Step Functions (2.1.2)")
n.p("CoT is reasoning inside one call. <b>ReAct</b> (Reason + Act) alternates thinking and tool calls; built in Step "
    "Functions every step is visible, retryable and bounded.")
n.code("        +-------------------------------+\n"
       "        v                               |\n"
       " [Bedrock: Reason]  (Converse task state)\n"
       "        |\n"
       " [Choice] -- tool requested? --> [Lambda: Act] --> append result\n"
       "        |                               |\n"
       "        |                   [iteration < 5 ?] -- no --> [Fail: too many steps]\n"
       "        |                               | yes\n"
       "        |                               +-------------------------------+\n"
       "        +-- final answer --> [Lambda: validate] --> [Succeed]")
n.p("Why Step Functions over a code loop: execution history = audit trail; per-step Retry/Catch; an iteration counter "
    "is a hard <b>stopping condition</b> (2.1.3). If the steps are <b>known in advance</b>, don't let the model choose "
    "them — <b>prompt chaining / decomposition</b> as fixed states (e.g. extract → check rules → draft letter).")
n.table(["Need", "Technique", "Where"], [
    ["Better reasoning in one answer", "Chain-of-thought", "Inside one model call"],
    ["Fixed multi-step process", "Prompt chaining", "Step Functions states or Bedrock Flows"],
    ["Model decides steps/tools", "ReAct loop with iteration cap", "Step Functions or agent framework"],
    ["Consistent persona/rules across teams", "Versioned templates", "Prompt Management"],
    ["Policy that must never be violated", "Guardrails", "Outside the model"],
    ["Parser-safe output", "Output spec + tool schema + validation", "Prompt + Lambda"],
], [0.35, 0.35, 0.3])

# ------------------------------------------------------------ Part 2
n.h1("Part 2 — Interactive systems, governance, QA, Flows, troubleshooting")
n.h2("Interactive systems that keep context (1.6.2)")
n.p("Models are stateless: 'memory' is your app re-sending earlier turns.")
n.bullets([
    "<b>DynamoDB history</b>: partition key sessionId, sort key timestamp; <b>TTL</b> (Time To Live) auto-deletes old "
    "sessions. Load last N turns; summarise older ones to avoid context-window overflow (5.2.1). AgentCore Memory is "
    "the managed agent alternative.",
    "<b>Amazon Comprehend</b> custom classifier tags the <b>intent</b> (cancel_order, complaint…) → route: complaints to "
    "humans, tracking to an API, only open questions to the FM. Sentiment can trigger escalation.",
    "<b>Step Functions clarification</b>: Choice 'all required fields present?' → no → ask the user and pause with "
    "<font face='DVM'>.waitForTaskToken</font> → resume on reply. Never let the model invent missing details. Use "
    "<b>Standard</b> workflows for long waits — Express max 5 minutes.",
])
n.code(" user msg -> [Lambda: intent + extract fields] -> [Choice: fields present?]\n"
       "                 ^                                 | no              | yes\n"
       "                 |                     [Ask user, .waitForTaskToken]  [Bedrock: answer]\n"
       "                 +---------------------------------+                  [Save turn: DynamoDB]")
n.h2("Prompt governance (1.6.3)")
n.code(" Author edits DRAFT -> automated tests -> APPROVAL (human) -> create VERSION -> move pointer (AppConfig)\n"
       "        +--------------- CloudTrail: who changed what, when ---------------+")
n.bullets([
    "<b>Parameterised templates</b>: teams fill variables, nobody rewrites wording → consistency.",
    "<b>Approval gate</b> you build around Prompt Management: CodePipeline manual approval or Step Functions task token; "
    "<b>IAM</b> lets authors edit drafts but only the pipeline role may CreatePromptVersion / change the pointer.",
    "<b>S3 template repository</b> with S3 Versioning for rollback / templates shared beyond Bedrock.",
    "<b>CloudTrail</b> = API calls (who, which role, when) — <b>no prompt text</b>.",
    "<b>Model invocation logging</b> → CloudWatch Logs / S3 = exact prompt and response text.",
])
n.table(["Question asks…", "Answer"], [
    ["Who changed the prompt / who called the model, when?", "CloudTrail"],
    ["What exact text was sent and returned?", "Model invocation logging → CloudWatch Logs / S3"],
    ["Why did this answer happen (sources, versions)?", "Decision logs in CloudWatch Logs"],
], [0.55, 0.45])
n.h2("Prompt quality assurance (1.6.4)")
n.bullets([
    "<b>Golden dataset</b> in S3 with edge cases: empty, very long, other language, sarcasm, injection, missing fields.",
    "<b>Step Functions Map state</b> runs every case against the candidate version.",
    "<b>Lambda validator</b>: JSON schema, required fields, allowed values, forbidden content; LLM-as-a-judge for "
    "subjective quality (Bedrock Evaluations offers it managed).",
    "<b>CloudWatch custom metric</b> PassRate{PromptVersion} + <b>alarm</b> below baseline → block promotion "
    "(regression testing).",
])
n.code(" S3 golden set -> Map -> [Bedrock: prompt vX] -> [Lambda: validate] -> PassRate{version}\n"
       "                                                     alarm if < baseline -> block / roll back")
n.h2("Amazon Bedrock Flows (1.6.6) — formerly Prompt Flows")
n.table(["Node", "Does"], [
    ["Input / Output", "Entry point and final result"],
    ["Prompt", "Calls a model; can reference a Prompt Management prompt → reusable component"],
    ["Condition", "Branches on an expression over earlier outputs (category == 'complaint')"],
    ["Knowledge base", "Retrieve from / query a Bedrock KB"],
    ["Lambda function", "Pre-processing (clean, mask PII) and post-processing (validate, format)"],
    ["Agent; Iterator / Collector; Inline code; S3 storage/retrieval; Lex", "Hand-off, loops, small scripts, I/O"],
], [0.38, 0.62])
n.code(" [Input] -> [Lambda: mask PII] -> [Prompt: classify] -> [Condition]\n"
       "    refund    -> [KB: policy] -> [Prompt: reply] --+\n"
       "    complaint -> [Prompt: summary for agent] ------+-> [Lambda: schema check] -> [Output]\n"
       "    other     -> [Prompt: general reply] ----------+")
n.p("Lifecycle: working draft → versions → <b>aliases</b>; the app calls the alias with <b>InvokeFlow</b> "
    "(bedrock-agent-runtime) and you move the alias to release. Never call the draft from production.")
n.table(["Bedrock Flows when…", "Step Functions when…"], [
    ["Mostly prompts, KBs, small Lambdas", "Many AWS services / external systems"],
    ["Low-code GenAI canvas inside Bedrock", "Long waits (days), callbacks, Standard up to 1 year"],
    ["Branching on model output", "Fine-grained Retry/Catch, Map over thousands, full audit"],
], [0.5, 0.5])
n.h2("Troubleshooting prompts (5.2.3, 5.2.5)")
n.bullets([
    "<b>Version comparison</b>: old vs new on the same inputs and settings; <b>change one thing at a time</b>.",
    "<b>CloudWatch Logs Insights</b> on invocation logs → inspect the <b>rendered prompt</b> ('prompt confusion': "
    "empty variable, literal {{claim_text}}, history pushing rules out, contradictory documents).",
    "<b>X-Ray</b> traces API Gateway → Lambda → KB → Bedrock → validator: which segment is slow or failing.",
    "<b>Schema-validation metric</b> catches format drift after a model or prompt change.",
])
n.table(["Symptom", "First move"], [
    ["JSON sometimes malformed after an update", "Schema metric + compare versions on golden set; roll back pointer"],
    ["Ignores instructions / off-topic for some requests", "Logs Insights on invocation logs → rendered prompt"],
    ["Slow or failing somewhere in a multi-service chain", "X-Ray trace by segment"],
    ["Who modified the production prompt?", "CloudTrail"],
    ["New prompt must not reduce quality", "Golden set + Map + Lambda checks + PassRate alarm gate"],
    ["Assistant guesses missing details", "Step Functions clarification loop (task token)"],
    ["Conversations lose earlier context / overflow", "DynamoDB history, trim + summarise, TTL"],
], [0.5, 0.5])

# ------------------------------------------------------------ Part 3
n.h1("Part 3 — Designing GenAI solutions (Skills 1.1.1–1.1.3)")
n.h2("Requirement-first design (1.1.1)")
n.code(" BUSINESS NEED + CONSTRAINTS (task, latency, volume, cost cap, accuracy, sensitivity, region)\n"
       "  1 KNOWLEDGE/BEHAVIOUR: prompt engineering -> RAG -> fine-tuning -> continued pre-training\n"
       "  2 MODEL: smallest that meets quality on YOUR test set; routing/cascade if mixed difficulty\n"
       "  3 INTEGRATION: sync (API GW + Lambda + streaming) | async (SQS) | batch | workflow/agent\n"
       "  4 DEPLOYMENT: on-demand | provisioned throughput | cross-Region inference | SageMaker endpoint\n"
       "  + always: Guardrails, IAM least privilege, KMS, logging")
n.table(["Clue in the stem", "Points to"], [
    ["Documents change weekly", "RAG (Knowledge Base), not fine-tuning"],
    ["Specific style / jargon consistently", "Fine-tuning (after prompting + few-shot fail)"],
    ["Overnight millions of records, cost-sensitive", "Batch inference"],
    ["Users wait in a chat window", "Synchronous + ConverseStream"],
    ["Must take actions in other systems", "Agent / tool use"],
    ["Steady high traffic, guaranteed throughput", "Provisioned throughput"],
    ["Spiky traffic, survive regional capacity limits", "Cross-Region inference profile"],
    ["Traffic must stay off the internet", "VPC endpoint (PrivateLink)"],
], [0.55, 0.45])
n.p("<i>Example:</i> adjusters querying 40,000 monthly-updated policy PDFs, < 5 s, confidential → RAG KB; mid-size model "
    "chosen by evaluation; API Gateway + Lambda + Retrieve/Converse with streaming; on-demand + grounding guardrail, "
    "KMS, VPC endpoint, metadata filters by region.")
n.h2("Proof of concept on Bedrock (1.1.2)")
n.numbered([
    "Measurable success criteria <b>before</b> building: accuracy on a golden set, p95 latency, cost per answer, "
    "business metric (ticket deflection).",
    "Smallest setup: playground + Prompt Management, KB quick create on a <b>representative sample</b>, "
    "<b>on-demand</b> (never provisioned throughput at PoC).",
    "Compare 2–3 models with <b>Bedrock model evaluation jobs</b> (automatic, LLM-as-a-judge, human).",
    "Measure tokens per request × expected volume → projected cost.",
    "Safe data (masked sample, target Region, production guardrails).",
    "Go / no-go against step 1.",
])
n.p("Traps: build full production pipeline first; fine-tune before trying prompting/RAG; buy provisioned throughput "
    "for the PoC; 'demo and collect impressions' (no measurable criteria).")
n.h2("Standard components and the Generative AI Lens (1.1.3)")
n.table(["Well-Architected pillar", "GenAI example"], [
    ["Operational excellence", "Prompt versioning, invocation logging, regression tests"],
    ["Security", "IAM least privilege, KMS, Guardrails, injection defences"],
    ["Reliability", "Retries with backoff, fallback models, cross-Region inference, circuit breakers"],
    ["Performance efficiency", "Right model size, streaming, caching, output caps"],
    ["Cost optimisation", "Batch, prompt caching, routing/cascades, token budgets"],
    ["Sustainability", "Smallest adequate model, batch over always-on, avoid needless retraining"],
], [0.3, 0.7])
n.p("The <b>Generative AI Lens</b> is an add-on question set applied in the <b>AWS Well-Architected Tool</b>: define a "
    "workload, apply the lens, answer, get high/medium-risk issues and an improvement plan, save <b>milestones</b> to "
    "track progress.")
n.h2("How the lens relates to standard components (your follow-up question)")
n.p("The lens says <b>what</b> good looks like and checks it; standard components are <b>how</b> you build good once "
    "so every team gets it. Java analogy: coding standard + SonarQube rules (lens) vs a shared Spring Boot starter "
    "(component). You need both.")
n.code(" 1 REVIEW      WA Tool + GenAI Lens -> high/medium-risk issues\n"
       " 2 STANDARD    platform team turns each best practice into a default\n"
       " 3 BUILD ONCE  CDK construct / CloudFormation 'secure-rag-module' -> AWS Service Catalog\n"
       " 4 REUSE       teams launch the product -> same guardrail, logging, KMS, alarms\n"
       " 5 RE-REVIEW   most questions already 'yes'; new gap -> update component -> all teams fixed -> 1")
n.p("<i>Example:</i> three apps lack contextual grounding → add a grounding guardrail to the construct's v2 → every "
    "team gets the fix. Wrong answers: a best-practices wiki (nothing enforced); each team reviews and fixes its own way "
    "(inconsistent, repeated work); letting teams create their own guardrail/logging settings.")

# ------------------------------------------------------------ Quiz
n.h1("Day 9 quiz — 8 / 10 (80%)")
n.table(["Q", "Level", "Skill", "You", "Key", "Why (and the trap)"], [
    ["1", "Hard", "1.6.1", "C ✓", "C", "Versioned Prompt Management prompt by ARN (no redeploy) + guardrail denied topic "
     "(holds against crafted inputs). D relies on the prompt alone; A needs redeploys; B fine-tuning isn't enforcement."],
    ["2", "Medium", "1.6.5", "D ✓", "D", "Tool schema + toolChoice + Lambda schema check. Temperature, few-shot + retry "
     "and regex reduce but don't guarantee structure."],
    ["3", "Hard", "2.1.2", "C, E ✓", "C, E", "Fixed steps → fixed states; dynamic tool choice → Step Functions loop "
     "with iteration counter → Fail. Lambda while-loop has no cap or audit; one CoT call can't call APIs."],
    ["4", "Medium", "1.6.3", "B, D ✓", "B, D", "CloudTrail CreatePromptVersion = who published; invocation logging = "
     "exact text. CloudTrail Converse events have no content; version history shows template, not rendered text."],
    ["5", "Hard", "1.6.4", "B, D, F ✓", "B, D, F", "Map state + Lambda validator + PassRate alarm gate. Variants are "
     "manual; Comprehend doesn't grade schemas; X-Ray traces timing, not schema validity."],
    ["6", "Medium", "1.6.2", "A ✓", "A", "Standard workflow + task token + DynamoDB by session. Express caps at 5 min; "
     "Lambda globals aren't durable; temperature doesn't stop invention."],
    ["7", "Hard", "1.6.6", "B, D ✓", "B, D", "Bedrock Flow (Lambda, prompt, condition nodes) + alias with InvokeFlow. "
     "Step Functions isn't low-code inside Bedrock; draft isn't a safe release; agent routing isn't deterministic."],
    ["8", "Hard", "5.2.5", "A ✗", "B", "<b>Behaviour</b> wrong, latency unchanged, one channel only → look at what the "
     "model actually received: Logs Insights on invocation logs (likely an empty/mis-filled variable for mobile). "
     "X-Ray shows time and errors per segment, not prompt content."],
    ["9", "Medium", "1.1.2", "D, E ✓", "D, E", "Measurable targets first + KB on a sample with evaluation jobs. "
     "Provisioned throughput, full fine-tune and full pipeline are not validation steps."],
    ["10", "Hard", "1.1.3", "B, F ✗", "B, D, F", "Select ALL: you missed <b>D</b> — the review found prompts "
     "hard-coded, so the fix for that finding is approved Prompt Management templates with version creation "
     "IAM-gated to the pipeline. Every finding in the stem needs its own fix."],
], [0.04, 0.1, 0.06, 0.1, 0.09, 0.61])

n.h1("Mistakes to add to the log")
n.bullets([
    "Wrong <b>content/behaviour</b> with normal latency → inspect the <b>rendered prompt</b> in invocation logs "
    "(Logs Insights). X-Ray is for <b>where time or errors occur</b> across services.",
    "Multi-finding stems: map <b>each</b> finding to an option (logging, guardrails, hard-coded prompts → templates) "
    "before choosing — a missing fix makes the answer incomplete.",
])

n.h1("Glossary — new terms")
n.table(["Term", "Meaning"], [
    ["Amazon Bedrock Prompt Management", "Managed, versioned store for prompt templates, model and settings."],
    ["Parameterised template / variable", "Prompt with {{placeholders}} filled at runtime."],
    ["Prompt variant", "Alternative wording/model compared side by side in the console."],
    ["Draft / prompt version", "Editable working copy / immutable numbered snapshot used in production."],
    ["ARN (Amazon Resource Name)", "Unique identifier of an AWS resource, e.g. a prompt version."],
    ["promptVariables", "Converse parameter carrying variable values when modelId is a prompt ARN."],
    ["Instruction framework", "Role/rules + guardrail policy + format spec controlling model behaviour together."],
    ["Structured input components", "Delimited blocks (XML-style tags) separating rules, data and question."],
    ["Output format specification", "Exact required output shape: schema, fields, length."],
    ["Prefill", "Starting the assistant's reply (e.g. '{') so the model continues in that format."],
    ["toolChoice", "Converse setting that forces the model to call a specific tool."],
    ["Few-shot prompting", "Including a few example input/output pairs in the prompt."],
    ["Chain-of-thought (CoT)", "Model reasons step by step before the final answer."],
    ["Extended thinking", "Built-in reasoning mode with a token budget on some models."],
    ["Feedback loop", "Collect user/validator signals → improve prompt → test → new version."],
    ["ReAct (Reason + Act)", "Loop alternating reasoning and tool calls until done."],
    ["Prompt chaining / decomposition", "Fixed sequence of prompts, each output feeding the next."],
    ["TTL (Time To Live)", "DynamoDB attribute that expires items automatically."],
    ["Intent recognition", "Classifying what a user wants (Comprehend custom classifier, Lex)."],
    ["Clarification workflow", "Workflow that asks the user for missing details before acting."],
    [".waitForTaskToken", "Step Functions callback: pause until a token is returned with a result."],
    ["Prompt governance", "Control of who changes prompts, approval, and audit."],
    ["Model invocation logging", "Bedrock logging of full prompt and response text to CloudWatch Logs / S3."],
    ["Golden dataset", "Fixed test cases with expected properties used for every prompt change."],
    ["Map state", "Step Functions state that runs the same steps for each item in a list."],
    ["LLM-as-a-judge", "A model scoring another model's answers against a rubric."],
    ["Regression testing", "Proving a new version didn't break what used to work."],
    ["Amazon Bedrock Flows", "Visual chaining of prompt, condition, KB, Lambda and other nodes; versions + aliases."],
    ["Condition node / InvokeFlow", "Flow branching on expressions / API that runs a flow (via an alias)."],
    ["Prompt confusion", "Model misbehaves because the rendered prompt is wrong or contradictory."],
    ["CloudWatch Logs Insights", "Query language over CloudWatch log data."],
    ["AWS X-Ray", "Distributed tracing: time and errors per service segment of one request."],
    ["Format drift", "Output structure gradually deviating from the expected schema."],
    ["PoC (proof of concept)", "Small, time-boxed build that validates feasibility, performance and value."],
    ["p95 latency", "Time that 95% of requests complete within."],
    ["Bedrock model evaluation job", "Managed comparison of models on a dataset (automatic, judge, human)."],
    ["AWS Well-Architected Framework", "Best-practice questions in six pillars."],
    ["Generative AI Lens / WA Tool", "GenAI-specific question set / console service running reviews with milestones."],
    ["CDK / CloudFormation", "Infrastructure as code in Python/Java / AWS template service."],
    ["AWS Service Catalog", "Catalogue of pre-approved products teams can launch themselves."],
], [0.36, 0.64])

n.callout("Next", "Exam tomorrow, Mon 9 Nov 1:30 PM IST. Tonight: re-read the mistakes log and this note's symptom "
          "tables, then sleep. Morning until 10 AM: skim the cheat-sheet tables only — no new topics.")
n.build()
print(os.path.abspath(OUT))
