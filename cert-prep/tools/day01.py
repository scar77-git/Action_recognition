"""Day 1 note: RAG Foundations and Amazon Bedrock Knowledge Bases."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notelib import Note  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "notes",
                   "Day_1_2026-10-13_RAG_Foundations_and_Bedrock_Knowledge_Bases.pdf")

n = Note(OUT, "Day 1 — RAG Foundations and Bedrock Knowledge Bases",
         "Tuesday 13 Oct 2026 &nbsp;·&nbsp; Target exams: AWS Certified Generative AI Developer – Professional "
         "(Sat 7 Nov) and Microsoft AI-103 (Sun 8 Nov) &nbsp;·&nbsp; Focus: AWS first")

# ---------------------------------------------------------------- summary
n.callout("Today in one paragraph",
          "RAG (Retrieval-Augmented Generation) lets an LLM answer from <i>your</i> data without retraining it: "
          "documents are prepared offline (ingest, parse, chunk, embed, index) and, for every question, the most "
          "relevant chunks are retrieved and pasted into the prompt so the model answers from them and can cite "
          "them. On AWS the managed way to do all of this is <b>Amazon Bedrock Knowledge Bases</b>. In the lab you "
          "built one on S3, tested default vs hierarchical chunking and semantic vs hybrid search.", "ok")

n.h1("1. What RAG is and why it exists")
n.bullets([
    "<b>Problem:</b> a foundation model only knows its training data — nothing private, nothing recent — and it "
    "will confidently invent answers (hallucinate) when it doesn't know.",
    "<b>Idea:</b> search your own knowledge first, then give the model the relevant passages and instruct it to "
    "answer <i>only</i> from them. Think of it as a search engine whose top results are pasted into a prompt template.",
    "<b>Benefits:</b> fresh data without retraining, citations / traceability, fewer hallucinations, access control "
    "at retrieval time, much cheaper than fine-tuning.",
    "<b>RAG vs fine-tuning:</b> knowledge that changes often → RAG. Changing the model's <i>style, tone, format or "
    "domain behaviour</i> → fine-tuning. Need both → do both.",
])

n.h1("2. The pipeline")
n.code(
    "OFFLINE  (indexing — runs on a schedule / when data changes)\n"
    "  1 Ingest -> 2 Parse -> 3 Chunk -> 4 Embed -> 5 Index/Store\n\n"
    "ONLINE   (every user question)\n"
    "  6 Query rewrite -> 7 Embed query -> 8 Retrieve -> 9 Rerank\n"
    "     -> 10 Augment prompt -> 11 Generate -> 12 Cite & check grounding")
n.p("Exam mindset: every RAG scenario question is really asking <b>which step is broken</b> and <b>which managed "
    "feature fixes it</b>.")

n.h1("3. Each step — what it is, AWS tool, Azure tool")
n.table(
    ["Step", "What it does", "AWS", "Azure"],
    [
        ["1. Ingest", "Pull source data in from where it lives; re-run when it changes.",
         "S3 (main KB source); connectors: web crawler, Confluence, SharePoint, Salesforce; custom/direct ingestion API; <b>sync (ingestion) jobs</b>",
         "Blob Storage / ADLS, Cosmos DB, Azure SQL, SharePoint via <b>AI Search indexers</b> (scheduled)"],
        ["2. Parse", "Turn PDFs, Word, scans, tables into clean text + structure. Bad parsing poisons everything after.",
         "KB default parser; <b>foundation-model parsing</b> or <b>Bedrock Data Automation</b> for complex PDFs/tables/images; Textract (OCR)",
         "<b>Document Intelligence</b> (Layout model); AI Search document cracking"],
        ["3. Chunk", "Split documents into passages. Too big = noise; too small = lost meaning.",
         "Default (~300 tokens), fixed-size, <b>hierarchical</b>, <b>semantic</b>, none, or custom via <b>Lambda</b>",
         "Text Split skill (pages/sentences); Document Layout skill (structure-aware)"],
        ["4. Embed", "Convert each chunk into a vector capturing its meaning; similar meaning = nearby vectors.",
         "<b>Titan Text Embeddings V2</b> (256/512/1024 dims), Titan Multimodal Embeddings, Cohere Embed",
         "Azure OpenAI <b>text-embedding-3-small/large</b>; integrated vectorization in AI Search"],
        ["5. Index / Store", "Save vectors + text + metadata in a store built for similarity search.",
         "<b>OpenSearch Serverless</b> (quick-create default), Aurora PostgreSQL (pgvector), <b>Neptune Analytics</b> (GraphRAG), S3 Vectors, Pinecone, MongoDB Atlas, Redis",
         "<b>AI Search</b> vector index; Cosmos DB vector search"],
        ["6. Query rewrite", "Clarify or split a complex question into sub-queries before searching.",
         "KB <b>query decomposition</b>", "AI Search query rewriting / agentic retrieval"],
        ["7. Embed query", "Vectorise the question with the <b>same</b> embedding model used in step 4.",
         "Same model as step 4 (automatic in KB)", "Same model as step 4"],
        ["8. Retrieve", "Fetch top-K chunks: semantic (vector), keyword (BM25) or <b>hybrid</b>; apply metadata filters.",
         "KB <b>Retrieve</b> API; semantic or hybrid; metadata filters", "AI Search hybrid query (fused with <b>RRF</b>), filters, security trimming"],
        ["9. Rerank", "Second, smarter model re-scores results so the best chunk is first.",
         "Bedrock <b>rerank models</b> (Amazon Rerank, Cohere Rerank)", "AI Search <b>semantic ranker</b>"],
        ["10. Augment", "Build the prompt: instructions + retrieved chunks + question.",
         "<b>RetrieveAndGenerate</b> prompt template; <b>Prompt Management</b>", "Foundry prompt flow / templates; Semantic Kernel; Agent Service"],
        ["11. Generate", "LLM writes the answer from the augmented prompt.",
         "Bedrock models (Claude, Nova, Llama, Mistral…) via <b>Converse / InvokeModel</b>", "Azure OpenAI GPT models / Foundry deployments"],
        ["12. Cite & check", "Attach sources; verify the answer is supported by retrieved text.",
         "RetrieveAndGenerate returns <b>citations</b>; <b>Guardrails contextual grounding check</b>",
         "Citations from AI Search / Agent Service; <b>Content Safety groundedness detection</b>"],
    ],
    [0.13, 0.27, 0.32, 0.28])

n.h2("Managed shortcuts (the 'least operational overhead' answers)")
n.table(["Need", "AWS", "Azure"], [
    ["Whole RAG pipeline managed", "<b>Bedrock Knowledge Bases</b>", "<b>AI Search</b> (integrated vectorization) + <b>Foundry Agent Service</b>"],
    ["RAG as one tool of an agent", "Bedrock Agents with a Knowledge Base attached", "Foundry Agent Service with the AI Search / file search tool"],
], [0.3, 0.35, 0.35])

n.h1("4. Chunking strategies (Bedrock Knowledge Bases)")
n.table(["Strategy", "How it works", "Use when"], [
    ["Default", "~300-token chunks, respects sentence boundaries.", "Quick start; general text."],
    ["Fixed-size", "You set max tokens per chunk + overlap %.", "Uniform docs; you want predictable chunk size."],
    ["Hierarchical", "Two layers: small <b>child</b> chunks are searched (precision); their larger <b>parent</b> chunk is returned to the model (context).",
     "Long, structured docs (contracts, manuals) where an answer needs surrounding context."],
    ["Semantic", "Splits where the meaning changes (uses an embedding model; costs more at ingestion).", "Docs without clear structure where topics shift mid-section."],
    ["None", "Each file is one chunk.", "Docs already pre-split (e.g. one FAQ per file)."],
    ["Custom (Lambda)", "Your own Lambda transforms/chunks content during ingestion.", "Special formats or business rules none of the above handle."],
], [0.17, 0.48, 0.35])

n.h1("5. Retrieval concepts")
n.bullets([
    "<b>Semantic (vector) search:</b> matches by meaning — 'car broke down' finds 'vehicle failure'. Weak on exact tokens.",
    "<b>Keyword (BM25) search:</b> matches exact words — great for product codes, error IDs, names.",
    "<b>Hybrid search:</b> runs both and merges results. Fix for 'exact part numbers aren't found'.",
    "<b>Reranking:</b> right documents retrieved but in the wrong order → add a reranker.",
    "<b>Metadata filtering:</b> restrict results by attributes (department, date, tenant). Enforce access control "
    "<i>here</i>, never by trusting the prompt.",
    "<b>Retrieve</b> API = returns chunks only (you build the prompt / custom logic). "
    "<b>RetrieveAndGenerate</b> = full managed answer with citations.",
])

n.h1("6. Exam decision rules (memorise)")
n.numbered([
    "'<b>Least operational overhead</b>' → managed service (Knowledge Bases), not a custom Lambda pipeline.",
    "Exact terms (codes, IDs, names) missed → <b>hybrid search</b>.",
    "Good docs retrieved, wrong order → <b>reranker</b>.",
    "Long docs lose surrounding context → <b>hierarchical chunking</b>.",
    "Tables / complex PDFs parsed badly → <b>foundation-model parsing</b> or <b>Bedrock Data Automation</b>.",
    "Users must only see permitted docs → <b>metadata filtering</b> at retrieval time.",
    "Knowledge changes frequently → RAG + <b>scheduled sync</b>; style/format change → fine-tuning.",
    "Relationships across connected entities → <b>GraphRAG</b> (Neptune Analytics).",
    "Need custom logic between retrieval and generation → <b>Retrieve</b>; otherwise <b>RetrieveAndGenerate</b>.",
    "Query and documents must use the <b>same embedding model</b> — a mismatch means nothing matches.",
])

n.h1("7. Evaluating RAG")
n.table(["Metric", "Question it answers", "Checks"], [
    ["Context precision", "Are the retrieved chunks relevant?", "Retrieval"],
    ["Context recall", "Did we retrieve everything needed?", "Retrieval"],
    ["Faithfulness / groundedness", "Is the answer supported by the retrieved context?", "Generation"],
    ["Answer relevance", "Does the answer actually address the question?", "Generation"],
], [0.28, 0.52, 0.2])
n.p("Tools: <b>Amazon Bedrock Evaluations</b> (RAG evaluation, LLM-as-a-judge) · Azure: <b>Foundry evaluations</b> "
    "(groundedness, relevance, coherence evaluators).")

n.h1("8. Lab work — what I did")
n.numbered([
    "Uploaded 5 documents to an <b>S3 bucket</b>.",
    "Created a <b>Bedrock Knowledge Base</b> with a quick-create <b>OpenSearch Serverless</b> vector store.",
    "Created a <b>data source</b> pointing at the bucket (default chunking) and <b>synced</b> it (ingestion job).",
    "Tested in the console with default settings and evaluated the model's responses.",
    "Added a <b>second data source</b> on the same documents with <b>hierarchical chunking</b>, and synced it.",
    "Switched the search type to <b>hybrid</b> and increased the <b>number of retrieved results</b>.",
])

n.h1("9. Mistakes and corrections")
n.table(["What happened", "Correction / learning"], [
    ["Described the setting as 'max chunking size for the search'.",
     "Two different settings. <b>Chunk size is an ingestion-time setting</b> on the data source (before sync). "
     "At query time you set <b>number of results</b>, search type and filters. The exam mixes these up on purpose."],
    ["Needed a new data source to try hierarchical chunking.",
     "Correct move: a data source's <b>chunking strategy can't be changed after creation</b>. Re-chunking = new data "
     "source (or new KB) + re-sync."],
    ["Both data sources point at the same 5 docs in one KB.",
     "The KB now holds <b>duplicate content chunked two ways</b>, so results mix both — not a clean A/B test. "
     "Use separate KBs (or delete the old data source) when comparing strategies."],
    ["(Possible surprise) fewer results than requested with hierarchical chunking.",
     "Expected: several child chunks can share one parent, and duplicate parents are merged. Not a bug."],
    ["Cost risk: OpenSearch Serverless left running after the lab.",
     "It bills <b>per hour even when idle</b>. Delete the collection + KB after each lab; set a billing alarm."],
], [0.38, 0.62])

n.h1("10. Key takeaways")
n.bullets([
    "RAG = offline indexing + online retrieve/augment/generate. Know all 12 steps and the AWS service for each.",
    "Bedrock Knowledge Bases is the managed answer; know its chunking options, vector-store options and the "
    "Retrieve vs RetrieveAndGenerate split.",
    "Chunking is decided at ingestion and is fixed per data source.",
    "Hybrid for exact terms, reranker for ordering, hierarchical for context, metadata filters for access control.",
    "Groundedness checks (Guardrails contextual grounding) are the defence against hallucinated answers.",
    "Clean experiments: change one variable at a time, in isolation.",
])

n.page_break()
n.h1("11. Revision questions")
n.h2("Warm-up (answer from memory)")
n.numbered([
    "Name the 5 offline steps of RAG, in order.",
    "Which API returns only chunks, and which returns a full answer with citations?",
    "When does hybrid search beat pure semantic search? Give an example.",
    "What does hierarchical chunking search over, and what does it return to the model?",
    "Your docs change every night. How does the Knowledge Base stay current?",
])
n.h2("Scenario quiz")
n.numbered([
    "A support bot on Bedrock KB misses answers when users type exact part numbers like 'XJ-4471-B'; semantic "
    "questions work. Least-effort fix? (A) fine-tune the embedding model (B) hybrid search (C) bigger chunks "
    "(D) Lambda custom chunker",
    "80-page contracts: answers cite the right clause but miss definitions it depends on. Which chunking? "
    "(A) fixed 200-token (B) none (C) hierarchical (D) semantic with 0% overlap",
    "An Azure app must refuse to answer when retrieved docs don't support the claim. Which feature?",
    "Product catalogue changes nightly; keep the Bedrock KB current with no servers to manage. How?",
    "Top-5 chunks are all somewhat relevant but the best one is usually ranked 4th or 5th. Which step, which fix?",
])

n.h2("Answers")
n.table(["#", "Answer"], [
    ["W1", "Ingest → Parse → Chunk → Embed → Index/Store."],
    ["W2", "<b>Retrieve</b> = chunks only; <b>RetrieveAndGenerate</b> = generated answer + citations."],
    ["W3", "When queries contain exact tokens — product codes, error IDs, names (e.g. 'XJ-4471-B')."],
    ["W4", "Searches small <b>child</b> chunks for precision; returns the larger <b>parent</b> chunk for context."],
    ["W5", "A scheduled <b>ingestion (sync) job</b> — e.g. EventBridge Scheduler calling StartIngestionJob, or an S3-event-triggered sync."],
    ["Q1", "<b>B</b> — hybrid search adds keyword matching for exact tokens."],
    ["Q2", "<b>C</b> — hierarchical: precise child match, parent chunk carries the surrounding definitions."],
    ["Q3", "<b>Azure AI Content Safety groundedness detection</b> (AWS equivalent: Guardrails contextual grounding check)."],
    ["Q4", "Schedule the KB <b>StartIngestionJob</b> (EventBridge Scheduler, serverless) after the nightly data load to S3."],
    ["Q5", "Retrieval ranking problem → add a <b>reranker</b> (Bedrock rerank model / Azure semantic ranker)."],
], [0.08, 0.92])

n.callout("Next: Day 2 — Agents and tool calling (Wed 14 Oct)",
          "Agent loop (reason → act → observe), Bedrock Agents, action groups (Lambda + OpenAPI schema / function "
          "details), return of control, attaching a Knowledge Base, session memory. Prep: basic Python Lambda handler.")

n.build()
print(os.path.abspath(OUT))
