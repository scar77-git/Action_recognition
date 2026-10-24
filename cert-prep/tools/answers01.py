"""Practice Set 1 answer key: graded against the learner's answers, with an explanation for every option."""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from notelib import S, Note  # noqa: E402
from practice01 import LETTERS, answer_key, shuffled  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Practice_Set_1_2026-10-23_Days_1-3_Answers.pdf")

MY = {1: "CE", 2: "B", 3: "C", 4: "B", 5: "C", 6: "B", 7: "C", 8: "B", 9: "BE", 10: "C",
      11: "A", 12: "C", 13: "D", 14: "B", 15: "C", 16: "A", 17: "A", 18: "D", 19: "D", 20: "A",
      21: "C", 22: "C", 23: "C", 24: "A", 25: "A", 26: "C", 27: "AC", 28: "D", 29: "A", 30: "D"}

# One explanation per option, in the ORIGINAL (unshuffled) option order of practice01.Q.
EXPL = {
    1: ["Hybrid search adds keyword (BM25) matching, which catches exact tokens such as 'Section 14.3(b)'.",
        "More results add noise and tokens; it doesn't put the best chunk first or fix exact-match misses.",
        "A reranker re-scores retrieved chunks so the most relevant one moves to the top.",
        "Chunking changes how text is split, not how exact tokens are matched or ranked.",
        "Heavy effort (custom training) and still weak on exact strings — not 'minimal development'."],
    2: ["Would introduce and operate a new service — the scenario says avoid that.",
        "Aurora PostgreSQL + pgvector is a supported KB vector store and allows SQL joins with existing relational data.",
        "Neptune Analytics is for GraphRAG (relationships), and is a new service for this team.",
        "DynamoDB is not a supported Bedrock Knowledge Base vector store."],
    3: ["Prompts are not an access-control mechanism — the model can still be shown other tenants' chunks.",
        "Metadata filtering at retrieval time ensures other tenants' chunks never reach the prompt. Reliable and low overhead.",
        "Guardrails filter content categories; 400 guardrails with name lists is fragile and high overhead.",
        "Post-processing after generation is too late and unreliable; the data already reached the model."],
    4: ["Bigger chunks don't restore table structure lost during parsing.",
        "FM parsing / Bedrock Data Automation understands tables, layouts and handwriting during ingestion.",
        "Search type affects matching, not how the document was parsed.",
        "Embedding dimensions don't fix structure that was lost before embedding."],
    5: ["Re-creating the KB is slow, wasteful and causes downtime.",
        "Scheduled StartIngestionJob is serverless and syncs incrementally (only changed documents).",
        "Rebuilds what the KB already manages; high effort and bypasses the managed pipeline.",
        "S3 Versioning does not trigger Knowledge Base syncs."],
    6: ["Temperature 0 makes output more deterministic, not grounded in the sources.",
        "The contextual grounding check blocks responses not supported by the retrieved source text.",
        "Metadata filters control which documents are retrieved, not whether the answer is faithful to them.",
        "A larger model can still hallucinate; it doesn't enforce grounding."],
    7: ["The model expects a result for every toolUse; skipping one breaks the conversation.",
        "Correct: append the assistant message, then ONE user message containing all toolResult blocks with matching toolUseIds.",
        "Calling again without results gives the model nothing new — it will ask for the tools again.",
        "Tool results belong in toolResult blocks in a user message, not in the system prompt."],
    8: ["300 agents is huge operational overhead and doesn't solve tool selection.",
        "Gateway exposes the APIs as MCP tools; semantic tool search sends only the relevant tools, fixing both problems.",
        "Output tokens don't affect tool choice or the size of the input prompt.",
        "Fine-tuning is costly, slow and doesn't shrink the tool definitions sent each call."],
    9: ["User input lets the agent ask the user for missing information instead of guessing.",
        "requireConfirmation makes the agent ask for explicit approval before running the function.",
        "Code Interpreter runs code; unrelated to asking for parameters or approvals.",
        "Higher temperature increases randomness — the opposite of what's needed.",
        "A KB provides knowledge; it neither asks the user nor gates destructive actions."],
    10: ["The steps are fixed — a workflow is cheaper, deterministic and auditable; an agent adds unpredictability.",
         "Standard workflows run up to 1 year with full execution history; waitForTaskToken pauses for the approval; retries are built in.",
         "Express workflows run at most 5 minutes — impossible for a 3-day approval.",
         "Polling Lambdas cost money, add code and give no built-in audit trail."],
    11: ["Works, but you manage containers, scaling and session isolation yourself.",
         "AgentCore Runtime: serverless, framework-agnostic, per-session microVM isolation, long-running sessions.",
         "Lambda has a 15-minute limit and no built-in session isolation for agents.",
         "Agents Classic doesn't host LangGraph/Strands code, and new accounts can't use it."],
    12: ["A shared token acts as one identity (not each user) and breaks the 'no tokens in env vars' rule.",
         "AgentCore Identity outbound OAuth gets user-delegated tokens from a token vault — each user's own permissions.",
         "IAM roles authorize access to AWS resources, not GitHub.",
         "Cognito identity pools hand out AWS credentials, not GitHub OAuth tokens."],
    13: ["Huge prompts and cost, and it breaks the 30-day retention requirement.",
         "Short-term events expire at 30 days; the user-preference strategy keeps extracted preferences long-term, per user.",
         "A bigger context window doesn't persist anything across sessions.",
         "A KB is shared document search, not per-user memory, and would keep raw logs."],
    14: ["Calling all three specialists for every request triples cost and latency.",
         "A router sends each request to exactly one specialist — the cheapest, fastest design for single-specialist traffic.",
         "Swarms are unpredictable and add hand-off calls.",
         "120 tools in one agent confuses tool selection and bloats every prompt."],
    15: ["A Python library doesn't help non-Python frameworks or centralize auth.",
         "MCP is the standard tool protocol every framework supports; Gateway centralizes hosting and auth.",
         "Flows are fixed workflows; rebuilding agents as flows loses agent behaviour.",
         "Pasting specs into prompts wastes tokens and doesn't execute or secure anything."],
    16: ["Huge chunks are noisy and the scenario already says large chunks fail.",
         "Hierarchical: small child chunks match precisely; the larger parent chunk gives the model full context.",
         "Whole manuals as one chunk — extremely noisy and may exceed limits.",
         "Semantic chunking splits by topic shifts; it doesn't give 'precise match + bigger context'."],
    17: ["Agents (Classic) add an orchestration loop you don't need, and new accounts can't create them.",
         "Retrieve returns chunks only, so you can filter them, add DynamoDB data and build your own prompt for Converse.",
         "StartIngestionJob syncs data; it doesn't answer queries.",
         "RetrieveAndGenerate is one managed call — no hook to apply business rules or add DynamoDB data between retrieval and generation."],
    18: ["Hybrid search improves term matching, not multi-hop relationships.",
         "GraphRAG with Neptune Analytics connects entities across documents for relationship questions.",
         "Bigger chunks can't capture relationships spread over thousands of documents.",
         "Reranking reorders chunks; it doesn't connect entities across them."],
    19: ["CloudWatch shows operational metrics, not retrieval quality scores.",
         "Bedrock Evaluations RAG (retrieve-only) jobs score context relevance/coverage with LLM-as-a-judge, comparing both KBs.",
         "Manual spot checks aren't managed, repeatable or statistically meaningful.",
         "Grounding checks block unfaithful answers at runtime; they don't evaluate retrieval quality."],
    20: ["The number of results doesn't fix vectors from incompatible embedding spaces.",
         "Query and document vectors must come from the same model; a new embedding model means a new KB + re-ingestion.",
         "Hybrid search can't compensate for a broken semantic half.",
         "A reranker only reorders what retrieval returns; retrieval itself is broken."],
    21: ["Every toolUse needs a toolResult; dropping it breaks the conversation contract.",
         "Return a toolResult with status 'error' and a message — the model can then retry differently or inform the user.",
         "Ending the conversation is poor UX when the model could recover.",
         "Unbounded retries can loop forever and burn tokens; use bounded retries with backoff."],
    22: ["Agents add reasoning loops and cost per document; nothing here needs runtime decisions.",
         "A single structured call per document, run as batch inference (~50% cheaper), fits fixed steps, no real-time need and cost focus.",
         "A supervisor multiplies model calls per document — far more expensive.",
         "Voting multiplies calls and cost for a simple classification."],
    23: ["Changes don't propagate by waiting; DRAFT must be prepared.",
         "PrepareAgent packages DRAFT changes; the built-in test alias (TSTALIASID) points to DRAFT.",
         "Deleting the production alias affects production and doesn't apply DRAFT changes.",
         "Tracing shows behaviour; it doesn't apply unprepared changes."],
    24: ["Direct Connect creates exactly the network path the security team forbids, and is new infrastructure.",
         "Return of control hands the parameters to the application server, which already reaches the inventory system.",
         "A nightly export isn't real-time stock data.",
         "Code Interpreter runs in a sandbox and can't reach the on-premises system."],
    25: ["Prompt text can be changed or ignored by the model and the user.",
         "sessionAttributes persist for the session and are passed to the Lambda event, outside the model's control.",
         "promptSessionAttributes last one turn and are inserted into the prompt, so they're visible to the model.",
         "Long-term memory stores summaries across sessions — not a reliable per-call parameter."],
    26: ["CloudTrail records API calls (who did what), not per-step latency or tokens.",
         "AgentCore Observability traces show each step, tool call, latency and tokens in CloudWatch (needs Transaction Search).",
         "S3 access logs are unrelated to agent execution.",
         "Config tracks resource configuration compliance, not runtime performance."],
    27: ["Inbound JWT authorization (e.g. Cognito) ensures only authenticated callers reach the gateway.",
         "Scoping lambda:InvokeFunction to the specific function ARNs is least privilege for the outbound side.",
         "Public function URLs remove authentication — the opposite of the requirement.",
         "AdministratorAccess violates least privilege.",
         "Embedding access keys in a schema leaks long-term credentials."],
    28: ["Code Interpreter runs agent-generated code (pandas, charts) in an isolated sandbox.",
         "Browser drives websites, not code execution.",
         "eval() of generated code in Lambda is unsafe and not isolated per session.",
         "Gateway exposes tools; it doesn't execute arbitrary generated code."],
    29: ["Timeout/HeartbeatSeconds on the callback task raises States.Timeout; a Catch routes it to escalation.",
         "A Wait state just delays before the task; it can't time out the approval.",
         "Express workflows run max 5 minutes — can't wait 48 hours at all.",
         "Polling adds cost and code for something Step Functions does natively."],
    30: ["Sequential calls add each specialist's latency together.",
         "Independent specialists run in parallel under a supervisor; latency ≈ the slowest one plus synthesis.",
         "A router picks one specialist, but the report needs all three.",
         "One agent working through everything sequentially is slow and mixes concerns."],
}

key = answer_key()
qs = shuffled()
by_task = defaultdict(lambda: [0, 0])
results = {}
for i, (task, _, _) in enumerate(qs, 1):
    ok = sorted(MY[i]) == sorted(key[i])
    results[i] = ok
    by_task[task][1] += 1
    by_task[task][0] += ok
score = sum(results.values())
pct = round(100 * score / len(qs))

n = Note(OUT, "Practice Set 1 — Final Results and Answers",
         f"Friday 23 Oct 2026 &nbsp;·&nbsp; Score: <b>{score} / {len(qs)} ({pct}%)</b> &nbsp;·&nbsp; "
         "AWS pass mark is 750/1000; aim for 75%+ on practice sets")

n.callout("Verdict",
          f"<b>{score}/{len(qs)} = {pct}%</b> on the topics covered so far — a strong first result. All four misses are "
          "'which option is the precise, intended mechanism' errors (exact API, exact limit, exact service support), "
          "which is exactly what the exam tests. They are now in your mistakes log below.", "ok")

n.h1("1. Score by exam task")
rows = []
for task in sorted(by_task, key=lambda t: [int(x) for x in t.split(".")]):
    got, tot = by_task[task]
    rows.append([task, f"{got} / {tot}", "✓ strong" if got == tot else ("½ review" if got / tot >= 0.5 else "✗ weak")])
n.table(["Task", "Score", "Status"], rows, [0.2, 0.4, 0.4])

n.h1("2. Mistakes log — the four misses")
miss_rows = []
for i, (task, stem, opts) in enumerate(qs, 1):
    if results[i]:
        continue
    mine = ", ".join(MY[i])
    right = ", ".join(key[i])
    miss_rows.append([str(i), task, mine, right])
n.table(["Q", "Task", "Your answer", "Correct"], miss_rows, [0.1, 0.15, 0.35, 0.4])
n.table(["Rule to remember", ""], [
    ["Q2 — vector stores", "<b>DynamoDB is not a Knowledge Base vector store.</b> Supported: OpenSearch Serverless, "
     "Aurora PostgreSQL (pgvector), Neptune Analytics, S3 Vectors, and third parties (Pinecone, MongoDB Atlas, Redis). "
     "'Already runs Aurora + SQL joins + no new service' → <b>Aurora pgvector</b>."],
    ["Q7 — tool results", "Tool outputs go in <b>toolResult blocks in ONE user message</b> (matching toolUseIds), "
     "never in the system prompt."],
    ["Q17 — Retrieve vs RetrieveAndGenerate vs agents", "Need <b>custom logic between retrieval and generation</b> "
     "(filter chunks, add other data) → <b>Retrieve + Converse</b>. InvokeAgent adds an unnecessary agent loop."],
    ["Q29 — Step Functions timeouts", "Escalate when nobody answers → <b>TimeoutSeconds / HeartbeatSeconds on the "
     "callback task + Catch States.Timeout</b>. <b>Express max = 5 minutes</b>; Standard up to 1 year."],
], [0.3, 0.7])

n.h1("3. Why the misses happened — reading traps")
n.p("Two of the four misses (Q7 and Q29) were <b>concept-right, letter-wrong</b>: the chosen option started with the "
    "correct idea and ended with the wrong mechanism. Q10 (Standard workflow) was answered correctly, then Q29 picked "
    "an Express workflow — a sign of fatigue, not a knowledge gap.")
n.table(["Q", "Trap", "Habit to build"], [
    ["7", "Option C began 'Run both tools…' (correct) and ended '…in the system prompt' (wrong).",
     "Read every option to the <b>last word</b>; compare options that share an opening."],
    ["29", "Express workflow chosen despite knowing its 5-minute limit (Q10 was right).",
     "Re-check hard limits (time, size, quotas) against the scenario's numbers (48 hours)."],
    ["2", "DynamoDB assumed to be a vector store.", "Memorise the supported KB vector stores list."],
    ["17", "Agent chosen where a simple Retrieve + Converse pipeline fits.",
     "'Custom logic between retrieval and generation' → Retrieve, then build the prompt."],
], [0.07, 0.5, 0.43])
n.callout("Exam technique", "Use <b>Flag for review</b> on any question where two options start the same way, and "
          "revisit flagged questions at the end. Concept score on this set, excluding the two reading errors: "
          "<b>28/30</b>.")

n.h1("4. Clarification — Q7 and the agent loop")
n.p("In the Converse API a <b>'user message'</b> means a message with <b>role: \"user\"</b> in the messages array — "
    "not a message to or from the human. The API only has two roles and they must alternate, so tool results (which "
    "come from your side) are sent in a role \"user\" message.")
n.code('''Call 1 -> messages = [
  { role: "user",      content: [ text: "Status of 1002 and 1003?" ] }       <- the human's question
]
<- model: stopReason = tool_use

Call 2 -> messages = [
  { role: "user",      content: [ text: "Status of 1002 and 1003?" ] },
  { role: "assistant", content: [ toolUse(id=a, get_order_status 1002),      <- model reply, appended as-is
                                  toolUse(id=b, get_order_status 1003) ] },
  { role: "user",      content: [ toolResult(id=a, "PROCESSING"),            <- YOUR tool results:
                                  toolResult(id=b, "DELIVERED") ] }             role "user", ONE message
]
<- model: stopReason = end_turn -> only NOW show the answer to the human''')
n.bullets([
    "Until stopReason is not <b>tool_use</b>, nothing goes to the human — keep looping.",
    "Every call re-sends the <b>whole history</b>: question, every assistant message, every tool-result message.",
])
n.table(["", "Who runs the loop", "Who runs the tool", "How results return"], [
    ["Converse API, your own loop", "<b>You</b>", "You", "toolResult blocks in a role 'user' message"],
    ["Bedrock Agents, return of control", "<b>Bedrock Agents</b>", "Your app (that one action)",
     "Next InvokeAgent call, sessionState.returnControlInvocationResults"],
    ["Bedrock Agents, Lambda action group", "Bedrock Agents", "Lambda", "Handled by Bedrock"],
], [0.28, 0.2, 0.22, 0.3])

n.h1("5. Readiness on the topics covered so far")
n.table(["Task", "Confidence", "Evidence and gap"], [
    ["2.1 Agents and tools", "High (~85%)", "14/16; agent loop well understood; misses were reading errors."],
    ["1.4 Vector stores", "Medium-high (~75%)", "Chunking, sync, GraphRAG solid. Gap: supported vector stores."],
    ["1.5 Retrieval", "Medium-high (~75%)", "Hybrid, rerank, filters solid. Gap: Retrieve vs RetrieveAndGenerate."],
], [0.25, 0.2, 0.55])
n.p("Overall: about <b>8 out of 10</b> on real exam questions for these tasks. Expect real-exam scores 5–10 points "
    "below self-made practice sets. To raise it: 10 minutes of mistakes-log review each morning, read every option "
    "to the end, and Practice Set 2 (31 Oct) will re-test 5 questions from Days 1–3.")

n.page_break()
n.h1("6. Every question explained")
for i, (task, stem, opts) in enumerate(qs, 1):
    mark = "✓" if results[i] else "✗"
    n.h2(f"Question {i} &nbsp;·&nbsp; Task {task} &nbsp;·&nbsp; {mark} you answered {', '.join(MY[i])}, "
         f"correct {', '.join(key[i])}")
    n.p(stem)
    for j, (orig, text, ok) in enumerate(opts):
        letter = LETTERS[j]
        tag = "<b>✓ CORRECT</b>" if ok else "✗"
        picked = " <i>(your choice)</i>" if letter in MY[i] else ""
        n.story.append(Paragraph(f"<b>{letter}.</b> {text}{picked}<br/>{tag} — {EXPL[i][orig]}", S["bullet"]))
    n.space(6)

n.build()
print(os.path.abspath(OUT), score, pct)
