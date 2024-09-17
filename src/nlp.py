from transformers import pipeline
from keybert import KeyBERT
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy
from .utils import calculate_sentence_similarity

# Ensure the necessary resources are downloaded once
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Initialize stopwords and stemmer globally for efficiency
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Initialize T5 summarization pipeline
summarizer = pipeline("summarization", model="t5-small")
# Initialize KeyBERT model
kw_model = KeyBERT()

# Load the Spacy model
nlp = spacy.load('en_core_web_sm')

def filter_content(content, keywords):
    # Process the content using Spacy
    doc = nlp(content)
    sentences = [sent.text for sent in doc.sents]
    # Extract keywords
    extracted_sentences = []
    for sentence in sentences:
        # Check if any of the keywords are similar to the words in the sentence
        max_similarity = 0
        for keyword in keywords:
            max_similarity = max(max_similarity, calculate_sentence_similarity(keyword, sentence))
            
        if max_similarity > 0.8:
            extracted_sentences.append(sentence)

    return extracted_sentences


