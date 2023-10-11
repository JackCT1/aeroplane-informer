import requests


class APIError(Exception):
    """Describes an error triggered by a failing API call."""

    def __init__(self, message: str, code: int = 500):
        """Creates a new APIError instance."""
        self.message = message
        self.code = code


def print_data(country_data: dict):
    """Displays country data from a dict."""
    currency_data = list(country_data[0]["currencies"].values())
    print(f'Country: {country_data[0]["name"]["common"]}')
    print(f'Capital: {country_data[0]["capital"][0]}')
    print(f"Currency: {currency_data[0]['name']}")


def fetch_data(country_name: str) -> dict:
    """Returns a dict of country data from the API."""
    response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
    json = response.json()
    return json


def main():
    """Repeatedly prompts the user for country names and displays the result."""
    print(" ")
    print("####################")
    print("Welcome to the REST Countries Searcher")
    print("####################")
    print(" ")

    while 1:
        entry = input("Search for a country: ")
        print(f"You searched for: {entry}")
        print("Fetching...")
        print(" ")
        try:
            country_data = fetch_data(entry)
            print_data(country_data)
        except APIError as e:
            print(e.message)
        print(" ")


if __name__ == "__main__":
    main()
