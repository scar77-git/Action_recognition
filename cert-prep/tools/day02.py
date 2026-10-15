"""Day 2 note: Agents and Tool Calling."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import Note  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Day_2_2026-10-14_Agents_and_Tool_Calling.pdf")

n = Note(OUT, "Day 2 — Agents and Tool Calling",
         "Wednesday 14 Oct 2026 &nbsp;·&nbsp; AWS AIP-C01 exam task covered: <b>2.1 Agentic AI and tool "
         "integrations (part A)</b> &nbsp;·&nbsp; Exam: Sat 7 Nov")

n.callout("Today in one paragraph",
          "An agent is a model plus instructions, tools and memory running in a <b>loop</b>: it decides at runtime "
          "which tool to call, observes the result and repeats until it can answer. The model never executes a "
          "tool itself — it only <i>requests</i> one, and your code (or Bedrock Agents' Lambda) runs it. Bedrock "
          "Agents packages this loop (action groups, return of control, memory, aliases), but it is now "
          "<b>Agents Classic in maintenance mode</b> and blocked for new accounts, so the hands-on path is the "
          "Converse API tool loop today and AgentCore / Strands tomorrow.", "ok")

# ---------------------------------------------------------------- warm-up results
n.h1("1. Warm-up results (Day 1 recall) — 3.5 / 5")
n.table(["#", "Question", "Your answer", "Verdict and correct answer"], [
    ["1", "KB quick-create vector store; why delete after lab?", "OpenSearch; billed per hour even when idle",
     "✓ Correct. Precisely: <b>OpenSearch Serverless</b>, billed in OCU-hours with a minimum."],
    ["2", "Can chunking be changed after creation?", "No — create a fresh data store",
     "½ Idea right, term wrong: create a new <b>data source</b> (or new KB) and <b>re-sync</b>."],
    ["3", "'error E-4031' returns irrelevant chunks", "Hybrid search",
     "✓ Correct — the keyword (BM25) side matches the exact token."],
    ["4", "Guardrails feature for answers not supported by retrieved docs", "Metadata filtering during prompt augmentation",
     "✗ Wrong. Answer: <b>Guardrails contextual grounding check</b>. Also, metadata filtering happens at "
     "<b>retrieval</b>, not augmentation."],
    ["5", "Two parsing options for table-heavy PDFs", "Bedrock Data Automation; FM parsing",
     "✓ Correct (Textract also valid for scanned pages)."],
], [0.04, 0.27, 0.27, 0.42])

# ---------------------------------------------------------------- concepts
n.h1("2. What an agent is")
n.code("AGENT = model + instructions + tools + memory + a LOOP")
n.table(["Approach", "What it does", "Who decides the steps"], [
    ["Plain LLM call", "Prompt in, answer out", "Nobody — single step"],
    ["RAG", "Retrieve once, then answer", "You (fixed)"],
    ["Workflow (Step Functions, Bedrock Flows)", "Predefined sequence of steps", "You, in advance"],
    ["Agent", "Chooses at runtime which tool, how often, in what order", "<b>The model</b>"],
], [0.3, 0.42, 0.28])
n.p("<b>ReAct loop (Reason + Act)</b> — the default Bedrock Agents orchestration:")
n.code('User: "Cancel my order 1001 if it hasn\'t shipped"\n'
       "  Thought: need the status first        -> Action: get_order_status(1001)\n"
       "  Observation: SHIPPED\n"
       "  Thought: shipped, cannot cancel       -> Final answer")
n.callout("Exam rule", "Known, fixed steps → <b>workflow</b> (cheaper, deterministic, auditable). "
          "Path depends on intermediate results → <b>agent</b>.")

n.h1("3. Tool calling — the mechanics")
n.numbered([
    "You send the model tool definitions: <b>name, description, JSON schema</b> of parameters.",
    "The model replies with a tool request — Converse API: <b>stopReason = \"tool_use\"</b> plus a "
    "<b>toolUse</b> block (name, input, toolUseId).",
    "<b>Your code executes the tool.</b> The model never runs anything.",
    "You send a <b>toolResult</b> (same toolUseId) back as a user message; the model continues the loop.",
])
n.bullets([
    "Tool <b>descriptions are prompts</b>: vague description → wrong tool chosen. First fix is better "
    "descriptions + instructions, not a bigger model.",
    "Build the loop yourself with <b>Converse API + toolConfig</b>, or let <b>Bedrock Agents</b> (Classic) / "
    "<b>AgentCore</b> run it.",
])

n.h1("4. Bedrock Agents (Classic) — components")
n.table(["Component", "What it is", "Exam angle"], [
    ["Model + instructions", "The FM the agent reasons with, plus its role/rules in natural language.", "Instructions shape tool use."],
    ["Action groups", "The tools. Defined by an <b>OpenAPI schema</b> or <b>function details</b>.", "One action group can hold several functions."],
    ["↳ Lambda executor", "Bedrock invokes your Lambda with the parameters.", "Most common."],
    ["↳ Return of control", "Bedrock returns the parameters <b>to your application</b>; your app executes and sends results back on the next InvokeAgent call.",
     "Action must run in the app's context (authenticated session, on-prem, long-running, UI)."],
    ["Built-in action groups", "<b>User input</b> (ask clarifying questions), <b>Code Interpreter</b> (write/run code: maths, charts, files).",
     "'Agent must ask for missing info' → User input."],
    ["Knowledge Bases", "Attach a KB with a description of when to use it.", "Agent decides when to retrieve."],
    ["User confirmation", "<b>requireConfirmation</b> on a function — asks before executing.", "Destructive actions."],
    ["Guardrails", "Attach a guardrail to filter inputs/outputs.", "Day 6."],
    ["Memory", "<b>sessionAttributes</b> (whole session), <b>promptSessionAttributes</b> (single turn); "
     "<b>long-term memory</b> = session summaries kept for N days under a memoryId.", "'Remember users across sessions' → long-term memory."],
    ["Advanced prompts", "Override pre-processing, orchestration, KB-response and post-processing templates; custom orchestration Lambda.", "Fine control."],
    ["Trace", "<b>enableTrace</b> shows rationale, invocation inputs, observations.", "How to debug 'why did it do that?'"],
    ["Versions and aliases", "Edit <b>DRAFT</b> → Prepare → <b>version</b> → <b>alias</b> points at a version. Apps call InvokeAgent(agentId, aliasId).",
     "Rollback = repoint alias. Production never calls DRAFT."],
], [0.2, 0.5, 0.3])
n.h2("Two permissions that trip people up")
n.numbered([
    "The <b>agent service role</b> needs bedrock:InvokeModel (and KB Retrieve if a KB is attached).",
    "The <b>Lambda needs a resource-based policy</b> allowing <b>bedrock.amazonaws.com</b> to invoke it. "
    "'Access denied calling the Lambda' → this is missing.",
])

n.h1("5. Lambda contract (function details)")
n.p("Bedrock sends:")
n.code('{ "actionGroup": "OrderActions", "function": "get_order_status",\n'
       '  "parameters": [{"name": "order_id", "type": "string", "value": "1002"}],\n'
       '  "sessionAttributes": {}, "promptSessionAttributes": {} }')
n.p("Your Lambda must return exactly this shape:")
n.code('{ "messageVersion": "1.0",\n'
       '  "response": { "actionGroup": "OrderActions", "function": "get_order_status",\n'
       '    "functionResponse": { "responseBody": { "TEXT": { "body": "Order 1002: PROCESSING" } } } } }')
n.p("OpenAPI-schema variant: input has <b>apiPath</b> and <b>httpMethod</b>; response has <b>httpStatusCode</b> "
    "and <b>responseBody[\"application/json\"]</b>.")

n.h1("6. Decision rules")
n.numbered([
    "Fixed, known steps → <b>Step Functions / Bedrock Flows</b>, not an agent.",
    "Managed agent, least effort → Bedrock Agents (Classic) / <b>AgentCore</b>. Full control → <b>Converse API with toolConfig</b>.",
    "Action must run inside the client app → <b>return of control</b>.",
    "Agent must ask for missing details → <b>User input</b>.",
    "Destructive action → <b>user confirmation</b> + guardrail.",
    "Wrong tool chosen → improve <b>descriptions and instructions</b>; verify with the <b>trace</b>.",
    "Remember users across sessions → <b>long-term memory</b>.",
    "Safe release and rollback → <b>aliases</b> pointing at versions.",
    "Agent can't invoke Lambda → Lambda <b>resource-based policy</b>.",
    "Maths / data analysis / charts → <b>Code Interpreter</b>.",
])
n.p("<b>Azure mapping:</b> Foundry Agent Service = agent + <b>threads / messages / runs</b>; tools include function "
    "calling, OpenAPI, Azure Functions, AI Search, file search, code interpreter. A run in status "
    "<b>requires_action</b> is Azure's return of control.")

n.h1("7. Industry update — Bedrock Agents Classic maintenance mode")
n.bullets([
    "Bedrock Agents is now <b>Bedrock Agents Classic</b>, in <b>maintenance mode</b> since <b>30 July 2026</b>.",
    "Accounts without Agents usage in the previous 12 months get <b>403</b> on <b>CreateAgent</b> and "
    "<b>InvokeInlineAgent</b>. No exception process — this is why your lab was blocked.",
    "Knowledge Bases, Guardrails and models are <b>not affected</b>.",
    "AWS's recommended path: <b>Amazon Bedrock AgentCore</b> (managed harness, Runtime, Gateway, Memory, "
    "Identity, Observability).",
    "<b>Exam impact:</b> the AIP-C01 guide predates this; Task 2.1 names <b>Strands Agents, AWS Agent Squad, "
    "MCP and Step Functions</b>. Know Agents Classic concepts <i>and</i> AgentCore.",
])

# ---------------------------------------------------------------- lab
n.h1("8. Lab work")
n.table(["Step", "Status"], [
    ["Planned: OrderHelper in Bedrock Agents console (action group + Lambda + confirmation + alias)",
     "Blocked — 'Bedrock Agents is in Maintenance Mode' (new account)."],
    ["Replacement: OrderHelper with the Converse API tool loop in Python",
     "<b>Pending</b> — waiting for the account's on-demand tokens-per-minute (TPM) quota for the model."],
], [0.65, 0.35])
n.p("Replacement lab code (run it once the quota is available):")
n.code('''import boto3

brt = boto3.client("bedrock-runtime", region_name="us-east-1")
MODEL_ID = "us.amazon.nova-lite-v1:0"   # check the exact ID / inference profile in the console

ORDERS = {"1001": "SHIPPED", "1002": "PROCESSING", "1003": "DELIVERED"}

def get_order_status(order_id):
    return f"Order {order_id} status: {ORDERS.get(order_id, 'NOT FOUND')}"

def cancel_order(order_id):
    # Human-in-the-loop: what "requireConfirmation" does in Bedrock Agents
    if input(f"!! Confirm cancel order {order_id}? (y/n): ").lower() != "y":
        return "User declined the cancellation."
    if ORDERS.get(order_id) == "PROCESSING":
        ORDERS[order_id] = "CANCELLED"
        return f"Order {order_id} cancelled."
    return f"Order {order_id} cannot be cancelled (status: {ORDERS.get(order_id, 'NOT FOUND')})."

TOOLS = {"get_order_status": get_order_status, "cancel_order": cancel_order}

def spec(name, desc):
    return {"toolSpec": {"name": name, "description": desc,
            "inputSchema": {"json": {"type": "object",
                "properties": {"order_id": {"type": "string",
                                            "description": "The order number, e.g. 1002"}},
                "required": ["order_id"]}}}}

TOOL_CONFIG = {"tools": [
    spec("get_order_status", "Returns the current status of a customer order."),
    spec("cancel_order", "Cancels an order. Only PROCESSING orders can be cancelled."),
]}
SYSTEM = [{"text": "You are an order support assistant. Use tools to check or cancel orders. "
                   "Never guess a status. If the order number is missing, ask for it."}]

def ask(question):
    messages = [{"role": "user", "content": [{"text": question}]}]
    while True:                                            # <-- the agent LOOP
        resp = brt.converse(modelId=MODEL_ID, system=SYSTEM,
                            messages=messages, toolConfig=TOOL_CONFIG)
        msg = resp["output"]["message"]
        messages.append(msg)
        print(f"[stopReason={resp['stopReason']}]")
        if resp["stopReason"] != "tool_use":
            return "".join(b.get("text", "") for b in msg["content"])
        results = []
        for block in msg["content"]:
            if "toolUse" in block:
                tu = block["toolUse"]
                print(f"  -> model requested {tu['name']}({tu['input']})")   # your "trace"
                out = TOOLS[tu["name"]](**tu["input"])                       # YOUR code executes
                print(f"  <- observation: {out}")
                results.append({"toolResult": {"toolUseId": tu["toolUseId"],
                                               "content": [{"text": out}]}})
        messages.append({"role": "user", "content": results})

if __name__ == "__main__":
    while (q := input("\\nYou: ")) not in ("exit", "quit"):
        print("Agent:", ask(q))''')
n.p("Test prompts: status of 1002 · cancel 1002 (confirmation fires) · cancel 1001 (refused) · 'cancel my order' "
    "(asks, no tool call) · two questions in one message (two tool calls). Stretch: move get_order_status into a "
    "Lambda and call it with boto3; make descriptions vague and watch the wrong tool get picked.")

# ---------------------------------------------------------------- mistakes
n.h1("9. Mistakes and learnings")
n.table(["What happened", "Correction / learning"], [
    ["Answered the grounding question with metadata filtering.",
     "<b>Grounding</b> = is the answer true to the sources → Guardrails contextual grounding check. "
     "<b>Filtering</b> = who may see which sources → metadata filters at retrieval. The exam pairs them to confuse you."],
    ["Said 'data store' for a KB data source.", "Use exact service vocabulary: <b>data source</b>, <b>sync / ingestion job</b>."],
    ["Wrote 'Bedrock work flows'.", "The service is <b>Amazon Bedrock Flows</b>."],
    ["Lab blocked: Agents Classic maintenance mode.", "New accounts can't call CreateAgent / InvokeInlineAgent. Use Converse tool loop or AgentCore."],
    ["Lab delayed: model TPM quota not yet available.",
     "New accounts can start with low or zero on-demand quotas. Check <b>Service Quotas → Amazon Bedrock</b> "
     "(tokens/requests per minute per model). Exceeding quota → <b>ThrottlingException</b>; fix with "
     "retries + exponential backoff, a quota increase, cross-region inference profiles or another model "
     "(exam Tasks 2.4 and 5.2)."],
], [0.35, 0.65])

# ---------------------------------------------------------------- quiz
n.h1("10. Day 2 quiz — your answers graded (5 / 5)")
n.table(["#", "Question", "Your answer", "Verdict"], [
    ["1", "Bank transfer must use the app's authenticated session; no backend creds in AWS.", "Return of control",
     "✓ The action executes inside the app, so credentials never leave it."],
    ["2", "Agent calls get_invoice for refund questions; get_refund_status exists. First fix?",
     "Sharpen function descriptions; instruct the agent to always use tools",
     "✓ Descriptions first, instructions second; confirm with the <b>trace</b>."],
    ["3", "Production broke after a change; need instant rollback.", "Versions + aliases; test on DRAFT",
     "✓ Rollback = <b>repoint the alias</b> to the previous version — no client change. Production never calls DRAFT."],
    ["4", "Agent role has lambda:InvokeFunction but still access denied.", "Lambda resource-based policy for bedrock.amazonaws.com",
     "✓ Correct."],
    ["5", "Fixed claims process: extract → validate → store → notify.", "Not an agent; Step Functions or Bedrock Flows",
     "✓ Correct — deterministic, auditable, cheaper. (Name: <b>Bedrock Flows</b>.)"],
], [0.04, 0.34, 0.27, 0.35])

n.h1("11. Key takeaways")
n.bullets([
    "Agent = model + instructions + tools + memory + loop; the model only <i>requests</i> tools.",
    "Converse API: stopReason <b>tool_use</b> → run tool → send <b>toolResult</b> with the same toolUseId.",
    "Bedrock Agents Classic vocabulary is still examinable: action groups, return of control, User input, "
    "Code Interpreter, confirmation, memory, trace, versions/aliases, Lambda resource policy.",
    "Workflow when steps are known; agent when the path depends on results.",
    "Quotas and throttling are real — and exam material.",
])

n.page_break()
n.h1("12. Warm-up for Day 3 — answer from memory (answers in the Day 3 note)")
n.numbered([
    "In the Converse API, which stopReason tells you the model wants a tool, and who executes the tool?",
    "Name the two ways to define the tools of a Bedrock Agents action group.",
    "Your agent must ask the user for a missing order number before acting. Which built-in capability enables this?",
    "What is the difference between sessionAttributes and promptSessionAttributes?",
    "Which two Bedrock Agents Classic operations are blocked for new accounts, and what does AWS recommend instead?",
])

n.callout("Next: Day 3 — Strands Agents, Agent Squad, MCP and AgentCore (Thu 15 Oct)",
          "Task 2.1 part B: building agents with Strands, multi-agent with Agent Squad, tools over MCP, "
          "AgentCore Runtime / Gateway / Memory / Identity / Observability, Step Functions for agent workflows.")

n.build()
print(os.path.abspath(OUT))
