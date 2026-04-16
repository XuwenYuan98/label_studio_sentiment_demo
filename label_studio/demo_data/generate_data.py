import random
import json

positive = [
"这个产品很好",
"服务非常棒",
"我很喜欢这个功能",
"体验非常不错",
"质量很好",
"速度很快",
"界面很漂亮",
"客服很专业",
"使用起来很顺手",
"真的很满意"
]

negative = [
"这个产品很糟糕",
"服务太差了",
"我很讨厌这个功能",
"体验非常不好",
"质量很差",
"速度太慢",
"界面很难看",
"客服很敷衍",
"使用起来很麻烦",
"真的很失望"
]

data = []

for i in range(200):

    if random.random() > 0.5:
        text = random.choice(positive)
        label = "Positive"
    else:
        text = random.choice(negative)
        label = "Negative"

    data.append({
        "text": text,
        "label": label
    })

with open("training_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("生成完成，共", len(data), "条数据")
