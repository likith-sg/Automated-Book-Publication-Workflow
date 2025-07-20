# Automated Book Publication Workflow

This project is an end-to-end system designed to automate the initial stages of book publication. It fetches chapter content from a web source, uses Large Language Models (LLMs) to rewrite and refine the text, and provides a web-based interface for a human editor to review, edit, and approve the final version.

## Key Features

* **Web Scraping**: Fetches chapter text and screenshots from a URL using Playwright.
* **AI-Powered Writing & Review**: Utilizes the Gemini API for two distinct AI agents: an **AI Writer** to spin the text and an **AI Reviewer** to refine it.
* **Content Versioning**: Saves every version of the text (original, AI-spun, AI-reviewed, and human-finalized) into a ChromaDB vector database.
* **Semantic Search**: Enables searching through chapter versions based on content similarity.
* **Human-in-the-Loop (HITL)**: A Streamlit web application allows a human editor to compare versions, make final edits, and approve the content.

## Tech Stack

* **Language**: Python
* **Web Scraping**: Playwright
* **AI Model**: Google Gemini API
* **Vector Database**: ChromaDB
* **Web Interface**: Streamlit

## Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/likith-sg/Automated-Book-Publication-Workflow.git
    cd Automated-Book-Publication-Workflow
    ```

2.  **Create and Activate Virtual Environment (Windows)**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright Browsers**
    ```bash
    playwright install
    ```

5.  **Set Environment Variable (Windows)**
    Set your Google API key as an environment variable. Use the `setx` command in a command prompt and then **restart your terminal**.
    ```bash
    setx GOOGLE_API_KEY "YOUR_API_KEY_HERE"
    ```

## How to Run

1.  **Run the Backend Pipeline**
    This script performs the initial scraping, AI processing, and populates the database. Run this first.
    ```bash
    python -m agents.llm_agent
    ```

2.  **Run the Frontend Web App**
    This starts the web interface for the human editor.
    ```bash
    streamlit run app.py
    ```

## Project Configuration

The target URL for web scraping is defined as a constant within the `agents/scraper_agent.py` script. While it is pre-configured for a specific chapter, it can be easily modified to point to other web pages.

* **Default Target URL**:
    `https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1`
