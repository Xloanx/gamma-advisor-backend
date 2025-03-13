'''
Accepts a user query and retrieved documents.
Send them to OpenAI’s GPT model or Groq's LLM API to generate a response.
Return the AI-generated response.
'''

import openai
import groq
from app.config import OPENAI_API_KEY, GROQ_API_KEY
from app.services.query_preprocessor import preprocess_query
from app.db.vector_store import search_faiss
import json

openai.api_key = OPENAI_API_KEY
client = groq.Client(api_key=GROQ_API_KEY)

dummy_doc=[
    # {"content":"Financial News is a weekly financial newspaper published in London and news website, founded in 1996. It is published by eFinancial News Limited, and provides news and opinions regarding the financial services sector, and information about its people."},
    # {"content":"Financial News is owned by Dow Jones & Company, which acquired eFinancial News in 2007. It is part of the Barron's Group division, which also includes Barron's, Factiva, MarketWatch and Mansion Global."},
    # {"content":"Financial News launched a revamped, mobile-first website and new weekly print edition in January 2017"},
    # {"content": "NVIDIA's stock has risen by 5% in the past week due to strong earnings."},
    # {"content": "Tesla's latest market report shows a 3% increase in stock value."},
    # {"content": "Alphabet (Google) is investing in AI-driven search models."}
    
]



def generate_response(query: str, dummy_docs: list = dummy_doc, llm: str = "groq"):
    """
    Uses OpenAI's GPT-4 and Groq API to generate a response based on retrieved documents.
    Falls back to AI’s general knowledge if no relevant documents are found.

    Args:
        query (str): User's input query.
        retrieved_docs (list): List of relevant document contents.
        llm (str): The LLM model of choice.

    Returns:
        str: AI-generated response.
    """

    # Preprocess the user query
    cleaned_query = preprocess_query(query)


    # Initialize retrieved_docs
    retrieved_docs = None 

    # Retrieve documents if none are provided
    if not dummy_docs:
        retrieved_docs = search_faiss(cleaned_query)

    # Ensure retrieved_docs is at least an empty list to prevent UnboundLocalError
    retrieved_docs = retrieved_docs or []

    # Check if any relevant documents were retrieved
    if retrieved_docs or dummy_docs:
        context_docs = retrieved_docs if retrieved_docs else dummy_docs
        context = "\n".join([doc["content"] for doc in context_docs])
        prompt = f"""
        You are a knowledgeable AI assistant specializing in financial stock analysis, particularly NVDA, TSLA, and GOOG. 
        You provide well-structured, accurate, and insightful responses while prioritizing information derived from the provided context.

        Context:
        {context}

        Question: {query}

        If the context contains relevant information, base your response strictly on it. 
        If the context does not provide an answer, use general financial knowledge while ensuring accuracy and avoiding speculation. 
        If the question is unrelated to finance, engage in a meaningful and informed conversation, keeping responses relevant and fact-based.
        """

    else:
        print("⚠️ No relevant documents found. Using AI's general knowledge.")
        prompt = f"""
        You are a knowledgeable AI assistant with extensive general knowledge.
        
        Question: {query}
        
        Provide a clear and accurate answer based on your training data and engage in a meaningful and informed conversation, keeping responses relevant and fact-based.
        """

    # Generate response using the selected LLM
    if llm == "groq":
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7
        )
    else:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7
        )

    # Convert response to dictionary if needed and extract the content
    try:
        response_dict = response.dict() if hasattr(response, "dict") else json.loads(response.json())
        return response_dict["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error extracting AI response: {e}")
        return "Sorry, I couldn't process your request."



