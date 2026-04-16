import json
from datasets import Dataset
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import TrainingArguments, Trainer

# 读取数据
with open("training_data_large.json", encoding="utf-8") as f:
    data = json.load(f)
    texts = [x["text"] for x in data]
    labels = [1 if x["label"]=="Positive" else 0 for x in data]
dataset = Dataset.from_dict({
"text": texts,
"label": labels
})

# 切分训练/验证
dataset = dataset.train_test_split(test_size=0.2)

# tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
def tokenize(example):
    return tokenizer(
example["text"],
padding="max_length",
truncation=True,
max_length=64
)
dataset = dataset.map(tokenize)

# 模型
model = BertForSequenceClassification.from_pretrained(
"bert-base-chinese",
num_labels=2
)

# 训练参数
training_args = TrainingArguments(
output_dir="./results",
# evaluation_strategy="epoch",
per_device_train_batch_size=8,
per_device_eval_batch_size=8,
num_train_epochs=2,
)
Trainer

trainer = Trainer(
model=model,
args=training_args,
train_dataset=dataset["train"],
eval_dataset=dataset["test"],
)

# 训练
trainer.train()

# 评估
trainer.evaluate()