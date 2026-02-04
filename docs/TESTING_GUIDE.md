# Testing Guide

## NEXORA AI - Testing Documentation

### Testing Checklist

This guide helps you verify that NEXORA AI is working correctly.

---

## 1. Pre-Testing Setup

### Check Installation
```bash
# Verify Python
python3 --version  # Should be 3.8+

# Verify dependencies
pip list | grep fastapi
pip list | grep pandas
pip list | grep scikit-learn
```

### Start Backend
```bash
# Method 1: Using startup script
./start.sh

# Method 2: Direct command
python3 -m uvicorn backend.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 2. Backend API Testing

### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "NEXORA AI"
}
```

### Test Session State
```bash
curl http://localhost:8000/api/session-state
```

Expected response:
```json
{
  "status": "no_session",
  "step": 0
}
```

### Test Decision Context
```bash
curl -X POST http://localhost:8000/api/decision-context \
  -H "Content-Type: application/json" \
  -d '{
    "decision_type": "career",
    "description": "Test decision",
    "domain": "technology"
  }'
```

Expected response:
```json
{
  "status": "success",
  "message": "Decision context saved",
  "session_id": "default",
  "context": {...}
}
```

### Test Data Upload
```bash
curl -X POST http://localhost:8000/api/upload-data \
  -F "file=@data/sample_financial_decision.csv"
```

Expected response:
```json
{
  "status": "success",
  "message": "Data uploaded successfully",
  "data_info": {
    "filename": "sample_financial_decision.csv",
    "rows": 20,
    "columns": 6,
    ...
  }
}
```

---

## 3. Frontend Testing

### Access Web Interface
1. Open browser
2. Navigate to: `http://localhost:8000`
3. Verify page loads with NEXORA AI title

### Test Each Step

#### Step 1: Decision Context
- [ ] Page displays correctly
- [ ] Dropdown has options
- [ ] Text areas accept input
- [ ] "Continue" button works
- [ ] Moves to Step 2

#### Step 2: Data Input
- [ ] File chooser opens
- [ ] CSV file can be selected
- [ ] Preview displays correctly
- [ ] "Preprocess Data" button works
- [ ] Moves to Step 3

#### Step 3: Preprocessing
- [ ] Report displays
- [ ] Shows steps performed
- [ ] Shows issues found (if any)
- [ ] Data quality metrics shown
- [ ] "Continue to EDA" works

#### Step 4: EDA
- [ ] Statistical summaries display
- [ ] Correlations shown
- [ ] Key observations listed
- [ ] "Continue to Feature Engineering" works

#### Step 5: Feature Selection
- [ ] Checkboxes for all columns
- [ ] Target dropdown populated
- [ ] Can select/deselect features
- [ ] "Train Model" button works

#### Step 6: Model Output
- [ ] Best model shown
- [ ] Comparison table displays
- [ ] Metrics are reasonable
- [ ] "View Explanations" works

#### Step 7: Explainable AI
- [ ] Feature importance shown
- [ ] Decision rules displayed
- [ ] Sample predictions shown
- [ ] "Generate Recommendations" works

#### Step 8: Recommendations
- [ ] Primary recommendation displays
- [ ] Alternative options shown
- [ ] Decision factors listed
- [ ] Risks and limitations shown
- [ ] "Provide Validation" works

#### Step 9: Human Validation
- [ ] Three validation buttons work
- [ ] Comment box accepts text
- [ ] Confidence slider works
- [ ] "View Decision Quality" works

#### Step 10: Quality Metrics
- [ ] Three gauges display
- [ ] Scores are calculated
- [ ] Decision summary shows
- [ ] "Start New Decision" works

---

## 4. Complete Workflow Test

### Using Sample Financial Data

1. **Start fresh**: Clear browser cache or use incognito

2. **Step 1**: 
   - Select "Financial Decision"
   - Description: "Investment decision based on profile"
   - Click Continue

3. **Step 2**:
   - Upload `data/sample_financial_decision.csv`
   - Verify preview shows age, income, education_level, etc.
   - Click Preprocess

4. **Step 3**:
   - Check preprocessing report
   - Should show no missing values (data is clean)
   - Click Continue

5. **Step 4**:
   - Review EDA results
   - Check statistical summaries
   - Click Continue

6. **Step 5**:
   - Select features: age, income, education_level, years_experience, risk_tolerance
   - Select target: investment_score
   - Click Train Model

7. **Step 6**:
   - Wait for training (5-10 seconds)
   - Check which model performed best
   - Note accuracy (should be > 70%)
   - Click View Explanations

8. **Step 7**:
   - Review feature importance
   - Check decision rules
   - Read sample explanations
   - Click Generate Recommendations

9. **Step 8**:
   - Read primary recommendation
   - Review alternatives
   - Check risks and limitations
   - Click Provide Validation

10. **Step 9**:
    - Click "Accept Recommendation"
    - Add comment: "Test validation"
    - Set confidence to 8
    - Click View Decision Quality

11. **Step 10**:
    - Check quality gauges
    - Verify scores make sense
    - Click Start New Decision

### Using Sample Education Data

Repeat above with `data/sample_education_decision.csv`:
- Features: gpa, study_hours, attendance, prev_score, projects_completed
- Target: admission_result

---

## 5. Error Testing

### Test Invalid Data

#### Empty File
```bash
touch empty.csv
# Try uploading - should show error
```

#### Invalid CSV Format
```bash
echo "not,a,valid,csv" > invalid.csv
echo "missing,data" >> invalid.csv
# Try uploading - should handle gracefully
```

#### Missing Target in Features
- Select all columns as features
- Select one as target
- Should show error: "Target column cannot be a feature"

### Test API Errors

#### Call endpoint before data upload
```bash
curl http://localhost:8000/api/preprocess
# Should return error: "No data uploaded"
```

#### Upload without file
```bash
curl -X POST http://localhost:8000/api/upload-data
# Should return error
```

---

## 6. Performance Testing

### Response Time Benchmarks

- Health check: < 10ms
- Decision context save: < 50ms
- Data upload (20 rows): < 100ms
- Preprocessing: < 500ms
- EDA: < 1s
- Model training: 5-30s (varies with data size)
- Explanations: < 500ms
- Recommendations: < 100ms

### Test with Larger Dataset

Create larger sample:
```python
import pandas as pd
import numpy as np

# Generate 1000 rows
data = {
    'feature1': np.random.rand(1000),
    'feature2': np.random.rand(1000),
    'feature3': np.random.randint(0, 10, 1000),
    'feature4': np.random.rand(1000),
    'target': np.random.randint(0, 2, 1000)
}

df = pd.DataFrame(data)
df.to_csv('large_test.csv', index=False)
```

Upload and verify:
- Should handle without issues
- Training may take 10-20 seconds
- All steps should complete

---

## 7. Browser Compatibility

Test on:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

Expected: Works on all modern browsers

---

## 8. Module Testing

### Test Data Processor
```python
from backend.data_processor import DataProcessor
import pandas as pd

# Create test data
df = pd.DataFrame({
    'num': [1, 2, None, 4],
    'cat': ['a', 'b', 'c', None]
})

processor = DataProcessor()
result = processor.preprocess(df)

print(result['report'])  # Should show missing value handling
```

### Test EDA Analyzer
```python
from backend.eda_analyzer import EDAAnalyzer
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 6, 8, 10]
})

analyzer = EDAAnalyzer()
results = analyzer.analyze(df)

print(results['statistical_summary'])
print(results['correlation_analysis'])
```

### Test ML Model
```python
from backend.ml_model import MLModelEngine
import pandas as pd

df = pd.DataFrame({
    'f1': [1, 2, 3, 4, 5, 6, 7, 8],
    'f2': [2, 3, 4, 5, 6, 7, 8, 9],
    'target': [0, 0, 0, 0, 1, 1, 1, 1]
})

engine = MLModelEngine()
results = engine.train_and_evaluate(df, ['f1', 'f2'], 'target')

print(results['best_model'])
print(results['best_score'])
```

---

## 9. Common Issues & Solutions

### Issue: Port 8000 already in use
**Solution**:
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn backend.main:app --port 8001
```

### Issue: Module not found
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Frontend not loading
**Solution**:
- Check backend is running
- Verify no CORS errors in browser console
- Check frontend files exist in frontend/

### Issue: Model training fails
**Solution**:
- Check data has enough rows (minimum 8)
- Verify target column has multiple classes
- Ensure no NaN values after preprocessing

---

## 10. Success Criteria

System passes testing if:

✅ All API endpoints respond correctly  
✅ Complete workflow executes without errors  
✅ Both sample datasets work  
✅ All 10 steps display correctly  
✅ Model training produces results  
✅ Explanations are generated  
✅ Quality metrics calculated  
✅ No console errors in browser  
✅ Response times reasonable  
✅ Error handling works gracefully  

---

## 11. Automated Testing (Future)

### Unit Tests Template
```python
import pytest
from backend.data_processor import DataProcessor

def test_missing_value_handling():
    processor = DataProcessor()
    df = pd.DataFrame({'col': [1, None, 3]})
    result = processor.preprocess(df)
    assert result['dataframe']['col'].isnull().sum() == 0

def test_categorical_encoding():
    processor = DataProcessor()
    df = pd.DataFrame({'cat': ['a', 'b', 'c']})
    result = processor.preprocess(df)
    assert result['dataframe']['cat'].dtype in [int, float]
```

### Integration Tests Template
```python
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_decision_context():
    response = client.post("/api/decision-context", json={
        "decision_type": "test",
        "description": "test description"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

---

## 12. Testing Log Template

Keep track of testing:

```
Date: ___________
Tester: ___________

Backend API Tests:
[ ] Health endpoint: _______
[ ] Decision context: _______
[ ] Data upload: _______
[ ] Preprocessing: _______
[ ] EDA: _______
[ ] Model training: _______
[ ] Explanations: _______
[ ] Recommendations: _______
[ ] Validation: _______
[ ] Quality metrics: _______

Frontend Tests:
[ ] All 10 steps display
[ ] Navigation works
[ ] Forms functional
[ ] Data displays correctly
[ ] No console errors

Sample Data Tests:
[ ] Financial data: _______
[ ] Education data: _______

Issues Found:
_________________________________
_________________________________

Notes:
_________________________________
_________________________________
```

---

**Testing Complete! 🎉**

If all tests pass, your NEXORA AI system is ready for demonstration and deployment.
