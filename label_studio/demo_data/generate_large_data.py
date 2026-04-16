import random
import json

subjects = [
    "这个产品","这个服务","这个软件","这个应用",
    "这个系统","这个平台","这个功能","这个工具"
]

positive = [
    "很好","非常不错","让我很满意","体验很好",
    "质量很好","真的很棒","非常喜欢","挺不错",
    "很稳定","很流畅","设计很好"
]

negative = [
    "很糟糕","非常差","让我很失望","体验很差",
    "质量很差","真的很垃圾","非常讨厌","很不好用",
    "非常卡顿","问题很多","让人很烦"
]

neutral_pos = [
    "还可以","还不错","一般但能用","还算可以",
    "整体还行"
]

neutral_neg = [
    "一般般","不太好","不是很好","有点差",
    "不太满意"
]

extras = [
    "",
    "，我会推荐给朋友",
    "，值得购买",
    "，以后还会继续用",
    "，感觉很专业",
    "，不太推荐",
    "，以后不会再用了",
    "，体验太差了"
]

data = []

def make_simple():
    subject = random.choice(subjects)

    if random.random() > 0.5:
        adj = random.choice(positive)
        label = "Positive"
    else:
        adj = random.choice(negative)
        label = "Negative"

    text = subject + adj + random.choice(extras)
    return {"text": text, "label": label}

def make_but_sentence():
    subject = random.choice(subjects)

    if random.random() > 0.5:
        text = subject + "虽然" + random.choice(neutral_pos) + "，但是" + random.choice(positive)
        label = "Positive"
    else:
        text = subject + "虽然" + random.choice(neutral_pos) + "，但是" + random.choice(negative)
        label = "Negative"

    return {"text": text, "label": label}

def make_negative_expression():
    subject = random.choice(subjects)

    if random.random() > 0.5:
        text = subject + "不是很好"
        label = "Negative"
    else:
        text = subject + "不太满意"
        label = "Negative"

    return {"text": text, "label": label}

def make_neutral():
    subject = random.choice(subjects)

    if random.random() > 0.5:
        text = subject + random.choice(neutral_pos)
        label = "Positive"
    else:
        text = subject + random.choice(neutral_neg)
        label = "Negative"

    return {"text": text, "label": label}

for i in range(20000):

    r = random.random()

    if r < 0.4:
        item = make_simple()
    elif r < 0.7:
        item = make_but_sentence()
    elif r < 0.85:
        item = make_negative_expression()
    else:
        item = make_neutral()

    data.append(item)

with open("training_data_large.json","w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=2)

print("生成完成:",len(data))


# import random
# import json

# subjects = ["这个产品","这个服务","这个软件","这个应用","这个系统"]

# positive = ["很好","非常不错","让我很满意","体验很好","质量很好","真的很棒","非常喜欢","挺不错"]
# negative = ["很糟糕","非常差","让我很失望","体验很差","质量很差","真的很垃圾","非常讨厌","很不好用"]

# extras = ["","，我会推荐给朋友","，值得购买","，以后还会继续用","，感觉很专业","，不太推荐","，以后不会再用了","，体验太差了"]

# data = []

# for i in range(5000):
#     subject = random.choice(subjects)

#     if random.random() > 0.5:
#         adj = random.choice(positive)
#         label = "Positive"
#     else:
#         adj = random.choice(negative)
#         label = "Negative"

#     extra = random.choice(extras)

#     text = subject + adj + extra

#     item = {"text": text, "label": label}
#     data.append(item)

# print("内存中数据条数:", len(data))

# with open("training_data_large.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=2)

# print("写入文件完成:", len(data))
