"""Full mock question bank, part 2 — rest of Domain 1 and start of Domain 2."""

QS = [
    dict(
        dom="1", skill="1.3.1", kind="single",
        stem=[
            "Before every Amazon Bedrock fine-tuning job, a data team assembles a training dataset of JSONL records in "
            "Amazon S3. These records are registered as a table in the AWS Glue Data Catalog. Past jobs wasted "
            "thousands of dollars because of records with empty completions, duplicate record IDs and prompts far "
            "longer than the model's limit. The team wants rule-based checks that run automatically in the existing "
            "Glue workflow, block the customisation job when the checks fail, and need no custom validation code.",
            "Which solution should the team implement?",
        ],
        opts=[
            "A SageMaker Data Wrangler data quality and insights report that a data scientist reviews before each "
            "fine-tuning job.",
            "An AWS Glue Data Quality ruleset (Completeness, Uniqueness, ColumnLength) evaluated in the Glue workflow, "
            "with a failure stopping the run and sending a notification.",
            "A Bedrock model evaluation job run on the training dataset to score its quality before customisation "
            "starts.",
            "An Amazon Macie discovery job on the bucket, with findings sent to EventBridge to cancel the "
            "customisation job.",
        ],
        ans="B",
        why="<b>Glue Data Quality</b> evaluates declarative DQDL rules (completeness, uniqueness, value length) inside "
            "Glue jobs and workflows. The results can gate the pipeline and raise alerts, with no custom code.",
        wrong={
            "A": "Data Wrangler is a visual, human-driven exploration tool. It doesn't block a pipeline automatically.",
            "C": "Model evaluation scores <i>model outputs</i>, not the structural quality of a training dataset.",
            "D": "Macie finds sensitive data such as PII. It doesn't check for empty, duplicate or over-length records.",
        }),
    dict(
        dom="1", skill="1.3.2", kind="two",
        stem=[
            "A contact centre records 40,000 customer calls a day. Leadership wants a knowledge base of resolved "
            "issues built from these calls. Card numbers and other personal data must be removed <b>before</b> any "
            "text is stored or embedded, and the transcripts must show which lines the agent said and which the "
            "customer said. The team wants managed services.",
            "Which TWO components should be part of the ingestion pipeline? (Select TWO.)",
        ],
        opts=[
            "Amazon Polly to convert each recording into text with speaker labels for the agent and the customer.",
            "Amazon Transcribe batch jobs with speaker diarization (or channel identification) and automatic PII "
            "redaction, writing to S3.",
            "A guardrail sensitive information filter applied to the assistant's answers as the only privacy control.",
            "Ingesting the raw audio files directly into the knowledge base's S3 data source, with a nightly sync.",
            "A Lambda step that calls Amazon Comprehend PII detection on each transcript and redacts any remaining "
            "entities before the KB sync.",
        ],
        ans="BE",
        why="<b>Transcribe</b> turns speech into text, labels the speakers, and redacts PII at transcription time. "
            "A <b>Comprehend</b> PII pass is a second redaction layer before ingestion, catching anything left over "
            "(defence in depth). Both act <b>before storage</b>, as the stem requires.",
        wrong={
            "A": "Polly does the opposite job: text-to-speech.",
            "C": "Output masking happens after the PII has already been stored and embedded, so it fails the "
                 "'before storage' rule.",
            "D": "Raw audio isn't redacted text, and personal data would be stored as-is.",
        }),
    dict(
        dom="1", skill="1.3.3", kind="single",
        stem=[
            "Once a month, a support organisation must summarise about 2 million closed tickets for a trend report. "
            "The report is due 24 hours after the month closes, and the CFO asks for the lowest possible cost. Each "
            "ticket is independent. The team will use one Amazon Bedrock text model.",
            "Which implementation meets these requirements?",
        ],
        opts=[
            "An SQS queue holding the ticket IDs, with Lambda workers calling InvokeModel on demand at the account's "
            "maximum concurrency.",
            "A StartAsyncInvoke call for each ticket, with outputs written to S3 and collected by a Lambda function.",
            "Provisioned Throughput for 24 hours, with a Step Functions Distributed Map state calling the model once "
            "per ticket.",
            "A JSONL input file in S3 (one record per ticket with recordId and modelInput), a batch inference job "
            "with a service role, and results written to S3.",
        ],
        ans="D",
        why="A large, non-interactive job with a 24-hour window fits <b>batch inference</b>: a JSONL file of records "
            "(recordId plus the model-specific modelInput), a service role with S3 access, and output to S3, at about "
            "50% of the on-demand price.",
        wrong={
            "A": "This pays on-demand prices for 2 million calls and risks throttling, so it isn't the lowest cost.",
            "B": "StartAsyncInvoke is native asynchronous invocation for slow generation such as video. It isn't a "
                 "discounted bulk path for 2 million text requests.",
            "C": "Provisioned Throughput is a capacity commitment priced for guaranteed throughput. It's not the "
                 "cheapest way to run a one-off bulk job.",
        }),
    dict(
        dom="1", skill="1.4.3", kind="single",
        stem=[
            "Employees ask an HR assistant (Bedrock knowledge base, RetrieveAndGenerate) compound questions such as: "
            "'Compare parental leave in India and the UK, and tell me which one needs manager approval.' The answers "
            "usually cover only India, because retrieval returns mostly India chunks. Single-topic questions work "
            "well. The team wants the smallest change that requires no new infrastructure.",
            "What should the team do?",
        ],
        opts=[
            "Enable query decomposition in the knowledge base's query transformation settings, so that each part is "
            "retrieved separately.",
            "Increase the number of retrieved results from 5 to 50, so that UK chunks are also likely to be included.",
            "Build a Step Functions workflow that classifies each question, splits it and runs a Map state of Retrieve "
            "calls.",
            "Switch to a larger embedding model, and re-ingest all policies so that each chunk carries richer meaning.",
        ],
        ans="A",
        why="The knowledge base's built-in <b>query decomposition</b> splits a complex question into sub-queries, "
            "retrieves for each, and combines the results. It's a configuration change with no new infrastructure.",
        wrong={
            "B": "One combined query still ranks India chunks highest. A much larger result set adds noise and cost "
                 "without guaranteeing the UK chunks.",
            "C": "This works, but it's new infrastructure and code. The built-in feature meets 'smallest change'.",
            "D": "Embedding quality isn't the problem; a single query for a multi-part question is. Re-ingesting is "
                 "costly and misses the cause.",
        }),
    dict(
        dom="1", skill="1.1.2", kind="two",
        stem=[
            "A retail bank wants to know within four weeks whether a GenAI assistant for branch staff is worth a full "
            "investment. The steering committee will decide based on three things: whether answers to real staff "
            "questions are accurate enough, what the solution would cost at the projected 1 million questions a "
            "month, and evidence that no customer data leaves the bank's approved Region.",
            "Which TWO actions should the proof of concept include? (Select TWO.)",
        ],
        opts=[
            "Agree measurable success criteria first, such as accuracy on 200 real staff questions, p95 latency and "
            "cost per answer.",
            "Buy one month of Provisioned Throughput so that latency is measured under guaranteed capacity.",
            "Use unmasked production customer records in the PoC so that accuracy results are fully realistic.",
            "Measure input and output tokens per request in the PoC, and project the cost at 1 million questions a "
            "month using on-demand prices.",
            "Build the complete multi-account landing zone and CI/CD pipeline first, so that the PoC can later be "
            "promoted unchanged.",
        ],
        ans="AD",
        why="A valid PoC defines <b>measurable criteria before building</b> and produces evidence for every decision "
            "factor. <b>Measured token usage × projected volume</b> answers the cost question. Region evidence comes "
            "from running in the approved Region with masked data, logging and endpoint configuration.",
        wrong={
            "B": "A capacity commitment before feasibility is proven: costly, and not a validation step.",
            "C": "This breaks data-protection rules and the committee's own residency and privacy concern. Use masked "
                 "or synthetic data.",
            "E": "Building production foundations is full-scale work, not a four-week feasibility test.",
        }),
    dict(
        dom="1", skill="1.1.3", kind="three",
        stem=[
            "A group with 30 product teams is adopting Amazon Bedrock. A Well-Architected review of five early "
            "workloads with the Generative AI Lens found the same high-risk issues in each: model invocation logging "
            "disabled, no guardrails, and KMS encryption missing on knowledge base data. The CTO wants every current "
            "and future team to implement fixes consistently, with minimal effort per team, automatic detection of "
            "teams that drift from the standard, and evidence of improvement over time.",
            "Which THREE actions meet these requirements? (Select THREE.)",
        ],
        opts=[
            "Publish a best-practices wiki based on the review, and ask each team lead to confirm compliance every "
            "quarter.",
            "Build a CDK construct library that provisions the knowledge base, guardrail, KMS keys and invocation "
            "logging by default, and publish it through AWS Service Catalog.",
            "Move all 30 teams into a single shared AWS account so that one administrator can configure everything "
            "centrally.",
            "Run Well-Architected Tool reviews with the Generative AI Lens on a schedule, saving milestones to track "
            "how the high-risk issues decline.",
            "Let each team design its own remediation, because each team knows its own application best.",
            "Deploy AWS Config rules across accounts that flag Bedrock workloads with logging disabled or knowledge "
            "base data unencrypted.",
        ],
        ans="BDF",
        why="<b>Reusable components</b> (a CDK library through Service Catalog) give consistent fixes with little "
            "effort per team. <b>Config rules</b> automatically detect drift. <b>WA Tool milestones</b> provide "
            "evidence of improvement over time. The lens finds the issues, the components fix them, and Config keeps "
            "them fixed.",
        wrong={
            "A": "A wiki and self-attestation are neither consistent nor automatic.",
            "C": "A single account breaks blast-radius and isolation best practice and doesn't scale to 30 teams.",
            "E": "Thirty different fixes is the opposite of consistent, and it's repeated effort.",
        }),
    dict(
        dom="1", skill="1.6.5", kind="single",
        stem=[
            "A claims system calls the Converse API with a model that supports tool use. A downstream Java service "
            "parses the reply into a ClaimDecision record (decision, reasonCode, payoutAmount). In about 3% of calls, "
            "the parser fails: the reply has an explanatory sentence before the JSON, uses a wrong field name, or puts "
            "a string where a number is expected. The architect wants the most reliable mechanism, plus a safety net "
            "for anything that still slips through.",
            "What should the developer implement?",
        ],
        opts=[
            "Set a stop sequence of a closing curly brace, so that generation always ends exactly where the JSON "
            "object finishes.",
            "Define a tool whose input schema is the ClaimDecision record, force it with toolChoice, and validate the "
            "returned input against the schema in Lambda.",
            "Set temperature to 0 and add 'Respond ONLY with valid JSON, no other text' at the start and the end of "
            "the system prompt.",
            "Add five few-shot examples of perfect JSON, and retry the call up to five times whenever parsing fails.",
        ],
        ans="B",
        why="Forcing a <b>tool whose input schema is the target record</b> makes the model return structured "
            "arguments that match the schema (names and types). <b>Schema validation in code</b> is the safety net. "
            "Prompt-only methods reduce errors but guarantee nothing.",
        wrong={
            "A": "A stop sequence can cut nested objects short and does nothing about wrong field names or types.",
            "C": "Lower randomness doesn't enforce a schema. The same malformed pattern can still appear consistently.",
            "D": "Examples plus retries lower the error rate but add latency and cost, and there's still no guarantee.",
        }),
    dict(
        dom="2", skill="2.1.1", kind="single",
        stem=[
            "A developer builds a tool-using assistant directly on the Converse API. In one turn, the model returns "
            "stopReason <i>tool_use</i> with <b>two</b> toolUse blocks (get_policy and get_claims). The developer runs "
            "both tools and sends the results back as two separate consecutive user messages, each holding one "
            "toolResult. The next Converse call fails with ValidationException.",
            "How should the developer fix this?",
        ],
        opts=[
            "Add the two tool outputs to the system prompt for the next call, and send a short user message asking "
            "the model to continue.",
            "Send the tool outputs as an assistant message, so that the model treats them as its own previous "
            "observations.",
            "After the assistant message that holds both toolUse blocks, send one user message containing both "
            "toolResult blocks, each with its matching toolUseId.",
            "Disable parallel tool calls, run only the first requested tool, and drop the second toolUse block.",
        ],
        ans="C",
        why="Converse requires roles to <b>alternate</b>. All results for one assistant tool-use turn go back in "
            "<b>a single user message</b> with one toolResult block per toolUse, matched by <b>toolUseId</b>.",
        wrong={
            "A": "Tool results are never put in the system prompt. Doing so breaks the tool protocol and mixes data "
                 "into the instructions.",
            "B": "Tool results come from the user/application side. An assistant message breaks the protocol.",
            "D": "Dropping a requested tool result leaves the conversation inconsistent and loses information.",
        }),
    dict(
        dom="2", skill="2.1.2", kind="two",
        stem=[
            "A fraud-investigation assistant must decide at runtime which of 8 internal APIs to call, and in what "
            "order, based on what earlier calls return. Requirements:",
            "every reasoning step and tool call must be reviewable for at least 90 days in the workflow's own "
            "execution history; the loop must stop after 10 iterations; transient model throttling must be retried "
            "per step with backoff; and any other failure must route to a fallback path.",
            "Which TWO design elements meet these requirements? (Select TWO.)",
        ],
        opts=[
            "A Step Functions Standard workflow looping through Bedrock Converse task → Choice (tool requested?) → "
            "Lambda tool, with an iteration counter that leads to a Fail state.",
            "A Step Functions Express workflow, because it handles high request volume and logs each step to "
            "CloudWatch Logs.",
            "A single Lambda function with a while loop that calls Converse until the model stops requesting tools.",
            "Retry on the Bedrock task for ThrottlingException with exponential backoff, plus a Catch that routes "
            "other errors to a fallback state.",
            "An Amazon Bedrock Flow that calls the 8 APIs through Lambda nodes in a fixed order.",
        ],
        ans="AD",
        why="A <b>ReAct loop in a Standard workflow</b> keeps per-step execution history for 90 days and enforces "
            "an iteration cap. Per-state <b>Retry</b> (backoff on ThrottlingException) and <b>Catch</b> (fallback) "
            "give the required error handling.",
        wrong={
            "B": "Express workflows have no execution history in Step Functions itself (only optional CloudWatch "
                 "Logs) and are limited to 5 minutes.",
            "C": "A code loop has no built-in audit history, cap or per-step retries.",
            "E": "A fixed order contradicts 'decide at runtime which APIs, in what order'.",
        }),
    dict(
        dom="2", skill="2.1.6", kind="single",
        stem=[
            "Four engineering teams build agents with different frameworks: Strands Agents, LangGraph, CrewAI and a "
            "custom Python loop. All four need the same 30 internal tools, which today are AWS Lambda functions and "
            "two REST APIs described by OpenAPI specifications. Inbound calls must be authenticated with the "
            "company's OAuth identity provider. Leadership wants no per-framework tool rewrites and the least "
            "operational overhead.",
            "Which solution meets these requirements?",
        ],
        opts=[
            "Create a Bedrock Agents action group per team that wraps the Lambda functions and OpenAPI APIs.",
            "Publish a shared Python package of tool functions that each team imports into its own framework.",
            "Put the APIs behind Amazon API Gateway with Cognito, and generate a client SDK for each framework.",
            "Expose the Lambda functions and OpenAPI APIs as MCP tools through Amazon Bedrock AgentCore Gateway, "
            "with inbound JWT authorisation.",
        ],
        ans="D",
        why="<b>MCP</b> is the framework-neutral protocol all four frameworks can use. <b>AgentCore Gateway</b> turns "
            "Lambda functions and OpenAPI targets into MCP tools, with inbound OAuth/JWT authorisation and no servers "
            "to run.",
        wrong={
            "A": "Action groups belong to Bedrock Agents and aren't usable from the other frameworks.",
            "B": "A shared library means per-language and per-framework integration work, and it doesn't fit the "
                 "custom loop or the OAuth requirement.",
            "C": "Each framework still needs custom wrapping of the SDK as tools, which is the per-framework work "
                 "leadership wants to avoid.",
        }),
    dict(
        dom="2", skill="2.1.6", kind="single",
        stem=[
            "An executive-assistant agent hosted on Amazon Bedrock AgentCore Runtime must create and update events in "
            "each employee's own Google Workspace calendar. Events must be created <b>as that employee</b>, only after "
            "the employee has consented once. Tokens must never appear in prompts or application code.",
            "Which approach meets these requirements?",
        ],
        opts=[
            "Store one Google service-account key in AWS Secrets Manager, and let the agent impersonate any employee "
            "with it.",
            "Use AgentCore Identity with an outbound OAuth credential provider, so each user grants consent once and "
            "the token vault supplies that user's tokens.",
            "Ask each employee to paste a personal API token into the chat at the start of each session.",
            "Create an IAM role federated with Google, and attach it to the AgentCore Runtime execution role.",
        ],
        ans="B",
        why="<b>AgentCore Identity</b> handles <b>outbound OAuth</b> on behalf of users: consent is recorded once, "
            "tokens are kept in a secure token vault, and the agent acts as that user without seeing raw secrets.",
        wrong={
            "A": "A shared impersonation key bypasses per-user consent and is a powerful long-lived credential.",
            "C": "Tokens would end up in prompts and logs, which is exactly what is forbidden.",
            "D": "IAM roles govern access to AWS resources, not to Google Workspace APIs on a user's behalf.",
        }),
    dict(
        dom="2", skill="2.1.1", kind="two",
        stem=[
            "A travel-planning agent on AgentCore must keep track of the itinerary being built during a conversation. "
            "Months later, it must still remember lasting preferences, such as an aisle seat, vegetarian meals and "
            "avoiding red-eye flights, without the user repeating them. Raw conversation events must expire after "
            "90 days.",
            "Which TWO capabilities should the team use? (Select TWO.)",
        ],
        opts=[
            "Store every past conversation in DynamoDB, and scan the user's full history into the prompt on each "
            "request.",
            "AgentCore Memory short-term memory (session events) for the context of the current conversation.",
            "Hard-code each user's preferences into the agent's system prompt, and redeploy when they change.",
            "AgentCore Memory long-term memory with a user-preference strategy that extracts lasting preferences "
            "across sessions.",
            "Switch to a model with a larger context window so that months of history fit in each request.",
        ],
        ans="BD",
        why="<b>Short-term memory</b> holds the events of the current session. <b>Long-term memory strategies</b> "
            "(such as user preferences) extract durable facts across sessions. Event expiry on the memory resource "
            "covers the 90-day rule.",
        wrong={
            "A": "Scanning the full history into every prompt is slow and expensive and eventually overflows the "
                 "context.",
            "C": "Redeploying per preference change doesn't scale and mixes user data into instructions.",
            "E": "A bigger window delays overflow but adds cost and latency and doesn't distil preferences.",
        }),
]
