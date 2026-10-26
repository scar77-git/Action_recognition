"""Practice Set 2 (Days 1-5 + gap lesson): 45 questions. Kept OUT of the repo until the learner has answered.

Run: python3 practice02.py            -> question PDF + key JSON in the scratchpad
"""
import json
import os
import random
import sys

REPO_TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO_TOOLS)
from notelib import S, Note  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

OUT = os.path.join(REPO_TOOLS, "..", "notes", "Practice_Set_2_2026-10-26_Days_1-5_and_Gap_Questions.pdf")
KEY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "practice02_key.json")

MC, TWO, THREE, ALL = "MC", "TWO", "THREE", "ALL"
LABEL = {MC: "", TWO: " (Select TWO.)", THREE: " (Select THREE.)",
         ALL: " (Select ALL that apply.) [extra-hard practice format — the real exam states the number]"}

# (skill, type, difficulty, stem, [(option, correct, why), ...])
Q = [
    ("1.2.1", MC, "M",
     "A retailer must write short alt-text descriptions for 40,000 product photos every night. Testing showed a small "
     "model gives acceptable descriptions. Results are needed by the next morning, and cost is the top priority. Which "
     "approach should the team use?",
     [("Send each image's file name and product title to a small text-only model through on-demand inference", False,
       "A text-only model can't see the photo, so it can only guess from the file name."),
      ("Submit the photos to a small multimodal model as one batch inference job each evening", True,
       "Multimodal input is required; batch inference is ~50% cheaper and finishes overnight."),
      ("Call a large multimodal model on demand with response streaming for each photo as it is uploaded", False,
       "Works, but a large model on demand is far more expensive than needed; streaming doesn't cut cost."),
      ("Use an image-generation model to regenerate each photo and keep the prompt it used as the description", False,
       "Image generation creates images; it doesn't describe existing ones.")]),
    ("1.2.3", MC, "H",
     "A company's application runs in eu-central-1. Customer data must never be processed outside the European Union. "
     "The model the team selected is not offered in eu-central-1, but is offered in other EU Regions. What should the "
     "team do?",
     [("Call the model through a global cross-Region inference profile so that capacity is always available", False,
       "A global profile can route requests outside the EU — violates the residency rule."),
      ("Call the model through an EU-geography cross-Region inference profile", True,
       "Routes only to EU Regions where the model is offered; no extra infrastructure."),
      ("Move the application to us-east-1, where the model and the most capacity are available", False,
       "Processing in the US violates the requirement."),
      ("Use Custom Model Import to bring the selected model's weights into eu-central-1", False,
       "Custom Model Import is for open-weight models you trained; provider models can't be imported this way.")]),
    ("1.2.2", MC, "H",
     "Thirty microservices owned by different teams call Amazon Bedrock. The security team must be able to change the "
     "approved model used by all services within an hour, without any team redeploying, and any change must be "
     "checked against a list of allowed models before it reaches the services. What should the platform team build?",
     [("Ask each service to read the model ID from an environment variable that the central team updates through pull requests", False,
       "Environment variable changes require each service to be redeployed."),
      ("A central AWS AppConfig configuration profile with a JSON Schema validator of allowed models, read by every service at runtime", True,
       "Runtime read = no redeploys; validators reject disallowed values before deployment."),
      ("A service control policy that denies every model except the approved one in all accounts", False,
       "An SCP blocks other models but doesn't tell services which model to use — they'd simply fail."),
      ("Bedrock Intelligent Prompt Routing configured separately in each of the thirty services", False,
       "Prompt routing picks between models in a family per prompt; it isn't central approval of one model.")]),
    ("1.2.4", MC, "H",
     "Version 5 of a fine-tuned model must replace version 4 on an Amazon SageMaker AI endpoint. Version 5 should first "
     "receive 10% of traffic for 30 minutes and must revert automatically if the endpoint's p99 latency alarm fires; "
     "otherwise it should take all traffic. What should the team do?",
     [("Create a separate endpoint for version 5 and adjust weighted Amazon Route 53 records by hand during the window", False,
       "Manual weighting has no automatic revert on the alarm."),
      ("Update the endpoint with a blue/green deployment that uses canary traffic shifting and CloudWatch alarm auto-rollback", True,
       "SageMaker deployment guardrails do exactly this: canary slice, bake time, alarm-based rollback."),
      ("Mark version 5 as Approved in SageMaker Model Registry so that it becomes the active version", False,
       "Approval governs which version may deploy; it doesn't shift traffic or roll back."),
      ("Replace the model artefact in the endpoint's existing S3 location and restart the endpoint", False,
       "All traffic switches at once, with no canary and no automatic rollback.")]),
    ("1.2.4", TWO, "H",
     "A Bedrock model used by a production assistant reaches end-of-life in 60 days. The company wants to move to a "
     "successor with the least risk to users. Which combination of steps should it take?",
     [("Compare candidate successors with a model evaluation job on production-like prompts", True,
       "Proves the replacement's quality before switching."),
      ("Switch to the chosen successor through runtime configuration with a gradual rollout and alarm-based rollback", True,
       "Limits blast radius and can revert automatically."),
      ("Purchase Provisioned Throughput for the current model so that it stays available after end-of-life", False,
       "Capacity purchases don't extend a model's lifecycle."),
      ("Keep the current model ID, because Bedrock forwards calls to the successor model after end-of-life", False,
       "Calls to an end-of-life model fail; there's no automatic forwarding."),
      ("Fine-tune the current model now so that the custom copy remains callable after the base model retires", False,
       "A custom copy depends on the base model and doesn't escape its lifecycle.")]),
    ("2.2.2", MC, "M",
     "A team self-hosts a 34-billion-parameter model at 16-bit precision on SageMaker AI. Its instance has four GPUs "
     "with 24 GB of memory each, so the model does not fit on a single GPU. Precision must not be reduced. How should "
     "the team serve the model?",
     [("Quantise the model to 4-bit so that it fits on one GPU", False,
       "Works for memory, but the requirement forbids lowering precision."),
      ("Use a Large Model Inference container with tensor parallelism across the four GPUs", True,
       "34B × 2 bytes ≈ 68 GB fits across 4 × 24 GB = 96 GB when split with tensor parallelism."),
      ("Lower the maximum output tokens so that the model needs less memory to load", False,
       "Output length doesn't change the memory needed for the weights."),
      ("Run the model on one GPU and let the container spill the remaining weights to the instance's CPU memory", False,
       "Offloading to CPU memory makes inference extremely slow and isn't the standard serving approach.")]),
    ("2.2.1", MC, "M",
     "A fine-tuned Bedrock model serves an internal fraud-review tool with a constant, predictable load around the "
     "clock. The business cannot accept throttled requests. Which deployment option fits best?",
     [("On-demand inference with SDK retries and exponential backoff", False,
       "Still subject to shared-capacity throttling; retries only soften it."),
      ("Provisioned Throughput with a commitment term sized to the steady load", True,
       "Dedicated capacity for steady, predictable volume — the classic way to serve custom models."),
      ("Batch inference jobs submitted every hour", False, "Not interactive; the tool needs responses in real time."),
      ("A cross-Region inference profile for the custom model", False,
       "Cross-Region inference spreads base-model traffic; it doesn't guarantee capacity for a custom model.")]),
    ("2.2.3", MC, "H",
     "In a support assistant, about 80% of questions are routine (order status, opening hours) and 20% are complex "
     "disputes. The company wants to cut model costs without lowering answer quality on the complex disputes. Which "
     "approach fits best?",
     [("Distil one small model from the large model and use it for every question", False,
       "A distilled small model may underperform on the hardest 20%."),
      ("Send every question to a small model and instruct it to reply that a human will follow up when unsure", False,
       "Avoids cost but degrades the complex cases instead of answering them well."),
      ("Answer with a small model first and pass the question to a larger model only when the answer fails validation", True,
       "Cascading: cheap path for routine queries, escalation preserves quality on hard ones."),
      ("Buy Provisioned Throughput for the large model so that each request costs less", False,
       "Doesn't remove the expensive model from routine traffic; can cost more at variable volume.")]),
    ("2.4.4", TWO, "H",
     "Legal questions should reach a large model paired with the legal knowledge base, coding questions should reach a "
     "code-specialised model, and everything else should go to a small model. Compliance wants a reviewable record of "
     "why each request went where it did. Which combination should the team implement?",
     [("A first step that labels each request's category using a small, inexpensive model", True,
       "Determines the category from the request's content."),
      ("An AWS Step Functions Choice state that branches to the matching model call, with execution history retained", True,
       "Branches per category; execution history records each routing decision."),
      ("Bedrock Intelligent Prompt Routing configured across the three different providers", False,
       "Prompt routing works within one model family on predicted quality, not on business categories."),
      ("API Gateway mapping templates that select the model from the request path", False,
       "Clients don't know the category, so the path can't encode it."),
      ("A weighted Lambda alias that sends one third of the traffic to each model", False,
       "Random split ignores the request's content.")]),
    ("2.4.1", MC, "M",
     "A Lambda function behind an API Gateway REST API generates detailed reports that take about three minutes. "
     "Clients receive gateway timeout errors. Users are happy to wait a few minutes for the report. What should the "
     "developer do?",
     [("Raise the Lambda function's timeout to 15 minutes", False,
       "The API Gateway integration still times out long before the report is ready."),
      ("Accept the request, queue the job in Amazon SQS, generate the report in a worker, store it in S3, and let clients check its status", True,
       "Asynchronous pattern decouples the long job from the request's timeout."),
      ("Switch to a much smaller model so that every report is generated within the timeout", False,
       "Changes report quality to fit a timeout instead of fixing the architecture."),
      ("Send each report request as its own Bedrock batch inference job", False,
       "Batch jobs can take hours; users expect minutes.")]),
    ("2.4.2", MC, "H",
     "In an interactive writing assistant, answers must appear word by word, and users can send corrections and "
     "follow-up messages while an answer is still arriving, all within the same open session. What should the team use "
     "between the browser and the backend?",
     [("An API Gateway REST API with Lambda response streaming", False,
       "One-way streaming per request; the user can't send messages on the same channel mid-answer."),
      ("An API Gateway WebSocket API, with Lambda posting each generated chunk to the client's connection", True,
       "Persistent two-way connection fits interactive, bidirectional sessions."),
      ("The browser polling an S3 object for partial results every second", False,
       "Polling adds latency and cost and isn't real time."),
      ("An Amazon SQS FIFO queue per user that the browser reads from", False,
       "Browsers don't consume SQS directly, and it isn't a push channel.")]),
    ("2.4.3", MC, "H",
     "Requests pass through API Gateway, a Lambda function, a knowledge base lookup and a Bedrock model call. After a "
     "release, p95 latency rose from 3 to 9 seconds. The team needs a timing breakdown for individual requests across "
     "every step. What should it use?",
     [("The Lambda Duration metric in Amazon CloudWatch", False,
       "Aggregate timing for Lambda only; no breakdown of downstream calls per request."),
      ("AWS X-Ray tracing on API Gateway and Lambda, with the SDK calls instrumented", True,
       "Per-request traces with a segment per service call show where the time goes."),
      ("AWS CloudTrail events for the Bedrock API calls", False, "Audit records of who called what, not latency breakdowns."),
      ("Bedrock model invocation logging to Amazon S3", False,
       "Records prompts and responses; doesn't time API Gateway, Lambda or retrieval.")]),
    ("2.4.3", THREE, "H",
     "During daily peaks, users of a chat assistant see errors because Bedrock returns ThrottlingException. About half "
     "of the traffic is non-urgent summarisation that can finish within an hour. The team wants fewer user-visible "
     "failures without buying dedicated capacity. Which actions should it take?",
     [("Enable SDK retries with exponential backoff and jitter", True, "Absorbs short bursts of throttling."),
      ("Switch the model ID to a geographic cross-Region inference profile", True,
       "More capacity across Regions at no extra cost."),
      ("Send the non-urgent summarisation requests to an SQS queue processed at a steady rate", True,
       "Smooths peaks so interactive traffic gets the quota."),
      ("Also retry ValidationException errors with backoff", False, "Validation errors need the request fixed; retries won't help."),
      ("Increase the Lambda function's memory allocation", False, "Lambda memory doesn't change Bedrock's quota."),
      ("Raise the Lambda function's reserved concurrency so that more requests run in parallel", False,
       "More parallel calls hit the quota harder and increase throttling.")]),
    ("1.4.5", MC, "M",
     "A knowledge base uses a Confluence data source. Pages change throughout the day, and answers must reflect edits "
     "within about 15 minutes. The team wants a serverless solution with minimal effort. What should it do?",
     [("Delete and re-create the knowledge base every night", False, "Too slow (daily) and wasteful."),
      ("Run StartIngestionJob for the Confluence data source every 15 minutes from Amazon EventBridge Scheduler", True,
       "Scheduled syncs are incremental and serverless."),
      ("Export Confluence pages to S3 by hand each week and sync that bucket instead", False, "Manual and weekly."),
      ("Increase the number of retrieved results so that newer pages are included", False,
       "Retrieval settings can't return content that hasn't been ingested.")]),
    ("1.4.2", MC, "H",
     "Employees in twelve countries use an HR assistant. Policies differ by country, and answers sometimes mix rules "
     "from several countries. Each user's country is available in their sign-in token. What should the team do?",
     [("Add an instruction to the system prompt telling the model to answer using the user's country", False,
       "Other countries' chunks still reach the prompt; instructions aren't reliable filtering."),
      ("Record each document's country as a metadata attribute and filter retrieval using the country from the token", True,
       "Only the user's country's documents are retrieved."),
      ("Create one guardrail per country with denied topics for every other country's policies", False,
       "Twelve guardrails with topic lists is fragile and doesn't stop retrieval mixing."),
      ("Increase the chunk size so that each chunk contains a full country policy", False,
       "Bigger chunks still come from several countries.")]),
    ("1.4.1", MC, "H",
     "A team already runs an Amazon OpenSearch Service cluster with custom analysers and scoring for product search. It "
     "wants to add semantic search using an Amazon Titan embedding model, without writing an embedding pipeline in its "
     "application code. What should it do?",
     [("Create a Bedrock knowledge base with a quick-create OpenSearch Serverless vector store", False,
       "A new store abandons the existing cluster and its custom analysers and scoring."),
      ("Configure neural search in the existing cluster with an ML connector to Amazon Bedrock", True,
       "OpenSearch calls Titan itself at ingest and query time; the app sends text."),
      ("Write a Lambda function that embeds every product and writes the vectors into the cluster", False,
       "This is the embedding pipeline in application code that they want to avoid."),
      ("Migrate the catalogue to Aurora PostgreSQL with pgvector and query it with SQL", False,
       "A migration away from the existing cluster, and still needs embedding code.")]),
    ("1.4.3", MC, "H",
     "A single vector index holds 400 million vectors for five business units. Each query only ever needs one business "
     "unit's data, the units have different freshness requirements, and search latency is too high. What should the "
     "team do?",
     [("Add replica shards to the existing index", False, "Adds read throughput but each query still searches all units' data."),
      ("Create one index per business unit and send each query to its unit's index", True,
       "Smaller per-domain indexes are faster and can be refreshed independently."),
      ("Increase the embedding dimensions to make matches more precise", False, "Larger vectors make search slower."),
      ("Enable hybrid search on the existing index", False, "Changes ranking, not the amount of data searched.")]),
    ("1.4.3", ALL, "H",
     "Which statements about scaling an Amazon OpenSearch Service vector index are correct?",
     [("A query runs on the relevant shards in parallel, and their results are merged", True, "Scatter-gather."),
      ("Replica shards can answer search requests, which increases read throughput", True, "Replicas serve reads."),
      ("Adding replicas reduces the amount of data each primary shard holds", False,
       "Replicas copy shards; primary shard size is unchanged."),
      ("Replicas let the index keep serving when a node holding a primary shard fails", True, "Copies on other nodes take over."),
      ("A search stops at the first shard that returns a matching vector", False, "Every relevant shard is searched for the best matches."),
      ("Approximate nearest-neighbour settings trade search recall against latency", True, "e.g. HNSW ef_search.")]),
    ("1.5.1", MC, "M",
     "A single file contains 2,000 independent question-and-answer pairs of roughly 100 tokens each. After ingestion "
     "with default chunking, retrieved chunks often contain the end of one answer and the start of an unrelated one. "
     "What should the team do?",
     [("Switch to hierarchical chunking with large parent chunks", False, "Large parents merge even more unrelated pairs."),
      ("Use a custom Lambda chunking function that splits the file at each question boundary", True,
       "Each chunk becomes exactly one Q&A pair."),
      ("Increase the fixed-size chunk overlap to 50%", False, "More overlap duplicates text; boundaries still cut across pairs."),
      ("Enable hybrid search so that exact question wording is matched", False, "Ranking can't fix chunks that mix answers.")]),
    ("1.5.2", MC, "H",
     "Users ask questions in Spanish and Portuguese. Documents are in English and Spanish. Retrieval is poor for "
     "Portuguese questions, and the current embedding model was trained mostly on English. What should the team do?",
     [("Increase the current model's embedding dimensions to 1024", False, "More dimensions don't add language understanding."),
      ("Choose an embedding model with strong multilingual support, re-embed the documents, and evaluate retrieval for each language", True,
       "Domain/language fit is the main embedding selection factor; queries and documents must share the model."),
      ("Add a rerank model on top of the current retrieval results", False, "Reranks poor candidates; the right chunks may not be retrieved at all."),
      ("Translate every document into Portuguese with Lambda and keep the current embedding model", False,
       "Triples the corpus and still uses an English-centric model.")]),
    ("1.5.5", MC, "H",
     "Analysts ask questions such as \"How did revenue and headcount change in EMEA and APAC compared with last year?\". "
     "The knowledge base returns chunks covering only one region or one metric. The team wants the least development "
     "effort. What should it do?",
     [("Enable query decomposition on the RetrieveAndGenerate call", True,
       "Built-in: splits the multi-part question into sub-queries and combines results."),
      ("Pass the sessionId from the previous RetrieveAndGenerate call", False, "Helps follow-ups, not multi-part questions."),
      ("Increase the chunk size so that each chunk covers more regions", False, "Doesn't make retrieval cover each part."),
      ("Lower the generation model's temperature", False, "Affects consistency, not retrieval coverage.")]),
    ("1.5.5", MC, "H",
     "Searches for \"cheap flights to Bombay\" miss documents that say \"low-cost fares to Mumbai\". Hybrid search is "
     "already enabled. The team is willing to add a custom step before retrieval. What should it do?",
     [("Have an FM generate alternative phrasings of the question, retrieve for each, and merge the results", True,
       "Query expansion bridges synonyms and renamed entities."),
      ("Split the question into separate sub-questions for flights and destinations", False, "Decomposition doesn't add synonyms."),
      ("Enable implicit metadata filtering on the destination attribute", False, "Filters narrow results; they don't add synonyms."),
      ("Re-embed the documents with more embedding dimensions", False, "Doesn't address vocabulary mismatch.")]),
    ("1.5.6", MC, "M",
     "Three agent teams use different frameworks. All of them must query the same vector store with consistent "
     "authentication and a consistent response format. What should the platform team provide?",
     [("Direct OpenSearch REST access, with each team managing its own credentials and parsing", False,
       "Inconsistent auth and formats across teams."),
      ("A retrieval tool exposed through an MCP server that each team's MCP client calls", True,
       "One standard interface for every framework."),
      ("A separate copy of the index for each team", False, "Triples storage and sync effort; still no common interface."),
      ("Instructions in each agent's system prompt describing how to search the store", False, "Prompts can't execute searches.")]),
    ("1.5.3", MC, "M",
     "A team with no existing database wants managed retrieval-augmented generation over documents in S3, with vectors "
     "stored and managed automatically and the least operational effort. What should it use?",
     [("A Bedrock knowledge base with a quick-create vector store", True, "Fully managed ingestion, embedding and storage."),
      ("A self-managed OpenSearch cluster on Amazon EC2", False, "Most operational effort."),
      ("Amazon RDS for PostgreSQL with pgvector and custom ingestion Lambda functions", False, "Custom pipeline to build and run."),
      ("An Amazon DynamoDB table storing vectors as item attributes", False, "DynamoDB has no vector similarity search.")]),
    ("1.3.3", MC, "M",
     "A chatbot uses the Converse API. Each call sends only the user's latest message, and the model keeps losing track "
     "of earlier parts of the conversation. What should the developer change?",
     [("Send the full alternating user and assistant message history on each call", True,
       "The API is stateless; conversation context must be resent."),
      ("Raise the temperature so that the model infers missing context", False, "Randomness doesn't restore missing context."),
      ("Copy the previous answers into the system prompt on every call", False,
       "Possible but the wrong structure; history belongs in the messages list."),
      ("Switch to a model with a larger context window", False, "Context that isn't sent can't be used, whatever the window.")]),
    ("2.1.1", MC, "H",
     "An agent must remember each customer's preferred language and seat type across conversations weeks apart. Raw "
     "conversation records must be deleted after 7 days. What should the developer implement?",
     [("AgentCore Memory with a 7-day expiry for short-term events and a long-term user-preference strategy per user", True,
       "Raw events expire; extracted preferences persist per user."),
      ("A DynamoDB table of transcripts with a 7-day time to live, loaded at the start of each session", False,
       "Preferences vanish after 7 days with the transcripts."),
      ("The preferences written into the agent's system prompt", False, "One prompt for all users isn't per-user memory."),
      ("A knowledge base that ingests all transcripts nightly", False, "Keeps raw transcripts and isn't per-user memory.")]),
    ("2.1.1", MC, "M",
     "A retailer has twelve specialist agents. Each customer message should reach the single most suitable specialist, "
     "and follow-up messages should keep their conversational context, with minimal custom routing code. What should "
     "the team use?",
     [("AWS Agent Squad with its classifier-based routing", True, "Routes each message to one specialist and keeps context."),
      ("A supervisor agent that sends every message to all twelve specialists and merges the replies", False,
       "Twelve calls per message — slow and expensive."),
      ("A swarm in which specialists hand messages to each other until one accepts", False, "Unpredictable and extra hand-offs."),
      ("One agent that holds all twelve specialists' tools", False, "Too many tools confuses selection.")]),
    ("2.1.2", MC, "H",
     "A team needs an agent loop in which every reasoning step, tool call and tool result is recorded and can be "
     "inspected visually afterwards. The tools are Lambda functions. What should the team build?",
     [("An AWS Step Functions state machine that loops through a model call, a choice of tool, and a Lambda task", True,
       "Each step appears in the execution history and graph."),
      ("A single Lambda function with a while loop that prints each step to its logs", False, "Logs aren't a visual, structured history."),
      ("A Bedrock batch inference job that processes the steps in order", False, "Batch jobs can't run an interactive loop."),
      ("A prompt flow with fixed nodes for three tool calls", False, "Fixed steps can't adapt the number of tool calls.")]),
    ("2.1.3", THREE, "H",
     "An internal agent can call tools that modify HR records. It must never run longer than 5 minutes, never make more "
     "than 20 tool calls per request, and, even if manipulated by a crafted prompt, must not change records outside the "
     "requester's department. Which combination of controls meets these requirements?",
     [("A workflow-level TimeoutSeconds of 300 on the Step Functions state machine", True, "Hard 5-minute cap."),
      ("A loop counter checked by a Choice state that ends the loop after 20 tool calls", True, "Hard cap on tool calls."),
      ("Least-privilege roles for the tool functions plus department-scoped authorisation checks in the tool code", True,
       "Limits damage regardless of what the model asks."),
      ("A higher temperature so that the agent explores fewer repeated tool calls", False, "No guarantee of anything."),
      ("Response streaming so that users can stop long-running answers", False, "User action isn't an enforced limit."),
      ("AWS X-Ray tracing on every tool call", False, "Observability, not prevention."),
      ("Storing every tool result in DynamoDB for later review", False, "Audit after the fact; doesn't stop changes.")]),
    ("2.1.4", MC, "M",
     "Three different models sometimes return different labels for the same content-moderation item. The company "
     "wants a final decision rule that improves accuracy and surfaces uncertain items. Which rule fits best?",
     [("Take the label most models agree on, and send items without a majority to human review", True,
       "Majority vote; disagreement signals uncertainty."),
      ("Always use the label from the model with the highest public benchmark score, and log the others", False,
       "Ignores disagreement, the most useful uncertainty signal."),
      ("Ask a fourth model to rewrite the three labels as one combined sentence", False, "Merging text doesn't produce a decision."),
      ("Use whichever label arrives first to keep latency low", False, "Optimises speed, not accuracy.")]),
    ("2.1.5", MC, "M",
     "A team wants users to rate each answer with thumbs up or down, and later analyse ratings by prompt and model "
     "version. What should it build?",
     [("An API Gateway endpoint and Lambda function that store request ID, prompt, answer, model version and rating in DynamoDB", True,
       "Captures ratings linked to the exact request and version."),
      ("AWS CloudTrail logging of the Bedrock API calls", False, "Records API calls, not user ratings."),
      ("Bedrock model invocation logging alone", False, "Has prompts and answers but no ratings."),
      ("A support email address where users send feedback", False, "Unstructured and unlinked to requests.")]),
    ("2.1.6", TWO, "M",
     "A create_ticket tool receives priority values like \"urgent!!\" and requests with no customer ID. Which "
     "combination makes the tool reliable?",
     [("Restrict priority to an enum in the tool's input schema and mark customer_id as required", True,
       "Prevents most bad calls at the schema level."),
      ("Validate inputs in the tool's Lambda function and return a descriptive error result the model can act on", True,
       "Catches what the schema misses and lets the model correct itself."),
      ("Quietly replace any invalid priority with low without telling the model", False, "Hides errors and creates wrong tickets."),
      ("Increase the model's max tokens so it writes complete parameters", False, "Output length isn't the problem."),
      ("Remove the priority parameter so that it can never be wrong", False, "Loses required functionality.")]),
    ("2.1.7", MC, "H",
     "A document-conversion tool needs 2 GB of libraries, keeps frequently used templates cached in memory, and some "
     "jobs run for 25 minutes. It must be exposed to agents through MCP. Where should the MCP server run?",
     [("AWS Lambda behind API Gateway", False, "15-minute limit and no warm in-memory cache between calls."),
      ("Amazon ECS on AWS Fargate", True, "Long-running, stateful, heavy dependencies."),
      ("An API Gateway mock integration", False, "Returns static responses; can't run the tool."),
      ("An AWS Step Functions Express workflow", False, "Express workflows run at most 5 minutes.")]),
    ("2.1.1", MC, "M",
     "An existing Bedrock agent (Agents Classic) sometimes invents missing values such as order numbers instead of "
     "asking the customer. What should the developer configure?",
     [("Enable the agent's built-in User input capability", True, "Lets the agent ask clarifying questions."),
      ("Mark every action parameter as optional so that the agent can proceed without them", False, "Encourages even more guessing."),
      ("Attach a knowledge base that contains example order numbers", False, "Gives the agent more values to invent from."),
      ("Configure return of control for every action group", False, "Hands execution to the app; doesn't make the agent ask.")]),
    ("2.4.1", MC, "H",
     "A developer's Converse tool loop fails with a validation error after the model requests a tool. The developer "
     "sends the tool's output back as a new message with role assistant containing plain text. What is the correct "
     "way to return tool output?",
     [("A message with role user containing toolResult blocks, each referencing the matching toolUseId", True,
       "Tool results come from the caller's side, as role user with toolResult blocks."),
      ("Add the tool output to the system prompt and resend the original messages", False, "Tool results don't belong in the system prompt."),
      ("Keep role assistant but wrap the output in a toolUse block", False, "toolUse is the model's request, not your result."),
      ("Start a new conversation that contains only the tool output", False, "Loses the conversation and the request ID link.")]),
    ("3.2.1", MC, "H",
     "Lambda functions in private subnets with no NAT gateway must call a Bedrock knowledge base and invoke models. "
     "Security requires that any Bedrock call not arriving through the company's private connections is refused. "
     "What should the team configure?",
     [("Interface endpoints for bedrock-runtime and bedrock-agent-runtime, plus an IAM deny when aws:SourceVpce is not one of them", True,
       "Both runtime APIs over PrivateLink; the condition refuses any other path."),
      ("A gateway endpoint for Amazon S3 and a security group allowing HTTPS", False, "Doesn't reach Bedrock APIs."),
      ("A NAT gateway with a security group restricted to AWS IP ranges", False, "Traffic still crosses the public internet."),
      ("An interface endpoint for the bedrock control-plane service only", False,
       "Inference and retrieval use bedrock-runtime and bedrock-agent-runtime.")]),
    ("3.2.3", MC, "H",
     "Analysts must test prompts on real support transcripts. Names and phone numbers must be replaced with consistent "
     "placeholders so that conversations remain readable. What should the team do?",
     [("Encrypt the transcripts with a customer managed KMS key", False, "Authorised readers still see the PII."),
      ("Detect PII with Amazon Comprehend and replace each entity with a type placeholder such as [NAME] before use", True,
       "Masking/anonymisation keeps utility while removing identities."),
      ("Apply a guardrail that blocks any prompt containing PII", False, "Blocks the transcripts instead of making them usable."),
      ("Add an S3 Lifecycle rule that deletes transcripts after 30 days", False, "Retention, not anonymisation.")]),
    ("3.2.1", MC, "M",
     "An analytics agent queries a data lake through Amazon Athena. It must never see the salary column of the "
     "employees table, while HR analysts can. What should the team use?",
     [("AWS Lake Formation column-level permissions for the agent's role", True, "Fine-grained column access."),
      ("An S3 bucket policy denying the agent access to the employees prefix", False, "Blocks the whole table, not one column."),
      ("A system prompt instruction telling the agent to ignore salaries", False, "Data still reaches the model."),
      ("A guardrail word filter for the word salary", False, "Filters text, not data access.")]),
    ("3.2.2", ALL, "M",
     "Which statements about data privacy in Amazon Bedrock are correct?",
     [("Prompts and responses are not used to train the base models", True, "Correct."),
      ("Prompts are shared with the model provider to improve future versions", False, "Not shared with providers."),
      ("Prompts and outputs are stored only if you enable model invocation logging", True, "Correct."),
      ("A global cross-Region inference profile can process requests outside your geography", True, "Correct."),
      ("Requests are always processed in the Region you call, even when using inference profiles", False,
       "Profiles route to other Regions.")]),
    ("3.2.1", MC, "H",
     "The security team wants an alert within minutes whenever any principal other than an approved application role "
     "invokes Bedrock models in a production account. What should it implement?",
     [("Capture Bedrock API activity with AWS CloudTrail and alert through an EventBridge rule or metric filter on unapproved principals", True,
       "CloudTrail records who called; EventBridge/metric filters alert in near real time."),
      ("Enable model invocation logging to S3 and review the logs monthly", False, "Not within minutes."),
      ("Enable AWS X-Ray sampling on the application", False, "Traces the app, not other principals."),
      ("Attach a guardrail to every model call", False, "Content safety, not access monitoring.")]),
    ("3.1.3", MC, "H",
     "A policy assistant sometimes states facts that aren't in the retrieved documents and sometimes answers a "
     "different question than the user asked. Both kinds of response must be blocked automatically, with minimal "
     "custom code. What should the team configure?",
     [("A guardrail contextual grounding check with both grounding and relevance thresholds", True,
       "Grounding catches unsupported claims; relevance catches off-question answers."),
      ("Temperature 0 and top-p 0.1 on the generation model", False, "Makes output consistent, not grounded."),
      ("A metadata filter that limits retrieval to policy documents", False, "Controls retrieval, not answer faithfulness."),
      ("A rerank model with twice as many retrieved results", False, "Improves context but doesn't block bad answers.")]),
    ("4.2.4", MC, "M",
     "An extraction feature returns slightly different invoice numbers for the same email on repeated runs, although "
     "the number is clearly present in the text. What should the developer change first?",
     [("Lower the temperature", True, "Reduces randomness; the fact is present, so consistency is the issue."),
      ("Increase the maximum output tokens", False, "Length isn't the problem."),
      ("Add a stop sequence after the invoice number", False, "Controls where output ends, not which value is chosen."),
      ("Switch to a model with a larger context window", False, "The email already fits.")]),
    ("5.2.1", MC, "M",
     "Generated summaries regularly end mid-sentence. The response metadata shows the model stopped because of a "
     "length limit. What should the developer do?",
     [("Increase the maximum output tokens for the request", True, "The answer is hitting the max_tokens limit."),
      ("Retry the request with exponential backoff", False, "The same limit applies on retry."),
      ("Lower the temperature to make answers shorter", False, "Temperature doesn't control length reliably."),
      ("Add a stop sequence at the end of each paragraph", False, "Would end answers even earlier.")]),
    ("5.1.5", TWO, "H",
     "Before rolling out a new chunking strategy, a team must show that retrieved passages are more relevant and that "
     "final answers stay faithful to the sources, using managed tooling. Which combination should it run?",
     [("A Bedrock Evaluations retrieve-only RAG evaluation that scores context relevance and coverage", True,
       "Measures retrieval quality."),
      ("A Bedrock Evaluations retrieve-and-generate RAG evaluation that scores faithfulness and correctness", True,
       "Measures answer quality against sources."),
      ("A CloudWatch dashboard of model invocation latency", False, "Performance, not quality."),
      ("A guardrail word filter on the generated answers", False, "Blocks words; doesn't evaluate."),
      ("AWS X-Ray traces of the retrieval calls", False, "Timing, not relevance.")]),
    ("5.2.2", ALL, "H",
     "A client calls Bedrock and receives various errors. Which of these errors should the client fix in the request "
     "or configuration rather than retry with backoff?",
     [("ValidationException because the input is longer than the model's context window", True, "Fix the request."),
      ("AccessDeniedException because the role lacks bedrock:InvokeModel", True, "Fix permissions."),
      ("ThrottlingException during a traffic peak", False, "Retry with backoff."),
      ("ServiceUnavailableException during a brief service disruption", False, "Retry with backoff."),
      ("ModelNotReadyException while capacity is being prepared", False, "Retry with backoff.")]),
]

assert len(Q) == 45, len(Q)
LETTERS = "ABCDEFG"
rng = random.Random(20261026)

n = Note(OUT, "Practice Set 2 — AIP-C01 (Days 1–5 + gap lesson)",
         "Monday 26 Oct 2026 &nbsp;·&nbsp; 45 questions &nbsp;·&nbsp; ~60% hard, ~40% medium &nbsp;·&nbsp; "
         "Official formats: multiple choice (4 options) and multiple response")
n.callout("Instructions",
          "Time limit: <b>105 minutes</b> (~2.3 minutes per question, the real exam's pace). No notes, no searching. "
          "Multiple response questions are graded all-or-nothing. <b>(Select ALL that apply.)</b> questions are an "
          "extra-hard practice format — the real exam always states how many to select. Answer every question (no "
          "penalty for guessing) and mark guesses with <b>(G)</b>. Reply as <b>1-B 2-A,D 3-C …</b>")

# Balance where the correct answer sits in multiple-choice questions (9 each of A-D).
n_mc = sum(1 for q in Q if q[1] == MC)
targets = [k % 4 for k in range(n_mc)]
rng.shuffle(targets)
mc_seen = 0

key = {}
for i, (skill, typ, diff, stem, opts) in enumerate(Q, 1):
    opts = opts[:]
    rng.shuffle(opts)
    if typ == MC:
        right = next(o for o in opts if o[1])
        opts.remove(right)
        opts.insert(targets[mc_seen], right)
        mc_seen += 1
    correct = [LETTERS[j] for j, (_, ok, _) in enumerate(opts) if ok]
    if typ == MC:
        assert len(opts) == 4 and len(correct) == 1, i
    elif typ == TWO:
        assert len(correct) == 2 and len(opts) >= 5, i
    elif typ == THREE:
        assert len(correct) == 3 and len(opts) >= 6, i
    key[i] = {"answer": correct, "skill": skill, "type": typ, "difficulty": diff,
              "options": [[LETTERS[j], t, ok, why] for j, (t, ok, why) in enumerate(opts)], "stem": stem}
    n.h2(f"Question {i}")
    n.p(stem + LABEL[typ])
    for j, (text, _, _) in enumerate(opts):
        n.story.append(Paragraph(f"<b>{LETTERS[j]}.</b> {text}", S["bullet"]))
    n.space(6)

n.page_break()
n.h1("Answer sheet")
rows = [[str(i), "", str(i + 15), "", str(i + 30), ""] for i in range(1, 16)]
n.table(["Q", "Answer", "Q", "Answer", "Q", "Answer"], rows, [0.08, 0.25, 0.08, 0.25, 0.08, 0.26])
n.build()
with open(KEY, "w") as f:
    json.dump(key, f, indent=1)
dist = {}
for v in key.values():
    if v["type"] == MC:
        dist[v["answer"][0]] = dist.get(v["answer"][0], 0) + 1
types = {}
for v in key.values():
    types[v["type"]] = types.get(v["type"], 0) + 1
print(OUT)
print("MC answer distribution:", dict(sorted(dist.items())), "types:", types,
      "hard:", sum(1 for v in key.values() if v["difficulty"] == "H"))
