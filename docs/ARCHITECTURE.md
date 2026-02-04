# System Architecture Documentation

## NEXORA AI - Explainable Decision Intelligence System

### Architecture Overview

NEXORA AI follows a **3-tier architecture** with clear separation of concerns:

```
┌───────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                        │
│                     (Frontend - HTML/CSS/JS)                   │
├───────────────────────────────────────────────────────────────┤
│                    APPLICATION LAYER                           │
│                    (FastAPI Backend)                           │
├───────────────────────────────────────────────────────────────┤
│                    DATA SCIENCE LAYER                          │
│    (ML Models, Preprocessing, EDA, XAI, Decision Logic)       │
└───────────────────────────────────────────────────────────────┘
```

## 1. Presentation Layer (Frontend)

### Purpose
Provide an intuitive, educational interface for users to interact with the decision intelligence system.

### Components

#### index.html
- **Single-page application** with 10 distinct steps
- Progress bar showing current workflow position
- Responsive forms and data displays
- Real-time feedback and validation

#### styles.css
- Modern, professional design
- Gradient color schemes for visual appeal
- Card-based layouts for information hierarchy
- Responsive design for mobile compatibility
- Accessibility considerations

#### app.js
- State management for session data
- API communication with backend
- Dynamic UI updates based on workflow
- Form validation and error handling
- Progress tracking across steps

### User Flow
```
Decision Context → Data Input → Preprocessing → EDA → 
Feature Selection → Model Training → XAI → Recommendations → 
Human Validation → Quality Metrics
```

## 2. Application Layer (Backend)

### Purpose
Orchestrate the decision intelligence workflow, manage sessions, and coordinate data science modules.

### Technology: FastAPI
- **Fast**: High performance, on par with NodeJS and Go
- **Modern**: Python 3.8+ type hints
- **Standards-based**: OpenAPI and JSON Schema
- **Easy**: Automatic interactive documentation

### API Endpoints

#### Health & Status
- `GET /health` - System health check
- `GET /api/session-state` - Current workflow state

#### Workflow Steps
1. `POST /api/decision-context` - Save decision problem definition
2. `POST /api/upload-data` - Upload and validate CSV data
3. `POST /api/preprocess` - Clean and prepare data
4. `GET /api/eda` - Perform exploratory data analysis
5. `POST /api/train-model` - Train ML models
6. `GET /api/explain` - Generate explanations
7. `GET /api/recommendations` - Create decision recommendations
8. `POST /api/validate` - Process human feedback
9. `GET /api/decision-quality` - Calculate quality metrics

### Session Management
- In-memory session storage (dictionary-based)
- Session ID: "default" (for demo; production would use UUIDs)
- Stores: context, data, models, explanations, validations
- Future: Database integration (PostgreSQL/MongoDB)

### CORS Configuration
- Allows cross-origin requests for development
- Production: Restrict to specific origins

## 3. Data Science Layer

### Module 1: Data Processor (`data_processor.py`)

**Purpose**: Handle data ingestion, validation, and preprocessing

**Key Functions**:
- `process_upload()`: Parse CSV, validate structure, extract metadata
- `preprocess()`: Clean data, handle missing values, encode categoricals
- `get_feature_info()`: Generate feature statistics

**Preprocessing Steps**:
1. **Missing Value Handling**:
   - Numeric: Median imputation
   - Categorical: Mode imputation
   - Rationale: Preserves distribution, robust to outliers

2. **Categorical Encoding**:
   - Label encoding for categorical features
   - Limited to features with ≤10 unique values
   - Rationale: Prevents dimensionality explosion

3. **Outlier Detection**:
   - IQR method (Q1 - 1.5*IQR, Q3 + 1.5*IQR)
   - Detection only, no removal
   - Rationale: Human should decide on outlier treatment

### Module 2: EDA Analyzer (`eda_analyzer.py`)

**Purpose**: Explore and understand data patterns

**Key Functions**:
- `analyze()`: Comprehensive EDA
- `_statistical_summary()`: Descriptive statistics
- `_correlation_analysis()`: Feature relationships
- `_distribution_insights()`: Data distributions
- `_feature_insights()`: Feature characterization

**Analysis Output**:
- **Statistical Summary**: Mean, median, std, quartiles, skewness, kurtosis
- **Correlations**: Identify strong correlations (|r| > 0.7)
- **Distributions**: Classify as normal, skewed
- **Feature Types**: Discrete, continuous, categorical

**Key Observations Generation**:
- Automated insight extraction
- Plain language summaries
- Actionable recommendations

### Module 3: ML Model Engine (`ml_model.py`)

**Purpose**: Train interpretable machine learning models

**Models Implemented**:

1. **Decision Tree Classifier**
   - max_depth=5 (interpretability constraint)
   - min_samples_split=10
   - min_samples_leaf=5
   - **Why**: Fully interpretable, rule-based, visual

2. **Logistic Regression**
   - max_iter=1000
   - **Why**: Linear relationships, coefficient interpretation

3. **Random Forest Classifier**
   - n_estimators=50
   - max_depth=5
   - **Why**: Ensemble robustness, feature importance

**Model Selection**:
- 80/20 train-test split
- Evaluate all models
- Select best by test accuracy
- Consider overfitting (train vs test gap)

**Evaluation Metrics**:
- Accuracy (overall correctness)
- Precision (positive prediction accuracy)
- Recall (positive case detection)
- F1-Score (harmonic mean of precision/recall)
- Confusion Matrix (detailed error analysis)

### Module 4: Explainer Engine (`explainer.py`)

**Purpose**: Generate explanations for model predictions (XAI)

**Explainability Techniques**:

1. **Feature Importance**
   - Tree-based: Gini importance
   - Linear: Coefficient magnitude
   - Ranking and percentage contribution

2. **Decision Rules**
   - Decision tree path extraction
   - Logistic regression equation
   - Human-readable format

3. **Instance Explanations**
   - Per-prediction analysis
   - Feature contribution calculation
   - Natural language generation

4. **Natural Language Summary**
   - Overall model behavior
   - Key driving factors
   - Confidence assessment

**Why This Matters**:
- Builds trust in AI decisions
- Enables validation by domain experts
- Supports regulatory compliance
- Educational value for students

### Module 5: Decision Intelligence (`decision_intelligence.py`)

**Purpose**: Convert ML insights into actionable recommendations

**Key Functions**:
- `generate_recommendations()`: Create decision options
- `process_validation()`: Handle human feedback
- `calculate_quality_metrics()`: Assess decision quality

**Recommendation Components**:

1. **Primary Recommendation**
   - Based on best model
   - Confidence score
   - Reasoning explanation
   - Recommended action

2. **Alternative Options**
   - Conservative approach
   - Data-driven approach
   - Hybrid approach (recommended)

3. **Decision Factors**
   - Ranked by importance
   - Impact assessment
   - Actionable insights

4. **Risks and Limitations**
   - Overfitting warnings
   - Low accuracy alerts
   - General AI limitations

5. **Human Considerations**
   - Ethical review points
   - Domain knowledge integration
   - Success criteria definition

**Quality Metrics**:
- **Clarity**: How understandable the decision is (0-100%)
- **Confidence**: User's confidence in decision (0-100%)
- **Trust**: Overall system trust (0-100%)

## Data Flow

```
1. User uploads CSV
   ↓
2. DataProcessor validates and cleans
   ↓
3. EDAAnalyzer explores patterns
   ↓
4. MLModelEngine trains models
   ↓
5. ExplainerEngine generates explanations
   ↓
6. DecisionIntelligence creates recommendations
   ↓
7. Human validates
   ↓
8. Quality metrics calculated
```

## Design Patterns

### 1. Separation of Concerns
- Each module has single responsibility
- Frontend doesn't contain business logic
- Backend orchestrates, doesn't implement DS logic

### 2. Pipeline Pattern
- Data flows through stages
- Each stage adds value
- Results accumulate in session

### 3. Strategy Pattern
- Multiple ML models (strategies)
- Select best at runtime
- Easy to add new models

### 4. Factory Pattern
- Model creation abstracted
- Configuration-driven
- Consistent interface

## Security Considerations

### Current Implementation (Demo/Academic)
- No authentication (single user)
- In-memory storage (no persistence)
- CORS open (development)
- No sensitive data encryption

### Production Requirements
- User authentication (JWT tokens)
- Database with encryption
- CORS restricted to known origins
- HTTPS only
- Rate limiting
- Input sanitization
- Audit logging

## Scalability Considerations

### Current Limitations
- Single-threaded session storage
- No caching
- Synchronous processing
- Limited to small datasets

### Scale-Up Path
1. **Database**: PostgreSQL for sessions
2. **Caching**: Redis for model results
3. **Async**: Background jobs for training
4. **Load Balancing**: Multiple FastAPI instances
5. **Containerization**: Docker + Kubernetes
6. **Monitoring**: Prometheus + Grafana

## Performance

### Expected Response Times
- Data upload: < 1s (for <10MB files)
- Preprocessing: < 2s
- EDA: < 3s
- Model training: 5-30s (depends on data size)
- Explanations: < 2s
- Recommendations: < 1s

### Optimization Strategies
- Lazy loading for large datasets
- Model caching
- Incremental updates
- Progressive rendering

## Testing Strategy

### Unit Tests
- Each module independently tested
- Mock external dependencies
- Test edge cases

### Integration Tests
- API endpoint testing
- Workflow validation
- Error handling

### User Acceptance Tests
- Complete workflow execution
- Sample data validation
- UI/UX verification

## Deployment

### Development
```bash
uvicorn backend.main:app --reload
```

### Production
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Future)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
```

## Maintenance

### Logging
- Application logs: uvicorn default
- Error tracking: Try-except blocks
- Audit trail: Decision logs (future)

### Monitoring
- Health endpoint: `/health`
- Session state: `/api/session-state`
- Model performance: Accuracy metrics

### Updates
- Model retraining: Manual (future: automated)
- Feature additions: Modular design
- Bug fixes: Version control

## Conclusion

NEXORA AI's architecture prioritizes:
- **Explainability** over complexity
- **Human control** over automation
- **Education** over obfuscation
- **Research value** over production optimization

This makes it ideal for academic projects while providing a foundation for real-world deployment.
