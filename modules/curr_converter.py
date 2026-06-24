import requests

def convert_currency(from_currency, to_currency, amount):
    try:

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        url = (
            f"https://api.frankfurter.app/latest"
            f"?from={from_currency}&to={to_currency}"
        )

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        if "rates" not in data:
            return None

        if to_currency not in data["rates"]:
            return None

        rate = data["rates"][to_currency]

        converted_amount = amount * rate

        return round(converted_amount, 2)

    except Exception as e:
        print("Currency Conversion Error:", e)
        return None