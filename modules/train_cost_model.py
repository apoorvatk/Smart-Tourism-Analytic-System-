import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(BASE_DIR, "H1.csv")

data = pd.read_csv(csv_path)

print("Dataset Shape:", data.shape)




data["TotalNights"] = (
    data["StaysInWeekendNights"] +
    data["StaysInWeekNights"]
)

data["AccommodationCost"] = (
    data["ADR"] * data["TotalNights"]
)

data["FoodCost"] = (
    data["Adults"] *
    data["TotalNights"] *
    500
)

data["TransportationCost"] = (
    data["Adults"] * 1000
)

data["TripCost"] = (
    data["AccommodationCost"] +
    data["FoodCost"] +
    data["TransportationCost"]
)

data = data[data["TotalNights"] > 0]

print("After removing zero-night stays:", data.shape)



features = [
    "LeadTime",
    "Adults",
    "Children",
    "Babies",
    "Meal",
    "MarketSegment",
    "CustomerType",
    "TotalNights",
    "IsRepeatedGuest",
    "BookingChanges"
]

X = data[features].copy()
y = data["TripCost"]





meal_encoder = LabelEncoder()
market_encoder = LabelEncoder()
customer_encoder = LabelEncoder()

X["Meal"] = meal_encoder.fit_transform(X["Meal"])

X["MarketSegment"] = market_encoder.fit_transform(
    X["MarketSegment"]
)

X["CustomerType"] = customer_encoder.fit_transform(
    X["CustomerType"]
)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)




y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\nModel Performance")
print("-----------------")
print("MAE :", round(mae, 2))
print("MSE :", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R²  :", round(r2, 4))



joblib.dump(
    model,
    "cost_prediction_model.pkl"
)

joblib.dump(
    meal_encoder,
    "meal_encoder.pkl"
)

joblib.dump(
    market_encoder,
    "market_encoder.pkl"
)

joblib.dump(
    customer_encoder,
    "customer_encoder.pkl"
)

print("\nFiles Saved Successfully")
print("cost_prediction_model.pkl")
print("meal_encoder.pkl")
print("market_encoder.pkl")
print("customer_encoder.pkl")