import json
import numpy as np
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

texts = []
labels = []
with open("training_data.json", encoding="utf-8") as f:
    data = json.load(f)
for item in data:
    texts.append(item["text"])
    labels.append(item["label"])

# 简单分词（按字切）
    # sentences = [[c for c in text] for text in texts]
# 加中文分词
import jieba
sentences = [list(jieba.cut(text)) for text in texts]

# 训练 Word2Vec
w2v_model = Word2Vec(sentences, vector_size=50, window=3, min_count=1)


# 把句子变成向量（取平均）
def sentence_vector(sentence):
    vecs = []
    for char in sentence:
        vecs.append(w2v_model.wv[char])
    print('###############')
    for x in vecs:
        print(x.shape)
    print('!!!!!!!!!!!!!!!')
    return np.concatenate(vecs, axis=0)

X = np.array([sentence_vector(s) for s in sentences])
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42
)
model = LogisticRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("验证集准确率:", accuracy_score(y_test, pred))

print("\n词语相似度测试")
print("很好 vs 不错:", w2v_model.wv.similarity("好", "棒"))
print("差 vs 糟:", w2v_model.wv.similarity("差", "糟"))
print("喜欢 vs 满意:", w2v_model.wv.similarity("喜", "满"))

print("\n词表:")
print(list(w2v_model.wv.index_to_key)[:20])
