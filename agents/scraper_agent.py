import asyncio
from playwright.async_api import async_playwright

# The URL of the chapter we want to scrape
TARGET_URL = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"

async def fetch_chapter_content(url: str):
    """
    Navigates to a URL, scrapes the main text content, and takes a screenshot.
    
    Args:
        url (str): The URL of the webpage to scrape.
        
    Returns:
        tuple: A tuple containing the chapter text (str) and the screenshot path (str).
    """
    print("Initializing Scraper Agent...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        print(f"Navigating to {url}")
        await page.goto(url, wait_until="domcontentloaded")
        
        # This selector targets all paragraph 
        content_selector = ".mw-parser-output p"
        
        print("Extracting chapter text...")
        # Wait for the selector to ensure the content is loaded
        await page.wait_for_selector(content_selector)
        
        # Get all matching elements
        content_elements = await page.query_selector_all(content_selector)
        
        # Extract the inner text from each element and join them
        text_parts = [await el.inner_text() for el in content_elements]
        chapter_text = "\n\n".join(text_parts) 
        
        # Take a screenshot 
        screenshot_path = "chapter_1_screenshot.png"
        print(f"Taking screenshot and saving to {screenshot_path}...")
        await page.screenshot(path=screenshot_path, full_page=True)
        
        await browser.close()
        
        print("Scraping complete.")
        return chapter_text, screenshot_path

async def main():
    """Main function to run the scraper for testing."""
    chapter_text, screenshot_file = await fetch_chapter_content(TARGET_URL)
    print("\nSCRAPED CONTENT: ")
    print(chapter_text[:500] + "...")
    print(f"\nScreenshot saved as: {screenshot_file}")

if __name__ == "__main__":
    asyncio.run(main())