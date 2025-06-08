
# modeling/model_preprocessing.py
# ---------------------------------------------
# Este módulo carga el dataset limpio (ya codificado),
# separa X e y, aplica train/test split,
# y opcionalmente escalado y SMOTE.
# ---------------------------------------------

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def load_cleaned_data(path="data/cleaned_dataset.csv", target="stroke"):
    '''
    Carga el dataset limpio, separa X e y, y devuelve ambos.
    '''
    df = pd.read_csv(path)
    X = df.drop(columns=[target])
    y = df[target]
    return X, y

def split_and_process(X, y, scale=True, balance=True, test_size=0.2, random_state=42):
    '''
    Divide en train/test. Aplica escalado si se desea.
    Aplica SMOTE si se desea. Devuelve todo.
    '''
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    if scale:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    if balance:
        smote = SMOTE(random_state=random_state)
        X_train, y_train = smote.fit_resample(X_train, y_train)

    return X_train, X_test, y_train, y_test
