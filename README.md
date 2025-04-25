# AI Web Scraper for Data Science Students

This project provides an AI-powered web scraper using **Google Generative AI (Gemini)** and **Selenium** for scraping web pages and extracting specific information based on a user’s description. The application is built with **Streamlit** for a user-friendly interface and **BeautifulSoup** for parsing the HTML content.

## Features

- **User Authentication**: Create accounts and log in using a secure login system.
- **Web Scraping**: Extracts content from any given URL using Selenium and BeautifulSoup.
- **Data Parsing**: Uses Google Gemini’s generative capabilities to parse text and extract specific information based on user instructions.
- **AI Integration**: Utilizes Google's Gemini AI model (`gemini-1.5-flash`) to analyze and process web content.

## Requirements

To run this project, you'll need the following dependencies:

- **google-generativeai**: For accessing Google's Gemini API for AI content generation.
- **selenium**: For scraping web content using Chrome.
- **beautifulsoup4**: For parsing HTML content from the web.
- **streamlit**: To create an interactive frontend for the web scraper.
- **python-dotenv**: For securely managing environment variables, especially API keys.

### Install the dependencies:

You can install the required packages by running:
  ```bash
  pip install -r requirements.txt
