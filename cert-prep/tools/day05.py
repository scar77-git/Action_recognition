"""Day 5 note: Models and Inference (new teaching style: explanations, examples, diagrams, glossary)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import Note  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Day_5_2026-10-25_Models_and_Inference.pdf")

n = Note(OUT, "Day 5 — Models and Inference",
         "Sunday 25 Oct 2026 &nbsp;·&nbsp; AWS AIP-C01 exam tasks: <b>1.2 Select and configure models · "
         "2.4 Call model APIs · 2.2 Deploy models</b> &nbsp;·&nbsp; Exam: Mon 9 Nov, 1:30 PM IST")

n.callout("Today in one paragraph",
          "Choose the <b>smallest model that is good enough</b> (prove it with a model evaluation), configure how it "
          "writes with inference parameters, call it through the <b>Converse API</b> (streaming for responsiveness, "
          "an SQS queue for long or bursty work, retries with backoff for throttling, cross-region inference for "
          "extra capacity), and pay for it the right way: <b>on-demand</b> by default, <b>Provisioned Throughput</b> "
          "for steady guaranteed capacity, <b>batch</b> for large non-urgent jobs. Customise only when prompting "
          "and RAG are not enough.", "ok")

# =============================================================== PART 1
n.h1("Part 1 — Choosing and configuring a foundation model (Task 1.2)")
n.h2("1.1 Why model choice is a real decision")
n.p("A <b>foundation model (FM)</b> is a large, general-purpose AI model trained on huge amounts of data, which you use "
    "without training it yourself. Amazon Bedrock offers many through one API: Amazon Nova, Anthropic Claude, Meta Llama, "
    "Mistral, Cohere and others. There is no single best model — every model trades off three things:")
n.code("                 QUALITY  (reasoning, instruction following)\n"
       "                    /\\\n"
       "                   /  \\        <- you pick a point in this triangle\n"
       "                  /____\\\n"
       "             COST        SPEED\n"
       "     (price per token)   (latency)")
n.p("Larger models are usually smarter but slower and pricier; smaller models are fast and cheap but weaker on hard "
    "reasoning. <b>Example:</b> classifying 5 million product reviews (simple task, huge volume) → a small, cheap model; "
    "drafting legal responses (costly mistakes, low volume) → a large, capable model.")
n.callout("Exam phrasing", "'The MOST cost-effective model that meets the quality requirement' → the <b>smallest model "
          "that is good enough</b>, never automatically the most powerful one.")

n.h2("1.2 Selection criteria")
n.numbered([
    "<b>Task quality</b> — can it actually do the job (reasoning, summarising, coding, classifying)?",
    "<b>Modality</b> — the type of data handled: text-only (Nova Micro); <b>multimodal</b> input such as images, "
    "documents, video (Nova Lite, Nova Pro, Claude); image generation (Nova Canvas); video generation (Nova Reel); "
    "<b>embeddings</b> for search (Titan Text Embeddings V2, Cohere Embed). Example: photos of damaged parcels → "
    "multimodal model.",
    "<b>Context window</b> — maximum tokens per request (a token is roughly ¾ of a word). A 300-page contract in one "
    "pass needs a large window.",
    "<b>Latency</b> — live chat needs fast responses; an overnight report doesn't.",
    "<b>Cost</b> — charged per input and output token; output tokens usually cost more.",
    "<b>Features</b> — tool use, streaming, vision, customisation support.",
    "<b>Language support</b> — e.g. Hindi or Japanese performance.",
    "<b>Region availability / data residency</b> — the model must exist where your data may live (Day 4).",
])

n.h2("1.3 Choose with evidence: Amazon Bedrock model evaluation")
n.p("Run your own prompt dataset through several candidate models and score them:")
n.code(" your 200 real prompts --> Model A --> answers --+\n"
       "                      --> Model B --> answers --+--> scores + cost/latency --> pick the winner\n"
       "                      --> Model C --> answers --+")
n.table(["Evaluation type", "How it scores", "Use when"], [
    ["Automatic", "Built-in metrics (accuracy, robustness) against reference answers", "You have correct answers to compare against"],
    ["LLM-as-a-judge", "A strong model grades each answer (helpfulness, correctness…)", "Open-ended answers, no single right answer"],
    ["Human", "Your own reviewers rate outputs", "Subjective quality (brand tone) or high stakes"],
], [0.2, 0.45, 0.35])

n.h2("1.4 Inference parameters — how the model writes")
n.p("<b>Inference</b> means running a model to get output. A model writes <b>one token at a time</b>: at each step it "
    "computes a probability for every possible next token, then picks one. Parameters change how that pick is made.")
n.code('Prompt: "The weather today is ..."\n'
       "next-token probabilities:  sunny 50% | cloudy 25% | rainy 15% | purple 0.1% | ...")
n.bullets([
    "<b>Temperature</b> (usually 0–1) — randomness of the pick. Low → consistent, predictable (invoice-number "
    "extraction: 0). High → varied, creative, more error-prone (five slogan ideas: ~0.8).",
    "<b>Top-p (nucleus sampling)</b> — consider only the smallest set of top tokens whose probabilities <b>add up to "
    "p</b>. It is a probability threshold, so the number of candidate tokens changes every step "
    "(p = 0.9: sunny+cloudy+rainy = 90% → 3 candidates; next step 'Paris' 95% → 1 candidate).",
    "<b>Top-k</b> — consider only the <b>k</b> most likely tokens (a fixed count). Not every model supports it.",
    "<b>Max tokens</b> — maximum answer length. When reached, generation stops there and the stop reason is "
    "<b>max_tokens</b> (answers cut off mid-sentence → raise it).",
    "<b>Stop sequences</b> — strings that end generation when produced (e.g. a blank line).",
    "<b>System prompt</b> — the model's role and rules.",
])
n.table(["Symptom or goal", "Adjust"], [
    ["Answers vary every time but must be consistent", "Lower temperature (and/or top-p)"],
    ["Creative output too repetitive", "Raise temperature"],
    ["Answers cut off mid-sentence (stop reason max_tokens)", "Raise max tokens"],
    ["Model keeps writing past what you need", "Stop sequence or lower max tokens"],
    ["Costs high because answers are long", "Lower max tokens; ask for concise answers"],
], [0.55, 0.45])

n.h2("1.5 Your question: why isn't hallucination a temperature problem?")
n.p("High temperature <i>does</i> raise the risk of made-up content, but it is not the root cause. Hallucinations have "
    "two causes:")
n.p("<b>Cause 1 — the model doesn't know the fact</b> (main cause). Its <i>most likely</i> answer is already wrong:")
n.code('Question: "What is AcmeShop\'s refund window?"   (real answer: 14 days; model never saw the policy)\n'
       '   "30" 60%  <- most common refund window on the internet\n'
       '   "14" 10%   "7" 8%   ...\n'
       "Temperature 0 -> always \"30\": wrong, every time, confidently\n"
       "Temperature 1 -> sometimes 30, 7 or 14: wrong in different ways")
n.p("<b>Cause 2 — randomness</b> (secondary). The model knows the answer but high temperature picks an unlikely wrong "
    "token; lowering temperature fixes this case.")
n.p("<b>Grounding</b> (RAG plus the Guardrails contextual grounding check) puts the facts in the prompt, which changes "
    "the probabilities themselves:")
n.code('Prompt contains: "AcmeShop policy: refunds accepted within 14 days of delivery."\n'
       '   "14" 97%   "30" 1%   <- the correct token is now the most likely')
n.table(["Scenario wording", "Real cause", "Fix"], [
    ["States facts not in our documents", "Missing knowledge", "Grounding (RAG + contextual grounding check)"],
    ["Different answer each time for the same question", "Randomness", "Lower temperature / top-p"],
    ["Both made-up and inconsistent", "Both", "Grounding + low temperature"],
], [0.4, 0.22, 0.38])
n.callout("One-line rule", "Temperature controls <b>consistency</b>; grounding controls <b>correctness</b>.")

# =============================================================== PART 2
n.h1("Part 2 — How your application calls the model (Task 2.4)")
n.h2("2.1 InvokeModel vs Converse")
n.p("<b>InvokeModel</b> is the older, model-specific operation: the JSON body must match each provider's own format, so "
    "switching models means rewriting request and response handling. <b>Converse</b> is the unified operation: one "
    "format for messages, system prompt, inference settings (<b>inferenceConfig</b>) and tools (<b>toolConfig</b>) "
    "across supported models — switching models changes only the model ID.")
n.code('brt.converse(modelId="amazon.nova-lite-v1:0", messages=[...], inferenceConfig={"maxTokens": 500, "temperature": 0})\n'
       'brt.converse(modelId="<a Claude model ID>",    messages=[...], inferenceConfig={"maxTokens": 500, "temperature": 0})\n'
       "#            ^ only this changes")
n.p("<b>Example:</b> Model B turns out 40% cheaper with equal quality — with Converse the switch is one line.")

n.h2("2.2 Streaming")
n.p("Without streaming the app waits for the whole answer; with <b>ConverseStream</b> (or "
    "InvokeModelWithResponseStream) tokens arrive as they are generated.")
n.code("WITHOUT streaming: [........ 15 s waiting ........] -> full answer appears\n"
       "WITH streaming:    [0.4 s] The -> refund -> policy -> allows -> ...\n"
       "                    ^ time to first token (TTFT): what the user feels")
n.p("Streaming improves <b>perceived latency</b> only. It doesn't finish the full answer sooner and doesn't reduce "
    "cost — same tokens, same price.")

n.h2("2.3 Synchronous vs asynchronous")
n.p("A synchronous call waits for the answer in the same request. Every link has a timeout: <b>Amazon API Gateway</b> "
    "(managed front door for HTTP APIs) defaults to <b>29 seconds</b>; <b>AWS Lambda</b> runs at most <b>15 minutes</b>. "
    "A 2-minute report through a default synchronous API fails. Fix: accept now, deliver later.")
n.code(" 1. Browser -> API Gateway -> Lambda: enqueue job -> returns \"Job 123 accepted\"\n"
       "                                   |\n"
       "                            Amazon SQS queue   (SQS = Simple Queue Service)\n"
       " 2.                         Worker Lambda -> Bedrock (2 minutes, no rush)\n"
       " 3.                         result saved in DynamoDB / S3\n"
       " 4. Browser polls \"is job 123 done?\"  or is notified (WebSocket / SNS)")
n.bullets([
    "The queue also <b>absorbs traffic spikes</b> and allows retries; messages that keep failing go to a "
    "<b>dead-letter queue (DLQ)</b> so nothing is silently lost.",
    "Bedrock's native async call <b>StartAsyncInvoke</b> handles slow generation types such as <b>Nova Reel video</b>; "
    "results are written to S3.",
])

n.h2("2.4 Quotas, throttling and retries")
n.p("Each account has per-model, per-Region quotas: <b>TPM</b> (tokens per minute) and <b>RPM</b> (requests per "
    "minute). Exceeding them returns <b>ThrottlingException</b> (HTTP 429). Retry with <b>exponential backoff</b> "
    "(wait 1 s, 2 s, 4 s…) plus <b>jitter</b> (a little randomness so clients don't retry in sync). The AWS SDKs "
    "(e.g. boto3) do this already; you configure them.")
n.code("Attempt 1 x (throttled) -> wait ~1s -> Attempt 2 x -> wait ~2s -> Attempt 3 x -> wait ~4s -> Attempt 4 OK")
n.table(["Error", "Meaning", "Retry?"], [
    ["ThrottlingException", "Over quota right now", "Yes, with backoff"],
    ["ServiceUnavailableException / ModelNotReadyException", "Temporary service-side issue", "Yes, with backoff"],
    ["ModelTimeoutException", "Model took too long", "Sometimes; consider shorter tasks or async"],
    ["ValidationException", "Request invalid (e.g. input exceeds context window)", "<b>No</b> — fix the request"],
    ["AccessDeniedException", "IAM permissions missing", "<b>No</b> — fix permissions"],
], [0.38, 0.37, 0.25])
n.p("For an input that is too long: reduce it — send only relevant chunks with <b>RAG</b>, chunk or summarise, or use "
    "a model with a larger context window.")
n.p("<b>Example — Black Friday 10x traffic</b>, cheapest fixes first: retries with backoff → cross-region inference → "
    "an SQS buffer (if slight delay is fine) → quota increase or Provisioned Throughput.")

n.h2("2.5 Cross-region inference")
n.p("You call an <b>inference profile</b> instead of a single-Region model; Bedrock routes each request to a Region in "
    "that group with spare capacity.")
n.code(' Your app (us-east-1) -- modelId = "us.amazon.nova-lite-v1:0" --> Bedrock router\n'
       "                                                                 |-> us-east-1\n"
       "                                                                 |-> us-east-2  (whichever has capacity)\n"
       "                                                                 |-> us-west-2")
n.bullets([
    "Prefixes: <b>us.</b>, <b>eu.</b>, <b>apac.</b>, or <b>global.</b> (worldwide).",
    "More throughput, fewer throttles, <b>no extra charge</b>, only the model ID changes.",
    "Data residency: a <b>geographic</b> profile (eu.) keeps processing in that geography; avoid <b>global.</b> when "
    "data must stay in, say, the EU.",
    "<b>Application inference profiles</b>: your own tagged profiles to <b>track cost and usage per team</b>.",
])
n.table(["", "Cross-region inference", "Quota increase"], [
    ["Capacity from", "Other Regions in the geography", "More capacity in your one Region"],
    ["Effort", "Change model ID — instant, no approval", "Service Quotas / Support request — needs approval"],
    ["Cost", "No extra charge", "No extra charge (pay for tokens used)"],
], [0.2, 0.4, 0.4])

# =============================================================== PART 3
n.h1("Part 3 — Deployment and paying for models (Task 2.2)")
n.code("                 +------------------- Amazon Bedrock ------------------+   +-- Amazon SageMaker AI --+\n"
       " real-time, pay  | 1. On-demand            (shared capacity)           |   | 4. Your own endpoint    |\n"
       " per token       | 2. Provisioned Throughput (reserved capacity)       |   |    (choose GPU, full    |\n"
       " not real-time,  | 3. Batch inference (file in -> file out, ~50% less) |   |    control, more work)  |\n"
       " cheapest        +-----------------------------------------------------+   +-------------------------+")
n.h2("3.1 On-demand")
n.p("Pay per input/output token, no commitment, shared capacity, limited by quotas. Default for most apps and "
    "unpredictable traffic. Example: an internal HR chatbot used a few hundred times a day.")
n.h2("3.2 Provisioned Throughput")
n.p("Buy <b>model units (MUs)</b> — dedicated slices of capacity — billed <b>per hour whether used or not</b>, optionally "
    "with 1- or 6-month commitments. For steady, high, predictable volume where throttling is unacceptable (e.g. a "
    "fraud-explanation service at a constant 2,000 requests/minute). Wrong choice for low or spiky traffic: you pay for "
    "idle hours. Classic exam answer for <b>serving a fine-tuned Bedrock model</b> (AWS now also offers on-demand "
    "serving for some custom models).")
n.h2("3.3 Batch inference")
n.p("Put many prompts in a <b>JSONL</b> file (one JSON request per line) in S3, start a batch job, get results in S3, "
    "usually within hours, at <b>~50% of on-demand price</b>. For large non-urgent jobs (Practice Set Q22).")
n.code(" S3: input.jsonl (2M prompts) --> Bedrock batch job --> (hours later) S3: output.jsonl")
n.table(["", "Batch inference", "Async SQS pattern"], [
    ["What", "Managed Bedrock job: one file in, one file out", "Your architecture: queue + worker + store"],
    ["Typical use", "Millions of prompts nobody is waiting for", "One user's long request, or buffering spikes"],
    ["Results", "Hours", "Seconds to minutes"],
    ["Price", "~50% cheaper", "Normal on-demand"],
], [0.18, 0.41, 0.41])

n.h2("3.4 Customisation ladder — cheapest that works")
n.code(" effort & cost\n"
       "     ^   5. Continued pre-training  (domain LANGUAGE from unlabeled text)\n"
       "     |   4. Fine-tuning             (TASK / STYLE from labeled examples)\n"
       "     |   3. Distillation            (SMALL model behaves like a BIG one)\n"
       "     |   2. RAG                     (the right FACTS at question time)   <- Day 1\n"
       "     |   1. Prompt engineering      (better instructions + examples)     <- Day 7\n"
       "     +------------------------------------------------------------------->")
n.bullets([
    "<b>Distillation</b>: a large <b>teacher</b> answers your prompts; those answers train a small <b>student</b>. "
    "Result: near-teacher quality for your use case at much lower cost/latency (support bot at 1M chats/month).",
    "<b>Fine-tuning</b>: hundreds–thousands of <b>labelled pairs</b> (prompt → ideal answer) change behaviour — "
    "format, tone, a specific task (strict JSON report format in brand voice).",
    "<b>Continued pre-training</b>: lots of <b>unlabelled domain text</b> teaches vocabulary (50,000 pharma research papers).",
    "Labelled pairs → fine-tuning; raw text → continued pre-training. Facts that change → RAG, not fine-tuning.",
    "Training data in S3; jobs can run in your VPC and be encrypted with your KMS key (Day 4).",
])
n.h2("3.5 Bringing your own model; SageMaker AI")
n.bullets([
    "<b>Custom Model Import</b>: import weights of an open-weight model you trained elsewhere (e.g. Llama fine-tuned "
    "in SageMaker) from S3 and call it through the same Bedrock APIs, serverlessly.",
    "<b>Bedrock Marketplace</b>: extra specialised models on managed endpoints, called via Bedrock APIs.",
    "<b>SageMaker AI endpoints</b> (incl. <b>JumpStart</b> catalogue): host any model on a GPU instance you choose; "
    "full control, more operations. Use only when Bedrock can't do it.",
])
n.h2("3.6 Which deployment option?")
n.table(["Scenario", "Choose"], [
    ["Typical app, unpredictable traffic, pay for use", "On-demand"],
    ["Steady high volume, guaranteed throughput", "Provisioned Throughput"],
    ["Serve a fine-tuned Bedrock model (classic answer)", "Provisioned Throughput"],
    ["Millions of prompts, no real-time need, lowest cost", "Batch inference"],
    ["Small fast model with big-model quality for one use case", "Model distillation"],
    ["Consistent format/style from labelled examples", "Fine-tuning"],
    ["Domain vocabulary from unlabelled documents", "Continued pre-training"],
    ["Up-to-date or private facts", "RAG"],
    ["Model trained elsewhere, serve via Bedrock serverlessly", "Custom Model Import"],
    ["Model not on Bedrock, specific GPU/container", "SageMaker AI endpoint"],
], [0.62, 0.38])

# =============================================================== rules
n.h1("Decision rules for Day 5")
n.numbered([
    "Most cost-effective → smallest model that's good enough, proven with <b>Bedrock model evaluation</b>.",
    "Image/video/document input → multimodal; search vectors → embedding model; long input → large context window.",
    "Consistency → low temperature; correctness → grounding; truncation (max_tokens) → raise max tokens.",
    "Switch/compare models with minimal code → <b>Converse API</b>.",
    "Feels slow → <b>streaming</b> (TTFT, not cost).",
    "Long generations time out → <b>SQS + worker + stored result</b>; video → <b>StartAsyncInvoke</b>.",
    "Throttling → backoff + jitter; ValidationException / AccessDenied → don't retry, fix.",
    "More throughput, no extra cost → <b>cross-region inference profile</b> (geographic for residency).",
    "Cost per team → <b>application inference profiles</b> with tags.",
    "Steady guaranteed capacity → <b>Provisioned Throughput</b>; low/spiky → on-demand.",
    "Huge non-urgent volume → <b>batch inference</b> (~50% cheaper).",
    "Labelled pairs → fine-tuning; raw text → continued pre-training; small-like-big → distillation; trained elsewhere → Custom Model Import.",
])

# =============================================================== part checks
n.h1("Your part checks — graded")
n.table(["Part", "Your answers", "Feedback"], [
    ["1", "Model choice depends on use case; temperature vs top-p; max_tokens meaning",
     "✓ / ½ / ½ — top-p is a <b>probability threshold</b>, not a count (that's top-k); at max_tokens the model "
     "<b>reaches</b> the limit and is stopped."],
    ["2", "Streaming vs cost; ValidationException; cross-region vs quota",
     "✓ ✓ ✓ — add RAG/summarising as fixes for too-long input; CRIS is instant with no approval."],
    ["3", "PT for spiky traffic; fine-tuning vs continued pre-training; batch vs SQS",
     "✓ ✓ ½ — the batch vs SQS difference is purpose, speed and price (table in 3.3)."],
], [0.07, 0.4, 0.53])

# =============================================================== lab
n.h1("Lab — console only, no model quota needed (status: to do later)")
n.table(["Part", "Steps", "Record (send to the professor)"], [
    ["A. Model catalogue (10 min)", "Bedrock → Model catalog; filter by provider and modality; open Nova Micro, Lite, Pro "
     "and note input modalities and context window.",
     "Pick a model for: (a) 5M short reviews, cheapest; (b) damage in parcel photos; (c) KB search vectors — with reasons."],
    ["B. Quotas (10 min)", "Service Quotas → Amazon Bedrock: on-demand TPM / RPM for Nova Lite, batch quotas, "
     "Provisioned Throughput model-unit quota. <b>Request a TPM increase</b> for Nova Lite or Micro.",
     "Current TPM / RPM; which quota relates to Provisioned Throughput."],
    ["C. Cross-region inference (10 min)", "Bedrock → Cross-region inference: open the Nova Lite us./global. profiles; "
     "create an application inference profile in CloudShell (commands below), list it, delete it.",
     "Regions in the us. profile; how a tagged profile splits costs by team."],
    ["D. Provisioned Throughput (5 min)", "Purchase form: model units, commitment options. <b>Do not buy — Cancel.</b>",
     "One scenario where it's right, one where it's wrong."],
    ["E. Batch inference (10 min)", "Batch inference → Create job: input S3, output S3, service role. <b>Don't submit.</b>",
     "Why every JSONL line has a recordId."],
    ["F. Customisation forms (10 min)", "Custom models → Customize model: fine-tuning, continued pre-training, distillation; "
     "hyperparameters (epochs, learning rate, batch size), S3 data, VPC, KMS. Imported models → Import model. Cancel both.",
     "Which form needs labelled pairs, which needs raw text."],
    ["G. Model evaluation (5 min)", "Evaluations → Create: automatic, LLM-as-a-judge, human. Cancel.",
     "Which type for 3 models × 200 open-ended support answers."],
], [0.18, 0.5, 0.32])
n.code('''aws bedrock create-inference-profile \\
  --inference-profile-name support-bot \\
  --model-source copyFrom=<the us. Nova Lite inference profile ARN> \\
  --tags key=team,value=support
aws bedrock list-inference-profiles --type-equals APPLICATION
aws bedrock delete-inference-profile --inference-profile-identifier <ARN from the create output>''')
n.p("Batch input format (one request per line; modelInput uses the model's request format):")
n.code('{"recordId": "REV0000001", "modelInput": {"messages": [{"role": "user", "content": [{"text": '
       '"Classify sentiment: \'Arrived broken, very disappointed.\'"}]}], "inferenceConfig": {"maxTokens": 10}}}\n'
       '{"recordId": "REV0000002", "modelInput": {"messages": [{"role": "user", "content": [{"text": '
       '"Classify sentiment: \'Fast delivery, love it!\'"}]}], "inferenceConfig": {"maxTokens": 10}}}')
n.callout("Cleanup", "Delete the application inference profile. Nothing else is created. Never press Purchase on "
          "Provisioned Throughput.")

# =============================================================== quiz
n.h1("Day 5 quiz — 8 / 8")
n.table(["#", "Scenario", "Answer", "Why"], [
    ["1", "4M reviews/month, weekly dashboard, small model is accurate enough, lowest cost", "B ✓",
     "Batch inference ~50% cheaper; no real-time need. PT would pay for idle hours; SQS uses on-demand prices."],
    ["2", "Different answers each time + quotes non-existent terms", "A, C ✓",
     "Lower temperature fixes inconsistency; grounding (KB + contextual grounding check) fixes made-up facts."],
    ["3", "5-page reports take 2 minutes and time out; users will wait", "C ✓",
     "Async SQS + worker + stored result. Streaming doesn't remove the gateway timeout for the total duration."],
    ["4", "Throttling at peaks; more throughput now, no cost, minimal change; data may be anywhere in US", "B ✓",
     "us. cross-region profile. global. could leave the US; PT costs money; moving Regions is a big change."],
    ["5", "ValidationException: input too long; retries keep failing", "C ✓",
     "Don't retry validation errors; reduce input (RAG, summarise)."],
    ["6", "Great large-model answers at 3M chats/month; want small model, minimal labelling", "B ✓",
     "Distillation: teacher generates the training data, no manual labelling."],
    ["7", "Llama fine-tuned in SageMaker; call via Bedrock APIs, no servers", "B ✓", "Custom Model Import from S3."],
    ["8", "Compare 3 providers, switch cheaply later, track cost per team", "A, C ✓",
     "Converse API (one-line switch) + application inference profiles tagged per team."],
], [0.04, 0.4, 0.1, 0.46])

n.h1("Mistakes and learnings")
n.table(["Point", "Correction"], [
    ["Top-p described as 'top p tokens'", "p is a cumulative probability threshold; a fixed count is top-k."],
    ["max_tokens 'generated more than the limit'", "It reaches the limit and is stopped there."],
    ["Batch vs SQS described as 'batches vs one at a time'", "Difference is purpose, result speed and price."],
    ["Hallucination vs temperature", "Temperature → consistency; grounding → correctness."],
], [0.38, 0.62])

n.h1("Glossary — new terms today")
n.table(["Term", "Meaning"], [
    ["Foundation model (FM)", "Large pre-trained general-purpose model you build on without training it yourself."],
    ["Modality / multimodal", "Type of data a model handles; multimodal models accept e.g. text and images."],
    ["Context window", "Maximum tokens a model can consider in one request."],
    ["Inference", "Running a model to get an output."],
    ["Temperature", "Randomness of token choice: low = consistent, high = creative."],
    ["Top-p (nucleus sampling)", "Sample only from top tokens whose probabilities add up to p."],
    ["Top-k", "Sample only from the k most likely tokens."],
    ["Max tokens / stop reason max_tokens", "Answer length limit; stop reason shown when the limit is reached."],
    ["Stop sequence", "String that ends generation when produced."],
    ["Bedrock model evaluation", "Managed comparison of models on your dataset (automatic, LLM-as-a-judge, human)."],
    ["InvokeModel", "Model-specific Bedrock call; request format differs per provider."],
    ["Converse / ConverseStream", "Unified Bedrock call format across models; streaming variant."],
    ["inferenceConfig / toolConfig", "Converse fields for inference parameters / tool definitions."],
    ["Streaming / TTFT", "Sending tokens as generated; time to first token = perceived latency."],
    ["Synchronous / asynchronous", "Caller waits for result / result delivered later."],
    ["API Gateway timeout", "Default 29-second integration timeout for synchronous APIs."],
    ["SQS / DLQ", "Simple Queue Service; dead-letter queue for messages that keep failing."],
    ["StartAsyncInvoke", "Bedrock native async call for slow generation (e.g. Nova Reel video) → S3."],
    ["TPM / RPM", "Tokens / requests per minute quotas."],
    ["ThrottlingException (HTTP 429)", "Over quota; retry with backoff."],
    ["Exponential backoff + jitter", "Retries with growing, slightly randomised waits."],
    ["ValidationException", "Invalid request (e.g. input too long); don't retry, fix it."],
    ["Cross-region inference / inference profile", "Routing requests across Regions in a geography via a profile ID (us., eu., apac., global.)."],
    ["Application inference profile", "Your own tagged profile to track cost/usage per team."],
    ["On-demand", "Pay per token, shared capacity, no commitment."],
    ["Provisioned Throughput / model unit (MU)", "Reserved dedicated capacity billed hourly; MU = unit of capacity."],
    ["Batch inference / JSONL", "File-based bulk job (~50% cheaper); JSON Lines = one JSON object per line."],
    ["Fine-tuning", "Further training on labelled prompt→answer pairs to change behaviour."],
    ["Continued pre-training", "Further training on unlabelled domain text to learn vocabulary."],
    ["Model distillation (teacher/student)", "Large model's answers train a smaller model."],
    ["Hyperparameters (epochs, learning rate, batch size)", "Training settings for customisation jobs."],
    ["Custom Model Import", "Bring open-weight model weights from S3 into Bedrock, served serverlessly."],
    ["Bedrock Marketplace", "Additional specialised models on managed endpoints via Bedrock APIs."],
    ["SageMaker AI / JumpStart", "AWS ML platform; JumpStart = its pre-trained model catalogue; host on chosen instances."],
], [0.38, 0.62])

n.callout("Next: Day 6 — Guardrails and Responsible AI (Tasks 3.1, 3.4)",
          "Content filters, denied topics, word filters, PII filters, contextual grounding, Automated Reasoning checks, "
          "prompt injection and jailbreaks, and responsible AI principles.")

n.build()
print(os.path.abspath(OUT))
