"""Day 3 note: Strands Agents, Agent Squad, MCP and AgentCore."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import Note  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Day_3_2026-10-15_Strands_AgentCore_MCP.pdf")

n = Note(OUT, "Day 3 — Strands, Agent Squad, MCP and AgentCore",
         "Thursday 15 Oct 2026 &nbsp;·&nbsp; AWS AIP-C01 exam task covered: <b>2.1 Agentic AI and tool "
         "integrations (part B)</b> &nbsp;·&nbsp; Exam: Sat 7 Nov")

n.callout("Today in one paragraph",
          "A <b>framework</b> (Strands Agents, LangGraph, CrewAI, Agent Squad) decides <i>how the agent thinks</i>; "
          "<b>Amazon Bedrock AgentCore</b> <i>hosts, connects, secures and watches</i> it — for any framework and any "
          "model. Tools are shared through <b>MCP</b> (often served by AgentCore Gateway). Use multi-agent designs only "
          "when one agent can't cope, and use <b>Step Functions</b> when the steps are fixed and need audit, retries "
          "or human approval.", "ok")

n.h1("1. The big picture")
n.code("BUILD the agent (framework):  Strands Agents · LangGraph · CrewAI · Agent Squad\n"
       "                     |  runs on\n"
       "OPERATE it (Amazon Bedrock AgentCore):\n"
       "   Runtime · Gateway (tools as MCP) · Memory · Identity · Observability\n"
       "   · Code Interpreter · Browser · managed harness\n"
       "                     |  calls\n"
       "MODELS:  Amazon Bedrock (Converse API) — or any other provider")
n.p("Exam Task 2.1 explicitly names <b>Strands Agents, AWS Agent Squad, MCP and Step Functions</b>.")

n.h1("2. Strands Agents (AWS open-source agent SDK)")
n.bullets([
    "<b>Model-driven:</b> give it a model, a system prompt and tools; the model plans the loop (ReAct) itself.",
    "A tool is a Python function decorated with <b>@tool</b>; the <b>docstring becomes the tool description</b> "
    "(so it is a prompt).",
    "Bedrock by default, other providers supported (e.g. Anthropic API directly); native <b>MCP</b> tool support.",
])
n.table(["Multi-agent pattern", "How it works", "Use when"], [
    ["Agents as tools", "Specialist agents wrapped as tools of an orchestrator agent", "Clear specialist roles, one coordinator"],
    ["Swarm", "Peer agents hand work to each other", "Collaborative, exploratory tasks"],
    ["Graph", "Agents are nodes with defined edges (conditions, branches)", "Structured flow with LLM decisions at each node"],
    ["Workflow", "Fixed sequence / dependency graph of tasks", "Repeatable pipelines"],
], [0.2, 0.48, 0.32])

n.h1("3. AWS Agent Squad (formerly Multi-Agent Orchestrator)")
n.bullets([
    "Open-source (AWS Labs). An LLM <b>classifier routes each request to the best specialist agent</b>.",
    "Keeps <b>conversation context across agents</b>, so follow-ups reach the right one.",
    "Also offers a <b>SupervisorAgent</b> (lead agent delegates to a team in parallel).",
    "Exam cue: 'many specialists, each request must reach the right one, cheaply' → <b>router / classifier</b>.",
])

n.h1("4. MCP — Model Context Protocol")
n.bullets([
    "Open standard for connecting AI apps to tools and data — 'USB-C for AI tools'.",
    "<b>Client–server:</b> the agent (MCP client) connects to MCP servers exposing <b>tools</b>, <b>resources</b> "
    "(data) and <b>prompts</b> (templates).",
    "Transports: <b>stdio</b> (local) and <b>Streamable HTTP</b> (remote).",
    "Write a tool once; every MCP-capable agent (Strands, LangGraph, Claude…) can use it.",
    "Exam cue: 'standardise / reuse tools across teams and frameworks' → <b>MCP</b>, often via <b>AgentCore Gateway</b>.",
])

n.h1("5. Amazon Bedrock AgentCore services")
n.table(["Service", "What it does", "Exam trigger"], [
    ["Runtime", "Serverless hosting for agents from <b>any framework</b>; each session isolated in its own microVM; "
     "long-running sessions (hours).", "'Host LangGraph/Strands agents, session isolation, no infrastructure'"],
    ["Gateway", "Turns <b>APIs, Lambda and OpenAPI specs into MCP tools</b> with built-in auth; <b>semantic tool "
     "search</b> across many tools.", "'Expose existing APIs as tools to many agents', 'hundreds of tools'"],
    ["Memory", "<b>Short-term</b> (session events, with expiry) and <b>long-term</b> strategies: semantic facts, "
     "user preferences, summaries — scoped by <b>namespaces</b>.", "'Remember user preferences across sessions'"],
    ["Identity", "<b>Inbound</b> auth (who may call the agent) and <b>outbound</b> auth (agent acts <i>on behalf of the "
     "user</i> in Google, GitHub, Salesforce…) with a token vault; secrets in Secrets Manager.",
     "'Use the user's own permissions in a third-party service'"],
    ["Observability", "Traces of steps, tool calls, tokens, latency (OpenTelemetry) in <b>CloudWatch</b> "
     "(GenAI Observability; needs Transaction Search enabled).", "'Debug / monitor agents in production'"],
    ["Code Interpreter", "Sandbox to run agent-generated code safely.", "'Run generated code safely'"],
    ["Browser", "Managed cloud browser the agent can drive.", "'Navigate websites, fill web forms'"],
    ["Managed harness", "Config-only agent definition (model, tools, instructions); AgentCore runs the loop.",
     "Replacement for console-created Classic agents"],
], [0.16, 0.54, 0.3])

n.h1("6. Agents Classic → modern equivalent")
n.table(["Bedrock Agents Classic", "AgentCore / framework equivalent"], [
    ["Action group + Lambda", "Strands @tool, or an AgentCore <b>Gateway</b> target (Lambda / OpenAPI)"],
    ["Return of control", "Tool executes in your own application / client code"],
    ["Attached Knowledge Base", "Retrieval tool calling the KB <b>Retrieve</b> API"],
    ["Session + long-term memory", "<b>AgentCore Memory</b> (short-term + long-term strategies)"],
    ["Trace", "<b>AgentCore Observability</b>"],
    ["Multi-agent collaboration (supervisor + collaborators)", "Strands multi-agent patterns, or Agent Squad"],
    ["Code Interpreter action group", "<b>AgentCore Code Interpreter</b>"],
], [0.45, 0.55])
n.p("<b>Classic multi-agent collaboration modes:</b> <b>Supervisor</b> (plans, delegates, combines) and "
    "<b>Supervisor with routing</b> (simple requests go straight to one collaborator) — the same supervisor-vs-router idea.")

n.h1("7. Step Functions for agent workflows")
n.bullets([
    "A ReAct-style loop can be a state machine: model call → Choice (tool wanted?) → Task (run tool) → loop. "
    "Visible, auditable, built-in <b>retries</b>.",
    "<b>Human approval:</b> a task with <b>.waitForTaskToken</b> pauses until someone calls "
    "<b>SendTaskSuccess</b> / SendTaskFailure with the token.",
    "<b>Standard</b> workflows run up to <b>1 year</b> with full execution history (audit). <b>Express</b> workflows "
    "run up to <b>5 minutes</b> — wrong choice for multi-day approvals.",
    "Optimised integration: <b>Bedrock InvokeModel</b> task calls a model directly from the state machine.",
    "Choose it when steps are mostly fixed and you need audit trails, retries, timeouts or human approval.",
])

n.h1("8. Choosing a multi-agent pattern")
n.table(["Pattern", "Strength", "Cost"], [
    ["Single agent, many tools", "Simplest, cheapest — <b>start here</b>", "Gets confused beyond a few dozen tools"],
    ["Router / classifier", "Fast, cheap; one specialist answers", "No cross-specialist collaboration"],
    ["Supervisor / agents as tools", "Handles complex multi-domain requests", "More model calls → latency + cost"],
    ["Swarm", "Flexible, emergent collaboration", "Hard to predict and debug"],
    ["Graph / workflow", "Predictable, auditable", "Less flexible"],
], [0.3, 0.38, 0.32])
n.callout("Exam rule", "Add agents only when one agent can't cope. 'Most cost-effective' usually means the simplest "
          "pattern that works.")

n.h1("9. Decision rules")
n.numbered([
    "Framework-agnostic hosting, session isolation, no servers → <b>AgentCore Runtime</b>.",
    "Existing APIs / Lambda as tools shared by many agents → <b>AgentCore Gateway (MCP)</b>.",
    "Hundreds of tools, wrong tool picked, huge prompts → <b>Gateway semantic tool search</b>.",
    "Agent acts in third-party services <i>as the user</i> → <b>AgentCore Identity</b> (outbound OAuth).",
    "Remember preferences across sessions → <b>AgentCore Memory, long-term</b> (user-preference strategy).",
    "Trace steps / tokens / latency in production → <b>AgentCore Observability</b> in CloudWatch.",
    "Each request to exactly one of many specialists → <b>router / Agent Squad classifier</b>.",
    "Complex request needs several specialists combined → <b>supervisor / agents as tools</b>.",
    "Fixed steps + human approval + audit trail → <b>Step Functions Standard</b> + <b>waitForTaskToken</b>.",
    "Reuse tools across frameworks and teams → <b>MCP</b>.",
    "Run generated code safely → <b>AgentCore Code Interpreter</b>; drive websites → <b>AgentCore Browser</b>.",
])

# ---------------------------------------------------------------- labs
n.h1("10. Lab work")
n.table(["Lab", "Status"], [
    ["Code lab: Strands single agent + supervisor (agents as tools)",
     "Pending — Bedrock on-demand TPM quota is 0 on the new account. Workaround: run with the Anthropic API directly."],
    ["Console lab: Gateway + Memory + Identity + Observability + Step Functions approval workflow",
     "Provided (needs no model quota). Run it and record the checklist answers."],
], [0.55, 0.45])

n.h2("Code lab — Strands (model setup: pick ONE)")
n.code('''pip install strands-agents strands-agents-tools "strands-agents[anthropic]" boto3

# Option 1 — Bedrock (once quota is available)
from strands.models import BedrockModel
model = BedrockModel(model_id="us.amazon.nova-lite-v1:0", region_name="us-east-1")

# Option 2 — Anthropic API directly (key in the ANTHROPIC_API_KEY env var, never in code/chat)
from strands.models.anthropic import AnthropicModel
model = AnthropicModel(model_id="claude-opus-5-5", max_tokens=16000)''')
n.code('''from strands import Agent, tool

ORDERS = {"1001": "SHIPPED", "1002": "PROCESSING", "1003": "DELIVERED"}

@tool
def get_order_status(order_id: str) -> str:
    """Returns the current status of a customer order.

    Args:
        order_id: The order number, e.g. 1002
    """
    return f"Order {order_id}: {ORDERS.get(order_id, 'NOT FOUND')}"

@tool
def cancel_order(order_id: str) -> str:
    """Cancels an order. Only orders in PROCESSING status can be cancelled.

    Args:
        order_id: The order number to cancel
    """
    if ORDERS.get(order_id) == "PROCESSING":
        ORDERS[order_id] = "CANCELLED"
        return f"Order {order_id} cancelled."
    return f"Order {order_id} cannot be cancelled ({ORDERS.get(order_id, 'NOT FOUND')})."

order_agent = Agent(model=model, tools=[get_order_status, cancel_order],
                    system_prompt="You handle order status and cancellations. Never guess a status.")

policy_agent = Agent(model=model, system_prompt=(
    "You answer refund and shipping policy questions. Policy: refunds within 30 days of delivery; "
    "shipping takes 3-5 business days; cancelled orders are refunded in 5 days."))

@tool
def order_specialist(query: str) -> str:
    """Handles anything about a specific order: status checks and cancellations."""
    return str(order_agent(query))

@tool
def policy_specialist(query: str) -> str:
    """Answers general refund, return and shipping policy questions."""
    return str(policy_agent(query))

supervisor = Agent(model=model, tools=[order_specialist, policy_specialist],
                   system_prompt="You are a customer support lead. Delegate to the right specialist "
                                 "and combine their answers into one reply.")

supervisor("Cancel order 1002 and tell me when I'll get my refund.")   # BOTH specialists
supervisor("How long does shipping take?")                             # ONE specialist''')
n.p("Watch: the first question calls both specialists, the second only the policy one; the supervisor pattern "
    "costs more model calls than a single agent.")

n.h2("Console lab — no model quota needed")
n.table(["Part", "Steps", "What to record"], [
    ["A. Gateway (30 min)",
     "Lambda <b>order-tools</b> → AgentCore <b>Gateways</b> → create <b>support-gateway</b> (inbound JWT, quick-create "
     "Cognito) → add <b>Lambda target</b> with an inline tool schema (get_order_status, cancel_order).",
     "MCP endpoint URL; inbound (Cognito JWT) vs outbound (IAM role → Lambda); role permission; how it compares to an action group."],
    ["B. Memory (15 min)",
     "Create <b>support-memory</b>: short-term event expiry (e.g. 30 days) + Semantic, User preferences and "
     "Summarization strategies.",
     "What each strategy extracts; namespaces; which strategy stores 'prefers email'."],
    ["C. Identity (10 min)",
     "Inspect the gateway's workload identity; browse OAuth providers; create an API-key provider "
     "<b>demo-api-key</b> (dummy value).",
     "Secret stored in Secrets Manager; which flow books into the user's own calendar."],
    ["D. Observability (10 min)",
     "CloudWatch → enable <b>Transaction Search</b> → open the GenAI Observability dashboard.",
     "What it would show: sessions, traces, tool calls, tokens, latency, errors."],
    ["E. Step Functions (25 min)",
     "SQS <b>approval-queue</b>; state machine: Pass ExtractDocuments → Pass RiskSummary (stand-in for Bedrock "
     "InvokeModel) → SQS SendMessage <b>Wait for callback</b> with the task token → Choice → Notify. Add a Retry. "
     "Run, poll SQS for the token, then in CloudShell: <b>aws stepfunctions send-task-success --task-token \"…\" "
     "--task-output '{\"approved\": true}'</b>.",
     "Execution event history = audit trail; why a workflow beats an agent here."],
], [0.17, 0.53, 0.3])
n.p("Task-token message body — JSONPath: <b>{\"TaskToken.$\": \"$$.Task.Token\", \"case\": \"loan-123\"}</b> · "
    "JSONata: <b>{% {\"TaskToken\": $states.context.Task.Token, \"case\": \"loan-123\"} %}</b>")
n.callout("Cleanup", "Delete the gateway + target, the quick-created Cognito user pool, support-memory, demo-api-key, "
          "the order-tools Lambda, the state machine and approval-queue. Optionally disable Transaction Search.")

# ---------------------------------------------------------------- learnings
n.h1("11. Blockers and learnings")
n.table(["What happened", "Learning"], [
    ["Bedrock on-demand TPM quota = 0 on the new account; requests rejected.",
     "Exam Tasks 2.4 / 5.2: quota exhaustion → <b>ThrottlingException</b> / rejections. Fixes: <b>Service Quotas</b> "
     "increase or AWS Support case, <b>cross-region inference profiles</b>, another model, retries with exponential backoff."],
    ["Bedrock Agents Classic unavailable (maintenance mode).",
     "AWS's direction is <b>AgentCore</b>; know both vocabularies for the exam."],
    ["Using Claude via the Anthropic API instead of Bedrock.",
     "Agent concepts are identical; only field names differ (see table below). Never paste API keys into chats or code."],
], [0.38, 0.62])
n.table(["Concept", "Bedrock Converse API", "Anthropic API"], [
    ["Tool definition", "toolSpec + inputSchema.json", "name, description, input_schema"],
    ["Model wants a tool", "stopReason = \"tool_use\"", "stop_reason = \"tool_use\""],
    ["Tool request", "toolUse block (toolUseId)", "tool_use block (id)"],
    ["Your result", "toolResult (toolUseId)", "tool_result (tool_use_id)"],
], [0.28, 0.36, 0.36])

n.h1("12. Key takeaways")
n.bullets([
    "Framework thinks, AgentCore operates — any framework, any model.",
    "Gateway = tools as MCP + auth + semantic tool search. Identity = inbound vs outbound (on behalf of the user).",
    "Memory = short-term events with expiry + long-term strategies scoped by namespace.",
    "Router for 'exactly one specialist'; supervisor for 'combine specialists'; single agent first.",
    "Step Functions Standard + waitForTaskToken for fixed, auditable, human-approved processes.",
])

n.page_break()
n.h1("13. Day 3 quiz — answer from memory (answers in the next note)")
n.numbered([
    "A company has agents built with LangGraph and Strands. It wants to host both without managing servers, with "
    "each user's session isolated. Which service?",
    "40 internal REST APIs must become tools for 6 agent teams, with authentication and no per-team glue code. "
    "Best approach?",
    "A travel assistant must book meetings in each user's own Google Calendar with that user's permissions. Which "
    "AgentCore capability handles this?",
    "Billing, technical and sales agents; each request must go to exactly one, as cheaply as possible. Supervisor "
    "or router? Name an AWS framework that does it.",
    "Loan process: extract documents → LLM risk summary → human underwriter approval → notify. Full audit trail and "
    "automatic retries required. What runs it, and what feature handles the approval?",
])

n.callout("Next: Practice Set #1 (15 questions, Days 1–3), then Day 4 — Security primer (Task 3.2)",
          "IAM, KMS, VPC endpoints / PrivateLink, Lake Formation, Macie, PII handling, S3 lifecycle and retention.")

n.build()
print(os.path.abspath(OUT))
