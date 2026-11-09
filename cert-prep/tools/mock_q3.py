"""Full mock question bank, part 3 — Domain 2 (implementation and integration)."""

QS = [
    dict(
        dom="2", skill="2.1.5", kind="two",
        stem=[
            "A bank runs 40 specialist agents (cards, mortgages, tax, investments, retirement and more). About 95% of "
            "customer requests belong to exactly one specialist and must be answered with minimum latency and cost. "
            "The other 5% are 'financial planning' requests, which need the tax, investment and retirement "
            "specialists' outputs combined into one coherent plan.",
            "Which TWO patterns should the architect combine? (Select TWO.)",
        ],
        opts=[
            "Broadcast every request to all 40 agents in parallel, and return the answer with the highest "
            "self-reported confidence.",
            "A classifier/router (for example, AWS Agent Squad) that sends each single-domain request to exactly one "
            "specialist agent.",
            "One large agent that holds all 40 specialists' tools and instructions in a single prompt.",
            "A Step Functions Parallel state that calls all 40 agents for every request and then merges the results.",
            "A supervisor agent that calls the tax, investment and retirement agents as tools for planning requests "
            "and combines their results.",
        ],
        ans="BE",
        why="Most traffic needs exactly one specialist, so a <b>router</b> (one cheap classification, then one agent) "
            "is fastest and cheapest. Planning requests need several specialists' outputs merged, which is a "
            "<b>supervisor / agents-as-tools</b> pattern.",
        wrong={
            "A": "Broadcasting multiplies cost and latency by 40, and self-reported confidence is unreliable.",
            "C": "Forty agents' tools and instructions in one prompt causes wrong tool choices and huge prompts.",
            "D": "Calling all 40 for every request has the same cost and latency problem as broadcasting.",
        }),
    dict(
        dom="2", skill="2.4.3", kind="three",
        stem=[
            "A summarisation service calls a primary model through Step Functions, with hundreds of concurrent "
            "executions. When the primary model's endpoint degrades, every execution keeps retrying and makes things "
            "worse. Requirements: after 5 consecutive failures, stop calling the primary model for 60 seconds and "
            "serve a fallback model instead. After the cool-down, let a single trial request through to test "
            "recovery. All executions must share the same state.",
            "Which THREE elements implement this? (Select THREE.)",
        ],
        opts=[
            "Keep the failure counter in a static variable inside the Lambda function that calls the model.",
            "A DynamoDB item that holds the circuit state, the consecutive failure count and the time the circuit "
            "opened, read at the start of each execution.",
            "A Choice state that sends the request to the fallback model branch whenever the circuit is OPEN.",
            "Retry every failed call up to 20 times with exponential backoff before treating it as a failure.",
            "A half-open state: after 60 seconds, one trial request goes to the primary model; success closes the "
            "circuit and failure reopens it.",
            "Increase the Lambda function timeout to 15 minutes so that slow primary responses can eventually "
            "succeed.",
        ],
        ans="BCE",
        why="This is a <b>circuit breaker</b>: <b>shared state</b> in DynamoDB (all executions see the same thing), "
            "an <b>OPEN → fallback</b> branch, and a <b>half-open</b> trial that decides whether to close the circuit.",
        wrong={
            "A": "Static variables live in one execution environment only and aren't shared across hundreds of "
                 "concurrent executions.",
            "D": "Heavy retrying is exactly the behaviour that piles extra load onto an already degraded endpoint.",
            "F": "Waiting longer makes users wait longer and protects nothing.",
        }),
    dict(
        dom="2", skill="2.4.3", kind="three",
        stem=[
            "On Black Friday, traffic to a retailer's GenAI features rises tenfold. Two workloads share the model: "
            "interactive chat, which must stay responsive, and product-description summaries, which can be delayed "
            "by several minutes. There are no data-residency restrictions. Finance wants no new long-term capacity "
            "commitments, and the cheapest effective mix.",
            "Which THREE actions should the team take? (Select THREE.)",
        ],
        opts=[
            "Purchase Provisioned Throughput sized for the tenfold peak for the whole month of November.",
            "Use the AWS SDK's exponential backoff with jitter for ThrottlingException on all model calls.",
            "Remove all retries so that requests fail fast and users simply try again.",
            "Use a cross-Region inference profile to draw throughput from several Regions at no extra cost.",
            "Put the summary requests into an SQS queue drained by workers with capped (reserved) concurrency.",
            "Raise the temperature so that responses are shorter and use fewer output tokens.",
        ],
        ans="BDE",
        why="The cheapest effective mix: <b>backoff with jitter</b> absorbs short bursts; <b>cross-Region inference</b> "
            "adds throughput with no commitment; an <b>SQS buffer</b> moves the delay-tolerant work out of chat's way.",
        wrong={
            "A": "A monthly commitment sized for a single-day peak contradicts the 'no long-term commitments' "
                 "requirement.",
            "C": "Failing fast without retries turns short throttling into user-facing errors.",
            "F": "Temperature controls randomness, not length. It doesn't reliably reduce tokens.",
        }),
    dict(
        dom="2", skill="2.4.2", kind="single",
        stem=[
            "A mobile banking app calls Amazon API Gateway (REST) → Lambda → Bedrock. Detailed answers take 40–60 "
            "seconds, and users get HTTP 504 errors. Product owners want text to appear word by word as it is "
            "generated. The user must also be able to tap 'Stop' and cancel the generation midway.",
            "Which design meets all of these requirements?",
        ],
        opts=[
            "Raise the Lambda timeout to 15 minutes, and return the complete answer when the model finishes.",
            "Return a job ID immediately, process the request from an SQS queue, and have the app poll for the "
            "finished answer.",
            "Put Amazon CloudFront in front of API Gateway with a 60-second origin timeout to absorb the long "
            "responses.",
            "Use an API Gateway WebSocket API with Lambda calling ConverseStream, pushing chunks to the connection and "
            "stopping on a cancel message.",
        ],
        ans="D",
        why="Streaming tokens fixes both the timeout and the perceived wait. A <b>WebSocket</b> is a two-way "
            "connection, so the client can also send 'stop', which one-way server-sent events cannot do.",
        wrong={
            "A": "The REST integration timeout still applies before Lambda finishes, and there's no incremental text.",
            "B": "Polling avoids the timeout, but users still wait for the whole answer and can't cancel mid-stream.",
            "C": "Caching doesn't help unique answers, and nothing becomes incremental or cancellable.",
        }),
    dict(
        dom="2", skill="2.4.4", kind="single",
        stem=[
            "A document-summary feature runs in Lambda and currently uses Model X. The team wants to move it to Model "
            "Y gradually, raising the share by 10% every 10 minutes, and roll back automatically if the feature's "
            "CloudWatch error alarm fires. Changing the model must not require a code change or redeploying the "
            "function.",
            "Which approach meets these requirements?",
        ],
        opts=[
            "Store the model ID in AWS AppConfig, read it at runtime through the AppConfig Lambda extension, and "
            "deploy changes with a linear strategy and an alarm monitor.",
            "Update the model ID in the function's environment variables through a CloudFormation stack update during "
            "a maintenance window.",
            "Publish a new function version with Model Y hard-coded, and shift traffic with weighted Lambda aliases "
            "through CodeDeploy.",
            "Store the model ID in Systems Manager Parameter Store, and update it manually in steps while watching "
            "the error dashboard.",
        ],
        ans="A",
        why="<b>AppConfig</b> delivers configuration at runtime with <b>deployment strategies</b> (linear 10% every 10 "
            "minutes) and <b>alarm-based automatic rollback</b>, with no code change or redeploy.",
        wrong={
            "B": "This is a stack update and redeploy, with no gradual shift or automatic rollback.",
            "C": "Gradual and rollback-capable, but it needs a code change and a new version, which the requirement "
                 "forbids.",
            "D": "Parameter Store has no gradual rollout or automatic rollback, so this relies on manual steps.",
        }),
    dict(
        dom="2", skill="2.4.4", kind="two",
        stem=[
            "A legal-services company has two routing needs:",
            "(1) general client questions should automatically use a cheaper or a more capable model from the same "
            "model family, based on each prompt's predicted response quality, with minimal engineering; "
            "(2) contract-review requests must always go to the company's fine-tuned contract model, and auditors "
            "must be able to see why each request was routed where it was.",
            "Which TWO solutions should the team use? (Select TWO.)",
        ],
        opts=[
            "An Amazon Bedrock Intelligent Prompt Routing prompt router across the models of one family for general "
            "questions.",
            "An Intelligent Prompt Routing router configured to send contract-review requests to the fine-tuned model.",
            "A random 50/50 traffic split between the two general models, with costs compared at the end of the month.",
            "A Step Functions workflow that classifies each request and uses a Choice state to send contract reviews "
            "to the fine-tuned model.",
            "Always sending every request to the most capable model so that routing logic is unnecessary.",
        ],
        ans="AD",
        why="<b>Intelligent Prompt Routing</b> picks between models <i>within one family</i> by predicted quality, "
            "with no code. <b>Business-category routing</b> to a specific custom model is a classify step plus a "
            "<b>Choice state</b>, and the execution history records why each request went where it did.",
        wrong={
            "B": "Prompt routers choose among supported models by predicted quality. They don't route by business "
                 "category to your custom model.",
            "C": "A random split isn't routing by quality, and it can't guarantee the correct model per request.",
            "E": "This ignores cost and can't guarantee contract reviews reach the fine-tuned model.",
        }),
    dict(
        dom="2", skill="2.3.2", kind="single",
        stem=[
            "A Git hosting service sends pull-request webhooks to a company. It expects an HTTP 2xx within 10 seconds "
            "and redelivers the same event (same delivery ID) if it doesn't get one. For each pull request, a Bedrock "
            "review takes 60–90 seconds, and the review is posted back as a comment. The team has seen duplicate "
            "review comments during provider redeliveries.",
            "Which design meets these requirements?",
        ],
        opts=[
            "A synchronous Lambda function with a 15-minute timeout that runs the review before returning HTTP 200 to "
            "the webhook.",
            "An EventBridge Scheduler rule that polls the Git API every minute for new pull requests and reviews them.",
            "API Gateway → Lambda that verifies the signature, records the delivery ID with a DynamoDB conditional "
            "write, queues new events in SQS and returns 200. A worker does the review.",
            "API Gateway → Lambda that invokes a second Lambda asynchronously for the review and returns 200, without "
            "storing anything.",
        ],
        ans="C",
        why="Acknowledge fast (signature check, then 200 within 10 s), do the slow work <b>asynchronously</b> through "
            "a queue, and make processing <b>idempotent</b>. A conditional write on the delivery ID means redelivered "
            "events are recognised and skipped.",
        wrong={
            "A": "The 60–90 second review exceeds the 10-second acknowledgement window, which causes the redeliveries.",
            "B": "Polling adds delay and API cost and replaces a supported push mechanism. It's also not the requested "
                 "event-driven design.",
            "D": "Fast acknowledgement, but nothing deduplicates redeliveries, so duplicate comments remain.",
        }),
    dict(
        dom="2", skill="2.3.1", kind="two",
        stem=[
            "A manufacturer's support assistant has two data needs:",
            "(1) a Bedrock knowledge base must reflect Salesforce knowledge articles within one hour of publication; "
            "(2) an agent tool queries product availability from an Amazon Aurora copy of the on-premises Oracle ERP "
            "database, and that copy must track ERP changes continuously, with minimal load on the ERP.",
            "Which TWO solutions meet these needs? (Select TWO.)",
        ],
        opts=[
            "A Bedrock knowledge base Salesforce data source, with EventBridge Scheduler starting an ingestion job "
            "every hour.",
            "A nightly full export of the Oracle database to CSV files in S3, loaded into Aurora with the COPY command.",
            "An AWS Glue crawler that runs hourly against the Oracle database to keep the Aurora tables up to date.",
            "AWS DMS with ongoing replication (change data capture) from Oracle to Aurora.",
            "Weekly manual uploads of exported Salesforce articles to the knowledge base's S3 bucket.",
        ],
        ans="AD",
        why="The KB's <b>Salesforce connector</b> plus a scheduled <b>ingestion job</b> meets the one-hour freshness "
            "target. <b>DMS CDC</b> streams only changed rows from Oracle to Aurora, so the copy stays continuously "
            "current with low source load.",
        wrong={
            "B": "A nightly full export is up to 24 hours stale and puts heavy load on the source.",
            "C": "Crawlers catalogue schemas; they don't copy data into Aurora.",
            "E": "Weekly manual uploads miss the one-hour target and add manual work.",
        }),
    dict(
        dom="2", skill="2.3.5", kind="all",
        stem=[
            "A platform team serves 25 product teams. Requirements:",
            "per-team rate limits; only approved models usable; the same guardrail applied to every call; cost "
            "attributed to each team; switching model providers without any team changing code; and every change to "
            "the shared layer canary-deployed with automatic rollback.",
            "Which actions meet these requirements? (Select ALL that apply.)",
        ],
        opts=[
            "A central GenAI gateway (API Gateway + Lambda) with a usage plan and API key per team.",
            "Granting each team's role bedrock:* on all models, so that teams can experiment freely.",
            "Gateway logic that applies the shared guardrail to every call and routes only to an approved-model list.",
            "Application inference profiles (with cost allocation tags) per team, used by the gateway for calls.",
            "Each team stores its chosen model IDs in its own repository and calls Bedrock directly.",
            "CodePipeline with CodeDeploy canary deployments of the gateway Lambda alias and alarm-based rollback.",
        ],
        ans="ACDF",
        why="A <b>gateway</b> centralises control: usage plans give per-team limits; central guardrail and model "
            "routing give approved, consistent calls and provider swaps; <b>application inference profiles</b> "
            "attribute cost; the <b>canary pipeline</b> covers safe change.",
        wrong={
            "B": "This breaks least privilege and the approved-model rule.",
            "E": "Direct calls bypass central control, and switching providers would need code changes in every team.",
        }),
    dict(
        dom="2", skill="2.3.4", kind="single",
        stem=[
            "An automotive company is building in-vehicle voice assistance for connected cars on a mobile carrier's "
            "5G network. The model's response must arrive within 20 milliseconds of network round-trip, which isn't "
            "achievable from the nearest AWS Region. The company wants AWS-managed infrastructure and APIs, and "
            "doesn't want hardware in its own facilities.",
            "Which deployment option should the company use?",
        ],
        opts=[
            "AWS Outposts racks installed in each dealership, running the model on GPU instances.",
            "An AWS Local Zone in the nearest large city, hosting a SageMaker endpoint.",
            "AWS Wavelength Zones in the carrier's 5G network, running the inference service on GPU instances.",
            "The nearest AWS Region with Amazon CloudFront in front of the inference API.",
        ],
        ans="C",
        why="<b>Wavelength</b> places AWS compute inside telecom 5G networks, so traffic from devices on that network "
            "never leaves it, giving the lowest latency for mobile and edge clients with AWS-managed infrastructure.",
        wrong={
            "A": "Outposts means hardware in the company's own facilities, which is explicitly unwanted, and "
                 "dealerships aren't on the car's network path.",
            "B": "Closer than a Region, but traffic still leaves the carrier network. The 5G-edge answer is Wavelength.",
            "D": "CloudFront caches content; it doesn't run low-latency inference for unique requests.",
        }),
    dict(
        dom="2", skill="2.5.3", kind="two",
        stem=[
            "A mortgage lender receives about 50 different document types (payslips, bank statements, tax returns) "
            "in varied layouts. It needs structured fields from each, with no custom models to train. Extractions "
            "below 85% confidence must wait for an underwriter's review, which can take up to 3 business days. Every "
            "step needs retries and a complete audit trail.",
            "Which TWO components meet these requirements? (Select TWO.)",
        ],
        opts=[
            "Amazon Bedrock Data Automation with a blueprint for each document type to extract the structured fields.",
            "A Step Functions Express workflow, with a Wait state that holds each case until the underwriter decides.",
            "A Step Functions Standard workflow with a Choice state on confidence and a .waitForTaskToken step for "
            "underwriter review.",
            "A single Lambda function that extracts, reviews and stores each document, sending failures to a "
            "dead-letter queue.",
            "An Amazon Comprehend custom classifier that reads each document and returns the required field values.",
        ],
        ans="AC",
        why="<b>BDA blueprints</b> extract structured fields from many layouts without training models. A "
            "<b>Standard</b> workflow allows waits of days through a task token, with per-step retries and full "
            "execution history.",
        wrong={
            "B": "Express workflows are limited to 5 minutes, and a fixed Wait can't respond to the underwriter's "
                 "actual decision.",
            "D": "Lambda runs for at most 15 minutes, so it can't wait days, and it has no workflow audit trail.",
            "E": "Classification labels whole documents; it doesn't extract field values from varied layouts.",
        }),
    dict(
        dom="2", skill="2.5.4", kind="two",
        stem=[
            "A GenAI platform team has two productivity problems:",
            "(1) developers spend days refactoring dozens of InvokeModel calls to the Converse API and writing unit "
            "tests for prompt-handling code; (2) the operations team must find patterns across thousands of "
            "production prompts and responses, such as which features trigger 'conversation must alternate' "
            "validation errors.",
            "Which TWO tools address these problems? (Select TWO.)",
        ],
        opts=[
            "Amazon Q Business, connected to the code repositories, so that developers can ask how to refactor the "
            "calls.",
            "Amazon Q Developer in the IDE, to refactor the calls to Converse and generate unit tests.",
            "AWS X-Ray service maps, to show which prompts led to validation errors.",
            "Amazon CodeGuru Profiler, to find inefficient prompt templates in the running application.",
            "CloudWatch Logs Insights queries over model invocation logs and structured application error logs.",
        ],
        ans="BE",
        why="<b>Q Developer</b> is the coding assistant (generate, refactor, test). <b>Logs Insights</b> queries "
            "prompt and response content and error logs at scale to find patterns.",
        wrong={
            "A": "Q Business answers employees' questions over company content. It isn't the IDE coding assistant "
                 "that refactors code.",
            "C": "X-Ray shows timing and errors across services, not prompt content patterns.",
            "D": "CodeGuru Profiler profiles CPU and latency hot spots in code; it doesn't analyse prompts.",
        }),
]
