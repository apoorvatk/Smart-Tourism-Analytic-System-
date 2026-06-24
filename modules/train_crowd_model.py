import os
import joblib
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from xgboost import XGBClassifier


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "tourism_recommendation_5000.csv"
    )
)

data = pd.read_csv(csv_path)

data["crowd_score"] = (
    data["popularity_score"] * 0.5 +
    data["rating"] * 0.3 +
    data["safety_score"] * 0.2
)


def assign_crowd(score):

    if score >= 8:
        return "High"

    elif score >= 6.5:
        return "Medium"

    else:
        return "Low"


data["crowd_level"] = data["crowd_score"].apply(
    assign_crowd
)

X = data.drop(
    [
        "destination_id",
        "name",
        "crowd_level",
        "crowd_score"
    ],
    axis=1
)

y = data["crowd_level"]

encoders = {}

for col in X.select_dtypes(include="object").columns:

    encoder = LabelEncoder()

    X[col] = encoder.fit_transform(
        X[col]
    )

    encoders[col] = encoder

target_encoder = LabelEncoder()

y = target_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("Accuracy:", accuracy)

print(
    classification_report(
        y_test,
        y_pred
    )
)

joblib.dump(
    model,
    os.path.join(
        BASE_DIR,
        "crowd_prediction_model.pkl"
    )
)

joblib.dump(
    encoders,
    os.path.join(
        BASE_DIR,
        "crowd_encoders.pkl"
    )
)

joblib.dump(
    target_encoder,
    os.path.join(
        BASE_DIR,
        "crowd_target_encoder.pkl"
    )
)

print("Crowd Prediction Files Saved Successfully")
