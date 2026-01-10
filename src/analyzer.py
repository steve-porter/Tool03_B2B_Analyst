import os
from openai import OpenAI
from src.prompts import SALES_OUTREACH_PROMPT, INTERVIEW_PREP_PROMPT

def generate_brief(
    company_name: str, 
    website_content: str, 
    news_results: list, 
    mode: str = "Sales Outreach",
    value_proposition: str = None,
    job_description: str = None,
    cv_text: str = None
) -> str:
    """
    Generates a strategic report (Sales Brief or Interview Strategy) using OpenAI.
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
             title = item.get('title', 'No Title')
             link = item.get('href', item.get('link', ''))
             snippet = item.get('body', item.get('snippet', 'No snippet'))
             news_text += f"- {title}: {snippet} ({link})\n"
    else:
        news_text = "No recent news found."

    # Determine status for header
    scraped_bool = len(website_content) > 100 and "unavailable" not in website_content
    scraped_status_str = "Yes" if scraped_bool else "No (Restricted)"
    
    # Select prompt based on mode
    if "Interview" in mode:  # Handles both "Job Interview Prep" and legacy "Interview Prep"
        prompt = INTERVIEW_PREP_PROMPT.format(
            company_name=company_name,
            website_content=website_content[:10000], # Slightly smaller context for multi-source
            news_text=news_text,
            job_description=job_description or "Not provided",
            cv_text=cv_text or "Not provided",
            scraped_status=scraped_status_str,
            article_count=article_count
        )
    else:
        # Default to Sales Outreach
        val_prop_context = value_proposition if value_proposition and value_proposition.strip() else "Premium B2B Services"
        prompt = SALES_OUTREACH_PROMPT.format(
            company_name=company_name,
            website_content=website_content[:15000],
            news_text=news_text,
            val_prop_context=val_prop_context,
            scraped_status=scraped_status_str,
            article_count=article_count
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are a helpful and insightful strategic assistant."},
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
        
        # Remove all backticks to prevent inline code formatting (white background issue)
        content = content.replace("`", "")
             
        return content

    except Exception as e:
        return f"Error generating report: {str(e)}"
