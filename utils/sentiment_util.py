from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch 
from typing import Tuple 

device = "cuda:0" if torch.cuda.isavailable() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to('device')
labels = ['positive', 'negative', 'neutral']

def estimate_sentiment(news): 
    if news:
       tokens = tokenizer(news, return_tensors="pt", padding=True, truncation=True).to(device)
       
       with torch.no_grad(): 
          outputs = model(**tokens)
      
       probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
       
       predicted_index = torch.argmax(probabilities, dim=-1).item() 
       
       return labels(predicted_index)
       
