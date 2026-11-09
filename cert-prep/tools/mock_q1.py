"""Full mock question bank, part 1 — Domain 1 (FM integration, data management, compliance)."""

QS = [
    dict(
        dom="1", skill="1.2.5", kind="two",
        stem=[
            "A research division continuously retrains a forecasting model pipeline built on Amazon SageMaker AI. Base "
            "embeddings are created in SageMaker Processing, features are encoded during SageMaker Feature Store "
            "ingestion, and the final supervised regression model is trained in SageMaker Training. Last quarter the "
            "regression model was tuned with SageMaker automatic model tuning (AMT), and the tuning job produced a "
            "stable set of high-performing hyperparameters.",
            "A new quarter's dataset is now being ingested. It is larger and has a different distribution, and it must "
            "be used for the next model update. The compute budget is limited, so the new tuning job must not start "
            "from zero. The tuning job must also stop automatically, without manual intervention, once the validation "
            "loss stops improving.",
            "Which combination of actions meets these requirements?",
        ],
        opts=[
            "Create the new tuning job with warm start type IDENTICAL_DATA_AND_ALGORITHM and list last quarter's "
            "tuning job as the parent tuning job.",
            "Create the new tuning job with warm start type TRANSFER_LEARNING and list last quarter's tuning job as "
            "the parent tuning job.",
            "Start a new tuning job from scratch with Bayesian search and a smaller MaxNumberOfTrainingJobs so that it "
            "stays within the compute budget.",
            "Configure the tuning job completion criteria so the job ends when the best objective metric has not "
            "improved for a set number of training jobs.",
            "Create a CloudWatch alarm on the validation-loss metric that invokes a Lambda function to call "
            "StopHyperParameterTuningJob.",
        ],
        ans="BD",
        why="Warm start reuses the results of earlier tuning jobs so the search does not begin from zero. "
            "<b>TRANSFER_LEARNING</b> is the warm start type for when the data (or algorithm inputs) have changed, as "
            "with this larger dataset that has a new distribution. The <b>tuning job completion criteria</b> "
            "(BestObjectiveNotImproving: stop after N training jobs without improvement) end the job automatically. "
            "Per-training-job early stopping (TrainingJobEarlyStoppingType = AUTO) can be added to save more compute.",
        wrong={
            "A": "IDENTICAL_DATA_AND_ALGORITHM assumes the same input data and training image. The dataset has changed "
                 "in size and distribution, so this type does not apply.",
            "C": "Starting from scratch throws away last quarter's knowledge, which the requirement explicitly forbids. "
                 "A smaller job count only limits spending; it does not reuse anything.",
            "E": "This is custom glue code that duplicates a built-in feature, and stopping on a raw metric threshold is "
                 "not the same as 'no longer improving'.",
        }),
    dict(
        dom="1", skill="1.1.1", kind="two",
        stem=[
            "A law firm is building an assistant for its associates. It must answer questions about financial "
            "regulations that the regulator amends almost every week, and every answer must cite the paragraph it "
            "relied on. The assistant must also draft client memos in the firm's strict house structure and tone. Over "
            "two months the team tried detailed system prompts and long few-shot examples for the memo format, but the "
            "output still drifts from the house structure in about 30% of drafts.",
            "Which TWO approaches should the firm use? (Select TWO.)",
        ],
        opts=[
            "Fine-tune a foundation model every week on the newest regulation texts so that the model learns the "
            "amendments.",
            "Use continued pre-training on all historical memos as unlabelled text so the model absorbs the house style.",
            "Build an Amazon Bedrock knowledge base over the regulations with scheduled syncs, and return citations "
            "with every answer.",
            "Add the complete house style guide and ten more full memo examples to the system prompt, and set the "
            "temperature to 0.",
            "Fine-tune a model on several thousand pairs of memo requests and the approved memos the firm sent in "
            "response.",
        ],
        ans="CE",
        why="Facts that change weekly and need citations call for <b>RAG</b> (a knowledge base with scheduled syncs "
            "that returns source references). A stable <b>output behaviour</b> that prompting has already failed to "
            "fix calls for <b>fine-tuning on labelled request → ideal-output pairs</b>. These are two different "
            "problems, so the solution uses both.",
        wrong={
            "A": "Weekly fine-tuning is slow and expensive. It doesn't reliably memorise exact wording, and it can't "
                 "cite sources. Changing facts belong in RAG.",
            "B": "Continued pre-training on raw text adapts the model to domain vocabulary. It doesn't teach the "
                 "request → memo task format, which needs labelled pairs.",
            "D": "The stem says prompting and few-shot examples have already failed. More of the same, with temperature "
                 "0, only makes wrong formats more consistent.",
        }),
    dict(
        dom="1", skill="1.4.1", kind="single",
        stem=[
            "An online retailer keeps its product catalogue (prices, stock levels, categories) in a relational "
            "PostgreSQL database that its engineering team has run for years. It wants semantic product search for a "
            "shopping assistant. A single query must combine vector similarity with SQL conditions such as "
            "<i>in stock</i> and <i>price under 2,000 rupees</i>, and must join to the live product rows. The team "
            "does not want to operate another database engine or keep a second copy of product data in sync.",
            "Which vector store meets these requirements?",
        ],
        opts=[
            "Amazon OpenSearch Serverless vector collection, with price and stock copied into each document as "
            "metadata for filtering.",
            "Amazon Neptune Analytics, with vector search over product nodes linked to category and brand nodes.",
            "Amazon DynamoDB, with an embedding attribute on each product item and a global secondary index on category.",
            "Amazon Aurora PostgreSQL with the pgvector extension, storing each embedding in the product table itself.",
        ],
        ans="D",
        why="<b>pgvector</b> adds vector columns and similarity operators to PostgreSQL. One SQL query can combine "
            "vector distance with WHERE clauses and joins on live rows, using skills the team already has, with no "
            "second engine and no data copy.",
        wrong={
            "A": "This is a second engine, and price and stock would be copies that must be kept in sync. It also "
                 "can't join to live rows.",
            "B": "Graph plus vector search suits relationship-heavy questions. It's another engine, and it has no SQL "
                 "joins to the catalogue.",
            "C": "DynamoDB is not a vector store and has no similarity search; a GSI does exact-key lookups only.",
        }),
    dict(
        dom="1", skill="1.5.1", kind="single",
        stem=[
            "An airline's maintenance assistant uses an Amazon Bedrock knowledge base over 800-page aircraft manuals. "
            "Technicians ask about specific procedure steps, such as torque values for a single bolt. The knowledge "
            "base uses fixed 300-token chunks. Retrieval finds the exact step reliably, but answers often leave out "
            "the safety warnings and preconditions written at the start of the parent section. Increasing the chunk "
            "size made step-level matches noticeably less precise.",
            "Which chunking strategy solves both problems?",
        ],
        opts=[
            "Hierarchical chunking: small child chunks are used for matching, and their larger parent chunks are "
            "returned as context.",
            "Semantic chunking with a lower breakpoint threshold, so that each chunk follows a change of topic in the "
            "text.",
            "Fixed-size chunking at 1,500 tokens with 25% overlap, so that warnings and steps usually share a chunk.",
            "No chunking, so that each manual section is stored and embedded as one complete document.",
        ],
        ans="A",
        why="<b>Hierarchical chunking</b> embeds small child chunks for precise matching. When a child matches, the "
            "larger <b>parent</b> chunk is returned to the model, bringing the section's warnings with it. You get "
            "precision and context together.",
        wrong={
            "B": "Semantic chunking improves chunk boundaries, but each chunk is still returned alone, so the parent "
                 "section's warnings are still missing.",
            "C": "This is the larger-chunk approach the stem says already reduced matching precision; overlap doesn't "
                 "fix that.",
            "D": "Whole sections dilute the embedding (poor precision) and can exceed embedding input limits.",
        }),
    dict(
        dom="1", skill="1.5.4", kind="two",
        stem=[
            "A multinational's HR assistant uses a knowledge base built from policy PDFs in Amazon S3. When a policy "
            "changes, HR uploads a new version and keeps the old one for legal reasons, so several versions sit in "
            "the bucket. Employees complain that the assistant sometimes quotes superseded rules. Separately, an "
            "employee in India must only receive answers based on India policies. The employee's country is "
            "available as a claim in the Amazon Cognito token the application already validates.",
            "Which TWO actions fix both issues with the least ongoing effort? (Select TWO.)",
        ],
        opts=[
            "Instruct the model in the system prompt to ignore any document whose effective date is earlier than the "
            "newest version of the same policy.",
            "Add a country attribute to each document's .metadata.json file and filter every Retrieve call on the "
            "country claim from the user's token.",
            "Create one guardrail per country, with denied topics that describe the other countries' HR policies.",
            "Add a status attribute (current or superseded) to the metadata, set it in the publishing pipeline, and "
            "filter on status = current.",
            "Increase the number of retrieved results so that the newest versions are always included, and let the "
            "model pick the right one.",
        ],
        ans="BD",
        why="Both needs are <b>filtering at retrieval time</b> using document metadata (.metadata.json next to each "
            "file, then a filter in the retrieval configuration). A country filter driven by the trusted token claim "
            "enforces access. A status attribute maintained by the publishing pipeline removes superseded versions "
            "<i>before</i> the model sees them.",
        wrong={
            "A": "Prompt instructions are requests, not filters. The model may still use old text and still can't "
                 "reliably compare dates across chunks.",
            "C": "Guardrails act on topics in text. They can't enforce document-level access, and describing 'other "
                 "countries' policies' as topics is unworkable.",
            "E": "More results means more superseded text reaches the model, which raises the risk.",
        }),
    dict(
        dom="1", skill="1.5.3", kind="all",
        stem=[
            "A team's knowledge base was built with an embedding model that produces 1,536-dimension vectors and is "
            "stored in an OpenSearch Serverless index. To cut storage cost, a developer changed only the application's "
            "query path to Amazon Titan Text Embeddings V2 at 1,024 dimensions. Retrieval calls now fail, and the "
            "developer's quick workaround returns irrelevant results. The team wants to complete the migration "
            "properly.",
            "Which actions are required? (Select ALL that apply.)",
        ],
        opts=[
            "Pad the 1,024-dimension query vectors with zeros to 1,536 dimensions so that they match the existing "
            "index mapping.",
            "Create a vector index (and knowledge base configuration) for 1,024-dimension vectors with the new "
            "embedding model.",
            "Lower the similarity score threshold to make up for the different scale of the new vectors.",
            "Re-embed and re-ingest all source documents with the new embedding model.",
            "Keep the existing vectors and embed only newly added documents with the new model to save cost.",
            "Make sure queries and documents are always embedded by the same model and dimension.",
        ],
        ans="BDF",
        why="Vectors from different embedding models live in <b>different vector spaces</b>, so they can't be "
            "compared, and the index mapping fixes the dimension. A proper migration needs a new index or KB "
            "configuration at the new dimension, <b>full re-embedding</b> of the corpus, and the same model for "
            "queries and documents from then on.",
        wrong={
            "A": "Zero-padding gives the right length but still compares vectors from different models. The results "
                 "would be meaningless.",
            "C": "The scores are meaningless across models; changing a threshold can't make incompatible vectors "
                 "comparable.",
            "E": "This leaves a mixed index where old documents can never match new-model queries correctly.",
        }),
    dict(
        dom="1", skill="1.2.1", kind="single",
        stem=[
            "Every night, an e-commerce company must classify about 5 million new product reviews into 12 complaint "
            "categories. Results are needed by 7 AM. A labelled sample of 2,000 reviews shows that the business "
            "requires at least 92% accuracy. Three Amazon Bedrock models of different sizes and prices are "
            "candidates. Leadership asks for the lowest total cost that provably meets the accuracy target.",
            "What should the team do?",
        ],
        opts=[
            "Choose the largest candidate model, because it is certain to exceed 92%, and run the job through batch "
            "inference to lower its price.",
            "Fine-tune the smallest model on the 2,000 labelled reviews first, then run it on demand through an SQS "
            "queue and Lambda workers.",
            "Evaluate all three models on the labelled sample with a Bedrock model evaluation job, choose the cheapest "
            "one that meets 92%, and run nightly batch inference.",
            "Use Intelligent Prompt Routing across the small and large models on demand, so that each review goes to "
            "the cheapest suitable model.",
        ],
        ans="C",
        why="'Provably meets the target at the lowest cost' means <b>measure, then pick the smallest model that "
            "passes</b> (a Bedrock model evaluation job on your labelled data). Then use <b>batch inference</b> for "
            "a large, non-urgent overnight volume, at about half the on-demand price.",
        wrong={
            "A": "Picking the largest model is a guess, not proof, and it is probably the most expensive option that "
                 "passes.",
            "B": "Fine-tuning before checking whether a base model already passes adds cost and time. On-demand calls "
                 "cost more than batch for this volume.",
            "D": "Routing decides per request at on-demand prices, so it isn't the cheapest for a nightly bulk job, "
                 "and it proves nothing about the 92% target.",
        }),
    dict(
        dom="1", skill="1.2.4", kind="single",
        stem=[
            "A German bank's assistant runs in eu-central-1 and receives ThrottlingException errors during the "
            "monthly salary-day peak. Its compliance office requires that prompts and responses are processed only "
            "inside the European Union. The architecture team wants the least operational overhead and no long-term "
            "capacity commitment.",
            "Which solution should the team use?",
        ],
        opts=[
            "Switch the application to a global cross-Region inference profile so that requests are spread across "
            "every commercial Region.",
            "Purchase Provisioned Throughput in eu-central-1 for the whole month, sized for the salary-day peak.",
            "Deploy a copy of the application in us-east-1, and fail over with Amazon Route 53 when throttling starts.",
            "Switch the application to the EU geographic cross-Region inference profile for the same model.",
        ],
        ans="D",
        why="A <b>geographic cross-Region inference profile</b> (EU) routes requests among EU Regions only, which adds "
            "throughput without extra cost or commitment and keeps processing in the EU.",
        wrong={
            "A": "A global profile can process requests outside the EU, which breaks the residency requirement.",
            "B": "This is a monthly commitment sized for a one-day peak: expensive, and it ignores 'no long-term "
                 "commitment'.",
            "C": "us-east-1 is outside the EU, and running a second stack is high operational overhead.",
        }),
    dict(
        dom="1", skill="1.2.3", kind="two",
        stem=[
            "A medical-device manufacturer wants a model for warranty triage. It has 3 million pages of unlabelled "
            "internal engineering documents full of proprietary component names and acronyms that current models "
            "misunderstand. It also has 4,000 curated examples, each pairing a warranty-claim description with the "
            "exact triage output the quality team expects (category, root-cause code, next step). Both the "
            "vocabulary gap and the output behaviour must be fixed on Amazon Bedrock.",
            "Which TWO customisation steps should the team use? (Select TWO.)",
        ],
        opts=[
            "Model distillation, using the 3 million raw pages as teacher responses for the student model.",
            "Continued pre-training on the 3 million pages of unlabelled engineering text.",
            "Custom Model Import of the base model, so that the proprietary vocabulary is added to its tokenizer.",
            "Fine-tuning on the 3 million pages, converting each page into a prompt with an empty completion.",
            "Fine-tuning on the 4,000 labelled claim → triage-output pairs.",
        ],
        ans="BE",
        why="<b>Continued pre-training</b> on raw, unlabelled text adapts the model to domain language. "
            "<b>Fine-tuning</b> on labelled input → output pairs teaches the task behaviour and format. Run them in "
            "that order: domain first, then task.",
        wrong={
            "A": "Distillation trains a smaller student on a teacher model's <i>generated responses</i> to prompts. "
                 "Raw documents are not teacher outputs.",
            "C": "Custom Model Import brings in weights trained elsewhere. It doesn't train the model on new vocabulary.",
            "D": "Empty completions teach nothing useful. Raw text belongs in continued pre-training.",
        }),
    dict(
        dom="1", skill="1.6.1", kind="two",
        stem=[
            "An insurer runs nine customer-facing applications built by different teams. All of them must use the "
            "same approved persona and legal disclaimer. Compliance must be able to change the wording centrally, "
            "and the change must reach all applications without redeploying any of them. Under no circumstances may "
            "an assistant give an opinion on a specific medical diagnosis, including when users use role-play or "
            "'ignore your instructions' tricks.",
            "Which TWO actions meet these requirements? (Select TWO.)",
        ],
        opts=[
            "Store the persona and disclaimer in a shared Lambda layer that each team bundles into its own functions.",
            "Store the persona as a parameterised Bedrock Prompt Management prompt, and have the applications read "
            "the approved version ARN from AWS AppConfig.",
            "Fine-tune a shared model on thousands of refusal examples for diagnosis questions and on persona-styled "
            "answers.",
            "Attach one guardrail to every model call, with a 'medical diagnosis' denied topic and the prompt-attack "
            "filter enabled on input.",
            "Add strongly worded refusal rules and three refusal examples to each application's system prompt.",
        ],
        ans="BD",
        why="<b>Prompt Management</b> centralises the versioned persona template. Keeping the approved version ARN "
            "in <b>AppConfig</b> lets compliance roll out new wording without redeploys. <b>Guardrails</b> (a denied "
            "topic plus the prompt-attack filter) enforce the never-allowed rule outside the model, where role-play "
            "can't talk its way past it.",
        wrong={
            "A": "A layer change still requires every team to rebuild and redeploy, which violates the "
                 "no-redeploy rule.",
            "C": "Fine-tuning makes refusals more likely but doesn't enforce them, and changing wording would need "
                 "retraining.",
            "E": "Prompt rules can be overridden by jailbreaks, and each copy has to be edited and redeployed.",
        }),
    dict(
        dom="1", skill="1.6.3", kind="three",
        stem=[
            "A bank's platform team manages 40 production prompts in Amazon Bedrock Prompt Management. New rules from "
            "the model risk office:",
            "(1) only senior prompt engineers may approve a change; (2) production may only run immutable, approved "
            "prompts; (3) auditors must be able to see who changed or published any prompt; (4) a bad prompt must be "
            "rolled back within minutes, without a code deployment.",
            "Which THREE actions meet these requirements? (Select THREE.)",
        ],
        opts=[
            "Use IAM so authors can edit only drafts, and allow only the release pipeline's role to call "
            "CreatePromptVersion.",
            "Point production applications at each prompt's working draft, so that approved edits take effect "
            "immediately.",
            "Add a manual approval stage, restricted to senior prompt engineers, to the release pipeline before a "
            "version is created and promoted.",
            "Use Amazon Bedrock model invocation logs as the record of who changed and published prompts.",
            "Keep the production prompt version ARN in AWS AppConfig, and roll back by switching it to the previous "
            "version's ARN.",
            "Create a Prompt Management alias called prod and move it between prompt versions to promote or roll back.",
        ],
        ans="ACE",
        why="IAM limits who can create the <b>immutable versions</b> production runs. A pipeline <b>manual approval</b> "
            "restricted to senior engineers enforces who approves. The <b>version pointer in AppConfig</b> gives "
            "rollback in minutes with no deployment. CloudTrail records the CreatePrompt, UpdatePrompt and "
            "CreatePromptVersion calls, which is the audit trail auditors need.",
        wrong={
            "B": "Drafts are mutable, so production would run unapproved, changing text. That breaks rule (2).",
            "D": "Invocation logs record prompt and response <i>content</i> for model calls. 'Who changed or published "
                 "a prompt' is a management API call, which CloudTrail records.",
            "F": "Prompt Management has versions but no aliases (aliases exist for agents and flows). Keep the pointer "
                 "in configuration instead.",
        }),
    dict(
        dom="1", skill="1.6.6", kind="two",
        stem=[
            "A marketing operations team (two prompt engineers, no backend developers) needs a content pipeline:",
            "classify each incoming request; branch on the JSON field <i>priority</i> returned by the classifier; for "
            "high priority, look up brand rules in a knowledge base before drafting; run a Lambda function that checks "
            "banned claims before returning. They want a visual, low-code tool inside Amazon Bedrock, must reuse "
            "prompts already approved in Prompt Management, and want to release new versions without changing the "
            "calling web application.",
            "Which TWO actions meet these requirements? (Select TWO.)",
        ],
        opts=[
            "Build a Step Functions Express workflow with Bedrock service integrations and a Choice state on the "
            "priority field.",
            "Build a Bedrock agent whose instructions tell it to classify, look up rules, draft and check claims, in "
            "that order.",
            "Have the web application call InvokeFlow with the flow's working draft, so that tested edits go live "
            "immediately.",
            "Build an Amazon Bedrock Flow with prompt nodes that reference the Prompt Management prompts, a condition "
            "node, a knowledge base node and a Lambda node.",
            "Have the web application call InvokeFlow with a flow alias, and move the alias to each newly tested flow "
            "version.",
        ],
        ans="DE",
        why="<b>Bedrock Flows</b> is the low-code canvas inside Bedrock: prompt nodes can reuse Prompt Management "
            "prompts, condition nodes branch on model output, and KB and Lambda nodes handle lookups and checks. "
            "Releasing through an <b>alias → version</b> means the app never changes.",
        wrong={
            "A": "Step Functions isn't a low-code tool inside Bedrock and needs developer skills the team doesn't have.",
            "B": "An agent decides its own steps at runtime, so it isn't a deterministic, reviewable sequence of "
                 "required steps.",
            "C": "Calling the draft means unreviewed edits reach production, with no versioned release or rollback.",
        }),
    dict(
        dom="1", skill="1.6.2", kind="all",
        stem=[
            "A telecom provider's support assistant must:",
            "(1) recognise whether each message is about billing, a technical fault or cancellation, and route it; "
            "(2) keep conversation context for sessions that can last up to two hours; (3) delete stored conversation "
            "data automatically after 30 days; (4) when an account number is missing, ask the customer for it instead "
            "of guessing. Customers sometimes reply hours later.",
            "Which actions meet these requirements? (Select ALL that apply.)",
        ],
        opts=[
            "Keep conversation history in the Lambda function's /tmp directory so that it is reused across invocations.",
            "Use an Amazon Comprehend custom classifier to label the intent of each message and route on the label.",
            "Use a Step Functions Express workflow that waits for the customer's reply about the account number.",
            "Store conversation turns in a DynamoDB table keyed by session ID and timestamp, with a TTL attribute "
            "set to 30 days.",
            "Use a Step Functions Standard workflow with a Choice state on the account number and a "
            ".waitForTaskToken step that asks the customer.",
            "Send the full, untrimmed conversation history with every request so that no context is ever lost.",
        ],
        ans="BDE",
        why="<b>Comprehend custom classification</b> handles intent routing. <b>DynamoDB</b> keyed by session, with "
            "<b>TTL</b>, gives durable history and automatic expiry. A <b>Standard</b> workflow with a task token can "
            "pause for hours while the customer answers the clarification question.",
        wrong={
            "A": "/tmp belongs to one execution environment and disappears when it's recycled. It isn't durable "
                 "session storage.",
            "C": "Express workflows run for at most 5 minutes, and replies can take hours.",
            "F": "Untrimmed history eventually overflows the context window and raises cost. Trim or summarise it "
                 "instead.",
        }),
]
