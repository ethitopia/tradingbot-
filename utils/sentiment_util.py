from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch 
from typing import Tuple 

device = "cuda:0" if torch.cuda.isavailable() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to('device')
labels = ['positive', 'negative', 'neutral']


