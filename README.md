# Assignment

## Implementation

- System: Company Name -> News -> Insight
- Delivery: Insight summary based on latest news
- Architecture: Vertical Slice. Works better for PoC/MVP and is extendable beyond this stage(e.g new features)

## Requirements

### Functional

- Inputs: company name + insight approach(optional)
- Extract relevant news
- System ingest, process and transforms data
- System process data to reduce AI token usage
- AI generates insights summary using processed data

### Non-Functional

- System should only generate insights for 1 company at a time
- System stores insights(for later)
- System latency is acceptable(processing time below 5000s)
- Insights report must not exceed 1 page, be concise and easy to read/explain

### Assumptions

- Users are willing to wait for the completion of the process
- Users want to give "tone" to the insight(e.g. marketing, finance, business focused responses)

## Tech Stack

### Backend

- FastAPI: fast development process, ideal for fast prototyping (PoC/MVP)
- External APIs: News feeds or news sites

### Frontend

- React: Library and unopinionated, allows us to start simple and grow as needed.
- Context API: Being a PoC, there is no need to use State Management libraries, this reduces boilerplate and development time but the trade off is that if the system out-grows the initial requirements we may need to refactor. For PoC i preffer Context over State Management.
- UI: Shadcn + Tailwind, AI is heavily influence by tailwind so we can expect seamless development process with AI tools. Shadcn is a mature/easy to use framework and comes with pre-built components so reduces the development cycle time.

## Run App

### Docker command

```bash
sudo docker run --env-file .env -p 5050:8000 business-insights
```

### Environmental variables

```bash
NEWS_API_KEY=[mediastack_api_key]
OPENAI_API_KEY=
ENVIRONMENT=production
```

## Images

![report generated](https://github.com/Bayzon88/bain_technical_assessment/report.png?raw=true)
