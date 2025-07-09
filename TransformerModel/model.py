import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import torch.utils
import torch.utils.data
from transformers import AutoTokenizer 
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch


class BookDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, index):
        item = {k: torch.tensor(v[index]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[index])
        return item
    
    def __len__(self):
        return len(self.labels)

file_path = file_path = (
    r"D:\Downloads\d2l-en\text tech\TextTech_project\books_with_prediction_confidence_score.csv"
)

df = pd.read_csv(file_path)

# Remove rows with missing descriptions
df = df.dropna(subset=["Description", "Genre"])
print(df["Genre"].value_counts())
# Convert descriptions to string type
df["Description"] = df["Description"].astype(str)

labelEncoder = LabelEncoder()
df["Genre_Encoded"] = labelEncoder.fit_transform(df["Genre"])

train_texts, val_texts, train_labels, val_labels = train_test_split(
    df["Description"].tolist(),
    df["Genre_Encoded"].tolist(),
    test_size=0.2,
    random_state=42,
)



model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

train_encodings = tokenizer(train_texts, truncation = True, padding = True, max_length = 256)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=256)

model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels = len(labelEncoder.classes_))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


train_dataset = BookDataset(train_encodings, train_labels)
val_dataset = BookDataset(val_encodings, val_labels)

training_args = TrainingArguments(
    output_dir = "./results",
    eval_strategy = "epoch",
    per_device_train_batch_size = 16,
    per_device_eval_batch_size = 16,
    num_train_epochs = 6,
    weight_decay = 0.01,
    logging_dir = "./logs",
    logging_steps = 10,
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = torch.argmax(torch.tensor(logits), dim=1)
    return {"accuracy": accuracy_score(labels, preds)}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()

model.save_pretrained("fine_tuned_genre_model")
tokenizer.save_pretrained("fine_tuned_genre_model")


trainer.evaluate()

def predict_genre(description):
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}  # Move inputs to same device
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    return labelEncoder.inverse_transform([predicted_class])[0]


print(predict_genre("An epic fantasy adventure through magical realms"))
print(predict_genre("A romantic drama set in post-war France"))
