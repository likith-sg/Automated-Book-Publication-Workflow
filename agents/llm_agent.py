import os
import google.generativeai as genai
import asyncio
from .scraper_agent import fetch_chapter_content, TARGET_URL
from core.database import add_chapter_version, semantic_search

def setup_llm():
    """Configures the Gemini API and returns the model."""

    api_key = ""
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("LLM Model Initialized (gemini-1.5-flash)")
    return model

# Initialize the model 
llm_model = setup_llm()

# Prompts for our AI Agents
AI_WRITER_PROMPT = """
You are an expert fiction author. Rewrite the following chapter from a classic adventure novel. 
Your goal is to modernize the language, increase the pacing, and make it more vivid for a contemporary young adult audience. 
Do not change the core plot points, character names, or the sequence of events.
Focus on making the prose punchy and engaging.
Here is the original chapter text:
"""

AI_REVIEWER_PROMPT = """
You are a meticulous editor. Review the following text. 
Correct any grammatical errors, fix awkward phrasing, and ensure the tone is consistent with a modern young adult adventure novel.
Output only the clean, corrected text. Do not add any commentary.
Here is the text to review:
"""

async def spin_text(original_text: str) -> str:
    """Uses the LLM to spin the text with the AI Writer prompt."""
    print("\nSending text to AI Writer for spinning...")
    full_prompt = f"{AI_WRITER_PROMPT}\n\n{original_text}"
    response = await llm_model.generate_content_async(full_prompt)
    print("AI Writer finished.")
    return response.text

async def review_text(spun_text: str) -> str:
    """Uses the LLM to review the text with the AI Reviewer prompt."""
    print("\nSending text to AI Reviewer for refinement...")
    full_prompt = f"{AI_REVIEWER_PROMPT}\n\n{spun_text}"
    response = await llm_model.generate_content_async(full_prompt)
    print("AI Reviewer finished.")
    return response.text

async def main():
    """Main function to run the full scrape -> spin -> review -> save pipeline."""
    # Define a unique ID for this chapter
    CHAPTER_NUMBER = 1
    
    # 1. Scrape the original content and save it
    original_text, _ = await fetch_chapter_content(TARGET_URL)
    add_chapter_version(original_text, "original", CHAPTER_NUMBER)

    # 2. Pass the original text to the AI Writer and save the result
    spun_version = await spin_text(original_text)
    add_chapter_version(spun_version, "ai_spun", CHAPTER_NUMBER)
    
    # 3. Pass the spun version to the AI Reviewer and save the result
    reviewed_version = await review_text(spun_version)
    add_chapter_version(reviewed_version, "ai_reviewed", CHAPTER_NUMBER)

    # 4. Print the final result for confirmation
    print("\n\nAI REVIEWER REFINED VERSION (Saved to DB)")
    print(reviewed_version)
    
    # 5. (Example) Perform a semantic search on the content we just saved
    search_query = "A description of the island"
    print(f"\nPerforming semantic search for: '{search_query}'")
    search_results = semantic_search(query_text=search_query, chapter_id=CHAPTER_NUMBER)
    print("Top search result document:", search_results['documents'][0][0][:200] + "...")


if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())