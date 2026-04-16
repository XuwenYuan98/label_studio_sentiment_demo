import torch
from transformers import BertTokenizer, BertForSequenceClassification

# 加载模型和tokenizer
model_path = "./results/checkpoint-1000"

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertForSequenceClassification.from_pretrained(model_path)

model.eval()

def predict(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=64
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probs = torch.softmax(logits, dim=1)

    label_id = torch.argmax(probs).item()
    score = probs[0][label_id].item()

    label = "Positive" if label_id == 1 else "Negative"

    return label, score


# 测试几句话
tests = [
    "这个软件真的很好用",
    "这个服务让我非常失望",
    "体验不错，下次还会再来",
    "质量太差了",
    "这个软件还可以",
    "这个产品一般般",
    "客服态度太差了",
    "功能挺多但是很卡",
    "我不太喜欢这个应用",
]

for t in tests:
    label, score = predict(t)
    print(t, "->", label, round(score,3))
