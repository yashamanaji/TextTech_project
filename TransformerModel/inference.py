import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import joblib  # if saving/loading LabelEncoder

# Load tokenizer and model
model_path = "fine_tuned_genre_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Move model to device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load or recreate label encoder

# labelEncoder = joblib.load("label_encoder.pkl")


labelEncoder = LabelEncoder()
labelEncoder.classes_ = [
    "Adventure",
    "Biography",
    "Children",
    "Default",
    "Fantasy",
    "Historical Fiction",
    "Horror",
    "Mystery",
    "Non-Fiction",
    "Romance",
    "Science Fiction",
    "Thriller",
]  


# Inference function
def predict_genre(description):
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    return labelEncoder.inverse_transform([predicted_class])[0]


# Example usage
print(predict_genre("An epic fantasy adventure through magical realms"))
print(predict_genre("A romantic drama set in post-war France"))
