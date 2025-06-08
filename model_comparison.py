
# extended_model_comparison.py
# ---------------------------------------------------------
# Este script compara varios modelos de clasificación usando
# validación cruzada y visualiza los resultados.
# ---------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

from model_preprocessing import load_cleaned_data, split_and_process

# Paso 1: Cargar y preprocesar datos
X, y = load_cleaned_data("data/cleaned_dataset.csv")
X_train, X_test, y_train, y_test = split_and_process(X, y, scale=True, balance=True)

# Paso 2: Definir los modelos a comparar
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC()
}

# Paso 3: Evaluar con validación cruzada (F1-score)
results = {}
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    results[name] = scores
    print(f"{name}: F1 mean={scores.mean():.3f}, std={scores.std():.3f}")

# Paso 4: Visualizar los resultados con boxplot
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
plt.title("Comparación de modelos por F1-score (5-Fold CV)", fontsize=14)
sns.boxplot(data=pd.DataFrame(results))
plt.ylabel("F1-score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Paso 5: Conclusión en consola
best_model = max(results.items(), key=lambda x: x[1].mean())
print(f"\n👉 El mejor modelo por media de F1-score es: {best_model[0]} ({best_model[1].mean():.3f})")
