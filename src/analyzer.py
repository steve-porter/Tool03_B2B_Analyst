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

    # Determine status for header
    scraped_bool = len(website_content) > 100 and "unavailable" not in website_content
    scraped_status_str = "Yes" if scraped_bool else "No (Restricted)"
    
    # Construct the data source line exactly as requested
    header_line = f"📊 Research Sources: DuckDuckGo + Google News | Website: {scraped_status_str} | Articles Analyzed: {article_count}"
    
    # Handle empty value proposition fallback for the prompt
    val_prop_context = value_proposition if value_proposition and value_proposition.strip() else "Premium B2B Services"

    prompt = f"""
    You are a B2B Strategy Expert creating a Strategic Account Brief for a sales professional.

    COMPANY: {company_name}

    WEBSITE CONTENT (truncated):
    {website_content[:15000]}

    RECENT NEWS (Last 6 Months):
    {news_text}

    USER'S SOLUTION:
    "{val_prop_context}"

    Generate a brief following this EXACT structure:

    At the very top, include this metadata line in plain text:
    📊 Research Sources: DuckDuckGo + Google News | Website: [Yes/No] | Articles Analyzed: {len(news_results)}

    # Strategic Account Brief: {company_name}

    ## 1. Company Profile
    Provide a concise 2-3 sentence overview of what the company does, their primary industry, and key offerings based on the website content provided.

    ## 2. Recent Developments
    List recent news with specific dates in [Month Year] format. Each item should be a bullet point starting with the date in square brackets, followed by the development. If no news found, state: "No recent news articles were found in our search."

    ## 3. Buying Signals & Strategic Shifts
    Identify 3-5 specific indicators from the news and company info that suggest they might need B2B solutions. Focus on: expansion, technology changes, regulatory challenges, growth signals, operational efficiency drives. Write as a cohesive paragraph, NOT bullet points.

    ## 4. Strategic Messaging Hooks

    CRITICAL FORMAT - You MUST follow this structure EXACTLY for each hook:

    1. [Hook Title]: "[Quoted messaging text the user can use verbatim with this prospect]"
    
    Relevance: [2-3 sentences explaining why this hook is specifically relevant to this company's situation based on the news/context you found]

    2. [Hook Title]: "[Quoted messaging text]"
    
    Relevance: [Explanation tied to specific company context]

    3. [Hook Title]: "[Quoted messaging text]"
    
    Relevance: [Explanation tied to specific company context]

    EXAMPLE of correct format:

    1. Securing Digital Currency Infrastructure: "With your recent expansion into digital currency scanning technologies, how do you ensure these systems remain protected from ransomware and breaches with managed threat detection solutions?"
    
    Relevance: The company's involvement in digital currency technologies creates new attack surfaces that require specialized cybersecurity monitoring and response capabilities.

    CRITICAL FORMATTING RULES:
    - Do NOT use markdown code blocks (```) anywhere in your output
    - Use ## for main section headings only  
    - Do NOT use bold (**) within paragraph text except for emphasis in hook titles
    - Keep all currency and number formatting as plain text
    - Each messaging hook MUST include both the quoted text AND the Relevance explanation
    - Relevance explanations must reference specific details from the company's news or situation
    - Never start a sentence with "Your" - use second person naturally within sentences only

    Output in clean, professional Markdown. Be specific and actionable throughout.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are a helpful and insightful B2B strategic assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content
        
        # Strip potential markdown code block wrapping
        if content.startswith("```markdown"):
            content = content.replace("```markdown", "").replace("```", "")
        elif content.startswith("```"):
             content = content.replace("```", "")
             
        # Content now includes the header as per the new prompt instructions
        return content

    except Exception as e:
        return f"Error generating brief: {str(e)}"
