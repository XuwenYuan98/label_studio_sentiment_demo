# NLP Learning Projects

This repository contains several small projects and experiments related to Natural Language Processing (NLP).  
The goal of this repository is to explore different NLP workflows including data generation, corpus processing, and sentiment analysis.

---

## Repository Structure

```
.
├── corpus_checker/
├── ITN processor/
├── label_studio/
├── .gitignore
└── README.md
```

### corpus_checker

Utilities for checking and analyzing text corpus data.

### ITN processor

Experiments related to **Inverse Text Normalization (ITN)**.

### label_studio

A demo project showing how to use **Label Studio** for sentiment annotation and model training.

---

## Label Studio Sentiment Demo

This demo demonstrates a simple NLP pipeline:

1. Generate a sentiment dataset  
2. Annotate data using Label Studio  
3. Train sentiment classification models  
4. Run predictions on new text  

Example models included in the project:

- BERT-based sentiment classifier  
- Word2Vec-based model  
- Simple baseline model  

---

## Example Usage

### Train a BERT Model

```
python label_studio/demo_data/train_bert.py
```

### Run Sentiment Prediction

```
python label_studio/demo_data/predict.py
```

---

## Dependencies

Typical libraries used in this project:

- Python 3.9+
- PyTorch
- Transformers
- Pandas
- Scikit-learn

Install dependencies:

```
pip install -r requirements.txt
```

---

## Notes

Model checkpoints and training results are **not included** in this repository.

Training outputs such as model checkpoints are stored locally in:

```
results/
```

These files are ignored by Git using `.gitignore`.

---

## Purpose

This repository is mainly used for learning and experimenting with NLP pipelines, dataset preparation, and model training workflows.
