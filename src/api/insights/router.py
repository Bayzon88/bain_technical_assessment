import json


from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional

from .config import ENVIRONMENT
from src.api.insights.insights_graph.graph import generate_graph_result
from src.api.insights.service import process_insights, request_news

router = APIRouter()

@router.get("/")
def get_company_insights(
    company_name: str = Query(..., description="Company name (required)"),
    approach: Optional[str] = Query(None, description="Optional approach"), 
    date_start: Optional[str] = Query(None, description="Start date for news retrieval (YYYY-MM-DD)"),
    date_end: Optional[str] = Query(None, description="End date for news retrieval (YYYY-MM-DD)")
):
    #Guard clause to enfore company_name
    if not company_name or not company_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="company_name is required"
        )
    try:
        #flag for development environment
        if ENVIRONMENT == 'dev':
            with open('news_response.json', 'r') as f:
                news = json.load(f)
        else:
            news = request_news(company=company_name, date_start=date_start, date_end=date_end)
        
        if news is None or len(news) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No news articles found for the specified company and date range"
            )
            
        insights_report = process_insights(news, approach)
        
        
        
        return {
        "company_name": company_name,
        "report": insights_report,
        "message": "Request received successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            
            detail=str(e)
        ) from e
    
    
    