import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Article(BaseModel):
    author: Optional[str]
    title: Optional[str]
    description: str
    url: str
    source: Optional[str]
    image: Optional[str]
    category: Optional[str]
    language: Optional[str]
    country: Optional[str]
    published_at: Optional[str]



class InsightsGraphState(BaseModel):
    # --- Input ---
    raw_articles: list[Article]
    insight_approach: str

    # --- Processing ---
    normalized_articles: list[Article] = Field(default_factory=list)
    relevant_topics: list[str] = Field(default_factory=list)
    keytakeaways: list[str] = Field(default_factory=list)
    interpreted_themes: list[str] = Field(default_factory=list)

    # --- Output ---
    final_report: Optional[str] = None

    # --- Validation ---
    citation_valid: bool = False
    retry_count: int = 0
    max_retries: int = 3
    validation_warning: Optional[str] = None