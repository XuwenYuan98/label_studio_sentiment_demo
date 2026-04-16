---
name: corpus-checker
description: 审查语料文件（Excel）的内容安全性，支持方言验证。输入文件路径即可触发。
---

# 语料安全审查 Skill

## 触发方式
用户输入示例：
- `检查 ./data/corpus.xlsx`
- `检查 ./data/粤语语料.xlsx`（自动触发方言检查）
- `检查 ./data/corpus.xlsx 方言=闽南语`（手动指定方言检查）

---

## 执行步骤

### Step 1：读取文件
生成并执行以下 Python 脚本读取 Excel 文件：

```python
import pandas as pd
import json
import os
from datetime import datetime

file_path = "<用户输入的路径>"
xl = pd.ExcelFile(file_path)

corpus = {}
for sheet in xl.sheet_names:
    df = xl.parse(sheet)
    corpus[sheet] = df.to_dict(orient='records')

print(json.dumps(corpus, ensure_ascii=False))
```

### Step 2：识别文本列
对每个 sheet，自动判断哪些列包含自然语言文本内容：
- 优先识别：列名包含 `text`、`content`、`input`、`output`、`语料`、`内容`、`问`、`答` 等关键词
- 兜底策略：取第一列，逐行判断是否为自然语言（非数字、非编码、非空）
- 忽略列：ID 列、时间戳列、纯数字列、URL 列
- **排除内容**：如果文本内容中包含括号（全角 `（）` / 半角 `()`）或斜杠 `/` 的条目（这类通常是注释、备选说法或非正式语料）
  - **豁免列**：`普通话` 列包含上述特殊符号时**不过滤**（该列为标准普通话对照，允许注释性内容）

### Step 3：安全审查
对识别出的每一条文本，逐条审查以下内容：

#### 审查维度与处置策略

##### P0 - 必须删除（高风险）

| 类别 | 关键词示例 | 说明 |
|------|-----------|------|
| **政治敏感** | 文革、文化大革命、红卫兵、造反派、走资派、牛鬼蛇神、黑五类、四类分子、反动派、反革命、批斗、游街、上山下乡、贫下中农、阶级斗争 | 特定历史时期的敏感表述，**零容忍** |
| **仇恨/歧视-身体** | 瞎子、聋子、哑巴、瘸子、跛子、瘫子、傻子、疯子、秃子、麻子、豁子、罗锅、驼子、矮冬瓜、瘦猴、憨子、信球、大低脑 | 针对身体缺陷的**蔑称**（注意区分正常用法） |
| **仇恨/歧视-身份** | 乡巴佬、土包子、北侉子、南蛮子、戏子、下九流、杂种、野种、拖油瓶、丧门星、绝户、断子绝孙、窑子婆儿、妓女、贱人、贱货、婊子、娼妇、淫妇、骚货、混蛋、王八、王八蛋、龟儿子、龟孙子、狗东西、猪狗、畜生、禽兽、败类、人渣、垃圾、白痴、笨蛋、蠢货、蠢猪、呆子 | 针对身份/地域的蔑称 |
| **仇恨/歧视-性别** | 二椅子、二姨子、二尾子、二倚子、娘娘腔、男人婆、变态、人妖、不男不女、阴阳人、妇道人家、赔钱货、丫头片子、克夫、克妻 | 针对性别的歧视性称呼 |
| **暴力/违法** | 毒药、炸弹、自杀、自残、强奸、猥亵、杀人、爆炸、炸药、毒品、制毒、贩毒、枪支、枪械、武器 | 违法或极端暴力内容 |
| **敏感语境** | 寡妇+占便宜 | 涉及性暗示或不当行为的组合 |

##### P1 - 标记但保留（中风险）

| 类别 | 关键词示例 | 说明 |
|------|-----------|------|
| **非方言内容** | 护肤品、化妆品、面膜、防晒、保湿、品牌、slogan、攻略、测评、推荐 | 现代消费话题，非方言研究范畴 |

#### 关键审查原则

##### 1. 区分歧视性称呼与正常用法

| 类型 | 示例 | 处置 |
|------|------|------|
| ❌ 歧视性称呼 | "他是个瘸子"、"那瞎子" | **删除** |
| ✅ 正常描述 | "腿瘸了"、"眼睛瞎了" | 保留 |
| ✅ 成语/俗语 | "吃哑巴亏"、"装疯卖傻" | 保留 |
| ✅ 方言表达 | "想疯咧"（非常想念）、"不疯不闹"（安静） | 保留 |
| ✅ 歇后语 | "瞎子点灯——白费蜡"、"秃子枕门槛——名声在外" | 保留 |

##### 2. 排除正常方言词汇（不应标记为风险）

- **动物描述**："大肥猪"（卖猪场景）
- **形容词使用**："疯张倒势"（形容兴奋）、"傻乎乎"（呆萌）
- **动词使用**："秃噜"（滑落）
- **身体部位**："驼背"（生理特征描述）
- **成语/俗语**："吃哑巴亏"、"装聋作哑"

##### 3. 政治敏感零容忍
- 涉及特定历史时期的敏感表述**必须删除**
- **不区分语境**，一律删除

#### 前置过滤规则（必须执行）

**在安全审查之前，先排除不符合规范的文本：**

| 类型 | 示例 | 处置 |
|------|------|------|
| 包含括号 | "你好（问候语）"、"吃饭（口语）" | **标记并排除**（普通话列除外） |
| 包含斜杠 | "去/走"、"快/迅速" | **标记并排除**（普通话列除外） |

**原因：** 这类内容通常是注释、备选说法、多选项或混合语料，非纯净方言表达。

**例外说明**：`普通话` 列作为标准普通话对照文本，允许包含括号注释（如词性标注）和斜杠（如多音字标注），该列内容不做前置过滤和重复检查。

#### 豁免判断原则（LLM 自主判断）

以下情形即使触发关键词也不应删除：

**1. 学术/科普性描述**
- 明显的知识介绍（如"一氧化碳是有毒气体，吸入会导致..."）
- 医疗健康领域的专业表述（如病症描述、药物副作用说明）
- 新闻事实性陈述（如"XX 事件造成 XX 人伤亡"）

**2. 文学/方言表达**
- 歇后语："瞎子点灯——白费蜡"、"秃子枕门槛——名声在外"
- 成语/俗语："吃哑巴亏"、"装疯卖傻"、"装聋作哑"
- 方言形容词："疯张倒势"（形容兴奋）、"傻乎乎"（呆萌）、"秃噜"（滑落）
- 文学作品中的情节描写，无实际操作指导性质

**3. 客观描述**
- 身体特征客观描述："腿瘸了"、"眼睛瞎了"、"驼背"（体态）
- 描述地域文化差异的客观陈述（如"XX 地区的人普遍有 XX 饮食习惯"属于文化描述，非歧视）
- 当事人自述身份的表达（如"我是 XX 人，我们那边..."不构成地域歧视）
- 动物/物品描述："大肥猪"（卖猪场景）

**4. 方言研究记录**
- 《方言志》等学术文献中的词汇记录
- 方言歇后语、谚语、俗语的完整记录
- 无实际操作指导性质的方言表达

**判断原则：看意图和实际危害性，而非仅匹配关键词。**

#### 可选项（方言验证）
触发条件：文件名/所在目录名包含方言关键词，或用户调用时指定 `方言=XX`

支持识别的方言关键词（文件名匹配）：
- 粤语/广东话/广府话/Cantonese
- 闽南语/台语/闽语/Hokkien
- 吴语/上海话/苏州话/Wu
- 客家话/客语/Hakka
- 普通话以外的其他地区方言：晋语/湘语/赣语/徽语/平话/官话

验证内容：
- 该文件/sheet 的语料是否符合对应方言的语言特征
- 是否混入了大量非该方言的内容
- 标记混入比例，不删除，仅在报告中注明

### Step 3.5：前置过滤（括号和斜杠检查）
在安全审查之前，先过滤掉包含括号或斜杠的内容：

```python
def should_filter_out(text):
    """检查文本是否应被过滤（包含括号或斜杠）"""
    if not text or pd.isna(text):
        return False
    
    text_str = str(text)
    
    # 检查是否包含括号（全角/半角）或斜杠
    filter_chars = ['(', ')', '（', '）', '/']
    if any(char in text_str for char in filter_chars):
        return True
    
    return False

# 在审查循环中使用
for idx, record in enumerate(records):
    # 先检查是否需要前置过滤
    is_filtered = False
    for col in text_cols:
        if col in record and should_filter_out(record[col]):
            is_filtered = True
            deleted_records.append({
                'sheet': sheet_name,
                'row': idx + 2,
                'content': str(record[col]),
                'reason': '包含括号/斜杠（非纯净语料）',
                'action': 'filtered'
            })
            break
    
    if is_filtered:
        continue  # 跳过此条目的后续审查
    
    # ... 继续进行正常的安全审查
```

# 对删除记录去重（同一个 text 只写一行，sheet/rows 记录为列表）
merged_records = defaultdict(lambda: {'sheets': [], 'rows': [], 'reason': '', 'action': ''})

for r in deleted_records:
    content = r.get('洛阳话', '') or r.get('content', '')
    sheet = r.get('sheet', '')
    row = r.get('row', 0)
    
    merged_records[content]['sheets'].append(sheet)
    merged_records[content]['rows'].append(row)
    merged_records[content]['reason'] = r.get('reason', '')
    merged_records[content]['action'] = r.get('action', 'deleted')

# 转换回列表格式
deleted_records = []
for content, data in merged_records.items():
    deleted_records.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sheet': data['sheets'],  # 列表格式
        'rows': data['rows'],     # 列表格式
        'content': content,
        'reason': data['reason'],
        'action': data['action']
    })

base_name = os.path.splitext(file_path)[0]
result_path = f"{base_name}_人工核查.xlsx"

with pd.ExcelWriter(result_path, engine='openpyxl') as writer:
    for sheet_name, records in cleaned_corpus.items():
        df = pd.DataFrame(records)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"结果已写入：{result_path}")
```

### Step 5：检查重复内容
在写入日志前，先检查各 Sheet 中是否存在重复内容：

```python
import pandas as pd

duplicate_warnings = []

for sheet_name in xl.sheet_names:
    df = xl.parse(sheet_name)
    
    # 识别文本列（优先检查洛阳话、普通话、text、content 等列）
    text_cols = [col for col in df.columns if any(keyword in str(col).lower() 
                 for keyword in ['洛阳话', '普通话', 'text', 'content', '语料', '内容', 'input', 'output'])]
    
    if not text_cols:
        text_cols = [df.columns[0]]  # 默认第一列
    
    for col in text_cols:
        if col in df.columns:
            # 统计重复值（排除空值）
            value_counts = df[col].dropna().value_counts()
            duplicates = value_counts[value_counts > 1]
            
            if len(duplicates) > 0:
                total_dup_rows = duplicates.sum() - len(duplicates)  # 重复的行数（排除首次出现）
                duplicate_warnings.append({
                    'sheet': sheet_name,
                    'column': col,
                    'duplicate_count': len(duplicates),  # 有多少种不同的内容重复了
                    'duplicate_rows': int(total_dup_rows)  # 涉及多少行重复
                })

# 输出重复警告
if duplicate_warnings:
    print("⚠️  重复内容风险提示：")
    for warn in duplicate_warnings:
        print(f"   Sheet [{warn['sheet']}] 列 [{warn['column']}] 有 {warn['duplicate_count']} 种内容重复，共涉及 {warn['duplicate_rows']} 行，需要去重")
    print()
```

### Step 6：写入日志
在原文件同级目录生成日志文件 `{base_name}_corpus_check_log.jsonl`（追加写入，不覆盖历史）：

**去重规则**：同一个 text 内容只写一行（即使出现在多个 sheet 或多个位置），`sheet` 字段可记录为列表格式。

每次删除操作写入一条记录，格式如下：

```jsonl
{"timestamp": "2026-03-09 10:00:00", "sheet": ["词汇", "短句"], "rows": [1453, 2939], "content": "妇道人家", "reason": "歧视性称呼-性别", "action": "deleted"}
{"timestamp": "2026-03-09 10:00:01", "sheet": ["多音节词"], "rows": [101, 174], "content": "信球", "reason": "身体歧视", "action": "deleted"}
```

字段说明：
- `timestamp`: 操作时间
- `sheet`: 所在Sheet名称列表（同一内容出现在多个sheet时）
- `rows`: 行号列表（与sheet一一对应，从0开始）
- `content`: 被删除的内容
- `reason`: 删除原因分类
- `action`: 操作类型（deleted/marked）

> **注意**：如果 Step 5 检测到重复内容，会在日志文件最上方添加重复风险提示（以 `#` 开头的注释行）

### Step 7：生成人工核查日志（Excel 格式）
将 JSONL 日志转换为 Excel 格式，便于人工核查：

```python
import pandas as pd
import json
import os

base_name = os.path.splitext(file_path)[0]
log_jsonl_path = f"{base_name}_corpus_check_log.jsonl"
log_excel_path = f"{base_name}_corpus_check_log.xlsx"

records = []
with open(log_jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):  # 跳过注释行（重复风险提示）
            try:
                record = json.loads(line)
                # 处理 sheet/rows 可能是列表的情况
                sheets = record.get('sheet', [])
                rows = record.get('rows', [])
                content = record.get('content', '') or record.get('洛阳话', '')
                
                # 如果 sheet 是列表，展开为多行；否则保持单行
                if isinstance(sheets, list) and isinstance(rows, list):
                    for i, (sheet, row) in enumerate(zip(sheets, rows)):
                        row_data = {
                            'sheet': sheet,
                            'row': row,
                            'content': content if i == 0 else '',  # 只在第一行显示内容
                            'reason': record.get('reason', '') if i == 0 else '',
                            'action': record.get('action', '') if i == 0 else ''
                        }
                        records.append(row_data)
                else:
                    # 兼容旧格式（单条记录）
                    row_data = {
                        'sheet': sheets,
                        'row': rows[0] if isinstance(rows, list) else rows,
                        'content': content,
                        'reason': record.get('reason', ''),
                        'action': record.get('action', '')
                    }
                    records.append(row_data)
            except json.JSONDecodeError:
                continue

# 保存为 Excel
df = pd.DataFrame(records)
df.to_excel(log_excel_path, index=False, engine='openpyxl')
print(f"日志 Excel 已生成：{log_excel_path}")
```

### Step 8：输出审查摘要
向用户输出以下内容（终端/对话框）：

```
✅ 审查完成：corpus.xlsx
─────────────────────────────
📄 处理 Sheet 数：3
📝 总语料条数：120
🗑️  删除条数：5
🗣️  方言不符条数：2（已记录，未删除）
📁 结果文件：./data/corpus_人工核查.xlsx
📋 JSONL 日志：./data/corpus_corpus_check_log.jsonl
📊 Excel 日志：./data/corpus_corpus_check_log.xlsx
─────────────────────────────
删除原因摘要：
- [Sheet1, 行12] 包含自杀方法描述
- [Sheet2, 行45] 涉及真实个人隐私信息
- [Sheet2, 行67] 针对特定群体的人身攻击
- [Sheet3, 行89] 地域歧视性表述
...
```

---

## 注意事项
- 所有脚本由 Cursor 生成后在用户本地执行，不上传原始语料内容到任何外部服务
- 日志中记录被删内容仅用于供应方争议留存，请妥善保管
- 方言检查结果仅供参考，不自动删除，需人工确认
- 如 Excel 文件过大，分 sheet 逐批处理，避免内存溢出

## 审查 Checklist

- [ ] 政治敏感内容已删除（零容忍）
- [ ] 歧视性称呼已删除（身体/身份/性别歧视）
- [ ] 暴力违法内容已删除
- [ ] 歇后语/成语/俗语未被误删
- [ ] 客观描述（如"腿瘸了"）未被误删
- [ ] 正常方言用法（如"疯张倒势"）未被误删
- [ ] 重复内容已检查并提示
- [ ] 删除内容已去重（避免同一内容多次记录）
- [ ] 操作日志已生成（JSONL格式）
- [ ] 操作日志已转换为 Excel 格式
- [ ] 清洗后文件已保存
```

---

## 使用方式

在 Cursor 对话框中直接输入：

```
@corpus-checker 检查 ./data/corpus.xlsx
@corpus-checker 检查 ./data/粤语对话.xlsx
@corpus-checker 检查 ./data/corpus.xlsx 方言=闽南语
```

---

## 依赖安装（首次使用前执行）

```bash
pip install pandas openpyxl
```