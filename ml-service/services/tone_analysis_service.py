import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast
import os

labels = dict({
    0: "NEUTRAL",
    1: "POSITIVE",
    2: "NEGATIVE"
})

models_dir = "ml_models/models/"
tokenizers_dir = "ml_models/tokenizers/"

model_name = "model"
tokenizer_name = "tokenizer"

if os.path.isdir(models_dir + model_name):
    model = AutoModelForSequenceClassification.from_pretrained(models_dir + model_name)
else:
    print("FATAL: no model dir detected. dir name=" + models_dir + model_name)
    exit(1)

if os.path.isdir(tokenizers_dir + tokenizer_name):
    tokenizer = BertTokenizerFast.from_pretrained(tokenizers_dir + tokenizer_name)
else:
    print("FATAL: no tokenizer dir detected. dir name=" + tokenizers_dir + tokenizer_name)
    exit(1)


class ModelWrapper(object):
    def __init__(self, model, tokenizer, labels):
        self.model = model
        self.tokenizer = tokenizer
        self.labels = labels

    @torch.no_grad()
    def predict_probs(self, text):
        inputs = self.tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**inputs)
        predicted = torch.nn.functional.softmax(outputs.logits, dim=1)

        predicted_label = torch.argmax(predicted, dim=1).numpy()[0]
        predicted_label_text = labels[predicted_label]

        probs_dict = dict(zip(list(self.labels.values()), predicted.numpy().flatten()))

        return predicted_label_text, probs_dict


ml_service = ModelWrapper(model, tokenizer, labels)
