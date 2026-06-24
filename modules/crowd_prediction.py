import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

model = joblib.load(
    os.path.join(
        BASE_DIR,
        "crowd_prediction_model.pkl"
    )
)

encoders = joblib.load(
    os.path.join(
        BASE_DIR,
        "crowd_encoders.pkl"
    )
)

target_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "crowd_target_encoder.pkl"
    )
)


def get_dropdown_options():

    options = {}

    for column, encoder in encoders.items():

        options[column] = list(
            encoder.classes_
        )

    return options


def predict_crowd_level(input_data):

    try:

        encoded_data = {}

        for column, value in input_data.items():

            if column in encoders:

                encoded_data[column] = (
                    encoders[column]
                    .transform([value])[0]
                )

            else:

                encoded_data[column] = value

        df = pd.DataFrame(
            [encoded_data]
        )

        prediction = model.predict(
            df
        )[0]

        crowd_level = (
            target_encoder
            .inverse_transform(
                [prediction]
            )[0]
        )

        return crowd_level

    except Exception as e:

        print(
            "Crowd Prediction Error:",
            e
        )

        return None