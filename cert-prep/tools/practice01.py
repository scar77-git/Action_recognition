"""Practice Set 1 (Days 1-3): question paper PDF + answer key kept out of the repo."""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import S, Note  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Practice_Set_1_2026-10-23_Days_1-3_Questions.pdf")

# (task, stem, [(option, is_correct), ...]); a stem containing "(Choose TWO)" has two correct options.
Q = [
    ("1.5", "<b>(Choose TWO)</b> A law firm uses an Amazon Bedrock Knowledge Base over 20,000 contracts. Natural-language "
     "questions work well, but queries containing exact clause references such as 'Section 14.3(b)' often return "
     "irrelevant chunks, and when the right chunk is returned it is usually ranked 7th or 8th. The firm wants to fix "
     "both problems with minimal custom development. Which actions should it take?",
     [("Switch the Knowledge Base search type to hybrid search.", True),
      ("Increase the number of retrieved results to 100.", False),
      ("Add an Amazon Bedrock rerank model to the retrieval configuration.", True),
      ("Re-create the data source with semantic chunking.", False),
      ("Fine-tune the embedding model on legal terminology.", False)]),
    ("1.4", "A company is building a RAG application on Amazon Bedrock Knowledge Bases. Its data team already operates "
     "Amazon Aurora PostgreSQL and wants to store the vectors where it can also join them with existing relational "
     "metadata using SQL. The company wants to avoid introducing and operating a new database service. Which vector "
     "store should it choose?",
     [("Amazon OpenSearch Serverless", False),
      ("Amazon Aurora PostgreSQL with the pgvector extension", True),
      ("Amazon Neptune Analytics", False),
      ("Amazon DynamoDB", False)]),
    ("1.5", "A SaaS provider serves 400 tenants from a single Bedrock Knowledge Base. Documents from one tenant must "
     "never appear in another tenant's answers. The solution must enforce isolation reliably with the least "
     "operational overhead. What should a developer do?",
     [("Add a system prompt instruction telling the model to answer only with the current tenant's documents.", False),
      ("Attach a tenant_id metadata attribute to every document and apply a metadata filter in each Retrieve call, "
       "set from the caller's authenticated tenant.", True),
      ("Create one Amazon Bedrock guardrail per tenant with denied topics for the other tenants' names.", False),
      ("Post-process every response with an AWS Lambda function that removes other tenants' names.", False)]),
    ("1.3", "An insurer ingests scanned claim forms as PDFs. Each contains tables of line items and some handwritten "
     "notes. The Knowledge Base returns wrong totals because the table structure is lost during ingestion. Which "
     "change most directly fixes the problem?",
     [("Increase the fixed chunk size to 1,000 tokens.", False),
      ("Configure the data source to use foundation-model parsing or Amazon Bedrock Data Automation as the parser.", True),
      ("Switch the search type from semantic to hybrid.", False),
      ("Use a higher-dimension embedding model.", False)]),
    ("1.4", "Product manuals in an Amazon S3 bucket are updated several times a day. The Bedrock Knowledge Base must "
     "reflect changes within one hour, using a serverless approach with the least effort. What should the developer "
     "implement?",
     [("Delete and re-create the Knowledge Base every hour.", False),
      ("An Amazon EventBridge Scheduler schedule that calls StartIngestionJob for the data source every hour.", True),
      ("A Lambda function that re-embeds every document and writes vectors directly into the OpenSearch index.", False),
      ("Enable S3 Versioning on the bucket so the Knowledge Base detects new object versions automatically.", False)]),
    ("3.1", "A customer support assistant built on a Bedrock Knowledge Base sometimes states refund amounts that do not "
     "appear anywhere in the retrieved policy documents. The company must block these unsupported responses with "
     "minimal custom code. What should a developer do?",
     [("Set the model's temperature to 0.", False),
      ("Configure an Amazon Bedrock guardrail with a contextual grounding check and apply it to responses.", True),
      ("Add metadata filters to the retrieval query.", False),
      ("Switch to a larger foundation model.", False)]),
    ("2.1", "A developer builds a custom agent loop with the Amazon Bedrock Converse API. A response returns stopReason "
     "tool_use with two toolUse blocks. What should the application do next?",
     [("Call Converse again with the same messages so the model can confirm which tool to use.", False),
      ("Run both tools, append the assistant message, then send one user message containing two toolResult blocks "
       "with the matching toolUseId values.", True),
      ("Run only the first tool and ignore the second until the next turn.", False),
      ("Run both tools and place their outputs in the system prompt of the next call.", False)]),
    ("2.1", "An enterprise wants agents to use 300 internal REST APIs as tools. In testing, the agent often picks the "
     "wrong API, and prompts become very large because every tool definition is sent on every call. Which solution "
     "addresses both problems with the least custom code?",
     [("Create one dedicated agent for each API.", False),
      ("Expose the APIs through Amazon Bedrock AgentCore Gateway with OpenAPI targets and semantic tool search "
       "enabled, so agents retrieve only the relevant tools.", True),
      ("Increase the model's maximum output tokens.", False),
      ("Fine-tune the foundation model on the API documentation.", False)]),
    ("2.1", "<b>(Choose TWO)</b> A team operates an existing Amazon Bedrock agent (Agents Classic). The agent must stop "
     "guessing missing parameters and ask the user for them instead. It must also obtain the user's explicit approval "
     "before running the delete_account function. Which configurations meet these requirements?",
     [("Enable the built-in User input action group.", True),
      ("Enable user confirmation (requireConfirmation) on the delete_account function.", True),
      ("Enable the Code Interpreter action group.", False),
      ("Raise the model's temperature so it explores alternatives.", False),
      ("Attach a Knowledge Base containing the account policies.", False)]),
    ("2.1", "A bank's mortgage process has fixed steps: extract documents, generate a risk summary with an LLM, wait for "
     "a human underwriter's approval (which can take up to 3 days), then notify the applicant. The bank needs a full "
     "audit history and automatic retries. What should a developer use?",
     [("An Amazon Bedrock agent with long-term memory to track each application.", False),
      ("An AWS Step Functions Standard workflow with a Bedrock InvokeModel task and a .waitForTaskToken callback "
       "step for the approval.", True),
      ("An AWS Step Functions Express workflow with a callback step for the approval.", False),
      ("A chain of Lambda functions that polls a database for the approval every minute.", False)]),
    ("2.1", "A company has agents built with LangGraph and with Strands Agents. It needs serverless hosting with "
     "per-user session isolation, support for sessions that run for several hours, and no container clusters to "
     "manage. Which service fits best?",
     [("Amazon ECS on AWS Fargate behind an Application Load Balancer", False),
      ("Amazon Bedrock AgentCore Runtime", True),
      ("AWS Lambda, one function per agent", False),
      ("Amazon Bedrock Agents (Classic) inline agents", False)]),
    ("2.1", "An internal agent must create issues in each user's own GitHub repositories using that user's permissions. "
     "Security policy forbids storing tokens in agent code or environment variables. What should the developer use?",
     [("A single shared GitHub personal access token stored in a Lambda environment variable.", False),
      ("An Amazon Bedrock AgentCore Identity outbound OAuth credential provider that obtains user-delegated tokens "
       "from its token vault for each authenticated user.", True),
      ("An IAM role with a trust policy for GitHub.", False),
      ("An Amazon Cognito identity pool that maps users to GitHub accounts.", False)]),
    ("2.1", "A travel assistant must remember each user's preferences (aisle seat, vegetarian meals) across "
     "conversations months apart. Raw conversation history must expire after 30 days for compliance. What should "
     "the developer implement?",
     [("Store full transcripts in Amazon DynamoDB and include the entire history in every prompt.", False),
      ("Amazon Bedrock AgentCore Memory with a 30-day short-term event expiry and a long-term user-preference "
       "strategy using per-user namespaces.", True),
      ("Use a model with a larger context window.", False),
      ("Ingest chat logs nightly into a Bedrock Knowledge Base.", False)]),
    ("2.1", "A customer service platform has billing, technical-support and sales agents. Analysis shows 95% of "
     "requests need exactly one specialist. The company wants the lowest latency and cost. Which design should it use?",
     [("A supervisor agent that sends every request to all three specialists and merges the answers.", False),
      ("A router/classifier that sends each request to the single best specialist, such as AWS Agent Squad or a "
       "supervisor in routing mode.", True),
      ("A swarm in which specialists pass the request among themselves.", False),
      ("One agent that holds all 120 tools from the three teams.", False)]),
    ("2.1", "Five teams build agents with different frameworks (Strands, LangGraph, CrewAI), and each team has written "
     "its own integration to the same internal ticketing and CRM tools. The company wants to write each tool once, "
     "reuse it across all frameworks and manage its authentication centrally. What should it do?",
     [("Publish a shared Python library that every team imports.", False),
      ("Expose the tools as MCP servers served centrally, for example through Amazon Bedrock AgentCore Gateway.", True),
      ("Rebuild every agent as an Amazon Bedrock Flow.", False),
      ("Paste each tool's OpenAPI specification into every agent's system prompt.", False)]),
    # ---------------------------------------------------------------- 16-30
    ("1.4", "A manufacturer's maintenance manuals contain long procedures. With small fixed-size chunks, answers are "
     "precise but miss the preceding safety steps; with large chunks, retrieval returns noisy, loosely related text. "
     "The team wants precise matching and full surrounding context in the prompt. Which chunking strategy should it "
     "use?",
     [("Fixed-size chunking with 1,500-token chunks and 50% overlap", False),
      ("Hierarchical chunking with small child chunks and larger parent chunks", True),
      ("No chunking, so each manual is one chunk", False),
      ("Semantic chunking with a very high breakpoint threshold", False)]),
    ("1.5", "A developer must retrieve policy chunks from a Bedrock Knowledge Base, drop chunks that fail custom "
     "business rules, add the customer's account details from Amazon DynamoDB to the prompt, and then call a "
     "foundation model. Which approach should the developer use?",
     [("Call RetrieveAndGenerate with a custom prompt template.", False),
      ("Call the Retrieve API, apply the business rules in application code, build the prompt, then call the "
       "Converse API.", True),
      ("Call InvokeAgent with the Knowledge Base attached.", False),
      ("Call StartIngestionJob with a custom Lambda transformation.", False)]),
    ("1.4", "A compliance team needs answers that depend on relationships spread across thousands of documents, such "
     "as 'Which of our suppliers are subsidiaries of companies headquartered in a sanctioned country?'. Standard "
     "vector retrieval returns isolated chunks that miss these connections. Which solution is most appropriate?",
     [("Switch the existing OpenSearch Serverless store to hybrid search.", False),
      ("Use a Bedrock Knowledge Base with Amazon Neptune Analytics as the vector store to enable GraphRAG.", True),
      ("Increase the chunk size so more relationships fit in each chunk.", False),
      ("Add a rerank model to the retrieval configuration.", False)]),
    ("5.1", "A team changed the chunking strategy of its Knowledge Base and must prove retrieval quality improved before "
     "rollout. It wants a managed approach that scores retrieval with LLM-as-a-judge metrics such as context relevance "
     "and context coverage on a prompt dataset. What should it use?",
     [("Amazon CloudWatch metrics for the Knowledge Base", False),
      ("An Amazon Bedrock Evaluations RAG evaluation (retrieve-only) job run against both Knowledge Bases with the "
       "same prompt dataset", True),
      ("Manual spot checks of 20 answers by the support team", False),
      ("A Bedrock guardrail contextual grounding check", False)]),
    ("1.4", "Documents in a Knowledge Base were embedded with Amazon Titan Text Embeddings V2. A developer changes the "
     "application to embed user queries with a different embedding model before running a vector search, and "
     "retrieval quality collapses. What is the cause and the correct fix?",
     [("The vector index is too small; increase the number of results.", False),
      ("Queries and documents must be embedded with the same model; to switch models, create a new Knowledge Base "
       "with the new embedding model and re-ingest the documents.", True),
      ("Hybrid search is disabled; enable it to compensate.", False),
      ("The rerank model is missing; add one to fix ranking.", False)]),
    ("2.4", "In a Converse API tool loop, a tool call fails because a downstream inventory API times out. The model "
     "should be able to recover, for example by retrying differently or telling the user. What should the "
     "application send back?",
     [("Nothing; drop the toolUse block and call Converse again without a result.", False),
      ("A toolResult with the same toolUseId, status set to error, and an error message as content.", True),
      ("An exception message directly to the end user, ending the conversation.", False),
      ("The same tool request again in an unbounded retry loop until it succeeds.", False)]),
    ("2.1", "A company must classify 2 million documents per month into five fixed categories. The steps never change, "
     "results are not needed in real time, and cost is the top priority. Which design is most appropriate?",
     [("An agent with classification tools that reasons about each document", False),
      ("One foundation model call per document with a structured output format, run as a batch job", True),
      ("A supervisor agent that delegates each document to five category specialists", False),
      ("A swarm of agents that vote on each document's category", False)]),
    ("2.1", "A developer updates an action group's OpenAPI schema on an existing Bedrock agent (Agents Classic). When "
     "testing through the built-in test alias, the agent still behaves as before. What should the developer do?",
     [("Wait up to 24 hours for the change to propagate.", False),
      ("Prepare the agent (PrepareAgent) and test again against the test alias, which points to the DRAFT version.", True),
      ("Delete and re-create the production alias.", False),
      ("Enable tracing; the change is applied but not visible.", False)]),
    ("2.1", "A retail agent must check stock in an on-premises inventory system that is reachable only from the "
     "company's own application servers. The security team prohibits any network path from AWS into the data center "
     "and does not want new network infrastructure. How should the action be implemented with Bedrock Agents "
     "(Classic)?",
     [("A Lambda function in a VPC connected to the data center through AWS Direct Connect", False),
      ("An action group configured with return of control, so the application server runs the inventory call and "
       "returns the result to the agent", True),
      ("A Knowledge Base synced nightly from an inventory export", False),
      ("The Code Interpreter action group calling the inventory system", False)]),
    ("2.1", "During a session, every action group call of a Bedrock agent (Agents Classic) needs the authenticated "
     "customer's ID. The agent must not ask the user for it, and the model must not be able to change it. How should "
     "the application provide the ID?",
     [("Include the customer ID in the text of each user prompt.", False),
      ("Pass it in sessionAttributes on InvokeAgent; the Lambda function reads it from the event's sessionAttributes.", True),
      ("Pass it in promptSessionAttributes on the first turn only.", False),
      ("Store it in the agent's long-term memory.", False)]),
    ("4.3", "A production agent hosted on Amazon Bedrock AgentCore Runtime shows latency spikes. The team must find "
     "which tool call is slow and how many tokens each step uses. What should it use?",
     [("AWS CloudTrail management events", False),
      ("AgentCore Observability traces in Amazon CloudWatch, with CloudWatch Transaction Search enabled", True),
      ("Amazon S3 server access logs", False),
      ("AWS Config rules", False)]),
    ("3.2", "<b>(Choose TWO)</b> A company exposes Lambda functions as tools through Amazon Bedrock AgentCore Gateway. "
     "Only authenticated agent applications may call the gateway, and the gateway must call the Lambda functions with "
     "least privilege. Which configurations meet these requirements?",
     [("Configure the gateway's inbound authorization with a JWT authorizer, such as an Amazon Cognito user pool.", True),
      ("Give the gateway's service role lambda:InvokeFunction scoped to the specific function ARNs.", True),
      ("Make each Lambda function URL public so the gateway can reach it.", False),
      ("Attach the AdministratorAccess policy to the gateway's service role.", False),
      ("Embed AWS access keys for the Lambda functions in the tool schema.", False)]),
    ("2.1", "An analytics agent must load a user-uploaded CSV file, run pandas code it writes itself and return a "
     "chart. The generated code must run in an isolated sandbox. Which capability should the agent use?",
     [("Amazon Bedrock AgentCore Code Interpreter", True),
      ("Amazon Bedrock AgentCore Browser", False),
      ("A Lambda function that runs the generated code with eval()", False),
      ("Amazon Bedrock AgentCore Gateway", False)]),
    ("2.1", "A Step Functions workflow pauses at a .waitForTaskToken step for a manager's approval. If nobody responds "
     "within 48 hours, the request must be escalated automatically. How should the developer implement this?",
     [("Set TimeoutSeconds (or HeartbeatSeconds) on the callback task and add a Catch for States.Timeout that "
       "routes to an escalation branch.", True),
      ("Add a 48-hour Wait state before the callback task.", False),
      ("Convert the workflow to an Express workflow.", False),
      ("Add a Lambda function that polls the approval status every minute for 48 hours.", False)]),
    ("2.1", "A research assistant must produce one report that combines analysis from market-data, legal and financial "
     "specialist agents. The specialists work independently of each other. The company wants to minimize end-to-end "
     "latency. Which design is best?",
     [("A sequential workflow that calls the three specialists one after another", False),
      ("A supervisor (agents-as-tools) that invokes the three specialists in parallel and synthesizes their results", True),
      ("A router that sends the request to the single most relevant specialist", False),
      ("One agent with all specialists' tools that works through them one by one", False)]),
]

LETTERS = "ABCDE"


def shuffled():
    """Questions with options in the printed order: [(task, stem, [(orig_idx, text, ok), ...]), ...]."""
    rng = random.Random(20261023)
    out = []
    for task, stem, opts in Q:
        indexed = [(k, text, ok) for k, (text, ok) in enumerate(opts)]
        rng.shuffle(indexed)
        out.append((task, stem, indexed))
    return out


def answer_key():
    return {i: [LETTERS[j] for j, (_, _, ok) in enumerate(opts) if ok]
            for i, (_, _, opts) in enumerate(shuffled(), 1)}


def main():
    n = Note(OUT, "Practice Set 1 — AIP-C01 (Days 1–3)",
             "Friday 23 Oct 2026 &nbsp;·&nbsp; 30 questions &nbsp;·&nbsp; Mixed medium and hard &nbsp;·&nbsp; "
             "Exam tasks 1.3–1.5, 2.1, 2.4, 3.1, 3.2, 4.3, 5.1")
    n.callout("Instructions",
              "Time limit: <b>75 minutes</b> (the real exam allows about 2.4 minutes per question). No notes, no searching. "
              "Questions marked <b>(Choose TWO)</b> need exactly two answers. Mark any answer you guessed with <b>(G)</b>. "
              "Reply in the form <b>1-A,C &nbsp;2-B &nbsp;3-D …</b>. The answer key with explanations comes after you answer.")
    for i, (_, stem, opts) in enumerate(shuffled(), 1):
        n.h2(f"Question {i}")
        n.p(stem)
        for j, (_, text, _) in enumerate(opts):
            n.story.append(Paragraph(f"<b>{LETTERS[j]}.</b> {text}", S["bullet"]))
        n.space(6)
    n.page_break()
    n.h1("Answer sheet")
    rows = [[str(i), "", str(i + 15), ""] for i in range(1, 16)]
    n.table(["Q", "Your answer", "Q", "Your answer"], rows, [0.1, 0.4, 0.1, 0.4])
    n.build()
    print(os.path.abspath(OUT))


if __name__ == "__main__":
    main()
