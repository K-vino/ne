// NEXORA AI - Frontend JavaScript Application

// API Base URL
const API_BASE = 'http://localhost:8000/api';

// Global state
let currentStep = 1;
let sessionData = {
    context: null,
    rawData: null,
    preprocessedData: null,
    edaResults: null,
    selectedFeatures: [],
    targetColumn: null,
    modelResults: null,
    explanations: null,
    recommendations: null,
    validation: null,
    qualityMetrics: null
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Setup file input listener
    document.getElementById('csvFile').addEventListener('change', handleFileSelect);
    
    // Setup confidence slider
    document.getElementById('confidenceSlider').addEventListener('input', function(e) {
        document.getElementById('confidenceValue').textContent = e.target.value;
    });
});

// Navigation
function goToStep(step) {
    // Hide all steps
    document.querySelectorAll('.step-container').forEach(el => {
        el.classList.remove('active');
    });
    
    // Show target step
    document.getElementById(`step${step}`).classList.add('active');
    
    // Update progress bar
    document.querySelectorAll('.progress-step').forEach((el, index) => {
        el.classList.remove('active');
        if (index + 1 === step) {
            el.classList.add('active');
        }
        if (index + 1 < step) {
            el.classList.add('completed');
        }
    });
    
    currentStep = step;
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Step 1: Save Decision Context
async function saveContext() {
    const decisionType = document.getElementById('decisionType').value;
    const description = document.getElementById('decisionDescription').value;
    const domain = document.getElementById('domain').value || 'general';
    
    if (!description.trim()) {
        alert('Please provide a decision description');
        return;
    }
    
    const contextData = {
        decision_type: decisionType,
        description: description,
        domain: domain
    };
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/decision-context`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(contextData)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            sessionData.context = result.context;
            goToStep(2);
        } else {
            alert('Failed to save context');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error connecting to server. Please ensure the backend is running.');
    } finally {
        showLoading(false);
    }
}

// Step 2: Handle File Selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById('fileName').textContent = `Selected: ${file.name}`;
        document.getElementById('uploadBtn').disabled = false;
        
        // Preview the file
        const reader = new FileReader();
        reader.onload = function(e) {
            const csv = e.target.result;
            previewCSV(csv);
        };
        reader.readAsText(file);
    }
}

function previewCSV(csv) {
    const lines = csv.split('\n').slice(0, 6); // Header + 5 rows
    const previewDiv = document.getElementById('dataPreview');
    
    if (lines.length < 2) {
        previewDiv.innerHTML = '<p>Invalid CSV file</p>';
        return;
    }
    
    let html = '<h3>Data Preview</h3><table>';
    
    lines.forEach((line, index) => {
        const cells = line.split(',');
        html += '<tr>';
        cells.forEach(cell => {
            if (index === 0) {
                html += `<th>${cell.trim()}</th>`;
            } else {
                html += `<td>${cell.trim()}</td>`;
            }
        });
        html += '</tr>';
    });
    
    html += '</table>';
    previewDiv.innerHTML = html;
}

async function uploadData() {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a CSV file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/upload-data`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            sessionData.rawData = result.data_info;
            await preprocessData();
        } else {
            alert('Failed to upload data: ' + result.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error uploading data');
    } finally {
        showLoading(false);
    }
}

// Step 3: Preprocess Data
async function preprocessData() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/preprocess`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            sessionData.preprocessedData = result.preprocessing_report;
            displayPreprocessingReport(result.preprocessing_report);
            goToStep(3);
        } else {
            alert('Preprocessing failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error during preprocessing');
    } finally {
        showLoading(false);
    }
}

function displayPreprocessingReport(report) {
    const container = document.getElementById('preprocessingReport');
    
    let html = '<div class="report-section">';
    html += '<h3>📊 Preprocessing Report</h3>';
    
    // Steps performed
    if (report.steps_performed && report.steps_performed.length > 0) {
        html += '<div class="success-box">';
        html += '<h4>✅ Steps Performed:</h4><ul>';
        report.steps_performed.forEach(step => {
            html += `<li>${step}</li>`;
        });
        html += '</ul></div>';
    }
    
    // Issues found
    if (report.issues_found && report.issues_found.length > 0) {
        html += '<div class="warning-box">';
        html += '<h4>⚠️ Issues Found and Fixed:</h4><ul>';
        report.issues_found.forEach(issue => {
            html += `<li>${issue}</li>`;
        });
        html += '</ul></div>';
    }
    
    // Data quality
    if (report.data_quality) {
        html += '<div class="info-box">';
        html += '<h4>📈 Data Quality:</h4>';
        html += `<p>Completeness: ${(report.data_quality.completeness * 100).toFixed(1)}%</p>`;
        html += `<p>Numeric Features: ${report.data_quality.numeric_features}</p>`;
        html += `<p>Categorical Features: ${report.data_quality.categorical_features}</p>`;
        html += '</div>';
    }
    
    html += '</div>';
    container.innerHTML = html;
}

// Step 4: Perform EDA
async function performEDA() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/eda`);
        const result = await response.json();
        
        if (result.status === 'success') {
            sessionData.edaResults = result.eda_results;
            displayEDAResults(result.eda_results);
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

function displayEDAResults(results) {
    const container = document.getElementById('edaResults');
    
    let html = '<div class="report-section">';
    html += '<h3>📊 Exploratory Data Analysis Results</h3>';
    
    // Key observations
    if (results.key_observations && results.key_observations.length > 0) {
        html += '<div class="info-box">';
        html += '<h4>🔍 Key Observations:</h4><ul>';
        results.key_observations.forEach(obs => {
            html += `<li>${obs}</li>`;
        });
        html += '</ul></div>';
    }
    
    // Statistical summary
    if (results.statistical_summary) {
        html += '<h4>Statistical Summary:</h4>';
        html += '<div style="overflow-x: auto;">';
        html += '<table style="width: 100%; border-collapse: collapse;">';
        html += '<tr><th>Feature</th><th>Mean</th><th>Median</th><th>Std Dev</th><th>Min</th><th>Max</th></tr>';
        
        for (const [feature, stats] of Object.entries(results.statistical_summary)) {
            if (typeof stats === 'object' && 'mean' in stats) {
                html += `<tr>
                    <td><strong>${feature}</strong></td>
                    <td>${stats.mean.toFixed(2)}</td>
                    <td>${stats.median.toFixed(2)}</td>
                    <td>${stats.std.toFixed(2)}</td>
                    <td>${stats.min.toFixed(2)}</td>
                    <td>${stats.max.toFixed(2)}</td>
                </tr>`;
            }
        }
        html += '</table></div>';
    }
    
    // Correlations
    if (results.correlation_analysis && results.correlation_analysis.strong_correlations) {
        const strongCorrs = results.correlation_analysis.strong_correlations;
        if (strongCorrs.length > 0) {
            html += '<h4>Strong Correlations:</h4><ul>';
            strongCorrs.forEach(corr => {
                html += `<li>${corr.feature1} ↔ ${corr.feature2}: ${corr.correlation.toFixed(3)} (${corr.strength})</li>`;
            });
            html += '</ul>';
        }
    }
    
    html += '</div>';
    container.innerHTML = html;
    
    // Prepare feature selection
    if (sessionData.rawData && sessionData.rawData.column_names) {
        prepareFeatureSelection(sessionData.rawData.column_names);
    }
}

// Step 5: Feature Selection
function prepareFeatureSelection(columns) {
    const featureDiv = document.getElementById('featureSelection');
    const targetSelect = document.getElementById('targetColumn');
    
    // Clear existing
    featureDiv.innerHTML = '';
    targetSelect.innerHTML = '';
    
    // Add checkboxes for features
    columns.forEach(col => {
        const label = document.createElement('label');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = col;
        checkbox.checked = true;
        
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(col));
        featureDiv.appendChild(label);
    });
    
    // Add options for target
    columns.forEach(col => {
        const option = document.createElement('option');
        option.value = col;
        option.textContent = col;
        targetSelect.appendChild(option);
    });
}

// Step 6: Train Model
async function trainModel() {
    // Get selected features
    const checkboxes = document.querySelectorAll('#featureSelection input:checked');
    const features = Array.from(checkboxes).map(cb => cb.value);
    const target = document.getElementById('targetColumn').value;
    
    if (features.length === 0) {
        alert('Please select at least one feature');
        return;
    }
    
    if (features.includes(target)) {
        alert('Target column cannot be a feature. Please uncheck it from features.');
        return;
    }
    
    sessionData.selectedFeatures = features;
    sessionData.targetColumn = target;
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/train-model`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                data: {},
                features: features,
                target: target
            })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            sessionData.modelResults = result.model_results;
            displayModelResults(result.model_results);
            goToStep(6);
        } else {
            alert('Model training failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error training model');
    } finally {
        showLoading(false);
    }
}

function displayModelResults(results) {
    const container = document.getElementById('modelResults');
    
    let html = '<div class="report-section">';
    html += '<h3>🤖 Model Training Results</h3>';
    
    // Best model
    html += `<div class="success-box">`;
    html += `<h4>🏆 Best Model: ${results.best_model}</h4>`;
    html += `<p>Accuracy: ${(results.best_score * 100).toFixed(2)}%</p>`;
    html += '</div>';
    
    // Model comparison
    if (results.comparison) {
        html += '<h4>Model Comparison:</h4>';
        html += '<div style="overflow-x: auto;">';
        html += '<table style="width: 100%; border-collapse: collapse;">';
        html += '<tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1 Score</th></tr>';
        
        results.comparison.forEach(model => {
            html += `<tr>
                <td><strong>${model.model}</strong></td>
                <td>${(model.accuracy * 100).toFixed(2)}%</td>
                <td>${(model.precision * 100).toFixed(2)}%</td>
                <td>${(model.recall * 100).toFixed(2)}%</td>
                <td>${(model.f1_score * 100).toFixed(2)}%</td>
            </tr>`;
        });
        html += '</table></div>';
    }
    
    // Interpretation
    if (results.interpretation) {
        html += '<div class="info-box">';
        html += `<h4>📝 Interpretation:</h4>`;
        html += `<p>${results.interpretation.summary}</p>`;
        html += `<p><strong>Confidence Level:</strong> ${results.interpretation.confidence_level}</p>`;
        html += `<p><strong>Reliability:</strong> ${results.interpretation.reliability}</p>`;
        html += '</div>';
    }
    
    html += '</div>';
    container.innerHTML = html;
}

// Step 7: Generate Explanations
async function generateExplanations() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/explain`);
        const result = await response.json();
        
        if (result.status === 'success') {
            sessionData.explanations = result.explanations;
            displayExplanations(result.explanations);
            goToStep(7);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating explanations');
    } finally {
        showLoading(false);
    }
}

function displayExplanations(explanations) {
    const container = document.getElementById('xaiResults');
    
    let html = '<div class="report-section">';
    html += '<h3>🔍 Explainable AI - Understanding the Model</h3>';
    
    // Natural language summary
    if (explanations.natural_language_summary) {
        html += '<div class="success-box">';
        html += `<h4>📝 Summary:</h4>`;
        html += `<p>${explanations.natural_language_summary}</p>`;
        html += '</div>';
    }
    
    // Feature importance
    if (explanations.feature_importance && explanations.feature_importance.ranked_features) {
        html += '<h4>📊 Feature Importance:</h4>';
        html += '<ul class="feature-list">';
        
        explanations.feature_importance.ranked_features.forEach((item, index) => {
            const percentage = item.percentage || (item.abs_coefficient * 10);
            html += `<li>
                <span><strong>#${index + 1}</strong> ${item.feature}</span>
                <div style="flex: 1; margin: 0 15px;">
                    <div class="feature-importance-bar" style="width: ${percentage}%;"></div>
                </div>
                <span>${percentage.toFixed(1)}%</span>
            </li>`;
        });
        html += '</ul>';
    }
    
    // Decision rules
    if (explanations.decision_rules && explanations.decision_rules.rules_text) {
        html += '<h4>📜 Decision Rules:</h4>';
        html += '<div class="info-box"><pre style="overflow-x: auto;">';
        explanations.decision_rules.rules_text.slice(0, 15).forEach(rule => {
            html += rule + '\n';
        });
        html += '</pre></div>';
    }
    
    // Sample predictions
    if (explanations.prediction_explanations && explanations.prediction_explanations.length > 0) {
        html += '<h4>🎯 Sample Prediction Explanations:</h4>';
        explanations.prediction_explanations.slice(0, 3).forEach(pred => {
            const statusClass = pred.correct ? 'success-box' : 'warning-box';
            html += `<div class="${statusClass}">`;
            html += `<p><strong>Instance ${pred.instance}:</strong> ${pred.explanation_text}</p>`;
            html += `<p>Confidence: ${(pred.confidence * 100).toFixed(1)}%</p>`;
            html += '</div>';
        });
    }
    
    html += '</div>';
    container.innerHTML = html;
}

// Step 8: Generate Recommendations
async function generateRecommendations() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/recommendations`);
        const result = await response.json();
        
        if (result.status === 'success') {
            sessionData.recommendations = result.recommendations;
            displayRecommendations(result.recommendations);
            goToStep(8);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating recommendations');
    } finally {
        showLoading(false);
    }
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    
    let html = '<div class="report-section">';
    
    // Primary recommendation
    const primary = recommendations.primary_recommendation;
    html += '<div class="recommendation-card">';
    html += `<h3>💡 ${primary.title}</h3>`;
    html += `<p style="font-size: 1.2em; margin: 15px 0;">${primary.reasoning}</p>`;
    html += `<div class="metric-card">`;
    html += `<div class="label">Confidence Score</div>`;
    html += `<div class="value">${primary.confidence_score.toFixed(1)}%</div>`;
    html += `</div>`;
    html += `<p><strong>Recommended Action:</strong> ${primary.recommended_action}</p>`;
    html += `<p><strong>Priority:</strong> ${primary.priority}</p>`;
    html += '</div>';
    
    // Alternative options
    html += '<h3>🔄 Alternative Options:</h3>';
    recommendations.alternative_options.forEach((alt, index) => {
        html += '<div class="alternative-option">';
        html += `<h4>Option ${index + 1}: ${alt.option}</h4>`;
        html += `<p>${alt.description}</p>`;
        html += `<p><strong>Rationale:</strong> ${alt.rationale}</p>`;
        html += `<p><strong>When to use:</strong> ${alt.when_to_use}</p>`;
        html += `<p><strong>Confidence:</strong> ${alt.confidence.toFixed(1)}%</p>`;
        html += '</div>';
    });
    
    // Decision factors
    if (recommendations.decision_factors) {
        html += '<h4>🎯 Key Decision Factors:</h4>';
        html += '<table style="width: 100%; border-collapse: collapse;">';
        html += '<tr><th>Rank</th><th>Factor</th><th>Importance</th><th>Impact</th></tr>';
        recommendations.decision_factors.forEach(factor => {
            html += `<tr>
                <td>${factor.rank}</td>
                <td>${factor.factor}</td>
                <td>${factor.importance}</td>
                <td>${factor.impact}</td>
            </tr>`;
        });
        html += '</table>';
    }
    
    // Risks
    if (recommendations.risks_and_limitations) {
        html += '<div class="warning-box">';
        html += '<h4>⚠️ Risks and Limitations:</h4><ul>';
        recommendations.risks_and_limitations.forEach(risk => {
            html += `<li>${risk}</li>`;
        });
        html += '</ul></div>';
    }
    
    // Human considerations
    if (recommendations.human_considerations) {
        html += '<div class="info-box">';
        html += '<h4>👤 Human Considerations:</h4><ul>';
        recommendations.human_considerations.forEach(consideration => {
            html += `<li>${consideration}</li>`;
        });
        html += '</ul></div>';
    }
    
    html += '</div>';
    container.innerHTML = html;
}

// Step 9: Validation
let selectedValidation = null;

function selectValidation(decision) {
    selectedValidation = decision;
    
    // Update button styles
    document.querySelectorAll('.validation-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    event.target.classList.add('selected');
    
    // Show/hide modify section
    const modifySection = document.getElementById('modifySection');
    if (decision === 'modify') {
        modifySection.style.display = 'block';
    } else {
        modifySection.style.display = 'none';
    }
}

async function submitValidation() {
    if (!selectedValidation) {
        alert('Please select a validation option');
        return;
    }
    
    const feedback = {
        decision: selectedValidation,
        comments: document.getElementById('validationComments').value,
        confidence: parseInt(document.getElementById('confidenceSlider').value)
    };
    
    if (selectedValidation === 'modify') {
        feedback.modified_recommendation = document.getElementById('modifiedRec').value;
    }
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/validate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(feedback)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            sessionData.validation = result.validation_result;
            await getQualityMetrics();
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error submitting validation');
    } finally {
        showLoading(false);
    }
}

// Step 10: Quality Metrics
async function getQualityMetrics() {
    try {
        const response = await fetch(`${API_BASE}/decision-quality`);
        const result = await response.json();
        
        if (result.status === 'success') {
            sessionData.qualityMetrics = result.quality_metrics;
            displayQualityMetrics(result.quality_metrics);
            goToStep(10);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error getting quality metrics');
    }
}

function displayQualityMetrics(metrics) {
    const container = document.getElementById('qualityMetrics');
    
    let html = '<div class="report-section">';
    html += '<h3>📊 Decision Quality Evaluation</h3>';
    
    // Quality gauges
    html += '<div class="quality-gauge">';
    
    // Clarity
    const clarityClass = metrics.clarity.score >= 80 ? 'gauge-high' : 
                        metrics.clarity.score >= 60 ? 'gauge-moderate' : 'gauge-low';
    html += `<div class="gauge">
        <div class="gauge-circle ${clarityClass}">
            <div>${metrics.clarity.score.toFixed(0)}%</div>
            <div style="font-size: 0.4em;">Clarity</div>
        </div>
        <h4>Clarity</h4>
        <p>${metrics.clarity.description}</p>
        <p><strong>${metrics.clarity.assessment}</strong></p>
    </div>`;
    
    // Confidence
    const confidenceClass = metrics.confidence.score >= 80 ? 'gauge-high' : 
                           metrics.confidence.score >= 60 ? 'gauge-moderate' : 'gauge-low';
    html += `<div class="gauge">
        <div class="gauge-circle ${confidenceClass}">
            <div>${metrics.confidence.score.toFixed(0)}%</div>
            <div style="font-size: 0.4em;">Confidence</div>
        </div>
        <h4>User Confidence</h4>
        <p>${metrics.confidence.description}</p>
        <p><strong>${metrics.confidence.assessment}</strong></p>
    </div>`;
    
    // Trust
    const trustClass = metrics.trust.score >= 80 ? 'gauge-high' : 
                      metrics.trust.score >= 60 ? 'gauge-moderate' : 'gauge-low';
    html += `<div class="gauge">
        <div class="gauge-circle ${trustClass}">
            <div>${metrics.trust.score.toFixed(0)}%</div>
            <div style="font-size: 0.4em;">Trust</div>
        </div>
        <h4>System Trust</h4>
        <p>${metrics.trust.description}</p>
        <p><strong>${metrics.trust.assessment}</strong></p>
    </div>`;
    
    html += '</div>';
    
    // Decision summary
    const summary = metrics.decision_summary;
    html += '<div class="success-box">';
    html += '<h4>✅ Decision Summary:</h4>';
    html += `<p><strong>Your Action:</strong> ${summary.user_action.toUpperCase()}</p>`;
    html += `<p><strong>Recommendation Followed:</strong> ${summary.recommendation_followed ? 'Yes' : 'No'}</p>`;
    html += `<p><strong>Model Used:</strong> ${summary.system_model}</p>`;
    html += `<p><strong>Model Accuracy:</strong> ${summary.model_accuracy.toFixed(2)}%</p>`;
    html += '</div>';
    
    html += '<div class="info-box">';
    html += '<h4>🎓 Research Insights:</h4>';
    html += '<p>This decision intelligence system successfully demonstrates:</p>';
    html += '<ul>';
    html += '<li>✓ Classical ML with interpretable models (Decision Tree, Logistic Regression)</li>';
    html += '<li>✓ Explainable AI with feature importance and decision rules</li>';
    html += '<li>✓ Human-in-the-loop validation maintaining human control</li>';
    html += '<li>✓ Domain-independent design for any structured decision problem</li>';
    html += '<li>✓ Quality metrics for continuous improvement</li>';
    html += '</ul>';
    html += '</div>';
    
    html += '</div>';
    container.innerHTML = html;
}

// Utility functions
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'flex' : 'none';
}

function resetSystem() {
    if (confirm('Are you sure you want to start a new decision process? All current data will be cleared.')) {
        // Reset state
        sessionData = {
            context: null,
            rawData: null,
            preprocessedData: null,
            edaResults: null,
            selectedFeatures: [],
            targetColumn: null,
            modelResults: null,
            explanations: null,
            recommendations: null,
            validation: null,
            qualityMetrics: null
        };
        
        selectedValidation = null;
        
        // Reset forms
        document.getElementById('decisionDescription').value = '';
        document.getElementById('domain').value = '';
        document.getElementById('csvFile').value = '';
        document.getElementById('fileName').textContent = '';
        document.getElementById('validationComments').value = '';
        document.getElementById('confidenceSlider').value = 5;
        
        // Go to step 1
        goToStep(1);
    }
}

// Auto-perform EDA when reaching step 4
window.addEventListener('load', function() {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.target.id === 'step4' && mutation.target.classList.contains('active')) {
                if (sessionData.preprocessedData && !sessionData.edaResults) {
                    performEDA();
                }
            }
        });
    });
    
    const step4 = document.getElementById('step4');
    if (step4) {
        observer.observe(step4, { attributes: true, attributeFilter: ['class'] });
    }
});
