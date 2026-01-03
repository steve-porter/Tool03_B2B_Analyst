SALES_OUTREACH_PROMPT = """
You are a B2B Strategy Expert creating a Strategic Account Brief for a sales professional.

COMPANY: {company_name}

WEBSITE CONTENT (truncated):
{website_content}

RECENT NEWS (Last 6 Months):
{news_text}

USER'S SOLUTION:
"{val_prop_context}"

Generate a brief following this EXACT structure:

At the very top, include this metadata line in plain text:
📊 Research Sources: DuckDuckGo + Google News | Website: {scraped_status} | Articles Analyzed: {article_count}

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

INTERVIEW_PREP_PROMPT = """
You are a Strategic Career Advisor helping a candidate prepare for an interview. Your analysis must be evidence-based, specific, and grounded in verifiable company data.

COMPANY: {company_name}

WEBSITE CONTENT (truncated):
{website_content}

RECENT NEWS (Last 6 Months):
{news_text}

JOB DESCRIPTION (JD):
{job_description}

CANDIDATE CV (Extracted Text):
{cv_text}

CRITICAL: You MUST generate ALL 6 sections below. Do NOT skip any section. Do NOT merge sections.

Generate an Interview Strategy Guide following this EXACT structure:

At the very top, include this metadata line in plain text:
📊 Research Sources: DuckDuckGo + Google News | Website: {scraped_status} | Articles Analyzed: {article_count}

# Interview Strategy Guide: {company_name}

## 1. Company Overview
Provide a concise 2-3 sentence overview of what the company does, their primary industry, and key offerings.

## 2. Recent Developments

CRITICAL FORMAT REQUIREMENT: This section MUST be a BULLETED LIST. Do NOT write a narrative paragraph.

Each bullet point MUST include:
1. A date in [Month Year] format at the start
2. A description of the development
3. A hyperlink to the source article in the format ([Source](URL))

EXAMPLE FORMAT:
- [Nov 2025] Company raised $50M Series C funding led by Accel Partners ([TechCrunch](https://example.com/article1))
- [Oct 2025] Launched AI-powered fraud detection module for enterprise clients ([Company Blog](https://example.com/blog))
- [Sep 2025] Appointed Jane Smith as new Chief Product Officer ([LinkedIn](https://example.com/announcement))

Focus on hard news: financial results, M&A activity, executive hires, product launches, strategic pivots.

If no news articles were found in the search, state: "No recent news articles were found in our search."

## 3. Role Hypothesis
Explain why they are hiring for this specific role NOW. Connect the Job Description requirements to the company's recent developments from Section 2. Be specific about what business need this role addresses.

## 4. Candidate Fit & Alignment

### Your Strongest Assets for This Role

Identify the 3 best achievements, experiences, or skills from the candidate's CV that are most relevant to this role and company.

CRITICAL: You MUST quote specific details from the CV. Look for:
- Revenue numbers (e.g., "generated $3M in Year 1")
- Team sizes (e.g., "led a team of 15")
- Percentages (e.g., "increased conversion by 40%")
- Timeframes (e.g., "launched in 6 months")

For each of the 3 assets:
1. **[Asset Title]**: [Quote the specific achievement from CV with metrics]
   - **Why it matters**: [Explain how this directly addresses a JD requirement or company challenge]

EXAMPLE FORMAT:
1. **Revenue Generation in New Markets**: Steve's launch of SD Worx Spain generated €3M ACV in Year 1 with a team of 8.
   - **Why it matters**: The JD emphasizes "proven ability to scale in emerging markets" - this demonstrates exactly that capability with quantified results.

### Strategic Proof Points

Attempt to create 2-3 specific "Company Challenge → Your Evidence" mappings.

MANDATORY FORMAT:
**Company Challenge**: [Specific challenge from Recent Developments or JD - be specific, not generic]
**Your Proof Point**: [Specific metric or achievement from CV that addresses this challenge]

EXAMPLE:
**Company Challenge**: The company's recent $50M raise (Nov 2025) indicates aggressive expansion plans requiring rapid team scaling.
**Your Proof Point**: Steve scaled the SD Worx team from 3 to 45 people in 18 months while maintaining 95% retention.

CRITICAL INSTRUCTION: If you cannot find specific metrics in the CV that map to company challenges, you MUST include this exact warning:

"⚠️ **Strengthen Your Application**: Based on the CV provided, we were unable to identify specific quantified achievements that directly map to the strategic challenges outlined above. Consider adding metrics (revenue impact, team size, % growth, cost savings, etc.) to strengthen your interview talking points."

## 5. Strategic Priorities to Explore

MANDATORY: This section MUST appear in your output. Do NOT skip it.

Based on the company's recent developments (Section 2) and JD requirements, identify 3-4 high-impact TACTICAL areas the candidate should explore during the interview. These should be OPERATIONAL or PROCESS-focused questions about how the team works.

MANDATORY FORMAT for each priority:
**[Priority Area]**: [Why this matters - reference specific news or JD requirement]
→ *Interview Angle*: "[Specific tactical/operational question to ask]"

EXAMPLE:
**Tech Stack & Tools**: Given the JD mentions "experience with modern data pipelines," understanding the current infrastructure is key.
→ *Interview Angle*: "What does the current data infrastructure look like, and what are the main technical challenges the team is facing?"

Focus on: team structure, processes, tools, day-to-day operations, immediate challenges. These are DIFFERENT from the strategic questions in Section 6.

## 6. Killer Strategic Questions

Generate 3 high-impact STRATEGIC questions the candidate should ask the hiring manager. These should be BIG PICTURE questions about company direction, vision, and long-term goals - NOT operational details (those are in Section 5).

For each question:
1. Provide 1-2 sentences of CONTEXT explaining why this question matters (reference specific company news or JD details)
2. State the QUESTION itself

EXAMPLE FORMAT:
**Context**: The company's recent Series C raise (Nov 2025) and new CPO hire (Sep 2025) suggest a major product evolution is underway.
**Question**: How do you see this role contributing to the product transformation over the next 12 months, and what does success look like in Year 1?

Focus on: company vision, strategic direction, market positioning, long-term roadmap, competitive landscape.

CRITICAL FORMATTING RULES:
- ABSOLUTELY NO BACKTICKS: Do NOT use backticks (`) anywhere in your output - not for code blocks, not for inline code, not for any reason
- Do NOT use markdown code blocks (```) anywhere in your output
- Do NOT wrap any text in backticks - this causes white background rendering issues
- Use ## for main section headings only
- Section 2 MUST be bulleted list with dates and hyperlinks - NOT a narrative paragraph
- Section 5 MUST appear - do not skip it
- Section 5 should focus on TACTICAL/OPERATIONAL questions (team, process, tools)
- Section 6 should focus on STRATEGIC questions (vision, direction, long-term goals)
- Include hyperlinks for all news sources in Section 2 using ([Source](URL)) format
- Quote specific CV metrics in Section 4 - do not use generic phrases like "extensive experience"
- Do NOT use bold (**) within paragraph text except for section labels (Company Challenge, Your Proof Point, Priority Area, Context, Question, Why it matters, Asset Title)
- Keep all currency and number formatting as plain text
- Be specific and evidence-based throughout - avoid generic career advice

Output in clean, professional Markdown.
"""
