# RAG-Powered Stock Advisory System

## Overview
This project is a **Retrieval-Augmented Generation (RAG)** system designed to provide financial advice on NVDA, TSLA, and GOOG stocks. The system leverages **web scraping**, **vector search**, and **LLM-based reasoning** to generate insights based on real-time financial news and discussions.

## Features
- **Web Scraping**: Collects financial news and discussions every 6 hours.
- **Temporary Data Storage**: Stores scraped data for 24 hours before deletion.
- **Vector Store (FAISS)**: Stores processed text for retrieval and contextual enrichment.
- **Financial Advice Query System**: Uses an LLM to provide stock-related insights.
- **Deployment**: Can be accessed via UI or API.
- **Bonus Features**:
  - Voice interaction
  - Video-based responses
  - User sentiment analysis

## Flow of a RAG-Powered Conversational Bot
User Input: The user types a query.
Query Preprocessing: The input is cleaned, tokenized, and converted into an embedding.
Document Retrieval: Relevant documents are retrieved from a knowledge base (in our case, a web-scraped dataset).
Context Fusion: The retrieved documents are combined with the original query.
Response Generation: An LLM generates a response based on the fused context.
Response Delivery: The AI-generated response is sent back to the user.

## System Architecture
1. **Data Collection**
   - Users can input preferred URLs for scraping.
   - Scrapes stock-related news and discussions every 6 hours.
   - Stores extracted content in **MongoDB** for temporary storage (24-hour retention).

2. **Vector Storage & Retrieval**
   - Processes text and stores embeddings in **FAISS**.
   - Implements `store_data_faiss` and `search_faiss` functions in `vector_store.py`.

3. **LLM-Based Reasoning**
   - Queries FAISS for relevant context.
   - Enhances responses using a language model.

4. **Deployment**
   - Accessible via a UI (gamma-advisor @ https://github.com/xloanx/gamma-advisor-backend.git) or API for querying financial insights.


## Project Structure
```sh
gamma-advisor-backend/
│── app/
│   │── __init__.py
│   │── main.py
│   │── config.py
│   │── routes/
│   │   │── __init__.py
│   │   │── chat.py
│   │   │── scraper.py
│   │   │── urls.py
│   │── services/
│   │   │── scraper_service.py
│   │   │── retrieval.py
│   │   │── llm_service.py
│   │   ├── web_scraper.py
│   │── models/
│   │   │── url_model.py
│   │   │── chat_model.py
│   │── db/
│   │   │── vector_store.py
│   │   ├── database.py
│── data/
│   │── scraped_data.json
│── requirements.txt
│── README.md
│── run.py
│── .env
```






## Installation
```sh
# Clone the repository
git clone https://github.com/xloanx/gamma-advisor-backend.git
cd gamma-advisor-backend

#Virtual Environment (Optional)
#Linux
python -m venv <env_name>        #create virtual environment
source <env_name>/bin/activate   #Activate the Virtual Environment

#Windows
python -m venv <env_name>        #create virtual environment
venv\Scripts\activate           #Activate the Virtual Environment


# Install dependencies
pip install -r requirements.txt
```

# Database Installation
Install MongoDB Database      #for URL and Scraped content Storage

## Environmental Variables

MONGO_URI=              #set as appropriate
DB_NAME=
GROQ_API_KEY=

## Usage
```sh

# test web scraping
python -m app.tests.test_scraper        #test to ensure URLs can be scraped

#Run Server
uvicorn app.main:app --reload

# Add preferred URLs
http://127.0.0.1:8000/api/urls/add?url=<Preferred_Financial_News_URL>
or via the: 
Frontend Manage Button on Dashboard

```


## Contributors
- **Abiodun Muhammad-Ahmad Odukaye** - Developer & AI Engineer

## License
This project is licensed under the MIT License.
