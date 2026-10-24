"""Day 4 note: Security and Data Privacy for GenAI."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import Note  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Day_4_2026-10-24_Security_and_Data_Privacy.pdf")

n = Note(OUT, "Day 4 — Security and Data Privacy for GenAI",
         "Saturday 24 Oct 2026 &nbsp;·&nbsp; AWS AIP-C01 exam task covered: <b>3.2 Implement data security and "
         "privacy controls</b> &nbsp;·&nbsp; Exam: Mon 9 Nov, 1:30 PM IST")

n.callout("Today in one paragraph",
          "Protect data at every point it passes through: source data (Macie, Comprehend), ingestion and the "
          "Knowledge Base (KMS, Lake Formation, OpenSearch Serverless policies), the call to the model (PrivateLink, "
          "IAM, SCPs), the response (Guardrails PII masking) and the logs (KMS, lifecycle, CloudTrail). Exam method: "
          "find <b>where</b> the data is in the scenario, then pick the control for that point.", "ok")

n.h1("1. The mental model")
n.code(" [Source data] -> [Ingestion / KB] -> [Prompt] -> [Model] -> [Response] -> [Logs]\n"
       "   Macie           KMS, Lake Formation  Guardrails  PrivateLink  Guardrails    KMS, lifecycle\n"
       "   Comprehend      OpenSearch policies  IAM         IAM / SCP    (PII mask)    CloudTrail")

n.h1("2. What Bedrock does with your data")
n.bullets([
    "Prompts and responses are <b>not used to train</b> AWS or third-party models and are <b>not shared with model "
    "providers</b>.",
    "Data stays <b>in the region you call</b>, unless you use cross-region inference. For residency, use a "
    "<b>geographic</b> inference profile (e.g. US, EU), not a global one.",
    "Bedrock <b>doesn't store prompts or outputs</b> by default; they are kept only if <i>you</i> enable "
    "<b>model invocation logging</b>.",
])

n.h1("3. Network isolation — VPC endpoints (PrivateLink)")
n.table(["Requirement", "Control"], [
    ["No traffic to Bedrock over the public internet",
     "<b>Interface VPC endpoint</b>: <b>bedrock-runtime</b> (inference), <b>bedrock-agent-runtime</b> (KB Retrieve, "
     "agents), <b>bedrock</b> (control plane). Enable private DNS."],
    ["Only allow Bedrock calls arriving through our endpoint",
     "IAM / resource policy <b>Deny</b> with condition <b>aws:SourceVpce</b> StringNotEquals the endpoint ID"],
    ["Limit what can be called through the endpoint", "<b>VPC endpoint policy</b> (allowed actions, model ARNs)"],
    ["Lambda tool in a private subnet calls Bedrock", "Lambda in the VPC + interface endpoint — <b>no NAT gateway</b>"],
    ["Fine-tuning job reaches training data privately", "<b>VPC configuration on the model customisation job</b>"],
], [0.4, 0.6])
n.callout("Trap", "Retrieval and agents use <b>bedrock-agent-runtime</b>, not bedrock-runtime.")

n.h1("4. Who can use which model — IAM and SCPs")
n.table(["Requirement", "Control"], [
    ["Developers may call only specific models",
     "Identity policy allowing bedrock:InvokeModel / InvokeModelWithResponseStream on <b>those model (or inference "
     "profile) ARNs only</b>"],
    ["Block a model across the whole organisation, admins included", "<b>Service Control Policy (SCP)</b> deny"],
    ["App needs credentials", "<b>IAM role</b> (short-term), never long-term access keys"],
    ["Tool / API secrets", "<b>Secrets Manager</b>, or <b>AgentCore Identity</b> for OAuth tokens"],
    ["Users retrieve only their own documents", "<b>KB metadata filtering</b> from their authenticated identity"],
    ["Cross-account access", "<b>Resource-based policy</b> or a cross-account role"],
], [0.45, 0.55])
n.p("An explicit <b>Deny always wins</b>. An SCP sets the maximum anyone in a member account can do, even "
    "administrators and root (it does not apply to the management account).")

n.h1("5. Encryption — KMS")
n.bullets([
    "<b>Customer managed KMS keys</b> when the scenario says 'control, rotate, audit key use, revoke access'.",
    "Used by: Knowledge Bases and ingestion, agents, <b>custom / fine-tuned models</b>, customisation job outputs, S3 "
    "data sources, invocation logs, OpenSearch Serverless collections.",
    "The service role (e.g. the KB role) needs <b>kms:Decrypt</b> (and <b>kms:GenerateDataKey</b> when writing) in "
    "the <b>key policy</b> or a grant. 'AccessDenied on KB sync after switching to SSE-KMS' → key policy missing the role.",
])
n.table(["OpenSearch Serverless policy", "Controls"], [
    ["Encryption policy", "Which KMS key encrypts the collection"],
    ["Network policy", "Public access, or only through a VPC endpoint"],
    ["Data access policy", "Which roles can read / write which indexes"],
], [0.35, 0.65])

n.h1("6. PII — find it, redact it, block it")
n.table(["When", "Tool", "What it does"], [
    ["Before ingestion: PII sitting in S3", "<b>Amazon Macie</b>", "Discovers and reports sensitive data in buckets"],
    ["In the data pipeline", "<b>Amazon Comprehend</b> DetectPiiEntities / redaction", "Removes PII before chunking and embedding"],
    ["At runtime: model input / output", "<b>Bedrock Guardrails</b> sensitive information filters",
     "<b>Block</b> or <b>mask</b> PII types, plus custom <b>regex</b> (e.g. employee IDs)"],
    ["Images and scanned documents", "Bedrock Data Automation / Textract → Comprehend", "Extract text first, then redact"],
], [0.3, 0.32, 0.38])
n.p("'PII must never be embedded in the KB' → <b>Macie to detect, Comprehend to redact, before ingestion</b>. "
    "'Don't show PII in responses' → <b>Guardrails masking</b> (defence in depth: use both).")

n.h1("7. Data lake access — AWS Lake Formation")
n.p("Fine-grained permissions on the Glue Data Catalog at <b>table, column, row and cell</b> level. 'The agent may read "
    "orders but never the card_number column' → <b>Lake Formation column-level permissions</b> — bucket policies can't "
    "do that.")

n.h1("8. Retention and deletion")
n.bullets([
    "<b>S3 lifecycle rules</b>: transition to cheaper storage, then <b>expire after N days</b> (invocation logs, "
    "transcripts, training data).",
    "<b>S3 Object Lock</b> (WORM): data must not be changed or deleted for a period — 'keep at least' vs lifecycle's "
    "'delete after'.",
    "Agent memory retention → <b>AgentCore Memory event expiry</b> (Day 3).",
])

n.h1("9. Logging and audit (preview of Task 3.3)")
n.table(["Need", "Tool"], [
    ["Who called which Bedrock API, when", "<b>AWS CloudTrail</b>"],
    ["Full prompt and response contents", "<b>Model invocation logging</b> to S3 and/or CloudWatch Logs"],
    ["Logs contain sensitive data", "Encrypt with <b>KMS</b>, restrict access, <b>lifecycle expiry</b>"],
], [0.45, 0.55])

n.h1("10. Decision rules")
n.numbered([
    "No public internet → <b>interface VPC endpoints</b> (bedrock-runtime; <b>bedrock-agent-runtime</b> for KB/agents), "
    "enforced with <b>aws:SourceVpce</b>.",
    "Restrict models for a team → <b>IAM with model ARNs</b>; whole organisation → <b>SCP deny</b>.",
    "Own / rotate / audit keys → <b>KMS customer managed key</b>; sync fails after enabling KMS → <b>key policy</b>.",
    "Find PII in S3 → <b>Macie</b>; redact in pipeline → <b>Comprehend</b>; mask/block at runtime → <b>Guardrails</b>.",
    "Column / row restrictions on lake data → <b>Lake Formation</b>.",
    "Delete after N days → <b>S3 lifecycle</b>; must not change → <b>Object Lock</b>.",
    "Data residency → in-region, or a <b>geographic</b> cross-region profile.",
    "'Is our data used for training?' → <b>No</b>; not stored or shared unless you enable logging.",
    "Who called what → <b>CloudTrail</b>; prompt contents → <b>invocation logging</b> (encrypted, with expiry).",
    "OpenSearch Serverless security → <b>encryption, network and data access policies</b>.",
])

# ---------------------------------------------------------------- lab
n.h1("11. Lab — console, no model quota needed")
n.p("<b>Status:</b> steps studied in full; not executed yet (no console access today). Run Parts A and G when "
    "console access returns — they are the most exam-relevant.")
n.table(["Part", "Steps", "What to record"], [
    ["A. IAM (15 min)", "Create policy <b>bedrock-nova-only</b> allowing InvokeModel on the Nova Lite ARN only; attach "
     "to a test role; IAM Policy Simulator: Nova Lite → allowed, an Anthropic model → implicitly denied.",
     "Implicit vs explicit deny; how an SCP does this org-wide."],
    ["B. VPC endpoint (15 min)", "Create interface endpoint <b>com.amazonaws.us-east-1.bedrock-runtime</b>, private DNS "
     "on; inspect the endpoint policy; find bedrock-agent-runtime. <b>Delete immediately</b> (hourly billing).",
     "Which endpoint Retrieve needs; how aws:SourceVpce forces traffic through it."],
    ["C. KMS (15 min)", "Create key <b>genai-data</b>; S3 bucket with default <b>SSE-KMS</b> using it; read the key policy.",
     "The two KMS permissions a KB role needs."],
    ["D. Macie (15 min)", "Upload a <b>fake</b> customers.csv (name, email, card 4111111111111111); enable Macie trial; "
     "run a one-time job on the bucket.", "Findings; Macie vs Comprehend vs Guardrails."],
    ["E. Lifecycle (5 min)", "Lifecycle rule on prefix logs/: expire after 30 days.", "When to use Object Lock instead."],
    ["F. Invocation logging (5 min)", "Bedrock → Settings → Model invocation logging: review S3 / CloudWatch options; "
     "don't save.", "Why logs need KMS + lifecycle."],
    ["G. Guardrail PII (optional)", "Guardrail <b>pii-guard</b>: Email → Mask, Credit card → Block, regex ORD-\\d{6} → "
     "Mask; test with <b>apply-guardrail</b> in CloudShell (no model call).", "What was masked vs blocked."],
], [0.17, 0.53, 0.3])
n.code('''aws bedrock-runtime apply-guardrail --guardrail-identifier <GUARDRAIL_ID> --guardrail-version DRAFT \\
  --source OUTPUT --content '[{"text":{"text":"Mail jane@example.com about ORD-123456, card 4111111111111111"}}]\'''')
n.callout("Cleanup", "Delete the VPC endpoint (immediately), Macie job (disable Macie if unused), bucket (empty first), "
          "KMS key (schedule deletion, min 7 days), IAM policy and test role, guardrail.")

# ---------------------------------------------------------------- quiz
n.h1("12. Day 4 quiz — your answers graded (4.25 / 5)")
n.table(["#", "Question", "Your answer", "Verdict"], [
    ["1", "Private subnets, no internet, no NAT: call models and query a KB; stop developers bypassing it.",
     "Interface endpoints bedrock-runtime and 'bedrock-runtime-agents'; endpoint ID in aws:SourceVpce",
     "¾ Right design. Exact name is <b>bedrock-agent-runtime</b>. Enforce with a <b>Deny</b> when aws:SourceVpce "
     "<b>StringNotEquals</b> the endpoint ID; enable private DNS."],
    ["2", "KB ingestion AccessDenied after switching the bucket to SSE-KMS (role still has s3:GetObject).",
     "We need the key policy",
     "½ Be specific: the <b>KMS key policy</b> (or a grant) must allow the <b>KB service role kms:Decrypt</b> "
     "(and GenerateDataKey when writing). The exam option will name the permission."],
    ["3", "Card numbers must never reach the vector index.",
     "Macie to find PII at ingestion, Comprehend to redact before chunking/embedding",
     "✓ Correct. Then ingest the redacted copy; add Guardrails masking at runtime for defence in depth."],
    ["4", "No account, admins included, may use a specific model.", "SCP deny",
     "✓ Correct. SCPs bind all principals in member accounts, including root (not the management account)."],
    ["5", "Agent may read orders but never card_number.", "Lake Formation column-level restriction",
     "✓ Correct (service name: <b>AWS Lake Formation</b>)."],
], [0.04, 0.3, 0.28, 0.38])

n.h1("13. Mistakes and learnings")
n.table(["What happened", "Correction"], [
    ["Wrote 'bedrock-runtime-agents'.", "Exact endpoint: <b>bedrock-agent-runtime</b>. Exam options differ by one word."],
    ["'We need the key policy' without the permission.", "Name it: KMS key policy grants the role <b>kms:Decrypt</b>."],
    ["Lab not executed (no console access).", "Theory is solid; schedule Parts A and G when access returns."],
], [0.4, 0.6])

n.h1("14. Key takeaways")
n.bullets([
    "Locate the data in the scenario, then pick the control for that point.",
    "bedrock-runtime vs bedrock-agent-runtime; aws:SourceVpce to enforce private paths.",
    "IAM restricts a team; SCP restricts the organisation, admins included.",
    "KMS failures are usually the key policy; OpenSearch Serverless has three policy types.",
    "Macie finds, Comprehend redacts, Guardrails masks at runtime; Lake Formation for columns and rows.",
])

n.callout("Next: Day 5 — Models and inference (Tasks 1.2, 2.2, 2.4)",
          "Model selection, inference parameters, Converse API and streaming, on-demand vs provisioned vs batch, "
          "cross-region inference, fine-tuning and distillation, quotas, throttling and retries.")

n.build()
print(os.path.abspath(OUT))
