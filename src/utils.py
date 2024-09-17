import re
import json
import time
import requests
import torch
from transformers import AutoModel, AutoTokenizer

# Load the pre-trained model and tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def resilient_request(url, retries=3):
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException:
            time.sleep(1)
    return None

def save_to_json(data, filename='output.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def is_relevant(link_text, keywords):
    # Score relevance based on keyword presence
    score = sum(keyword.lower() in link_text.lower() for keyword in keywords)
    return score > 0  # Adjust threshold as needed

def calculate_sentence_similarity(sentence1, sentence2):
    # Tokenize the input sentences
    inputs1 = tokenizer(sentence1, return_tensors="pt")
    inputs2 = tokenizer(sentence2, return_tensors="pt")

    # Get the sentence embeddings
    embeddings1 = model(**inputs1).last_hidden_state[:, 0, :]
    embeddings2 = model(**inputs2).last_hidden_state[:, 0, :]

    # Compute the similarity between the sentence embeddings
    similarity = torch.cosine_similarity(embeddings1, embeddings2)

    return similarity.item()

def clean_text(text):
    # Remove excessive whitespace and newlines
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove any non-printable characters, escape sequences, or control codes
    cleaned_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned_text)
    
    return cleaned_text