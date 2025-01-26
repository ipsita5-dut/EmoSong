# train_model.py
import pandas as pd
from datasets import load_dataset, Dataset
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments

# Load the Synthetic Persona-Chat dataset
dataset = load_dataset("google/Synthetic-Persona-Chat")

# Convert the dataset to DataFrames
train_df = pd.DataFrame(dataset['train'])
val_df = pd.DataFrame(dataset['validation'])

# Prepare the training dataset
train_data = []
for index, row in train_df.iterrows():
    conversation = f"User   1: {row['user 1 personas']} User 2: {row['user 2 personas']} Best Generated Conversation: {row['Best Generated Conversation']}"
    train_data.append({"input_text": conversation, "target_text": row['Best Generated Conversation']})

# Prepare the validation dataset
val_data = []
for index, row in val_df.iterrows():
    conversation = f"User   1: {row['user 1 personas']} User 2: {row['user 2 personas']} Best Generated Conversation: {row['Best Generated Conversation']}"
    val_data.append({"input_text": conversation, "target_text": row['Best Generated Conversation']})

# Create Dataset objects
train_dataset = Dataset.from_pandas(pd.DataFrame(train_data))
val_dataset = Dataset.from_pandas(pd.DataFrame(val_data))

# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.pad_token = tokenizer.eos_token  # Set padding token
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Tokenize the datasets
def tokenize_function(examples):
    return tokenizer(examples['input_text'], padding="max_length", truncation=True)

tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True)
tokenized_val_dataset = val_dataset.map(tokenize_function, batched=True)

# Set training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='epoch',  # Keep this to evaluate at the end of each epoch
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,  # Add this line for evaluation batch size
    num_train_epochs=3,
    weight_decay=0.01,
)

# Create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_val_dataset,  # Pass the validation dataset here
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained('./fine_tuned_model')
tokenizer.save_pretrained('./fine_tuned_model')

print("Model training complete and saved to './fine_tuned_model'")