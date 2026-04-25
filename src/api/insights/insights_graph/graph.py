import json
import logging
from typing import Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain.messages import HumanMessage, SystemMessage

logging.basicConfig(level=logging.INFO)

from src.api.insights.insights_graph.prompt_templates import generate_citation_validation_prompt, generate_report_human_message_prompt, generate_report_system_message_prompt
from src.api.insights.insights_graph.normalization import normalize_articles
from src.api.insights.config import OPENAI_API_KEY
from .state import InsightsGraphState

llm = ChatOpenAI(model="gpt-5-nano", temperature=0.1, api_key=OPENAI_API_KEY) #TODO: Check model effectiveness

def normalize_data(state: InsightsGraphState) -> InsightsGraphState:
    logging.info("Normalizing articles...")
    state.normalized_articles = normalize_articles(state)
    
    return state


def extract_relevant_topics(state: InsightsGraphState) -> InsightsGraphState:
    logging.info("Extracting relevant topics...")
    messages = [
    (
        "system",
        "You are an expert insights analyst. Your task is to extract a maximum of 10 the most relevant topics and themes from a set of news articles about a company, and synthesize them into a concise report. Focus on identifying key trends, sentiments, and any emerging issues that could impact the company's business. Use the normalized article data provided to inform your analysis.",
    ),
    ("human", str(state.raw_articles)),
]

    llm_response = llm.invoke(messages)
    state.relevant_topics = llm_response.content.splitlines()  
    logging.info("Relevant topics extracted: %s", len(state.relevant_topics))
    return state


def extract_keytakeaways(state: InsightsGraphState) -> InsightsGraphState:
    logging.info("Extracting key takeaways...")
    messages = [
        (
            "system",
            "You are an expert insights analyst. Your task is to extract the most important takeaways from a set of news articles about a company, max 10 takeaways.",
        ),
        ("human", str(state.raw_articles)),
    ]

    llm_response = llm.invoke(messages)
    state.keytakeaways = [key_takeaway for key_takeaway in llm_response.content.splitlines() if key_takeaway.strip() ] 
    logging.info("Key takeaways extracted: %s", len(state.keytakeaways))

    return state


def generate_report(state: InsightsGraphState) -> InsightsGraphState:
    logging.info("Generating report...")
    system_message = SystemMessage(generate_report_system_message_prompt())
    human_message = HumanMessage(generate_report_human_message_prompt(state.insight_approach, state.normalized_articles, state.relevant_topics, state.keytakeaways))
    messages = [
        system_message,
        human_message
    ]
    llm_response = llm.invoke(messages)
    state.final_report = llm_response.content
    
    return state


def is_citations_valid(state: InsightsGraphState) -> Literal["increment_retry", END]:
    # Validate citations to make sure the information in the report is supported by the articles
    # TODO: This needs more work, currently it correctly identifies citations and relevant content in the report about 85% of the time. 
    if state.retry_count >= state.max_retries:
        raise Exception("Report validation failed after maximum retries.")
    
    logging.info("Validating citations...")
    system_message = generate_citation_validation_prompt(state.final_report,state.normalized_articles)
    messages = [
        system_message
    ]
    llm_response = llm.invoke(messages)
    validation_result = llm_response.content.strip().lower()
    is_valid = (validation_result.strip().strip(".").lower() in ['true', 'valid', 'yes'])
    if is_valid:
        logging.info("Citations are valid.")
        return END
        
    return "increment_retry"
        
def increment_retry(state:  InsightsGraphState) -> dict: 
    logging.warning(f"Citations are invalid. Retrying #{state.retry_count+1} report generation...")
    return {"retry_count": state.retry_count + 1}

def build_graph():
    builder = StateGraph(InsightsGraphState)

    # Nodes
    builder.add_node("normalize", normalize_data)
    builder.add_node("extract", extract_relevant_topics)
    builder.add_node("keytakeaways", extract_keytakeaways)
    builder.add_node("generate_report", generate_report)
    builder.add_node("validate", is_citations_valid)
    
    builder.add_node("increment_retry", increment_retry)
    
    builder.set_entry_point("normalize")

    builder.add_edge("normalize", "extract")
    builder.add_edge("extract", "keytakeaways")
    builder.add_edge("keytakeaways", "generate_report")
    builder.add_edge("increment_retry", "generate_report")
    
    #Loop for validating report against articles. 
    builder.add_conditional_edges("generate_report", is_citations_valid, ["increment_retry", END])
    
    return builder.compile()


def generate_graph_result(news: list, approach: str) -> str:
    graph = build_graph()

    messages = [HumanMessage(content="test")]
    messages = graph.invoke({"raw_articles": news, "insight_approach": approach}) 
    
    return  messages['final_report']


# if __name__ == "__main__":
#     generate_graph_result([], "finance")