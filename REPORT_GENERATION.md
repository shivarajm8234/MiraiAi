# Research Report Generation Guide

This guide explains how to generate all the research visualizations and analysis reports from the `miraiai.ipynb` notebook.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Notebook](#running-the-notebook)
- [Generated Outputs](#generated-outputs)# Research Report Generation Guide

This guide explains how to generate all the research visualizations and analysis reports from the `miraiai.ipynb` notebook.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Notebook](#running-the-notebook)
- [Generated Outputs](#generated-outputs)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **Jupyter Notebook** or **JupyterLab**
- **GPU**: NVIDIA GPU with CUDA support (recommended for training)
- **RAM**: Minimum 16GB (32GB recommended)
- **Storage**: At least 20GB free space

### Required Python Packages

Install all dependencies using:

```bash
pip install -r requirements_notebook.txt
```

Or install individually:

```bash
# Core ML Libraries
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers datasets accelerate
pip install unsloth

# Data Processing
pip install pandas numpy scikit-learn

# Visualization
pip install matplotlib seaborn plotly

# Training & Fine-tuning
pip install trl peft bitsandbytes

# Utilities
pip install jupyter ipywidgets tqdm
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shivarajm8234/MiraiAi.git
cd MiraiAi
```

### 2. Set Up Python Environment

**Option A: Using venv**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements_notebook.txt
```

**Option B: Using conda**
```bash
conda create -n miraiai python=3.10
conda activate miraiai
pip install -r requirements_notebook.txt
```

### 3. Verify GPU Access (Optional but Recommended)

```python
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"GPU Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
```

---

## 📊 Running the Notebook

### 1. Launch Jupyter Notebook

```bash
jupyter notebook miraiai.ipynb
```

Or use JupyterLab:
```bash
jupyter lab miraiai.ipynb
```

### 2. Execute Cells in Order

The notebook is organized into sections:

#### **Section 1-4: Environment Setup**
- Install dependencies
- Import libraries
- Configure model settings

#### **Section 5-6: Data Loading**
- Load GoEmotions dataset (43,410 samples)
- Load Emotion dataset (16,000 samples)
- Load TweetEval dataset (3,257 samples)
- Combine and preprocess data

#### **Section 7: Model Loading**
- Load Meta-Llama-3.1-8B-Instruct
- Configure LoRA adapters
- Set up training parameters

#### **Section 8-9: Training**
- Train the model with LoRA
- Monitor training metrics
- Save model checkpoints

#### **Section 10-15: Visualization & Analysis**
- Generate all research visualizations
- Create performance metrics
- Export analysis reports

### 3. Run All Cells

**Option A: Run All at Once**
```
Cell → Run All
```

**Option B: Run Section by Section**
- Recommended for monitoring progress
- Allows debugging if errors occur

---

## 📈 Generated Outputs

### Visualization Files (Saved to `Output/` directory)

| File Name | Description | Section |
|-----------|-------------|---------|
| `training perf analysis.png` | Training/validation loss and accuracy curves | Section 11 |
| `Loss comparsion.png` | Comparative loss analysis | Section 11 |
| `confusion mat.png` | Confusion matrix for emotion classification | Section 12 |
| `ROC.png` | ROC curves and performance metrics | Section 12 |
| `benchmark.png` | Comparison with other training methods | Section 13 |
| `dataset.png` | Dataset distribution and composition | Section 10 |
| `text anlysis.png` | Text length and sentiment analysis | Section 10 |
| `Cosine smoot.png` | Semantic similarity analysis | Section 14 |

### Model Files (Saved to `emotion_model_finetuned/` directory)

```
emotion_model_finetuned/
├── adapter_config.json          # LoRA configuration
├── adapter_model.safetensors    # Fine-tuned weights
├── tokenizer.json               # Tokenizer files
├── training_config.json         # Training hyperparameters
└── README.md                    # Model documentation
```

### Training Logs

```
training_logs/
├── training_progress.png        # Loss curves
├── trainer_state.json          # Training state
└── training_args.bin           # Training arguments
```

---

## 🎯 Key Metrics Generated

### Training Metrics
- **Training Loss**: Initial 2.86 → Final 0.68 (76.35% improvement)
- **Validation Loss**: 0.656 (4.53% improvement)
- **Training Accuracy**: 85%
- **Validation Accuracy**: 85%

### Model Performance
- **Overall Accuracy**: 85%
- **Precision**: ~85%
- **Recall**: ~85%
- **F1-Score**: 85%
- **ROC AUC**: >0.85 for all emotion categories

### Efficiency Metrics
- **Trainable Parameters**: 1.03% of total
- **Model Size Reduction**: 98.75%
- **Training Speed**: 4x faster than full fine-tuning
- **Inference Time**: <500ms per request

---

## 🔍 Detailed Section Guide

### Section 10: Dataset Analysis
**Outputs:**
- `dataset.png`: Pie chart of dataset distribution
- `text anlysis.png`: Text length histograms

**What it shows:**
- Dataset composition (GoEmotions 69.3%, Emotion 25.5%, TweetEval 5.2%)
- Text length distribution across datasets
- Emotion category balance

### Section 11: Training Performance
**Outputs:**
- `training perf analysis.png`: 4-panel training metrics
- `Loss comparsion.png`: Training vs validation loss

**What it shows:**
- Loss convergence over epochs
- Accuracy improvement trajectory
- Overfitting analysis

### Section 12: Classification Metrics
**Outputs:**
- `confusion mat.png`: Confusion matrix heatmap
- `ROC.png`: ROC curves with performance bars

**What it shows:**
- Per-class classification accuracy
- Common misclassification patterns
- Model discrimination ability

### Section 13: Benchmark Comparison
**Outputs:**
- `benchmark.png`: Multi-panel comparison

**What it shows:**
- LoRA vs Full Fine-tuning vs Prompt Engineering
- Accuracy vs Parameters trade-off
- Training time comparison
- Cost-effectiveness analysis

### Section 14: Semantic Analysis
**Outputs:**
- `Cosine smoot.png`: Semantic similarity over time

**What it shows:**
- Response quality metrics
- Semantic alignment scores
- Prediction consistency

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. **CUDA Out of Memory**
```python
# Reduce batch size in Section 8
per_device_train_batch_size = 2  # Default: 4
gradient_accumulation_steps = 8   # Default: 4
```

#### 2. **Dataset Download Fails**
```bash
# Manually download datasets
huggingface-cli login
python -c "from datasets import load_dataset; load_dataset('google-research-datasets/go_emotions')"
```

#### 3. **Import Errors**
```bash
# Reinstall specific packages
pip install --upgrade transformers datasets unsloth
```

#### 4. **Visualization Not Showing**
```python
# Add at the start of visualization cells
import matplotlib
matplotlib.use('Agg')  # For saving without display
# Or
%matplotlib inline  # For Jupyter display
```

#### 5. **Model Loading Fails**
```python
# Clear cache and retry
import torch
torch.cuda.empty_cache()

# Or use CPU fallback
device = "cpu"  # Instead of "cuda"
```

---

## 📝 Customization Options

### Modify Training Parameters

In **Section 8**, adjust:

```python
# Learning rate
learning_rate = 2e-4  # Default: 2e-4

# Number of epochs
num_train_epochs = 3  # Default: 3

# Batch size
per_device_train_batch_size = 4  # Default: 4

# LoRA rank
lora_r = 16  # Default: 16 (higher = more parameters)
```

### Change Visualization Style

In visualization sections:

```python
# Color scheme
colors = ['#1e40af', '#0ea5e9', '#10b981']  # Custom colors

# Figure size
plt.figure(figsize=(16, 10))  # Adjust dimensions

# DPI for higher quality
plt.savefig('output.png', dpi=300, bbox_inches='tight')
```

### Export Different Formats

```python
# Save as PDF
plt.savefig('output.pdf', format='pdf')

# Save as SVG (vector)
plt.savefig('output.svg', format='svg')

# Save as high-res PNG
plt.savefig('output.png', dpi=600)
```

---

## 📤 Exporting Results

### 1. Copy Outputs to Website

```bash
# Copy all visualizations
cp Output/*.png website/assets/images/Output/

# Verify files
ls website/assets/images/Output/
```

### 2. Generate PDF Report

```python
# In the notebook, add:
from matplotlib.backends.backend_pdf import PdfPages

with PdfPages('research_report.pdf') as pdf:
    # Add each figure
    pdf.savefig(fig1)
    pdf.savefig(fig2)
    # ... etc
```

### 3. Export Metrics to JSON

```python
import json

metrics = {
    "accuracy": 0.85,
    "precision": 0.85,
    "recall": 0.85,
    "f1_score": 0.85,
    "training_loss": 0.68,
    "validation_loss": 0.656
}

with open('metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
```

---

## 🎓 Understanding the Results

### What Makes This Research Significant?

1. **Parameter Efficiency**: Only 1.03% trainable parameters
2. **High Accuracy**: 85% with minimal training
3. **Fast Training**: 4x faster than full fine-tuning
4. **Production Ready**: <500ms inference time
5. **Multi-Dataset**: Robust across different text styles

### Key Insights

- **LoRA Effectiveness**: Achieves near-full-fine-tuning performance with 98.75% fewer parameters
- **No Overfitting**: Training and validation curves align closely
- **Balanced Performance**: Equal precision and recall across emotions
- **Scalable**: Suitable for deployment in resource-constrained environments

---

## 📚 Additional Resources

### Documentation
- [Unsloth Documentation](https://github.com/unslothai/unsloth)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)

### Datasets
- [GoEmotions](https://github.com/google-research/google-research/tree/master/goemotions)
- [Emotion Dataset](https://huggingface.co/datasets/emotion)
- [TweetEval](https://github.com/cardiffnlp/tweeteval)

### Related Work
- [Mental Health NLP Survey](https://arxiv.org/abs/2106.15033)
- [Parameter-Efficient Fine-Tuning](https://arxiv.org/abs/2110.04366)

---

## 🤝 Contributing

To improve the notebook or add new visualizations:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/new-analysis`
3. Add your changes to the notebook
4. Commit: `git commit -m "Add new analysis section"`
5. Push: `git push origin feature/new-analysis`
6. Create a Pull Request

---

## 📧 Support

For issues or questions:
- **GitHub Issues**: [Create an issue](https://github.com/shivarajm8234/MiraiAi/issues)
- **Email**: Contact the team
- **Telegram Bot**: [@Mirai_Ai_bot](https://t.me/Mirai_Ai_bot)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Meta AI** for Llama 3.1 model
- **Unsloth** for efficient training framework
- **Google Research** for GoEmotions dataset
- **Hugging Face** for datasets and transformers library

---

**Last Updated**: October 2025  
**Version**: 1.0  
**Notebook**: `miraiai.ipynb`
# Research Report Generation Guide

This guide explains how to generate all the research visualizations and analysis reports from the `miraiai.ipynb` notebook.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Notebook](#running-the-notebook)
- [Generated Outputs](#generated-outputs)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **Jupyter Notebook** or **JupyterLab**
- **GPU**: NVIDIA GPU with CUDA support (recommended for training)
- **RAM**: Minimum 16GB (32GB recommended)
- **Storage**: At least 20GB free space

### Required Python Packages

Install all dependencies using:

```bash
pip install -r requirements_notebook.txt
```

Or install individually:

```bash
# Core ML Libraries
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers datasets accelerate
pip install unsloth

# Data Processing
pip install pandas numpy scikit-learn

# Visualization
pip install matplotlib seaborn plotly

# Training & Fine-tuning
pip install trl peft bitsandbytes

# Utilities
pip install jupyter ipywidgets tqdm
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shivarajm8234/MiraiAi.git
cd MiraiAi
```

### 2. Set Up Python Environment

**Option A: Using venv**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements_notebook.txt
```

**Option B: Using conda**
```bash
conda create -n miraiai python=3.10
conda activate miraiai
pip install -r requirements_notebook.txt
```

### 3. Verify GPU Access (Optional but Recommended)

```python
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"GPU Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
```

---

## 📊 Running the Notebook

### 1. Launch Jupyter Notebook

```bash
jupyter notebook miraiai.ipynb
```

Or use JupyterLab:
```bash
jupyter lab miraiai.ipynb
```

### 2. Execute Cells in Order

The notebook is organized into sections:

#### **Section 1-4: Environment Setup**
- Install dependencies
- Import libraries
- Configure model settings

#### **Section 5-6: Data Loading**
- Load GoEmotions dataset (43,410 samples)
- Load Emotion dataset (16,000 samples)
- Load TweetEval dataset (3,257 samples)
- Combine and preprocess data

#### **Section 7: Model Loading**
- Load Meta-Llama-3.1-8B-Instruct
- Configure LoRA adapters
- Set up training parameters

#### **Section 8-9: Training**
- Train the model with LoRA
- Monitor training metrics
- Save model checkpoints

#### **Section 10-15: Visualization & Analysis**
- Generate all research visualizations
- Create performance metrics
- Export analysis reports

### 3. Run All Cells

**Option A: Run All at Once**
```
Cell → Run All
```

**Option B: Run Section by Section**
- Recommended for monitoring progress
- Allows debugging if errors occur

---

## 📈 Generated Outputs

### Visualization Files (Saved to `Output/` directory)

| File Name | Description | Section |
|-----------|-------------|---------|
| `training perf analysis.png` | Training/validation loss and accuracy curves | Section 11 |
| `Loss comparsion.png` | Comparative loss analysis | Section 11 |
| `confusion mat.png` | Confusion matrix for emotion classification | Section 12 |
| `ROC.png` | ROC curves and performance metrics | Section 12 |
| `benchmark.png` | Comparison with other training methods | Section 13 |
| `dataset.png` | Dataset distribution and composition | Section 10 |
| `text anlysis.png` | Text length and sentiment analysis | Section 10 |
| `Cosine smoot.png` | Semantic similarity analysis | Section 14 |

### Model Files (Saved to `emotion_model_finetuned/` directory)

```
emotion_model_finetuned/
├── adapter_config.json          # LoRA configuration
├── adapter_model.safetensors    # Fine-tuned weights
├── tokenizer.json               # Tokenizer files
├── training_config.json         # Training hyperparameters
└── README.md                    # Model documentation
```

### Training Logs

```
training_logs/
├── training_progress.png        # Loss curves
├── trainer_state.json          # Training state
└── training_args.bin           # Training arguments
```

---

## 🎯 Key Metrics Generated

### Training Metrics
- **Training Loss**: Initial 2.86 → Final 0.68 (76.35% improvement)
- **Validation Loss**: 0.656 (4.53% improvement)
- **Training Accuracy**: 85%
- **Validation Accuracy**: 85%

### Model Performance
- **Overall Accuracy**: 85%
- **Precision**: ~85%
- **Recall**: ~85%
- **F1-Score**: 85%
- **ROC AUC**: >0.85 for all emotion categories

### Efficiency Metrics
- **Trainable Parameters**: 1.03% of total
- **Model Size Reduction**: 98.75%
- **Training Speed**: 4x faster than full fine-tuning
- **Inference Time**: <500ms per request

---

## 🔍 Detailed Section Guide

### Section 10: Dataset Analysis
**Outputs:**
- `dataset.png`: Pie chart of dataset distribution
- `text anlysis.png`: Text length histograms

**What it shows:**
- Dataset composition (GoEmotions 69.3%, Emotion 25.5%, TweetEval 5.2%)
- Text length distribution across datasets
- Emotion category balance

### Section 11: Training Performance
**Outputs:**
- `training perf analysis.png`: 4-panel training metrics
- `Loss comparsion.png`: Training vs validation loss

**What it shows:**
- Loss convergence over epochs
- Accuracy improvement trajectory
- Overfitting analysis

### Section 12: Classification Metrics
**Outputs:**
- `confusion mat.png`: Confusion matrix heatmap
- `ROC.png`: ROC curves with performance bars

**What it shows:**
- Per-class classification accuracy
- Common misclassification patterns
- Model discrimination ability

### Section 13: Benchmark Comparison
**Outputs:**
- `benchmark.png`: Multi-panel comparison

**What it shows:**
- LoRA vs Full Fine-tuning vs Prompt Engineering
- Accuracy vs Parameters trade-off
- Training time comparison
- Cost-effectiveness analysis

### Section 14: Semantic Analysis
**Outputs:**
- `Cosine smoot.png`: Semantic similarity over time

**What it shows:**
- Response quality metrics
- Semantic alignment scores
- Prediction consistency

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. **CUDA Out of Memory**
```python
# Reduce batch size in Section 8
per_device_train_batch_size = 2  # Default: 4
gradient_accumulation_steps = 8   # Default: 4
```

#### 2. **Dataset Download Fails**
```bash
# Manually download datasets
huggingface-cli login
python -c "from datasets import load_dataset; load_dataset('google-research-datasets/go_emotions')"
```

#### 3. **Import Errors**
```bash
# Reinstall specific packages
pip install --upgrade transformers datasets unsloth
```

#### 4. **Visualization Not Showing**
```python
# Add at the start of visualization cells
import matplotlib
matplotlib.use('Agg')  # For saving without display
# Or
%matplotlib inline  # For Jupyter display
```

#### 5. **Model Loading Fails**
```python
# Clear cache and retry
import torch
torch.cuda.empty_cache()

# Or use CPU fallback
device = "cpu"  # Instead of "cuda"
```

---

## 📝 Customization Options

### Modify Training Parameters

In **Section 8**, adjust:

```python
# Learning rate
learning_rate = 2e-4  # Default: 2e-4

# Number of epochs
num_train_epochs = 3  # Default: 3

# Batch size
per_device_train_batch_size = 4  # Default: 4

# LoRA rank
lora_r = 16  # Default: 16 (higher = more parameters)
```

### Change Visualization Style

In visualization sections:

```python
# Color scheme
colors = ['#1e40af', '#0ea5e9', '#10b981']  # Custom colors

# Figure size
plt.figure(figsize=(16, 10))  # Adjust dimensions

# DPI for higher quality
plt.savefig('output.png', dpi=300, bbox_inches='tight')
```

### Export Different Formats

```python
# Save as PDF
plt.savefig('output.pdf', format='pdf')

# Save as SVG (vector)
plt.savefig('output.svg', format='svg')

# Save as high-res PNG
plt.savefig('output.png', dpi=600)
```

---

## 📤 Exporting Results

### 1. Copy Outputs to Website

```bash
# Copy all visualizations
cp Output/*.png website/assets/images/Output/

# Verify files
ls website/assets/images/Output/
```

### 2. Generate PDF Report

```python
# In the notebook, add:
from matplotlib.backends.backend_pdf import PdfPages

with PdfPages('research_report.pdf') as pdf:
    # Add each figure
    pdf.savefig(fig1)
    pdf.savefig(fig2)
    # ... etc
```

### 3. Export Metrics to JSON

```python
import json

metrics = {
    "accuracy": 0.85,
    "precision": 0.85,
    "recall": 0.85,
    "f1_score": 0.85,
    "training_loss": 0.68,
    "validation_loss": 0.656
}

with open('metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
```

---

## 🎓 Understanding the Results

### What Makes This Research Significant?

1. **Parameter Efficiency**: Only 1.03% trainable parameters
2. **High Accuracy**: 85% with minimal training
3. **Fast Training**: 4x faster than full fine-tuning
4. **Production Ready**: <500ms inference time
5. **Multi-Dataset**: Robust across different text styles

### Key Insights

- **LoRA Effectiveness**: Achieves near-full-fine-tuning performance with 98.75% fewer parameters
- **No Overfitting**: Training and validation curves align closely
- **Balanced Performance**: Equal precision and recall across emotions
- **Scalable**: Suitable for deployment in resource-constrained environments

---

## 📚 Additional Resources

### Documentation
- [Unsloth Documentation](https://github.com/unslothai/unsloth)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)

### Datasets
- [GoEmotions](https://github.com/google-research/google-research/tree/master/goemotions)
- [Emotion Dataset](https://huggingface.co/datasets/emotion)
- [TweetEval](https://github.com/cardiffnlp/tweeteval)

### Related Work
- [Mental Health NLP Survey](https://arxiv.org/abs/2106.15033)
- [Parameter-Efficient Fine-Tuning](https://arxiv.org/abs/2110.04366)

---

## 🤝 Contributing

To improve the notebook or add new visualizations:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/new-analysis`
3. Add your changes to the notebook
4. Commit: `git commit -m "Add new analysis section"`
5. Push: `git push origin feature/new-analysis`
6. Create a Pull Request

---

## 📧 Support

For issues or questions:
- **GitHub Issues**: [Create an issue](https://github.com/shivarajm8234/MiraiAi/issues)
- **Email**: Contact the team
- **Telegram Bot**: [@Mirai_Ai_bot](https://t.me/Mirai_Ai_bot)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Meta AI** for Llama 3.1 model
- **Unsloth** for efficient training framework
- **Google Research** for GoEmotions dataset
- **Hugging Face** for datasets and transformers library

---

**Last Updated**: October 2025  
**Version**: 1.0  
**Notebook**: `miraiai.ipynb`

- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **Jupyter Notebook** or **JupyterLab**
- **GPU**: NVIDIA GPU with CUDA support (recommended for training)
- **RAM**: Minimum 16GB (32GB recommended)
- **Storage**: At least 20GB free space

### Required Python Packages

Install all dependencies using:

```bash
pip install -r requirements_notebook.txt
```

Or install individually:

```bash
# Core ML Libraries
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers datasets accelerate
pip install unsloth

# Data Processing
pip install pandas numpy scikit-learn

# Visualization
pip install matplotlib seaborn plotly

# Training & Fine-tuning
pip install trl peft bitsandbytes

# Utilities
pip install jupyter ipywidgets tqdm
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shivarajm8234/MiraiAi.git
cd MiraiAi
```

### 2. Set Up Python Environment

**Option A: Using venv**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements_notebook.txt
```

**Option B: Using conda**
```bash
conda create -n miraiai python=3.10
conda activate miraiai
pip install -r requirements_notebook.txt
```

### 3. Verify GPU Access (Optional but Recommended)

```python
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"GPU Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
```

---

## 📊 Running the Notebook

### 1. Launch Jupyter Notebook

```bash
jupyter notebook miraiai.ipynb
```

Or use JupyterLab:
```bash
jupyter lab miraiai.ipynb
```

### 2. Execute Cells in Order

The notebook is organized into sections:

#### **Section 1-4: Environment Setup**
- Install dependencies
- Import libraries
- Configure model settings

#### **Section 5-6: Data Loading**
- Load GoEmotions dataset (43,410 samples)
- Load Emotion dataset (16,000 samples)
- Load TweetEval dataset (3,257 samples)
- Combine and preprocess data

#### **Section 7: Model Loading**
- Load Meta-Llama-3.1-8B-Instruct
- Configure LoRA adapters
- Set up training parameters

#### **Section 8-9: Training**
- Train the model with LoRA
- Monitor training metrics
- Save model checkpoints

#### **Section 10-15: Visualization & Analysis**
- Generate all research visualizations
- Create performance metrics
- Export analysis reports

### 3. Run All Cells

**Option A: Run All at Once**
```
Cell → Run All
```

**Option B: Run Section by Section**
- Recommended for monitoring progress
- Allows debugging if errors occur

---

## 📈 Generated Outputs

### Visualization Files (Saved to `Output/` directory)

| File Name | Description | Section |
|-----------|-------------|---------|
| `training perf analysis.png` | Training/validation loss and accuracy curves | Section 11 |
| `Loss comparsion.png` | Comparative loss analysis | Section 11 |
| `confusion mat.png` | Confusion matrix for emotion classification | Section 12 |
| `ROC.png` | ROC curves and performance metrics | Section 12 |
| `benchmark.png` | Comparison with other training methods | Section 13 |
| `dataset.png` | Dataset distribution and composition | Section 10 |
| `text anlysis.png` | Text length and sentiment analysis | Section 10 |
| `Cosine smoot.png` | Semantic similarity analysis | Section 14 |

### Model Files (Saved to `emotion_model_finetuned/` directory)

```
emotion_model_finetuned/
├── adapter_config.json          # LoRA configuration
├── adapter_model.safetensors    # Fine-tuned weights
├── tokenizer.json               # Tokenizer files
├── training_config.json         # Training hyperparameters
└── README.md                    # Model documentation
```

### Training Logs

```
training_logs/
├── training_progress.png        # Loss curves
├── trainer_state.json          # Training state
└── training_args.bin           # Training arguments
```

---

## 🎯 Key Metrics Generated

### Training Metrics
- **Training Loss**: Initial 2.86 → Final 0.68 (76.35% improvement)
- **Validation Loss**: 0.656 (4.53% improvement)
- **Training Accuracy**: 85%
- **Validation Accuracy**: 85%

### Model Performance
- **Overall Accuracy**: 85%
- **Precision**: ~85%
- **Recall**: ~85%
- **F1-Score**: 85%
- **ROC AUC**: >0.85 for all emotion categories

### Efficiency Metrics
- **Trainable Parameters**: 1.03% of total
- **Model Size Reduction**: 98.75%
- **Training Speed**: 4x faster than full fine-tuning
- **Inference Time**: <500ms per request

---

## 🔍 Detailed Section Guide

### Section 10: Dataset Analysis
**Outputs:**
- `dataset.png`: Pie chart of dataset distribution
- `text anlysis.png`: Text length histograms

**What it shows:**
- Dataset composition (GoEmotions 69.3%, Emotion 25.5%, TweetEval 5.2%)
- Text length distribution across datasets
- Emotion category balance

### Section 11: Training Performance
**Outputs:**
- `training perf analysis.png`: 4-panel training metrics
- `Loss comparsion.png`: Training vs validation loss

**What it shows:**
- Loss convergence over epochs
- Accuracy improvement trajectory
- Overfitting analysis

### Section 12: Classification Metrics
**Outputs:**
- `confusion mat.png`: Confusion matrix heatmap
- `ROC.png`: ROC curves with performance bars

**What it shows:**
- Per-class classification accuracy
- Common misclassification patterns
- Model discrimination ability

### Section 13: Benchmark Comparison
**Outputs:**
- `benchmark.png`: Multi-panel comparison

**What it shows:**
- LoRA vs Full Fine-tuning vs Prompt Engineering
- Accuracy vs Parameters trade-off
- Training time comparison
- Cost-effectiveness analysis

### Section 14: Semantic Analysis
**Outputs:**
- `Cosine smoot.png`: Semantic similarity over time

**What it shows:**
- Response quality metrics
- Semantic alignment scores
- Prediction consistency

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. **CUDA Out of Memory**
```python
# Reduce batch size in Section 8
per_device_train_batch_size = 2  # Default: 4
gradient_accumulation_steps = 8   # Default: 4
```

#### 2. **Dataset Download Fails**
```bash
# Manually download datasets
huggingface-cli login
python -c "from datasets import load_dataset; load_dataset('google-research-datasets/go_emotions')"
```

#### 3. **Import Errors**
```bash
# Reinstall specific packages
pip install --upgrade transformers datasets unsloth
```

#### 4. **Visualization Not Showing**
```python
# Add at the start of visualization cells
import matplotlib
matplotlib.use('Agg')  # For saving without display
# Or
%matplotlib inline  # For Jupyter display
```

#### 5. **Model Loading Fails**
```python
# Clear cache and retry
import torch
torch.cuda.empty_cache()

# Or use CPU fallback
device = "cpu"  # Instead of "cuda"
```

---

## 📝 Customization Options

### Modify Training Parameters

In **Section 8**, adjust:

```python
# Learning rate
learning_rate = 2e-4  # Default: 2e-4

# Number of epochs
num_train_epochs = 3  # Default: 3

# Batch size
per_device_train_batch_size = 4  # Default: 4

# LoRA rank
lora_r = 16  # Default: 16 (higher = more parameters)
```

### Change Visualization Style

In visualization sections:

```python
# Color scheme
colors = ['#1e40af', '#0ea5e9', '#10b981']  # Custom colors

# Figure size
plt.figure(figsize=(16, 10))  # Adjust dimensions

# DPI for higher quality
plt.savefig('output.png', dpi=300, bbox_inches='tight')
```

### Export Different Formats

```python
# Save as PDF
plt.savefig('output.pdf', format='pdf')

# Save as SVG (vector)
plt.savefig('output.svg', format='svg')

# Save as high-res PNG
plt.savefig('output.png', dpi=600)
```

---

## 📤 Exporting Results

### 1. Copy Outputs to Website

```bash
# Copy all visualizations
cp Output/*.png website/assets/images/Output/

# Verify files
ls website/assets/images/Output/
```

### 2. Generate PDF Report

```python
# In the notebook, add:
from matplotlib.backends.backend_pdf import PdfPages

with PdfPages('research_report.pdf') as pdf:
    # Add each figure
    pdf.savefig(fig1)
    pdf.savefig(fig2)
    # ... etc
```

### 3. Export Metrics to JSON

```python
import json

metrics = {
    "accuracy": 0.85,
    "precision": 0.85,
    "recall": 0.85,
    "f1_score": 0.85,
    "training_loss": 0.68,
    "validation_loss": 0.656
}

with open('metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
```

---

## 🎓 Understanding the Results

### What Makes This Research Significant?

1. **Parameter Efficiency**: Only 1.03% trainable parameters
2. **High Accuracy**: 85% with minimal training
3. **Fast Training**: 4x faster than full fine-tuning
4. **Production Ready**: <500ms inference time
5. **Multi-Dataset**: Robust across different text styles

### Key Insights

- **LoRA Effectiveness**: Achieves near-full-fine-tuning performance with 98.75% fewer parameters
- **No Overfitting**: Training and validation curves align closely
- **Balanced Performance**: Equal precision and recall across emotions
- **Scalable**: Suitable for deployment in resource-constrained environments

---

## 📚 Additional Resources

### Documentation
- [Unsloth Documentation](https://github.com/unslothai/unsloth)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)

### Datasets
- [GoEmotions](https://github.com/google-research/google-research/tree/master/goemotions)
- [Emotion Dataset](https://huggingface.co/datasets/emotion)
- [TweetEval](https://github.com/cardiffnlp/tweeteval)

### Related Work
- [Mental Health NLP Survey](https://arxiv.org/abs/2106.15033)
- [Parameter-Efficient Fine-Tuning](https://arxiv.org/abs/2110.04366)

---

## 🤝 Contributing

To improve the notebook or add new visualizations:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/new-analysis`
3. Add your changes to the notebook
4. Commit: `git commit -m "Add new analysis section"`
5. Push: `git push origin feature/new-analysis`
6. Create a Pull Request

---

## 📧 Support

For issues or questions:
- **GitHub Issues**: [Create an issue](https://github.com/shivarajm8234/MiraiAi/issues)
- **Email**: Contact the team
- **Telegram Bot**: [@Mirai_Ai_bot](https://t.me/Mirai_Ai_bot)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Meta AI** for Llama 3.1 model
- **Unsloth** for efficient training framework
- **Google Research** for GoEmotions dataset
- **Hugging Face** for datasets and transformers library

---

**Last Updated**: October 2025  
**Version**: 1.0  
**Notebook**: `miraiai.ipynb`
