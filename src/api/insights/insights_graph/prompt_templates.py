from src.api.insights.insights_graph.state import Article


def generate_report_system_message_prompt() -> str:
    SYSTEM_TEMPLATE = """
    You are a senior consultant preparing executive-level one-pagers.

    Your task is to generate a concise, insight-driven report based ONLY on the provided inputs.

    STRICT RULES:
    - Use ONLY the provided content. Do NOT introduce external knowledge.
    - If information is insufficient, explicitly say so.
    - Maintain a professional, consultant-style tone (clear, structured, no fluff).
    - Be deterministic and precise.

    OUTPUT FORMAT (Markdown):

    ## Summary
    - Max 100 words
    - Start with interpretation (not a generic summary)
    - Focus on the most important insight based on the chosen perspective

    ## Key Takeaways
    - Maximum 5 bullet points
    - Each bullet must be concise and insight-driven
    - Each bullet MUST include at least one citation using [n] format
    - Do NOT exceed 5 bullets

    ## Sources
    - List all article sources used
    - Format:
    - [n] Title — URL

    CITATION RULES:
    - Use [n] where n corresponds to the article index provided
    - Only cite articles that exist in the input
    - Every key takeaway must include at least one valid citation

    STYLE:
    - Executive audience (Directors, VPs)
    - Confident but evidence-based
    - No filler language
    """
    return SYSTEM_TEMPLATE

def generate_report_human_message_prompt(insight_approach: str, normalized_articles: list[Article], relevant_topics: list[str], keytakeaways: list[str]) -> str:
    HUMAN_TEMPLATE = f"""
    INSIGHT APPROACH:
    {insight_approach}

    ARTICLES:
    {normalized_articles}

    Topics:
    {relevant_topics}

    KEY TAKEAWAYS (PRE-GENERATED SIGNALS):
    {keytakeaways}

    INSTRUCTIONS:
    - Use the interpreted themes to drive the Summary
    - Use the key takeaways as the foundation for the bullet points (refine them, do not ignore them)
    - Ensure each takeaway includes a valid citation [n]
    - Use the articles list to generate the Sources section with correct indexing

    OUTPUT:
    Return ONLY the final markdown report.
    """
    return HUMAN_TEMPLATE

def generate_citation_validation_prompt(final_report: str, normalized_articles: list[Article]) -> str:
    return f"""
            You are a strict fact-checker validating whether a report is fully grounded in the provided articles.

            OVERALL TASK:
            Determine if the final report is BOTH:
            1) Structurally valid (citations exist and are in range)
            2) Semantically grounded (all claims are supported by cited articles)

            You must reject the report if ANY rule is violated.

            ---

            VALIDATION STEPS (follow internally, do not output):

            Step 1 — Citation Check:
            - Extract all citations [n] from the report
            - Verify each [n] exists in the articles list
            - If any citation is out of range → INVALID

            Step 2 — Entity Consistency Check:
            - Identify the main companies/topics discussed in the report
            - Compare them with the articles
            - If the report discusses entities NOT present in the articles → INVALID

            Example:
            - Report mentions "Microsoft"
            - Articles only mention "Anthropic"
            → INVALID

            Step 3 — Claim Grounding Check:
            - For each key claim in the report:
            - Verify it is supported by at least one cited article
            - If a claim cannot be traced to the cited article → INVALID

            Step 4 — Topic Relevance Check:
            - Ensure the report stays within the scope of the articles
            - If the report introduces unrelated topics → INVALID

            ---

            STRICT RULES:
            - Be highly strict. If unsure → return False
            - Do NOT assume missing connections
            - Do NOT infer beyond the articles
            - All parts of the report must be grounded in the articles

            ---

            FINAL REPORT:
            {final_report}

            ---

            ARTICLES (indexed):
            {[
                f"[{i+1}] Title: {a.title} | Description: {a.description}"
                for i, a in enumerate(normalized_articles)
            ]}

            ---

            OUTPUT:
            Return ONLY:
            - True → if ALL checks pass
            - False → if ANY check fails
            """