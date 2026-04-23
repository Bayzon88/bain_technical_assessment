from src.api.insights.insights_graph.state import Article, InsightsGraphState

# Do not move to utils file, this is domain specific logic for langgraph management. 
def normalize_articles(state: InsightsGraphState) -> list[Article]:
    normalized = []

    for raw in state.raw_articles:
        author = (raw.author or "").strip()
        title = (raw.title or "").strip()
        description = (raw.description or "").strip()
        url = (raw.url or "").strip()
        source = (raw.source or "").strip()

        # Fallbacks
        if not author:
            author = "Unknown"
        if not title:
            title = "Untitled"
        if not description:
            description = "No content provided."
        if not url:
            url = "N/A"
        if not source:
            source = "Unknown"

        article = Article(
            author=author,
            title=title,
            description=description,
            url=url,
            source=source,
            image=raw.image,
            category=raw.category,
            language=raw.language,
            country=raw.country,
            published_at=raw.published_at,
        )

        normalized.append(article)

    return normalized