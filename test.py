import requests
token = "your token here"

headers = {"Authorization": f"Bearer {token}"}

data_sentiment = {"inputs": "I love this product. It's amazing!"}

resp = requests.post(
    "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment",
    headers=headers,
    json=data_sentiment
)
print("Sentiment (nlptown):", resp.status_code, resp.text)