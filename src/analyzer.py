import os
from openai import OpenAI

def generate_brief(company_name: str, website_content: str, news_results: list, value_proposition: str) -> str:
    """
    Generates a strategic account brief using OpenAI.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY not found in environment variables."

    client = OpenAI(api_key=api_key)

    # Format news for the prompt
    news_text = ""
    article_count = 0
    if news_results:
        article_count = len(news_results)
        for item in news_results:
             # keys from .text() are 'title', 'href', 'body'
             title = item.get('title', 'No Title')
             link = item.get('href', item.get('link', ''))
             snippet = item.get('body', item.get('snippet', 'No snippet'))
             # date check for RSS or text results
             
             news_text += f"- {title}: {snippet} ({link})\n"
    else:
        news_text = "No recent news found."

    scraped_status = "Yes" if len(website_content) > 100 and "unavailable" not in website_content else "No"

    prompt = f"""
    You are a B2B Strategy Expert. Your goal is to write a "Strategic Account Brief" for a sales rep who is about to meet with executives from {company_name}.
    
    Here is the Company's Website Content (truncated):
    {website_content[:15000]}
    
    Here is Recent News (Last 6 Months):
    {news_text}

    Here is the User's Value Proposition / Product Focus:
    "{value_proposition}"
    
    Please generate a structured Markdown Brief. 
    
    CRITICAL INSTRUCTIONS:
    1. List ALL news items found. If zero news, state: 'No news found across targeted search queries.'
    2. LANGUAGE PERSPECTIVE: When referencing the user's solution, ALWAYS use 'Your' (e.g., 'Your cybersecurity solutions...'). NEVER use 'Our'. You are writing FOR the user, not AS the user. Keep tone professional and geographically neutral.
    3. DATE FORMATTING: In 'Recent Developments', always start with "[Month Year]:" if date is available, or "Recent:" if not. Extract dates from news snippets where possible.

    Start the brief with exactly this Header Section:
    ## Research Data Sources: DuckDuckGo + Google News
    * Scraped Website: {scraped_status}
    * Total Articles Analyzed: {article_count}
    
    Then continue with the standard sections:
    
    # Strategic Account Brief: {company_name}
    
    ## 1. Company Profile
    *High-level overview of what they do, their primary industry, and key offerings.*
    
    ## 2. Recent Developments
    *Summarize the key recent news events and what they mean for the company's direction. Use the date format "[Month Year]: [Development]".*
    
    ## 3. Buying Signals & Strategic Shifts
    *Identify specific initiatives, expansions, or challenges that might indicate a need for B2B solutions.*
    
    ## 4. Strategic Messaging Hooks
    *Using the user's 'Value Proposition', generate 3 specific conversation starters connecting the company's news/challenges to 'Your' solution. Explain relevance.*
    
    Format the output as clean Markdown.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are a helpful and insightful B2B strategic assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating brief: {str(e)}"
