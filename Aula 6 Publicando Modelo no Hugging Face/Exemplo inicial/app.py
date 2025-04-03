from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Carregar o tokenizador e o modelo pré-treinado
tokenizer = AutoTokenizer.from_pretrained("tadrianonet/distilbert-text-classification")
model = AutoModelForSequenceClassification.from_pretrained("tadrianonet/distilbert-text-classification")

# Função de previsão
def predict(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_label = torch.argmax(probabilities, dim=1).item()
    return predicted_label, probabilities

# Testar vários textos positivos e neutros para verificar a resposta do modelo
texts_to_test = [
    "I'm, extremyly sad with the results of the last project. I don't know what to do now.",
    "Last nigth's party was amazing! I had so much fun with my friends.",
    "The food was great and the service was excellent!",
    "Today was the best day ever! I can't believe how much fun I had.",
    "The meeting was so boring and unproductive. I felt like I was wasting my time.",
]

# Definição das classes
classes = ["Negative/Neutral", "Positive"]

# Realizar previsões para cada texto
for text in texts_to_test:
    predicted_label, probabilities = predict(text)
    print(f"Text: {text}")
    print(f"Predicted: {predicted_label} ({classes[predicted_label]})")
    print(f"Probabilities: {probabilities}\n")
