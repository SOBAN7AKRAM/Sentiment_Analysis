# Sentiment Analysis API

This project is a **Sentiment Analysis API** built using **Django** and integrated with a machine learning model trained on a large dataset of text. The API takes input text and platform information, processes it using a pre-trained **Random Forest Classifier**, and returns the predicted sentiment.

## Features

- **Preprocessing Pipeline**: Cleans text by removing special characters, numbers, URLs, mentions, and stop words, and applies stemming and lemmatization.
- **Platform Context**: Combines the `platform` and `text` to add contextual information to the sentiment analysis.
- **Machine Learning**: Uses a pre-trained **Random Forest Classifier** and **TF-IDF Vectorizer** to make predictions.
- **API-Driven**: Implements a API endpoint for prediction.

## Project Structure

```plaintext
project/
├── api/
│   ├── ML_Model/
│   │   ├── runner.ipynb     # Trained Random Forest model
│   ├── views.py                     # Django views and API
│   ├── urls.py                      # Django URL routing
├── ml_model.py                      # Python script for training and testing
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
```

## How to start project

- Firstly, run the **runner.py** file in ML_Model to generate **sentiment_model.pkl** and **vectorizer.pkl** file

- Run 

  ```python
  pip install -r requirements.txt
  ```

​	to install the dependencies

- Run 

  ```python
  python manage.py runserver
  ```

  to launch the project