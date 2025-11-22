import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
from financial_analyzer import FinancialAnalyzer

def verify_improvement():
    print("Initializing Financial Analyzer with IMPROVED training logic...")
    analyzer = FinancialAnalyzer()
    
    print("Generating synthetic test data using the SAME logic...")
    np.random.seed(100) # Different seed
    n_samples = 200
    
    # Features
    X_test = np.random.rand(n_samples, 5)
    X_test[:, 0] = np.random.randint(18, 70, n_samples)  # age
    X_test[:, 1] = np.random.uniform(30000, 200000, n_samples)  # income
    X_test[:, 2] = np.random.uniform(20000, 150000, n_samples)  # expenses
    X_test[:, 3] = np.random.uniform(5000, 100000, n_samples)  # savings
    X_test[:, 4] = np.random.uniform(0, 1, n_samples)  # risk_tolerance
    
    # Replicate the new ground truth logic
    norm_age = (X_test[:, 0] - 18) / (70 - 18)
    norm_income = (X_test[:, 1] - 30000) / (200000 - 30000)
    norm_savings = (X_test[:, 3] - 5000) / (100000 - 5000)
    risk_tol = X_test[:, 4]
    
    base_risk = (risk_tol * 0.5) + ((1 - norm_age) * 0.3) + ((norm_income + norm_savings)/2 * 0.2)
    y_risk_true = np.clip(base_risk + np.random.normal(0, 0.05, n_samples), 0, 1)
    y_return_true = 0.03 + (y_risk_true * 0.12) + np.random.normal(0, 0.01, n_samples)
    
    print("\nEvaluating Risk Model...")
    y_risk_pred = analyzer.risk_model.predict(X_test)
    r2_risk = r2_score(y_risk_true, y_risk_pred)
    print(f"Risk Model R2: {r2_risk:.4f}")
    
    print("\nEvaluating Return Model...")
    y_return_pred = analyzer.return_model.predict(X_test)
    r2_return = r2_score(y_return_true, y_return_pred)
    print(f"Return Model R2: {r2_return:.4f}")
    
    if r2_risk > 0.8 and r2_return > 0.7:
        print("\nSUCCESS: Models are now highly accurate!")
    else:
        print("\nWARNING: Accuracy is still lower than expected.")

if __name__ == "__main__":
    verify_improvement()
