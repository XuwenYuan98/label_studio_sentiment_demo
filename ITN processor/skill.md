---
name: itn-processor
description: 处理CSV文件中的中文语音转写文本
version: 2.0
last_updated: 2026-04-14
---

# ITN处理器

## 任务概述
对`data/`目录中的所有CSV文件进行批量处理，为每条记录生成唯一标识符（UID）并进行ITN转写。

## 核心流程

### 1. 读取CSV文件
- 扫描`data/`目录下所有`.csv`文件
- 每个文件包含列：`index`、`transcription`、`translation`、`gloss`
- 编码格式：UTF-8 with BOM

### 2. 生成带UID的中间文件
**目标**：为所有数据生层UID，并与检查需要ITN转写的行
 