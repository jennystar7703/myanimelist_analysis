import pandas as pd 
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def text_process(text):
    # Convert the text to lowercase
    text = text.lower()
    # Remove any HTML tags
    text = re.sub('<[^>]*>', '', text)
    # Replace any URLs with the word 'url'
    text = re.sub(r'http\S+', 'url', text)
    # Remove any non-word characters (excluding spaces)
    text = re.sub(r'[^\w\s!]', ' ', text)
    # Remove any numbers
    
    # Remove any stopwords
    STOPWORDS = stopwords.words('english') + ['u', 'ü', 'ur', '4', '2', 'im', 'dont', 'doin', 'ure']
    
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    
    # Remove any extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Now just remove any stopwords
    return text.strip()

comment = "loved it!!!!!!!!!!!!!!!! ..."
cleaned_comment = text_process(comment)
print(cleaned_comment)