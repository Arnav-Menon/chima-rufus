# Introduction
Rufus is a web scraping and information extraction tool designed to integrate with Retrieval-Augmented Generation (RAG) pipelines. It provides a simple and efficient way to extract relevant information from web pages and return it in a structured format.

# How Rufus Works
Rufus works by taking in a URL and a set of instructions as input, and then using a combination of web scraping and natural language processing techniques to extract relevant information from the web page. The extracted information is then returned in a JSON format, which can be easily integrated into a RAG pipeline.

# Architecture
Rufus consists of the following components:

- Web Scraper: Responsible for scraping the web page and extracting relevant information.
- Natural Language Processing (NLP) Module: Responsible for processing the extracted information and returning it in a structured format.
- API: Provides a simple interface for integrating Rufus into a RAG pipeline.

# Integrating Rufus into a RAG Pipeline
To integrate Rufus into a RAG pipeline, follow these steps:

1. Install Rufus: Install Rufus using pip: pip install rufus
2. Import Rufus: Import Rufus into your RAG pipeline: from rufus import RufusClient
3. Create a Rufus Client: Create a Rufus client instance: client = RufusClient()
4. Define Instructions: Define the instructions for Rufus to extract relevant information: instructions = "Extract all information about the company"
5. Call Rufus: Call Rufus with the URL and instructions: results = client.scrape("https://www.nba.com", instructions)
6. Process Results: Process the results returned by Rufus and integrate them into your RAG pipeline.

# Example Use Case
Here is an example of how to use Rufus to extract information about a company:

```
from rufus import RufusClient

# Create a Rufus client instance
client = RufusClient()

# Define the instructions
instructions = "Give me all information about the Sacramento Kings"

# Call Rufus with the URL and instructions
results = client.scrape("https://www.nba.com", instructions)

# Process the results
print(results)
```

# Setup

## Prerequisites

- Python 3.9 or above (3.11 recommended)
- Open in VSCode and install recommmended extensions for optimal dev experience
- sudo apt install python3.x-venv (For LINUX)

## Create virtual environment

```bash
python -m venv .venv
```

## Activate virtual environment

```bash
#UNIX
source .venv/bin/activate

#Windows
.venv/Scripts/activate.bat
#OR
.venv/Scripts/Activate.ps1
```

## Install requirements

```bash
pip install -r requirements.txt
```

# API Documentation
The Rufus API provides the following methods:

- `scrape(url, instructions)`: Scrapes the web page at the specified URL and extracts relevant information based on the instructions.