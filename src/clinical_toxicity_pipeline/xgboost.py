import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, average_precision_score, PrecisionRecallDisplay
import matplotlib.pyplot as plt

def run_xgboost(X, y):
    '''
    Trains and evaluates the XGBoost model
    Parameters
    ----------
    X : Feature matrix 
    y : labels
    '''
    print("Splitting data into train and test sets")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Training XGBoost Classifier")
    model = xgb.XGBClassifier(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=5, 
        random_state=42, 
        scale_pos_weight=30,
        eval_metric='logloss'
    )

    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    y_scores = model.predict_proba(X_test)[:,1]

    f1 = f1_score(y_test, y_pred)
    pr_auc = average_precision_score(y_test, y_scores)

    print("\nXGBoost Baseline Metrics\n")
    print(f"F1-Score:   {f1:.2f}")
    print(f"PR-AUC:     {pr_auc:.2f}")

    #Generate figures
    plt.figure(figsize=(8,6))
    display = PrecisionRecallDisplay.from_predictions(y_test, y_scores, name="XGBoost", color="darkorange")
    plt.title(f"Precision-Recall Curve (AUC = {pr_auc:.2f})")
    plt.grid(alpha=0.3)
    plt.savefig('pr_curve_xgboost_scaled.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Feature Importance Plot
    plt.figure(figsize=(8,6))
    xgb.plot_importance(model, importance_type='gain', xlabel='Gain', color='steelblue', show_values=False)
    plt.tight_layout()
    plt.savefig('feature_importance_xgboost_scaled.png', dpi=300)
    plt.close()

