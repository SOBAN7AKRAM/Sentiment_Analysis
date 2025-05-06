# import joblib
import re
import nltk
import os
import emoji
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Ensure required NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLP tools
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Path to model and vectorizer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'ML_Model', 'sentiment_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'ML_Model', 'vectorizer.pkl')

# Load model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
else:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# Load pre-trained vectorizer
if os.path.exists(VECTORIZER_PATH):
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Vectorizer loaded successfully.")
else:
    raise FileNotFoundError(f"Vectorizer file not found at {VECTORIZER_PATH}")

# Text cleaning function
def clean_text(text):
    if isinstance(text, str):  # Check if the input is a string
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions (@username)
        text = re.sub(r'@\w+', '', text)
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        # Remove special characters (optional, if not already done)
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    else:
        return ""  # Return an empty string for non-string inputs

# Preprocessing function
def preprocess_text(text, platform):
    if not text:
        return ""
    
    # Clean text
    text = clean_text(text)
    text = text.lower()
    # Remove stop words
    text = ' '.join([word for word in text.split() if word not in stop_words])
    # Apply stemming
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    # Apply lemmatization
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    # Convert emojis to text
    text = emoji.demojize(text)
    # Combine with platform 
    text = platform.lower() + ' ' + text
    return text

# Predict sentiment function
def predict_sentiment(text, platform):
    processed_text = preprocess_text(text, platform)
    if not processed_text:
        return "Error: Input text is empty after preprocessing."

    # Transform using pre-trained vectorizer
    vectorized_text = vectorizer.transform([processed_text])
    
    # Predict using the loaded model
    prediction = model.predict(vectorized_text)
    return prediction[0]
