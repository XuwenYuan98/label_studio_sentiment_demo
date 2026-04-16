import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
texts = []
labels = []
with open("project-1-at-2026-04-14-06-22-5024f2cc.json") as f:
    data = json.load(f)
for item in data:
    text = item["data"]["text"]
    label = item["annotations"][0]["result"][0]["value"]["choices"][0]
    texts.append(text)
    labels.append(label)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
model = LogisticRegression()
model.fit(X, labels)
print("模型训练完成")
test = ["这个产品很好"]
X_test = vectorizer.transform(test)
prediction = model.predict(X_test)
print("预测结果:", prediction)
