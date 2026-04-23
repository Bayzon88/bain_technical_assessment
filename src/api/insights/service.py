import json

import requests
from src.api.insights.insights_graph.state import Article
from src.api.insights.config import NEWS_API_KEY
from src.api.insights.insights_graph.graph import generate_graph_result
from src.api.shared.utils import date_range, process_response, url_builder


def request_news(company: str, date_start: str = None, date_end: str = None) -> list[Article]: 
    
    url = url_builder(
        keywords=f'{company} news',
        categories='business, general, technology',
        date=date_range(date_start, date_end), #* latest news 
        countries='us',
        limit='10',
        access_key=NEWS_API_KEY
    )

    response = requests.get(url)
    
    news = process_response(response.json(), 'data')
   
    return news
    
def process_insights(news: list, approach: str = None) -> dict:
    #Created this function to separate concerns. The Graph implementation could change or be moved to a shared folder 
    # in the future, this way we can keep the slice focused on their process without worrying about the technology of 
    # ai insights generation.
    try:
        insights_report = generate_graph_result(news, approach)
        return insights_report
    except Exception as e:
        print(f"Error processing insights: {e}")
        raise e
    


if __name__ == "__main__":
    request_news("anthropic")