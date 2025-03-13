import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import spacy
nlp = spacy.load("en_core_web_sm")


# Download required NLTK resources (only once)
#nltk.download("punkt")
#nltk.download("stopwords")
#nltk.download("wordnet")

# def preprocess_query(query: str) -> str:
#     """
#     Preprocesses the user query by tokenizing, removing stopwords, and lemmatizing.

#     Args:
#         query (str): The raw user query.

#     Returns:
#         str: The cleaned and processed query.
#     """
#     # Convert to lowercase
#     query = query.lower()

#     # Tokenize words
#     words = word_tokenize(query)

#     # Remove stopwords (e.g., "the", "is", "a")
#     stop_words = set(stopwords.words("english"))
#     filtered_words = [word for word in words if word not in stop_words]

#     # Lemmatize words (convert to base form)
#     lemmatizer = WordNetLemmatizer()
#     processed_words = [lemmatizer.lemmatize(word) for word in filtered_words]

#     # Reconstruct query
#     processed_query = " ".join(processed_words)

#     return processed_query


def preprocess_query(text: str) -> str:
    """Cleans and tokenizes user input using spaCy."""
    doc = nlp(text.lower())  # Convert to lowercase and tokenize
    cleaned_tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(cleaned_tokens)