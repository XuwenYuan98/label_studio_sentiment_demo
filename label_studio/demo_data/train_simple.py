import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
texts = []
labels = []
with open("training_data.json") as f:
    data = json.load(f)
for item in data:
    texts.append(item["text"])
    labels.append(item["label"])
X_train, X_test, y_train, y_test = train_test_split(
texts, labels, test_size=0.2, random_state=42
)
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
model = LogisticRegression()
model.fit(X_train_vec, y_train)
pred = model.predict(X_test_vec)
print("验证集准确率:", accuracy_score(y_test, pred))

feature_names = vectorizer.get_feature_names_out()
coefs = model.coef_[0]
top_positive = sorted(zip(coefs, feature_names))[-10:]
top_negative = sorted(zip(coefs, feature_names))[:10]
print("最正面的词:")
for c,w in top_positive:
    print(w,c)
print("\n最负面的词:")
for c,w in top_negative:
    print(w,c)