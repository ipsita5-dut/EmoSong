# train_data.py
from datasets import load_dataset

# Load the Synthetic Persona-Chat dataset
dataset = load_dataset("google/Synthetic-Persona-Chat")

# Inspect the dataset structure
print(dataset)