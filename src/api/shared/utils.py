from datetime import date,timedelta

def url_builder(**kwargs) -> str:
    ## Reusable function for building url with multiple query parameters
    ## I'm creating this function to avoid hardcoding urls or creating multiple functions for different 
    ## requests using news api
    base_url = 'https://api.mediastack.com/v1/news?'
    query_params = []
    
    for key, value in kwargs.items():
        query_params.append(f"{key}={value}")
    
    url = base_url + '&'.join(query_params)
    
    return url 


def date_range(start: str, end: str) -> str:
    #generates comma separated date range for news api service
    if not start:
        start =  (date.today() - timedelta(days=15)).isoformat()
    if not end:
        end = date.today().isoformat()
        
    return f"{start},{end}"
    
def process_response(response: dict, key: str) -> list: 
    #access response and returns the selected key value
    
    articles = response.get(key, [])
    if(not articles):
        return []

    return articles