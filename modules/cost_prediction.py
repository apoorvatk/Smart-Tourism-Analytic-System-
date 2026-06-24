import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(
    os.path.join(
        BASE_DIR,
        "cost_prediction_model.pkl"
    )
)

meal_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "meal_encoder.pkl"
    )
)

market_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "market_encoder.pkl"
    )
)

customer_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "customer_encoder.pkl"
    )
)

MEAL_OPTIONS = list(meal_encoder.classes_)

MARKET_OPTIONS = list(market_encoder.classes_)

CUSTOMER_OPTIONS = list(customer_encoder.classes_)


def predict_trip_cost(
    lead_time,
    adults,
    children,
    babies,
    meal,
    market_segment,
    customer_type,
    total_nights,
    repeated_guest,
    booking_changes
):
    try:

        meal_encoded = meal_encoder.transform(
            [meal]
        )[0]

        market_encoded = market_encoder.transform(
            [market_segment]
        )[0]

        customer_encoded = customer_encoder.transform(
            [customer_type]
        )[0]

        input_df = pd.DataFrame(
            [[
                lead_time,
                adults,
                children,
                babies,
                meal_encoded,
                market_encoded,
                customer_encoded,
                total_nights,
                repeated_guest,
                booking_changes
            ]],
            columns=[
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
        )

        prediction = model.predict(
            input_df
        )[0]

        return round(
            prediction,
            2
        )

    except Exception as e:

        print(
            "Cost Prediction Error:",
            e
        )

        return None