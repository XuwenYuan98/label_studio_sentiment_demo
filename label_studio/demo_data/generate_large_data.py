import random
import json

subjects = ["这个产品","这个服务","这个软件","这个应用","这个系统"]

positive = ["很好","非常不错","让我很满意","体验很好","质量很好","真的很棒","非常喜欢","挺不错"]
negative = ["很糟糕","非常差","让我很失望","体验很差","质量很差","真的很垃圾","非常讨厌","很不好用"]

extras = ["","，我会推荐给朋友","，值得购买","，以后还会继续用","，感觉很专业","，不太推荐","，以后不会再用了","，体验太差了"]

data = []

for i in range(5000):
    subject = random.choice(subjects)

    if random.random() > 0.5:
        adj = random.choice(positive)
        label = "Positive"
    else:
        adj = random.choice(negative)
        label = "Negative"

    extra = random.choice(extras)

    text = subject + adj + extra

    item = {"text": text, "label": label}
    data.append(item)

print("内存中数据条数:", len(data))

with open("training_data_large.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("写入文件完成:", len(data))
