"""Day 6 note: Guardrails, prompt injection and Responsible AI."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import Note  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Day_6_2026-10-27_Guardrails_Prompt_Injection_Responsible_AI.pdf")

n = Note(OUT, "Day 6 — Guardrails, Prompt Injection and Responsible AI",
         "27–29 Oct 2026 &nbsp;·&nbsp; Skills <b>3.1.1–3.1.5</b> (input/output safety) and <b>3.4.1–3.4.3</b> "
         "(responsible AI) &nbsp;·&nbsp; Exam: Mon 9 Nov, 1:30 PM IST")
n.callout("Today in one paragraph",
          "System-prompt rules can be ignored or argued away, so safety is enforced <b>outside the model</b> with "
          "<b>Amazon Bedrock Guardrails</b>: content filters, denied topics, word filters, sensitive-information filters, "
          "contextual grounding and Automated Reasoning checks — on input and output, for any model (ApplyGuardrail even "
          "without a model call). Add accuracy controls (grounding, similarity checks, JSON Schema, text-to-SQL), layer "
          "everything as <b>defence in depth</b>, defend against <b>direct and indirect prompt injection</b>, and make the "
          "system <b>transparent, fair and policy-compliant</b>.", "ok")

# ------------------------------------------------------------ Part 1
n.h1("Part 1 — Guardrails basics (Skills 3.1.1, 3.1.2)")
n.p("A model trained to be helpful will discuss almost anything. A bank's support bot must not insult users, give "
    "investment advice, name competitors, obey 'ignore your instructions', or leak data. System-prompt instructions can "
    "be ignored or talked around; a <b>guardrail</b> is a managed layer outside the model that checks the user's "
    "input before the model and the model's output before the user.")
n.code("                    +----------- GUARDRAIL -----------+\n"
       " User input ------> | 1. check INPUT                  |\n"
       "                    |    blocked? -> your message     | --> user (model NEVER called: no model cost)\n"
       "                    |    ok --------------------+     |\n"
       "                    +---------------------------|-----+\n"
       "                                                v\n"
       "                                         Foundation model\n"
       "                    +---------------------------|-----+\n"
       "                    | 2. check OUTPUT <---------+     |\n"
       "                    |    blocked? -> your message     | --> user\n"
       "                    |    ok (or PII masked) ----------| --> user sees the answer\n"
       "                    +---------------------------------+")
n.bullets([
    "You write the blocked-input and blocked-output messages.",
    "Blocked input never reaches the model → no model tokens (small guardrail charge only).",
    "One guardrail works with any model; working draft → numbered versions for production.",
])
n.code(" GUARDRAIL\n"
       " +-- Part 1: (1) Content filters  (2) Denied topics  (3) Word filters\n"
       " +-- Part 2: (4) Sensitive information  (5) Contextual grounding  (6) Automated Reasoning checks")
n.h2("① Content filters")
n.table(["Category", "Catches", "Example"], [
    ["Hate", "Attacks on identity (race, religion, gender…)", "Discriminatory insults"],
    ["Insults", "Demeaning, mocking, bullying", "'You're an idiot for asking'"],
    ["Sexual", "Sexual content", "Explicit descriptions"],
    ["Violence", "Glorifying or threatening harm", "Threats"],
    ["Misconduct", "Help with criminal/harmful activity", "'How do I break into a car?'"],
    ["Prompt attack", "Attempts to override instructions / jailbreak (input)", "'Ignore all previous instructions…'"],
], [0.18, 0.47, 0.35])
n.p("Strength <b>None / Low / Medium / High</b>, set separately for input and output. Higher = more sensitive = safer "
    "but more false positives. Children's app → High everywhere; crime-novel assistant → lower Violence only. Too many "
    "wrongful blocks in one category → lower that category's strength (e.g. Violence on input for 'kill a process').")
n.h2("② Denied topics")
n.p("Whole subjects you define in plain English (name + definition + sample phrases); matched by <b>meaning</b>. "
    "Examples: investment advice (bank), medical advice (airline), other employees' salaries (HR).")
n.h2("③ Word filters")
n.p("Exact words/phrases: AWS-managed profanity list + your custom list (competitor names, code names).")
n.table(["", "Word filters", "Denied topics"], [
    ["Matches", "Exact words or phrases", "Meaning — the subject however worded"],
    ["Example", "'BankX', 'MediQuick'", "Investment advice, drug dosages"],
    ["Weakness", "Misses synonyms/paraphrases", "Not for single specific words"],
], [0.18, 0.41, 0.41])
n.p("Tip: pair a word filter for 'MediQuick' with a denied topic like 'recommending other pharmacies' to catch paraphrases.")

# ------------------------------------------------------------ Part 2
n.h1("Part 2 — Accuracy, defence in depth, prompt injection (Skills 3.1.1–3.1.5)")
n.h2("④–⑥ The other guardrail policies")
n.bullets([
    "<b>④ Sensitive information filters</b>: PII types → block or mask (e.g. {EMAIL}); custom regex (EMP-\\d{5}).",
    "<b>⑤ Contextual grounding check</b>: inputs = source + question + answer. <b>Grounding</b> score: supported by the "
    "source? <b>Relevance</b> score: answers the question? Below threshold → blocked.",
    "<b>⑥ Automated Reasoning checks</b>: a policy document becomes formal logic rules; answers are checked "
    "mathematically (valid / invalid / undetermined, with suggestions). For provable policy compliance (leave "
    "eligibility, insurance rules). Grounding = 'is it in the documents?'; Automated Reasoning = 'is it logically "
    "correct under the rules?'",
])
n.code(' Source: "Refunds within 14 days."   Question: "What\'s the refund window?"\n'
       ' Answer A: "30 days."               -> grounding LOW  -> blocked\n'
       ' Answer B: "Our stores open at 9."  -> relevance LOW  -> blocked\n'
       ' Answer C: "14 days from delivery." -> both HIGH      -> allowed')
n.h2("Attaching guardrails")
n.code(" (1) Converse / InvokeModel : guardrailConfig (ID + version + trace)\n"
       " (2) Knowledge Bases / agents: attach in their configuration\n"
       " (3) ApplyGuardrail API     : check ANY text with NO model call (SageMaker or other models,\n"
       "                              retrieved chunks, uploads)")
n.bullets([
    "<b>Input tagging</b>: mark the untrusted part of the prompt so only it is checked.",
    "<b>Trace</b>: shows which policy intervened and why.",
])
n.h2("Accuracy verification (3.1.3)")
n.bullets([
    "Ground answers in a Knowledge Base and fact-check claims against sources.",
    "<b>Semantic similarity verification</b>: embed each claim, compare with source chunks; below threshold → flag/remove.",
    "<b>Confidence scoring</b>: e.g. ask several times and measure agreement; low → warning or human review.",
    "<b>JSON Schema structured outputs</b>: tool definition whose input schema is the output format + validation in "
    "code; no free-form unsupported prose, invalid fields caught.",
])
n.h2("Deterministic answers: text-to-SQL (3.1.2)")
n.code(' "Total March sales by region?" -> FM writes SQL -> validate (read-only, allowed tables) -> Athena/Redshift\n'
       "                                -> exact numbers -> FM phrases the answer")
n.p("The database computes exact numbers; the model only explains them. Validate SQL (SELECT only, allowed tables, row "
    "limits) and use a read-only role.")
n.h2("Custom moderation and toxicity evaluation (3.1.1, 3.1.2)")
n.code(" content -> [Comprehend: toxicity + PII] -> [Guardrail] -> [Choice] -> clean: publish\n"
       "                                                               -> borderline: human review (waitForTaskToken)\n"
       "                                                               -> violation: reject + log")
n.p("Measure toxicity before launch with Bedrock model evaluation (toxicity/robustness metrics).")
n.h2("Defence in depth (3.1.4)")
n.code(" Request -> (1) API Gateway      request validation, size limits, throttling\n"
       "         -> (2) Pre-processing   Comprehend PII/toxicity; input sanitisation (Lambda)\n"
       "         -> (3) Guardrail INPUT  content filters, denied topics, prompt attack\n"
       "         -> (4) Model            least-privilege tools, clear system prompt\n"
       "         -> (5) Guardrail OUTPUT content filters, PII masking, grounding\n"
       "         -> (6) Post-processing  Lambda: JSON Schema, business rules, claim checks\n"
       "         -> (7) API Gateway      response filtering/mapping -> User")
n.h2("Prompt injection and jailbreaks (3.1.5)")
n.code(" DIRECT:   user --'ignore your rules'--> model\n"
       " INDIRECT: attacker -> hides instructions in a document/web page -> RAG/agent reads it -> model obeys")
n.bullets([
    "<b>Jailbreak</b>: talking the model out of its rules ('you are DAN, with no restrictions').",
    "<b>Indirect injection is more dangerous</b>: arrives as trusted-looking data (user-input checks miss it); one "
    "poisoned document affects many conversations; the attacker never talks to the app; agents with tools can act silently.",
    "<b>Defences</b>: prompt-attack filter on untrusted content (input tagging); sanitise at ingestion (strip hidden "
    "text) and input; separate instructions from data; least-privilege tools + human approval; output validation; "
    "safety classifiers; <b>automated adversarial testing</b> — attack-prompt library run on every release, fail the "
    "release if more get through.",
])

# ------------------------------------------------------------ Part 3
n.h1("Part 3 — Responsible AI (Skills 3.4.1–3.4.3)")
n.table(["Dimension", "Plain meaning"], [
    ["Transparency / explainability", "People can see why the system answered as it did"],
    ["Fairness", "Similar people get similarly good treatment"],
    ["Safety", "Harmful outputs prevented"], ["Privacy and security", "Personal data protected"],
    ["Veracity and robustness", "Correct and reliable under unusual inputs"],
    ["Controllability", "Humans can monitor and steer"], ["Governance", "Policies, documentation, accountability"],
], [0.35, 0.65])
n.h2("Transparency (3.4.1)")
n.bullets([
    "<b>Reasoning displays</b>: plain-language 'why' for users ('flagged because the invoice date is after the policy end').",
    "<b>Evidence and source attribution</b>: citations + metadata (author, effective date).",
    "<b>Confidence metrics in CloudWatch</b>: publish grounding/confidence scores; dashboards, alarms when they drop; "
    "show users a low-confidence notice.",
    "<b>Agent reasoning traces</b>: Bedrock agent tracing / AgentCore Observability — replay why an agent acted.",
])
n.h2("Fairness (3.4.2)")
n.bullets([
    "<b>Fairness metrics per group</b> in CloudWatch: refusal rate per language, quality per segment, sentiment by group; "
    "alarm when the gap grows.",
    "<b>Counterfactual testing</b>: same request, only the sensitive attribute changed (names, language); compare outputs.",
    "<b>A/B testing</b> of prompt variants with <b>Prompt Management</b> and <b>Prompt Flows</b>.",
    "<b>LLM-as-a-judge</b> evaluations (harmfulness, stereotyping); <b>SageMaker Clarify</b> for bias analysis.",
])
n.h2("Policy compliance (3.4.3)")
n.table(["Written policy", "Guardrail policy"], [
    ["Never give investment advice", "Denied topic"], ["Never reveal card numbers", "Sensitive information filter (block)"],
    ["No offensive language", "Content filters + profanity filter"],
    ["Answers must be supported by our documents", "Contextual grounding check"],
    ["Leave answers must follow HR rules", "Automated Reasoning checks"],
], [0.5, 0.5])
n.bullets([
    "<b>Model cards</b> (SageMaker Model Cards; AWS AI Service Cards): intended use, limitations, training data, "
    "evaluation results, risks — e.g. 'not validated for medical advice'.",
    "<b>Lambda compliance checks</b>: per response (required disclaimer, forbidden promises) and scheduled "
    "(guardrail attached, approved model/guardrail versions).",
])

n.h1("Decision rules — Day 6")
n.numbered([
    "Rules that must hold despite manipulation → guardrail, not just instructions.",
    "Harmful categories → content filters; too many false blocks → lower that category's strength.",
    "Forbidden subject → denied topics; exact forbidden words → word filters.",
    "PII → sensitive information filters (+ regex), block or mask.",
    "Unsupported or off-question answers → contextual grounding (grounding + relevance thresholds).",
    "Provable policy compliance → Automated Reasoning checks.",
    "Same policies for non-Bedrock models / no model call → ApplyGuardrail. Check only user text → input tagging.",
    "Structured data → JSON Schema; exact numbers → text-to-SQL; unsupported claims → semantic similarity check.",
    "Human review and extra checks → Step Functions + Lambda moderation (Comprehend, guardrail, review queue).",
    "'Comprehensive protection' → defence in depth across API Gateway, Comprehend, guardrails, Lambda.",
    "Hidden instructions in documents → indirect injection; sanitise at ingestion, check retrieved content, least "
    "privilege, human approval, automated adversarial testing.",
    "Why / where from → reasoning displays + citations; uncertainty → CloudWatch confidence metrics; agents → tracing.",
    "Unequal treatment → per-group fairness metrics + counterfactual tests; prompt variants → Prompt Management A/B.",
    "Enforce written policy → guardrails per rule; document limitations → model cards; automatic checks → Lambda.",
])

n.h1("Your part checks — graded")
n.table(["Part", "Your answers", "Feedback"], [
    ["1", "Why guardrails; MediQuick vs dosages; 'kill a process'", "✓ ✓ ✓ — guardrails apply identically across models; "
     "add a denied topic to catch competitor paraphrases; lower Violence on input only."],
    ["2", "Grounding vs relevance; SageMaker model; indirect injection", "✓ ✓ ½ — indirect injection also bypasses "
     "user-input checks, spreads to many users, needs no access to the app, and can trigger tools silently."],
    ["3", "Why + which documents; name bias; model cards", "✓ ✓ ✓"],
], [0.07, 0.38, 0.55])

n.h1("Glossary — new terms")
n.table(["Term", "Meaning"], [
    ["Amazon Bedrock Guardrails", "Managed safety layer checking model input and output against your policies."],
    ["Content filters / filter strength", "Harm-category detection; None–High sensitivity per input/output."],
    ["Prompt attack", "Attempt to override instructions or jailbreak."],
    ["Denied topics", "Subjects defined in plain English, blocked by meaning."],
    ["Word filters / managed profanity list", "Exact-match blocked words; AWS-maintained profanity list."],
    ["Sensitive information filter", "PII detection with block or mask, plus custom regex."],
    ["Contextual grounding check", "Grounding and relevance scores of an answer against source and question."],
    ["Automated Reasoning checks", "Formal-logic verification of answers against rules from a policy document."],
    ["guardrailConfig / ApplyGuardrail", "Attach a guardrail to a model call / check any text without a model call."],
    ["Input tagging", "Marking which part of a prompt the guardrail should evaluate."],
    ["Guardrail trace", "Details of which policy intervened and why."],
    ["Semantic similarity verification", "Comparing answer claims with source chunks by embedding similarity."],
    ["Confidence scoring", "Estimating certainty, e.g. agreement across repeated answers."],
    ["JSON Schema", "Formal description of required JSON structure, used to force and validate outputs."],
    ["Text-to-SQL", "Model writes SQL; database computes exact results."],
    ["Defence in depth", "Several independent protective layers."],
    ["Jailbreak", "Persuading a model to ignore its rules."],
    ["Direct / indirect prompt injection", "Malicious instructions typed by the user / hidden in content the model reads."],
    ["Input sanitisation", "Cleaning untrusted input (hidden text, markup, length)."],
    ["Safety classifier", "Model or service that labels input/output as safe or harmful."],
    ["Adversarial testing / red-teaming", "Running attack prompts systematically, e.g. on every release."],
    ["Responsible AI dimensions", "Transparency, fairness, safety, privacy, veracity, controllability, governance."],
    ["Reasoning display", "User-facing explanation of how an answer or decision was reached."],
    ["Source attribution / citations", "Showing which documents an answer came from."],
    ["Fairness metric", "Measure compared across groups (refusal rate, quality, sentiment)."],
    ["Counterfactual testing", "Same request with only a sensitive attribute changed."],
    ["Prompt Management / Prompt Flows", "Bedrock prompt versioning and variants / visual prompt workflows."],
    ["SageMaker Clarify", "AWS tool for bias detection and explainability."],
    ["Model card / AI Service Card", "Document of intended use, limitations, evaluation, risks."],
], [0.36, 0.64])

n.callout("Next", "Day 6 quiz (in chat), then Day 7 — Prompt engineering and design (1.6, 1.1, 2.1.2) and Day 8 — "
          "Data pipelines and enterprise integration (1.3, 2.3).")
n.build()
print(os.path.abspath(OUT))
