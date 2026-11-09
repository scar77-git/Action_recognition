"""Full mock question bank, part 5 — Domain 4 (efficiency, monitoring) and Domain 5 (testing, troubleshooting)."""

QS = [
    dict(
        dom="4", skill="4.1.4", kind="single",
        stem=[
            "Every request to a product-advice assistant sends the same 12,000-token prefix (detailed instructions "
            "plus the full current product catalogue), followed by a user question of about 300 tokens. The catalogue "
            "changes once a day. Input-token cost dominates the bill, and time to first token is high. Answers must "
            "stay personalised to each question.",
            "Which change gives the largest cost and latency reduction?",
        ],
        opts=[
            "A semantic cache that returns stored answers when a new question is similar to an earlier one.",
            "Bedrock prompt caching, with the static prefix placed first and a cache checkpoint after it.",
            "A lower maxTokens setting, so that each answer uses fewer output tokens.",
            "Batch inference for all requests, which is about 50% cheaper than on-demand inference.",
        ],
        ans="B",
        why="A long, <b>identical prefix</b> on every call is exactly what <b>prompt caching</b> is for. Cached input "
            "tokens are cheaper and faster to process, and each question still gets its own answer.",
        wrong={
            "A": "This skips the model for similar questions but returns stored answers, which conflicts with "
                 "personalised answers, and it doesn't reduce the prefix cost on cache misses.",
            "C": "The cost is dominated by input tokens; limiting output tokens barely helps.",
            "D": "Batch is for offline workloads; this is an interactive assistant.",
        }),
    dict(
        dom="4", skill="4.1.4", kind="two",
        stem=[
            "A support assistant receives many questions that mean the same thing but are worded differently ('How "
            "long do refunds take?' / 'When will I get my money back?'). Answers come from a knowledge base that "
            "syncs every night. Some questions are about the customer's own account (balances, orders), and those "
            "answers must never be served to another customer.",
            "Which TWO design choices should the team make? (Select TWO.)",
        ],
        opts=[
            "A semantic cache that matches on embedding similarity with a carefully tuned threshold, used only for "
            "general (non-account-specific) questions.",
            "An exact-match cache keyed on a hash of the question text, which is simple and never returns a wrong "
            "answer.",
            "Caching every answer, including account-specific ones, keyed by the question text, to maximise the hit "
            "rate.",
            "Clearing or versioning the cache when each knowledge base ingestion job completes, triggered through "
            "EventBridge.",
            "CloudFront caching of the POST /ask API responses, with a 24-hour TTL.",
        ],
        ans="AD",
        why="Questions with the same meaning in different words need a <b>semantic cache</b>, restricted to general "
            "content so personal answers never leak. Clearing it on each <b>KB sync</b> stops it from serving answers "
            "that no longer match the knowledge base.",
        wrong={
            "B": "Different wordings produce different hashes, so the hit rate would be close to zero.",
            "C": "Account-specific answers would be served to other customers, which is a data leak.",
            "E": "CloudFront doesn't cache POST requests by default, and cached personal answers would leak across "
                 "users.",
        }),
    dict(
        dom="4", skill="4.1.2", kind="single",
        stem=[
            "A team compares two options for answering support tickets.",
            "<b>Option 1:</b> always use Model A at $0.012 per request, with a 97% success rate. "
            "<b>Option 2:</b> use Model B at $0.002 per request (80% success); every request that B fails is "
            "escalated to Model A (97% success on escalated requests). Validation that detects a failure costs "
            "nothing extra.",
            "Which statement about cost per successful answer is correct?",
        ],
        opts=[
            "Option 1 is cheaper, at about $0.0124 per success compared with about $0.0150 for Option 2.",
            "Option 2 is cheaper, at about $0.0024 per success compared with about $0.0124 for Option 1.",
            "Option 2 is cheaper, at about $0.0044 per success compared with about $0.0124 for Option 1.",
            "The two options cost about the same per success, because Option 2's escalations cancel out its savings.",
        ],
        ans="C",
        why="Option 1: $0.012 ÷ 0.97 ≈ <b>$0.0124</b>. Option 2: each request costs $0.002 + 0.20 × $0.012 = "
            "$0.0044, and succeeds with probability 0.80 + 0.20 × 0.97 = 0.994, so ≈ <b>$0.0044</b> per success. "
            "The cascade is about 64% cheaper.",
        wrong={
            "A": "This overstates Option 2's cost, which isn't $0.0150 per success.",
            "B": "$0.0024 forgets B's own $0.002 cost and counts only the escalation part (0.20 × $0.012).",
            "D": "Only 20% of requests escalate, so the savings clearly outweigh the escalation cost.",
        }),
    dict(
        dom="4", skill="4.2.1", kind="two",
        stem=[
            "Profiling a research assistant shows a time to first token of about 0.6 seconds, but a total generation "
            "time of about 14 seconds for an average of 1,100 output tokens. Usage analytics show that most users "
            "read only the first paragraph. The product target is for answers to <i>feel</i> instant and finish in "
            "under 5 seconds for typical questions.",
            "Which TWO changes should the team make first? (Select TWO.)",
        ],
        opts=[
            "Increase the number of retrieved knowledge base chunks so that the model needs fewer reasoning steps.",
            "Set a lower maxTokens and instruct the model to give a concise answer of about 150 words, with details "
            "on request.",
            "Purchase Provisioned Throughput, which makes each output token generate faster for the application.",
            "Stream the response so that the first words appear within a second while the rest is still generating.",
            "Switch to a larger embedding model so that retrieval returns more precise context.",
        ],
        ans="BD",
        why="Time is spent <b>generating many output tokens</b>, so <b>limit the output length</b> first, and "
            "<b>stream</b> so the answer feels instant. Together they meet both targets.",
        wrong={
            "A": "More chunks means more input tokens and slower prefill; it doesn't shorten the output.",
            "C": "Provisioned Throughput guarantees capacity; it isn't a way to make a 1,100-token answer fast.",
            "E": "Retrieval isn't the bottleneck (time to first token is already 0.6 s).",
        }),
    dict(
        dom="4", skill="4.1.1", kind="single",
        stem=[
            "A coaching chatbot's cost per conversation keeps rising: long conversations reach 80 turns, and every "
            "request sends the full history. The product team says the assistant must remember goals and decisions "
            "from early in the conversation, but the exact wording of old small talk doesn't matter.",
            "Which change reduces cost while keeping the important context?",
        ],
        opts=[
            "Switch to a model with a larger context window so that the complete history always fits in each "
            "request.",
            "Keep the most recent turns verbatim, and replace older turns with a running summary of goals and "
            "decisions that is updated as the conversation grows.",
            "Increase maxTokens so that the model can produce a complete recap of the conversation in every response.",
            "Move all conversations to batch inference, because batch requests cost about half as much as on-demand.",
        ],
        ans="B",
        why="<b>Context pruning with a rolling summary</b> cuts input tokens sharply while keeping the facts that "
            "matter (goals, decisions) and the recent turns verbatim.",
        wrong={
            "A": "A bigger window lets the cost keep growing instead of reducing it.",
            "C": "This adds output tokens, which makes it more expensive.",
            "D": "Batch inference doesn't work for interactive chat turns.",
        }),
    dict(
        dom="4", skill="4.3.2", kind="two",
        stem=[
            "A public GenAI endpoint's OutputTokenCount follows a strong daily pattern. Last weekend a scraper hammered "
            "the endpoint at 3 AM and burned a week's budget before anyone noticed. A static alarm threshold would "
            "either miss night-time spikes or fire every afternoon. The team wants detection that adapts to the "
            "daily pattern, and an automatic limit on abusive callers.",
            "Which TWO actions should the team take? (Select TWO.)",
        ],
        opts=[
            "A CloudWatch anomaly detection alarm on OutputTokenCount for the model, using the learned daily band.",
            "An AWS Budgets budget with a fixed monthly amount and an email alert at 80% of the amount.",
            "A static CloudWatch alarm set at the 99th percentile of the previous month's OutputTokenCount values.",
            "An AWS WAF rate-based rule on the API, plus API Gateway throttling, to limit requests from each "
            "source automatically.",
            "A service quota increase so that the scraper's traffic no longer causes throttling for real users.",
        ],
        ans="AD",
        why="<b>Anomaly detection</b> learns the daily pattern and alerts on unusual deviations. A <b>WAF rate-based "
            "rule</b> together with API Gateway throttling automatically limits abusive callers.",
        wrong={
            "B": "A fixed monthly budget notices too late and doesn't follow the daily pattern.",
            "C": "This is exactly the static threshold the stem says doesn't work.",
            "E": "This feeds the abuse: more capacity means more cost.",
        }),
    dict(
        dom="4", skill="4.3.5", kind="single",
        stem=[
            "A SaaS company's knowledge base uses OpenSearch Serverless and now holds about 50 million vectors for 3,000 "
            "tenant companies. Query latency has risen steadily as the index has grown. Every query belongs to "
            "exactly one tenant, and every chunk already carries a tenant_id metadata attribute. The team wants the "
            "most effective first fix without re-architecting.",
            "What should the team do?",
        ],
        opts=[
            "Switch to an embedding model with more dimensions, so that each comparison distinguishes chunks more "
            "precisely.",
            "Increase the number of results requested from 5 to 25, so that relevant chunks are found in fewer "
            "searches.",
            "Apply a tenant_id metadata filter on every retrieval call, so that each search covers only that tenant's "
            "vectors.",
            "Replace approximate nearest-neighbour (HNSW) search with exact k-NN search to avoid approximation overhead.",
        ],
        ans="C",
        why="<b>Metadata filtering</b> on tenant_id reduces each search to one tenant's small slice of the index. "
            "That improves latency, and it also enforces tenant isolation.",
        wrong={
            "A": "More dimensions make each comparison more expensive, so latency gets worse.",
            "B": "More results means more work and larger payloads, not less.",
            "D": "Exact k-NN over 50 million vectors is much slower. Approximate search exists precisely for scale.",
        }),
    dict(
        dom="4", skill="4.3.4", kind="all",
        stem=[
            "A customer-service agent's monthly cost has doubled, yet answer quality is unchanged. The traces show "
            "the agent calling the search_orders tool again and again with identical arguments when an order isn't "
            "found, sometimes 30 times in one session.",
            "Which actions should the team take? (Select ALL that apply.)",
        ],
        opts=[
            "Track tool calls per session against a usage baseline, with an anomaly alarm when a session exceeds the "
            "normal pattern.",
            "Enforce a per-session limit on tool calls and iterations, ending gracefully with a helpful message when "
            "the limit is reached.",
            "Raise the model's temperature so that it tries different tools instead of repeating the same one.",
            "Make search_orders return a clear 'order not found' result with guidance, and improve the tool's "
            "description about what to do when nothing is found.",
            "Cache identical read-only tool calls within a session, so that repeated identical calls don't hit the "
            "backend.",
            "Turn off tracing to reduce observability costs, which are part of the doubled bill.",
        ],
        ans="ABDE",
        why="Use <b>baselines and alarms</b> to detect the pattern, a <b>stopping condition</b> to cap the damage, "
            "<b>clear tool results and descriptions</b> to fix why the model retries, and a <b>per-session cache</b> "
            "for idempotent reads to cut the remaining cost.",
        wrong={
            "C": "Randomness doesn't fix a missing 'not found' signal, and it makes behaviour less predictable.",
            "F": "Tracing is how this problem was found; removing it hides problems, and it isn't the cost driver.",
        }),
    dict(
        dom="5", skill="5.1.6", kind="single",
        stem=[
            "A team has tuned retrieval and now wants to measure the <b>complete</b> RAG answers from its Bedrock "
            "knowledge base: whether every claim is supported by the retrieved passages (faithfulness), and whether "
            "the cited passages actually support what is cited. It wants a managed capability that works on its own "
            "question set, with minimal custom code.",
            "What should the team use?",
        ],
        opts=[
            "A knowledge base evaluation job in retrieve-only mode, measuring context relevance and context coverage.",
            "A Bedrock model evaluation job with automatic metrics for toxicity and robustness on built-in datasets.",
            "A guardrail contextual grounding check applied at runtime to every production response.",
            "A knowledge base evaluation job in retrieve-and-generate mode, with faithfulness and citation metrics, on "
            "its own prompt dataset.",
        ],
        ans="D",
        why="<b>Retrieve-and-generate</b> RAG evaluation scores whole answers for <b>faithfulness</b>, correctness, "
            "completeness and <b>citation precision and coverage</b> (using an LLM judge) on your own dataset.",
        wrong={
            "A": "Retrieve-only mode evaluates the chunks, not the generated answer or its citations.",
            "B": "Toxicity and robustness on built-in data don't measure RAG faithfulness on your questions.",
            "C": "A runtime filter blocks individual responses; it isn't an evaluation that produces quality "
                 "metrics.",
        }),
    dict(
        dom="5", skill="5.1.2", kind="two",
        stem=[
            "A company plans to upgrade its assistant from model v1 to v2. Step 1: before any customer sees v2, "
            "compare v2's outputs with v1's on 100% of real production traffic. Step 2: once v2 passes, measure the "
            "business impact (resolution rate and CSAT) of v2 against v1 on separate groups of real users over two "
            "weeks.",
            "Which TWO approaches match the two steps? (Select TWO.)",
        ],
        opts=[
            "Shadow testing: send copies of live requests to v2 without returning its responses, and compare them "
            "with v1.",
            "A canary release that sends 5% of users to v2, rolling back automatically if error alarms fire.",
            "A blue/green switch that moves 100% of traffic to v2 at night, with the option to switch back.",
            "An A/B test that randomly splits users between v1 and v2 for two weeks, comparing resolution rate and "
            "CSAT.",
            "An offline evaluation job on a curated dataset, with no production traffic involved.",
        ],
        ans="AD",
        why="'All real traffic, no customer sees v2' is <b>shadow testing</b>. 'Business impact on separate user "
            "groups' is an <b>A/B test</b>.",
        wrong={
            "B": "In a canary, real users see v2. It's a safety rollout, not a comparison of business impact.",
            "C": "Everyone sees v2, and there's no comparison group.",
            "E": "Offline evaluation doesn't use real production traffic, so it fails step 1.",
        }),
    dict(
        dom="5", skill="5.1.5", kind="three",
        stem=[
            "A wealth-management firm wants its advice assistant evaluated from several perspectives: scoring that "
            "scales to every response, detection of subtle tone and suitability problems that automated scoring "
            "misses, and learning from what customers actually experience. Evaluation cost must stay reasonable.",
            "Which THREE practices should the firm adopt? (Select THREE.)",
        ],
        opts=[
            "LLM-as-a-judge scoring of every response for faithfulness and helpfulness, using a different, strong "
            "judge model calibrated against human labels.",
            "Using the production model to judge its own outputs, which keeps evaluation consistent with how it "
            "reasons.",
            "Expert annotation of a weekly sample, weighted toward low-rated responses, using SageMaker Ground Truth "
            "or Amazon A2I.",
            "BLEU scores against a single reference answer as the primary quality metric for every advice response.",
            "Thumbs-up/down and comment feedback linked to response IDs, analysed regularly to find failure "
            "categories.",
            "Replacing all human review with the judge model once its agreement with humans is above 80%.",
        ],
        ans="ACE",
        why="Scale comes from a <b>calibrated, independent LLM judge</b>. Subtle suitability and tone problems need "
            "<b>expert human review on a targeted sample</b>. The customer perspective comes from <b>user "
            "feedback</b> linked to responses. Together they're multi-perspective at a reasonable cost.",
        wrong={
            "B": "Self-judging tends to rate the model's own style highly and misses its own blind spots.",
            "D": "Word overlap with one reference penalises correct paraphrases and says nothing about suitability.",
            "F": "80% agreement still misses the subtle cases. Some expert review must remain.",
        }),
    dict(
        dom="5", skill="5.2.4", kind="two",
        stem=[
            "A product-support RAG assistant gives wrong answers about specification tables. Calling Retrieve alone "
            "shows two things: (1) for many questions, the correct chunk is returned but ranked 7th–9th while top-k "
            "is 5; (2) large specification tables are split across chunks, so the chunks containing the values have "
            "lost their column headers.",
            "Which TWO fixes address these root causes? (Select TWO.)",
        ],
        opts=[
            "Retrieve a larger candidate set (for example 20) and apply a reranker model, passing the top 5 to the "
            "generator.",
            "Lower the generation model's temperature so that it reads the retrieved values more carefully.",
            "Use foundation-model parsing (or Bedrock Data Automation) on ingestion so that tables are kept whole, "
            "with their headers.",
            "Fine-tune the generation model on product manuals so that it already knows the specification values.",
            "Raise maxTokens so that the model has enough room to explain the table values in full.",
        ],
        ans="AC",
        why="Ranking problem → <b>reranker</b> over a larger candidate set. Parsing and chunking problem → "
            "<b>FM parsing / BDA</b> to keep tables intact with their headers. Both fix retrieval, which is where "
            "the diagnosis points.",
        wrong={
            "B": "Generation settings can't fix chunks that are missing or out of order.",
            "D": "Fine-tuning for facts is unreliable, has to be redone when specifications change, and ignores the "
                 "retrieval cause.",
            "E": "Answer length isn't the issue; the right data isn't reaching the model.",
        }),
    dict(
        dom="5", skill="5.2.5", kind="single",
        stem=[
            "A team moved its product Q&amp;A template into Prompt Management (version 4) with a "
            "{{product_name}} variable. Since then, about 15% of answers say 'I need more information about which "
            "product you mean.' Every affected request comes from the partner API client; the web and mobile clients "
            "are fine. Latency and error rates haven't changed.",
            "What should the developer do FIRST?",
        ],
        opts=[
            "Enable AWS X-Ray on the partner API path and compare segment timings with the web and mobile clients.",
            "Publish version 5 with stronger instructions and more few-shot examples about identifying the product.",
            "Raise the temperature for partner requests so that the model is more willing to infer which product is "
            "meant.",
            "Use CloudWatch Logs Insights on the model invocation logs for partner requests to inspect the fully "
            "rendered prompts.",
        ],
        ans="D",
        why="Wrong <b>behaviour</b> limited to one client, with normal latency, points to a bad <b>input</b>, most "
            "likely an empty or unsent product_name variable. Inspecting the <b>rendered prompt</b> in the invocation "
            "logs confirms it.",
        wrong={
            "A": "Nothing is slow or failing, so a timing trace won't show the missing variable.",
            "B": "This is a blind change that doesn't address a missing input and adds risk.",
            "C": "This encourages guessing the product, which creates wrong answers.",
        }),
    dict(
        dom="5", skill="5.2.2", kind="all",
        stem=[
            "A platform team is writing a standard error-handling policy for every application that calls Amazon "
            "Bedrock.",
            "Which rules belong in the policy? (Select ALL that apply.)",
        ],
        opts=[
            "ThrottlingException: retry with exponential backoff and jitter, with a capped number of attempts.",
            "ValidationException 'input is too long': trim or summarise context before trying again; never resend "
            "the same request unchanged.",
            "stopReason max_tokens: resend the identical request until the model returns end_turn.",
            "AccessDeniedException right after switching models: check that model access is enabled and that IAM "
            "allows that model; don't retry.",
            "ModelTimeoutException or ServiceUnavailableException: retry with backoff, then fall back to an "
            "alternative model or a graceful message.",
            "ResourceNotFoundException: retry in a loop, because the model may take a few minutes to appear.",
        ],
        ans="ABDE",
        why="<b>Retry transient errors</b> (throttling, timeouts, service unavailable) with backoff and a fallback. "
            "<b>Fix permanent errors</b> (validation, access, wrong ID or Region) instead of retrying them.",
        wrong={
            "C": "max_tokens means the output limit was reached. Resending the same request gives the same truncation; "
                 "raise maxTokens or ask for a shorter answer.",
            "F": "ResourceNotFound means a wrong model ID or Region (or a missing inference profile). Retrying never "
                 "fixes it.",
        }),
    dict(
        dom="5", skill="5.1.9", kind="two",
        stem=[
            "A company releases model and prompt updates at 2 AM, when almost no users are active. Two recent "
            "releases caused problems that were only noticed hours later: first, a multi-turn order-tracking "
            "conversation broke at turn 3; second, answers to standard policy questions subtly changed meaning "
            "after a model upgrade, although they still looked fluent.",
            "Which TWO mechanisms detect these problems right after a release? (Select TWO.)",
        ],
        opts=[
            "CloudWatch Synthetics canaries that run a scripted multi-turn order-tracking conversation against the "
            "endpoint every few minutes.",
            "A CloudWatch alarm on the Lambda function's CPU utilisation, which is set to fire if processing patterns "
            "change after a release.",
            "A semantic-drift check that embeds answers to a fixed set of policy questions and compares them with a "
            "pre-release baseline.",
            "AWS CloudTrail trails that record every API call made by the release pipeline during the release window.",
            "A rule that waits for the customer-complaint rate to rise above its normal level before investigating.",
        ],
        ans="AC",
        why="<b>Synthetic workflows</b> exercise real user journeys even when no users are active. A <b>semantic "
            "drift</b> check catches meaning changes in fluent-looking answers by comparing them with the baseline.",
        wrong={
            "B": "CPU says nothing about whether conversations work or what answers mean.",
            "D": "CloudTrail records who called which API, not whether the application behaves correctly.",
            "E": "Waiting for complaints is the hours-later detection that caused the problem.",
        }),
]
