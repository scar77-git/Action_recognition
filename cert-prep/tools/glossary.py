"""Glossary of abbreviations and jargon used in Days 1-4."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import S, Note  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

# Long tables follow each heading; keeping heading + whole table together wastes pages.
H1_SPLIT = ParagraphStyle("h1split", parent=S["h1"], keepWithNext=0)

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Glossary_Days_1-4_2026-10-24.pdf")

# (term, full form, plain-English meaning, example / where you'll meet it)
SECTIONS = [
    ("1. AI and model basics", [
        ("AI", "Artificial Intelligence", "Software that performs tasks needing human-like judgement.",
         "The umbrella term for everything in this exam."),
        ("GenAI", "Generative AI", "AI that creates new content (text, images, code) instead of only classifying.",
         "A chatbot writing a refund email."),
        ("LLM", "Large Language Model", "A model trained on huge amounts of text that predicts the next words.",
         "Claude, Amazon Nova, Llama."),
        ("FM", "Foundation Model", "A large, general-purpose pre-trained model you build applications on.",
         "Amazon Bedrock is a catalogue of FMs."),
        ("Token", "—", "A chunk of text (roughly ¾ of a word) that models read and write; billing and limits count tokens.",
         "'Hello world' is about 2–3 tokens."),
        ("Context window", "—", "The maximum number of tokens a model can consider in one request.",
         "Why you can't paste 10,000 documents into one prompt."),
        ("Hallucination", "—", "A confident answer that isn't supported by facts or sources.",
         "Inventing a refund amount not in the policy."),
        ("Embedding", "—", "A list of numbers representing the meaning of text; similar meanings give nearby vectors.",
         "'car broke down' sits near 'vehicle failure'."),
        ("Vector", "—", "The list of numbers produced by an embedding model.", "Titan V2 produces 256/512/1024 numbers."),
        ("Fine-tuning", "—", "Further training a model on your examples to change its behaviour or style.",
         "Teaching a model your company's writing tone."),
        ("Inference", "—", "Running a trained model to get an output (as opposed to training it).",
         "Every InvokeModel / Converse call."),
        ("Temperature", "—", "Setting controlling randomness of output; low = more deterministic.",
         "0 for extraction tasks, higher for brainstorming."),
        ("LLM-as-a-judge", "—", "Using a model to score another model's outputs against criteria.",
         "Bedrock Evaluations scoring context relevance."),
    ]),
    ("2. RAG and retrieval (Day 1)", [
        ("RAG", "Retrieval-Augmented Generation", "Search your own data first, then give the relevant passages to the "
         "model so it answers from them.", "A support bot answering from company policy PDFs."),
        ("KB", "Knowledge Base (Amazon Bedrock Knowledge Bases)", "AWS's managed RAG service: ingests, chunks, embeds, "
         "stores and retrieves your documents.", "Day 1 lab: KB over 5 PDFs in S3."),
        ("Data source", "—", "The location a Knowledge Base ingests from (e.g. an S3 bucket); chunking is set here.",
         "Not to be confused with a data store."),
        ("Sync / ingestion job", "—", "The process that reads a data source and updates the KB index.",
         "StartIngestionJob, scheduled hourly."),
        ("Chunking", "—", "Splitting documents into smaller passages before embedding.",
         "Fixed-size, hierarchical, semantic, none, custom (Lambda)."),
        ("Hierarchical chunking", "—", "Small 'child' chunks are searched; their larger 'parent' chunk is returned.",
         "Precise match plus full surrounding context."),
        ("Semantic search", "—", "Search by meaning using vectors.", "Finds synonyms and paraphrases."),
        ("BM25", "Best Matching 25", "A classic keyword-ranking algorithm (exact word matching).",
         "Finds 'XJ-4471-B' exactly."),
        ("Hybrid search", "—", "Combines semantic and keyword (BM25) search.", "Fix for missed product codes."),
        ("RRF", "Reciprocal Rank Fusion", "A method of merging two ranked result lists into one.",
         "Azure AI Search hybrid queries."),
        ("Reranker / rerank model", "—", "A second model that re-scores retrieved chunks so the best is first.",
         "Amazon Rerank, Cohere Rerank; Azure semantic ranker."),
        ("HNSW", "Hierarchical Navigable Small World", "A fast algorithm for finding nearest vectors.",
         "Used inside vector databases."),
        ("kNN", "k-Nearest Neighbours", "Finding the k vectors closest to a query vector.", "Vector search."),
        ("Metadata filtering", "—", "Restricting retrieval to chunks whose attributes match (tenant, department).",
         "Multi-tenant isolation."),
        ("GraphRAG", "Graph-based RAG", "RAG that uses relationships between entities stored in a graph.",
         "Neptune Analytics as the vector store."),
        ("Retrieve vs RetrieveAndGenerate", "—", "Retrieve returns chunks only; RetrieveAndGenerate returns a full "
         "answer with citations.", "Custom logic in between → Retrieve."),
        ("OCR", "Optical Character Recognition", "Reading text from images or scanned pages.", "Amazon Textract."),
        ("BDA", "Amazon Bedrock Data Automation", "Managed extraction of structured data from documents, images, audio, "
         "video.", "Parsing table-heavy PDFs for a KB."),
        ("Grounding / groundedness", "—", "Whether an answer is supported by the retrieved sources.",
         "Guardrails contextual grounding check."),
        ("Context precision / recall", "—", "Precision: are retrieved chunks relevant? Recall: was everything needed "
         "retrieved?", "RAG evaluation metrics."),
    ]),
    ("3. Agents and tools (Days 2–3)", [
        ("Agent", "—", "A model plus instructions, tools and memory running in a loop, deciding at runtime which tool "
         "to call.", "OrderHelper checking then cancelling an order."),
        ("ReAct", "Reason + Act", "The agent loop pattern: think → call a tool → observe → repeat.",
         "Default Bedrock Agents orchestration."),
        ("Tool / function calling", "—", "The model requests a named tool with arguments; your code runs it.",
         "stopReason = tool_use."),
        ("toolUse / toolResult", "—", "Converse API blocks: the model's tool request, and your reply with the output "
         "(matched by toolUseId).", "Results go in a role 'user' message."),
        ("Action group", "—", "Bedrock Agents Classic's way of defining tools (OpenAPI schema or function details).",
         "get_order_status, cancel_order."),
        ("RoC", "Return of control", "Bedrock Agents hands the tool call back to your application to execute.",
         "Banking app using the user's authenticated session."),
        ("DRAFT / version / alias", "—", "DRAFT is the editable agent; Prepare → version (snapshot); an alias points "
         "to a version.", "Rollback = repoint the alias."),
        ("TSTALIASID", "Test alias ID", "Built-in alias that points to the DRAFT version, for testing.",
         "Test after PrepareAgent."),
        ("HITL", "Human-in-the-loop", "A person approves or reviews a step before it proceeds.",
         "requireConfirmation; Step Functions approval."),
        ("Agents Classic", "Amazon Bedrock Agents (Classic)", "The original managed agents service, now in "
         "maintenance mode for new accounts.", "Why your Day 2 console lab was blocked."),
        ("AgentCore", "Amazon Bedrock AgentCore", "AWS services to host, connect, secure and observe agents built with "
         "any framework.", "Runtime, Gateway, Memory, Identity, Observability."),
        ("Strands Agents", "—", "AWS's open-source Python SDK for building agents.", "@tool decorator."),
        ("Agent Squad", "AWS Agent Squad (formerly Multi-Agent Orchestrator)", "Open-source framework that routes each "
         "request to the best specialist agent.", "Billing / tech / sales routing."),
        ("MCP", "Model Context Protocol", "Open standard for connecting AI apps to tools and data ('USB-C for AI tools').",
         "Tools exposed once, usable by any framework."),
        ("A2A", "Agent-to-Agent protocol", "Open standard for agents to communicate with other agents.",
         "Mentioned for Azure/AI-500."),
        ("Supervisor / router", "—", "Supervisor: delegates to several agents and combines. Router: sends to exactly "
         "one.", "95% single-specialist traffic → router."),
        ("Swarm", "—", "Peer agents hand work to each other without a central coordinator.", "Exploratory tasks."),
        ("microVM", "Micro virtual machine", "A tiny, fast-starting isolated VM.", "AgentCore Runtime session isolation."),
        ("OpenTelemetry (OTel)", "—", "Open standard format for traces, metrics and logs.", "AgentCore Observability."),
        ("Code Interpreter", "—", "A sandbox where an agent runs code it writes.", "pandas analysis of a CSV."),
    ]),
    ("4. AWS services named so far", [
        ("AWS", "Amazon Web Services", "Amazon's cloud platform.", "—"),
        ("S3", "Amazon Simple Storage Service", "Object storage for files of any kind.", "KB source documents."),
        ("Lambda", "AWS Lambda", "Runs your code on demand without servers (max 15 minutes per run).",
         "Action group executor, Gateway target."),
        ("Step Functions", "AWS Step Functions", "Visual workflows that chain steps with retries and history.",
         "Mortgage approval workflow."),
        ("Standard vs Express", "Step Functions workflow types", "Standard: up to 1 year, full history. Express: up to "
         "5 minutes, high volume.", "Multi-day approval → Standard."),
        ("waitForTaskToken", "—", "Step Functions pattern that pauses until someone returns a task token.",
         "Human approval via SQS + SendTaskSuccess."),
        ("SQS", "Amazon Simple Queue Service", "Message queue between components.", "Delivering the approval token."),
        ("SNS", "Amazon Simple Notification Service", "Pub/sub notifications (email, SMS, HTTP).", "Alerting."),
        ("EventBridge", "Amazon EventBridge", "Event bus and scheduler that triggers targets on events or schedules.",
         "Hourly StartIngestionJob."),
        ("API Gateway", "Amazon API Gateway", "Managed front door for HTTP/REST APIs.", "Exposing a GenAI app."),
        ("ECS / Fargate", "Elastic Container Service / serverless containers", "Run containers; Fargate removes server "
         "management.", "Distractor vs AgentCore Runtime."),
        ("ALB", "Application Load Balancer", "Distributes HTTP traffic across targets.", "Distractor in Q11."),
        ("OpenSearch Serverless", "Amazon OpenSearch Serverless", "Managed search/vector engine without clusters.",
         "Default KB vector store."),
        ("OCU", "OpenSearch Compute Unit", "Billing unit for OpenSearch Serverless capacity, charged hourly.",
         "Why you delete it after labs."),
        ("Aurora / pgvector", "Amazon Aurora PostgreSQL + pgvector extension", "Relational database with vector "
         "search support.", "Vector store when you need SQL joins."),
        ("Neptune Analytics", "Amazon Neptune Analytics", "Graph analytics database.", "GraphRAG."),
        ("DynamoDB", "Amazon DynamoDB", "Key-value / document NoSQL database. <b>Not</b> a KB vector store.",
         "Practice Set Q2 trap."),
        ("Textract", "Amazon Textract", "Extracts text, forms and tables from scans (OCR).", "Scanned claim forms."),
        ("Comprehend", "Amazon Comprehend", "Natural-language service; detects and redacts PII.", "Redact before ingestion."),
        ("Macie", "Amazon Macie", "Scans S3 to discover sensitive data such as PII.", "Find card numbers in buckets."),
        ("Glue / Data Catalog", "AWS Glue", "Data integration (ETL) and a catalogue of datasets/tables.",
         "Tables governed by Lake Formation."),
        ("Lake Formation", "AWS Lake Formation", "Fine-grained table/column/row permissions for data lakes.",
         "Hide card_number column."),
        ("CloudWatch", "Amazon CloudWatch", "Metrics, logs, dashboards and alarms.", "GenAI Observability dashboard."),
        ("CloudTrail", "AWS CloudTrail", "Records who called which AWS API, and when.", "Audit of Bedrock calls."),
        ("X-Ray / Transaction Search", "AWS X-Ray, CloudWatch Transaction Search", "Distributed tracing; Transaction "
         "Search must be enabled for AgentCore traces.", "Day 3 console lab Part D."),
        ("Secrets Manager", "AWS Secrets Manager", "Stores and rotates secrets (passwords, API keys).",
         "AgentCore Identity API-key provider."),
        ("Cognito", "Amazon Cognito", "User sign-up/sign-in; issues JWTs.", "Gateway inbound auth quick-create."),
        ("CloudShell", "AWS CloudShell", "Browser terminal with the AWS CLI pre-configured.", "send-task-success."),
        ("Service Quotas", "—", "Console for viewing and raising account limits.", "Bedrock TPM quota of 0."),
    ]),
    ("5. Security and networking (Day 4)", [
        ("IAM", "AWS Identity and Access Management", "Who (users, roles) can do what (actions) on which resources.",
         "Allow InvokeModel on one model only."),
        ("IAM role", "—", "An identity with permissions that services or apps assume, giving short-term credentials.",
         "KB service role."),
        ("Identity-based vs resource-based policy", "—", "Identity policy is attached to the caller; resource policy is "
         "attached to the resource saying who may use it.", "Lambda resource policy allowing bedrock.amazonaws.com."),
        ("ARN", "Amazon Resource Name", "The unique ID string of an AWS resource.",
         "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0"),
        ("Implicit vs explicit deny", "—", "Implicit: nothing allowed it. Explicit: a Deny statement — always wins.",
         "Policy Simulator results."),
        ("SCP", "Service Control Policy", "Organisation-wide guardrail capping what any member account (even admins) "
         "can do.", "Block one model across the company."),
        ("AWS Organizations", "—", "Groups many AWS accounts under central management; where SCPs live.", "—"),
        ("KMS", "AWS Key Management Service", "Creates and controls encryption keys; every use is auditable.",
         "Encrypt KB data with your own key."),
        ("CMK / customer managed key", "Customer managed KMS key", "A KMS key you create and control (rotation, policy, "
         "revocation).", "'Control and audit the keys'."),
        ("Key policy", "—", "The resource policy on a KMS key saying who may use it.", "Must allow KB role kms:Decrypt."),
        ("SSE", "Server-Side Encryption", "The service encrypts data when storing it.", "S3 default encryption."),
        ("SSE-S3 / SSE-KMS", "—", "SSE-S3: keys managed by S3. SSE-KMS: encryption using a KMS key you can control.",
         "Switching to SSE-KMS broke the KB sync."),
        ("VPC", "Virtual Private Cloud", "Your private, isolated network inside AWS.", "Private subnets."),
        ("Subnet (private)", "—", "A slice of a VPC with no direct internet route.", "Healthcare app in Q1."),
        ("NAT gateway", "Network Address Translation gateway", "Lets private resources reach the internet outbound.",
         "Not needed when you use VPC endpoints."),
        ("VPC endpoint / VPCE", "VPC Endpoint", "A private connection from your VPC to an AWS service, no internet.",
         "bedrock-runtime, bedrock-agent-runtime endpoints."),
        ("PrivateLink", "AWS PrivateLink", "The technology behind interface VPC endpoints.", "—"),
        ("aws:SourceVpce", "—", "IAM condition key: which VPC endpoint the request came through.",
         "Deny if not our endpoint."),
        ("Endpoint policy", "—", "A policy on a VPC endpoint limiting what can be called through it.", "Only Nova models."),
        ("DNS / private DNS", "Domain Name System", "Translates service names into addresses; private DNS makes the "
         "normal service name resolve to your endpoint.", "Enable when creating the endpoint."),
        ("PII", "Personally Identifiable Information", "Data that identifies a person.", "Names, emails, card numbers."),
        ("Mask vs block", "Guardrails PII actions", "Mask replaces the PII with a placeholder; block rejects the "
         "whole input/output.", "Email → mask, card → block."),
        ("Regex", "Regular expression", "A text pattern for matching strings.", "ORD-\\d{6} for order IDs."),
        ("WORM / Object Lock", "Write Once, Read Many", "Data can't be changed or deleted for a set period.",
         "Compliance retention."),
        ("Lifecycle rule", "S3 Lifecycle", "Automatically moves or deletes objects after N days.", "Expire logs after 30 days."),
        ("Data residency", "—", "Requirement that data stays in a specific country/region.",
         "Use a geographic cross-region inference profile."),
        ("CRIS", "Cross-Region Inference", "Bedrock routes requests to other regions for capacity.",
         "us.* inference profile IDs."),
        ("Invocation logging", "Model invocation logging", "Optional Bedrock feature recording full prompts and "
         "responses to S3/CloudWatch.", "Encrypt with KMS, expire with lifecycle."),
    ]),
    ("6. Authentication, APIs and developer terms", [
        ("API", "Application Programming Interface", "A defined way for programs to call each other.", "Converse API."),
        ("SDK", "Software Development Kit", "Libraries for calling a service from code.", "boto3 (Python AWS SDK)."),
        ("boto3", "—", "The AWS SDK for Python.", "brt.converse(...)."),
        ("CLI", "Command Line Interface", "Terminal tool for calling a service.", "aws stepfunctions send-task-success."),
        ("CDK", "AWS Cloud Development Kit", "Define infrastructure in code (TypeScript, Python…).", "—"),
        ("REST / HTTP", "Representational State Transfer", "Common style of web APIs over HTTP.", "300 internal REST APIs."),
        ("OpenAPI", "OpenAPI Specification", "A standard file describing a REST API's endpoints and parameters.",
         "Action group schema, Gateway target."),
        ("JSON", "JavaScript Object Notation", "Text format for structured data.", "Tool input schemas."),
        ("JSONPath / JSONata", "—", "Two expression languages Step Functions uses to read and transform data.",
         "$$.Task.Token vs $states.context.Task.Token."),
        ("OAuth", "Open Authorization", "Standard for letting an app act on a user's behalf without their password.",
         "AgentCore Identity outbound to GitHub."),
        ("JWT", "JSON Web Token", "A signed token proving who the caller is.", "Cognito-issued token for the Gateway."),
        ("Inbound vs outbound auth", "—", "Inbound: who may call the agent/gateway. Outbound: how the agent calls other "
         "services.", "Cognito JWT in; IAM role/OAuth out."),
        ("PAT", "Personal Access Token", "A long-lived token tied to one user (e.g. GitHub).", "Q12 distractor."),
        ("TPM / RPM", "Tokens / Requests Per Minute", "Rate limits on model usage.", "Your quota was 0 TPM."),
        ("Throttling", "ThrottlingException", "Error when you exceed a rate limit.", "Fix: backoff, quota increase."),
        ("Exponential backoff", "—", "Retry with growing waits (1s, 2s, 4s…).", "Handling throttling."),
        ("ETL", "Extract, Transform, Load", "Moving and reshaping data between systems.", "Ingestion pipelines."),
        ("Pass / Choice / Task state", "Step Functions states", "Pass: placeholder; Choice: branch; Task: do work.",
         "Day 3 console lab Part E."),
    ]),
    ("7. Exam and Azure terms", [
        ("AIP-C01", "—", "Exam code for AWS Certified Generative AI Developer – Professional.", "Mon 9 Nov."),
        ("AI-103", "—", "Microsoft exam: Developing AI Apps and Agents on Azure.", "Sat 28 Nov."),
        ("AI-500", "—", "Microsoft exam: Designing and Implementing Multi-Agent AI Solutions (Expert).", "December."),
        ("Foundry", "Microsoft (Azure AI) Foundry", "Azure's platform for models and agents.", "Azure equivalent of Bedrock."),
        ("Agent Service", "Foundry Agent Service", "Azure's managed agent runtime (threads, messages, runs).",
         "requires_action = return of control."),
        ("AI Search", "Azure AI Search", "Azure's search/vector service.", "Azure equivalent of KB vector store."),
        ("Content Safety", "Azure AI Content Safety", "Azure content filtering incl. groundedness detection.",
         "Azure equivalent of Guardrails."),
        ("Entra ID", "Microsoft Entra ID", "Azure's identity service (formerly Azure AD).", "Azure equivalent of IAM users."),
        ("ESL +30", "English as a Second Language +30 minutes", "AWS exam accommodation (not requested).", "—"),
    ]),
]

n = Note(OUT, "Glossary — Days 1 to 4",
         "Saturday 24 Oct 2026 &nbsp;·&nbsp; Every abbreviation and key term used so far, with a plain-English "
         "meaning and where you met it")
n.callout("How to use this", "Skim a section before revising the matching day's note. If a term in a question feels "
          "fuzzy, find it here first. From Day 5 onwards every term is explained in the lesson itself, and each day's "
          "note ends with its own glossary.", "ok")
total = 0
for title, rows in SECTIONS:
    n.story.append(Paragraph(title, H1_SPLIT))
    n.table(["Term", "Full form", "Meaning", "Example / where you met it"], [list(r) for r in rows],
            [0.17, 0.22, 0.36, 0.25])
    total += len(rows)
n.build()
print(os.path.abspath(OUT), total)
