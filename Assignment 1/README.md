# Assignment 1: News Classification

## Overview
This assignment focuses on text classification using deep learning techniques. We implement LSTM and GRU neural networks to classify news articles into different categories.

## Dataset
**AG News Topic Classification Dataset**
- **Language**: English
- **Classes**: 
  - 0 → World
  - 1 → Sports
  - 2 → Business
  - 3 → Sci/Tech
- **Training samples**: 120,000
- **Test samples**: 7,600

## Objectives
1. Implement complete data preparation pipeline
2. Build LSTM and GRU text classifiers
3. Compare three embedding strategies:
   - GloVe embeddings (frozen)
   - GloVe embeddings (fine-tuned)
   - Random embeddings
4. Perform hyperparameter tuning experiments
5. Evaluate and compare all models

## File
- `ag_news_classification.ipynb` - Jupyter notebook containing the complete implementation

## How to Run
1. Open the notebook in Jupyter or Google Colab
2. Install required dependencies (specified in the notebook)
3. Run all cells to train and evaluate models

## Requirements
- Python 3.6+
- TensorFlow/PyTorch
- NumPy
- Pandas
- Matplotlib
- GloVe embeddings (downloaded within notebook)

## Learning Outcomes
- Text preprocessing and tokenization
- Word embeddings and their applications
- LSTM and GRU architectures for sequence modeling
- Hyperparameter tuning strategies
- Model evaluation and comparison

---
*Part of AI Lab coursework*
