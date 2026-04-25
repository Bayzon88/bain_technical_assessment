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
    articles_text = "\n".join([
        f"[{i+1}] Title: {a.title}\nDescription: {a.description}"
        for i, a in enumerate(normalized_articles)
    ])

    return f"""
    You are a fact-checker validating whether a report is grounded in the provided articles.

    TASK:
    Determine if the final report is valid by checking two things only:
    1) Every citation [n] in the report exists in the articles list
    2) Every key claim in the report can be reasonably traced to at least one cited article

    ---
    VALIDATION STEPS:

    Step 1 — Citation Range Check:
    - Extract all [n] citations from the report
    - Verify each n is between 1 and {len(normalized_articles)}
    - If any citation is out of range → INVALID

    Step 2 — Claim Grounding Check:
    - For each key claim in the report, check if it is reasonably supported by its cited article
    - "Reasonably supported" means the article describes the same event, trend, or fact
    - Do NOT penalize for minor paraphrasing or summarization
    - Do NOT penalize for mentioning companies that appear in articles as context

    ---
    RULES:
    - Only fail if a claim is clearly fabricated or unsupported
    - Paraphrasing and interpretation are allowed
    - If unsure whether a claim is supported → assume True

    ---
    FINAL REPORT:
    {final_report}

    ---
    ARTICLES:
    {articles_text}

    ---
    OUTPUT:
    Return ONLY one word:
    - True → if all citations are in range and claims are reasonably grounded
    - False → if any citation is out of range or a claim is clearly fabricated
    """