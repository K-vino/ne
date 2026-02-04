# NEXORA AI - Explainable Decision Intelligence System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🧠 Overview

NEXORA AI is a **domain-independent, explainable decision intelligence system** built for academic research and final-year engineering projects. It uses classical AI/ML techniques to support human decision-making without automation, chatbots, or generative AI.

### Key Principles

✅ **Classical AI/ML** - Uses interpretable models (Decision Trees, Logistic Regression)  
✅ **Explainable AI** - Every decision is explained with feature importance and rules  
✅ **Human-in-the-Loop** - Humans validate and control all decisions  
✅ **Domain-Independent** - Works with any structured data  
✅ **Research-Grade** - Suitable for academic projects and viva presentations  

### What Makes This Different?

- ❌ No ChatGPT or LLM logic
- ❌ No automated decision-making
- ❌ No black-box models
- ✅ Pure data science workflow
- ✅ Full transparency and explainability
- ✅ Human oversight at every step

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    NEXORA AI System                      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Frontend (HTML/CSS/JS)                                  │
│  ├─ 10 Interactive Pages                                │
│  ├─ Progress Tracking                                   │
│  └─ Responsive UI                                       │
│                                                           │
│  Backend (FastAPI)                                       │
│  ├─ RESTful API Endpoints                              │
│  ├─ Data Processing Pipeline                           │
│  └─ Session Management                                  │
│                                                           │
│  Data Science Modules                                    │
│  ├─ Data Processor (Cleaning, Encoding)                │
│  ├─ EDA Analyzer (Statistics, Correlations)            │
│  ├─ ML Models (Decision Tree, Logistic Regression)     │
│  ├─ Explainer Engine (XAI, SHAP, Feature Importance)   │
│  └─ Decision Intelligence (Recommendations)             │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## 📋 Features

### Complete Workflow (10 Steps)

1. **Decision Context** - Define your decision problem
2. **Data Input** - Upload CSV or enter structured data
3. **Data Preprocessing** - Automatic cleaning and validation
4. **EDA** - Statistical analysis and visualizations
5. **Feature Engineering** - Select relevant features
6. **ML Modeling** - Train interpretable models
7. **Explainable AI** - Understand model decisions
8. **Recommendations** - Get actionable insights with alternatives
9. **Human Validation** - Accept/Modify/Reject recommendations
10. **Quality Metrics** - Measure decision quality (Clarity, Confidence, Trust)

### Technical Features

- **Interpretable Models**: Decision Tree, Logistic Regression, Random Forest
- **Explainability**: Feature importance, decision rules, prediction explanations
- **Data Processing**: Missing value handling, encoding, normalization
- **EDA**: Statistical summaries, correlations, distribution analysis
- **Quality Assessment**: Clarity, confidence, and trust metrics

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/K-vino/ne.git
cd ne
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start the backend server**
```bash
python -m uvicorn backend.main:app --reload
```

4. **Access the application**

Open your browser and navigate to:
```
http://localhost:8000
```

### Using Sample Data

Sample datasets are provided in the `data/` directory:
- `sample_financial_decision.csv` - Investment decision data
- `sample_education_decision.csv` - Admission decision data

## 📖 Usage Guide

### Step-by-Step Workflow

#### 1. Define Decision Context
- Select decision type (Career, Business, Finance, Healthcare, Education)
- Describe your decision problem
- Specify domain (optional)

#### 2. Upload Data
- Click "Choose CSV File"
- Upload your structured data
- Preview data to verify

#### 3. Data Preprocessing
- System automatically:
  - Handles missing values
  - Encodes categorical variables
  - Detects outliers
  - Validates data quality

#### 4. Exploratory Data Analysis
- View statistical summaries
- Identify correlations
- Understand data distributions
- Review key observations

#### 5. Feature Engineering
- Select relevant feature columns
- Choose target column
- System validates selections

#### 6. Model Training
- System trains multiple interpretable models
- Compares performance metrics
- Selects best model automatically
- Shows accuracy, precision, recall, F1-score

#### 7. Explainable AI
- View feature importance rankings
- Understand decision rules
- See sample prediction explanations
- Read natural language summary

#### 8. Decision Recommendations
- Primary recommendation with confidence score
- Alternative options with rationale
- Key decision factors
- Risks and limitations
- Human considerations

#### 9. Human Validation
- Accept recommendation
- Modify recommendation
- Reject recommendation
- Provide comments and confidence level

#### 10. Quality Metrics
- Clarity score (how clear the decision is)
- Confidence score (your confidence)
- Trust score (system trust)
- Decision summary

## 🔬 Data Science Workflow

### Data Preprocessing
```python
# Automated steps:
1. Missing value imputation (median for numeric, mode for categorical)
2. Categorical encoding (label encoding)
3. Outlier detection (IQR method)
4. Data quality assessment
```

### Exploratory Data Analysis
```python
# Analysis includes:
1. Statistical summaries (mean, median, std, quartiles)
2. Correlation analysis (identify strong relationships)
3. Distribution analysis (skewness, kurtosis)
4. Feature type classification
```

### Machine Learning Models
```python
# Interpretable models:
1. Decision Tree Classifier (max_depth=5 for interpretability)
2. Logistic Regression (linear relationships)
3. Random Forest (ensemble for comparison)

# Evaluation metrics:
- Train/Test accuracy
- Precision, Recall, F1-Score
- Confusion Matrix
```

### Explainable AI
```python
# XAI techniques:
1. Feature Importance (from tree-based models)
2. Coefficient Analysis (from logistic regression)
3. Decision Rules Extraction (tree visualization)
4. Per-instance Explanations (contribution analysis)
```

## 🎓 Academic Value

### For Final-Year Projects

✅ **Complete System** - End-to-end implementation  
✅ **Research Oriented** - Based on XAI and Decision Intelligence literature  
✅ **Explainable** - Every component can be explained in viva  
✅ **Ethical** - Human-centric, no automation  
✅ **Reproducible** - Clear methodology and code  

### Viva Preparation

**Key Points to Explain:**

1. **Why not use deep learning?**
   - Deep learning is a black box
   - Our goal is explainability
   - Classical ML provides interpretable results

2. **Why no chatbot/LLM?**
   - Chatbots automate decisions
   - We support human decision-making
   - LLMs lack transparency

3. **What is Decision Intelligence?**
   - Converting data insights into actionable recommendations
   - Providing alternatives, not just one answer
   - Keeping humans in control

4. **How is explainability achieved?**
   - Feature importance shows what matters
   - Decision rules show how decisions are made
   - Natural language explanations make it understandable

### Research Extensions

Potential areas for further research:
- Multi-criteria decision analysis integration
- Time-series decision support
- Group decision-making features
- Advanced XAI techniques (LIME, SHAP deep integration)
- Domain-specific customizations

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **SHAP** - Explainable AI

### Frontend
- **HTML5** - Structure
- **CSS3** - Modern styling with gradients and animations
- **JavaScript** - Interactive functionality
- **Fetch API** - Backend communication

### Data Science
- **Preprocessing**: Missing value imputation, encoding, normalization
- **EDA**: Statistical analysis, correlation analysis
- **ML Models**: Decision Tree, Logistic Regression, Random Forest
- **XAI**: Feature importance, decision rules, SHAP values

## 📁 Project Structure

```
ne/
├── backend/
│   ├── __init__.py
│   ├── main.py                    # FastAPI server
│   ├── data_processor.py          # Data preprocessing
│   ├── eda_analyzer.py            # Exploratory data analysis
│   ├── ml_model.py                # ML model training
│   ├── explainer.py               # Explainable AI
│   └── decision_intelligence.py   # Decision recommendations
├── frontend/
│   ├── index.html                 # Main UI (10 pages)
│   ├── styles.css                 # Styling
│   └── app.js                     # Frontend logic
├── data/
│   ├── sample_financial_decision.csv
│   └── sample_education_decision.csv
├── docs/
│   └── (documentation files)
├── requirements.txt
├── README.md
└── LICENSE
```

## 🔒 Ethical Considerations

1. **Transparency** - All decisions are explainable
2. **Human Control** - Humans make final decisions
3. **No Bias Amplification** - Uses interpretable models
4. **Data Privacy** - Session-based, no persistent storage
5. **Responsible AI** - Support, not replacement, of human judgment

## ⚠️ Limitations & Future Scope

### Current Limitations

- Session-based storage (no database)
- Limited to binary/multi-class classification
- Requires structured data (CSV)
- Basic feature engineering
- Single-user sessions

### Future Enhancements

1. **Database Integration** - Persistent storage
2. **Advanced ML** - Support for regression, clustering
3. **Real-time Data** - API integration for live data
4. **Multi-user** - Collaborative decision-making
5. **Advanced Visualization** - Interactive charts
6. **Mobile App** - Native mobile interface
7. **Export Features** - PDF reports, decision logs
8. **Domain Templates** - Pre-configured for specific domains

## 🤝 Contributing

This is an academic project. Contributions are welcome for:
- Bug fixes
- Documentation improvements
- Additional sample datasets
- New explainability features
- UI/UX enhancements

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

- Academic Research Project
- Built for Final-Year Engineering Students
- Focus: Decision Intelligence & Explainable AI

## 📞 Support

For questions or issues:
1. Check documentation
2. Review code comments
3. Test with sample data
4. Verify backend is running

## 🎯 Project Goals Achieved

✅ Domain-independent decision intelligence system  
✅ Classical AI/ML with no generative AI  
✅ Complete explainability at every step  
✅ Human-in-the-loop validation  
✅ Quality metrics for decision evaluation  
✅ Research-grade implementation  
✅ Academic presentation ready  
✅ Ethical and responsible AI  

---

**NEXORA AI** - Making AI decisions explainable, controllable, and human-centric.

*"Not about replacing human judgment, but about augmenting it with data-driven insights."*