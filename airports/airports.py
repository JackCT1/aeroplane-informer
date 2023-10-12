import json
import requests
from rich.prompt import Prompt
from rich.console import Console

# Instead of using print(), you should use the Console from Rich instead.
console = Console()


def get_search() -> str:
    return Prompt.ask("Search for an an airport")


def load_airport_JSON() -> list:
    """Load airport data from airports.json"""
    f = open("airports.json")
    airport_data = json.load(f)
    return airport_data


def find_airports_from_name(name: str, airport_data: list) -> list:
    """
    Find an airport from the airportData given a name
    Could return one or more airport objects
    """
    airportResults = [
        airport
        for airport in airport_data
        if name.lower() in str(airport["name"]).lower()
    ]
    if len(airportResults) == 0:
        return "No airports match your search"
    elif len(airportResults) == 1:
        return airportResults
    else:
        possibleChoices = [airport for airport in airportResults]
        airportChoice = Prompt.ask(
            "Multiple airports found, please choose one: ", choices=possibleChoices
        )
        return airportChoice


def get_flights_from_iata(iata: str, airport_data: list) -> list:
    """Given an IATA get the flights that are departing from that airport from Airlabs"""
    airport = [airport for airport in airport_data if str(iata) in str(airport["iata"])]
    return airport


def load_weather_for_location(lat: str, lng: str) -> dict:
    """Given a location, load the current weather for that location"""

    return {}


def render_flights(flights: list) -> None:
    """Render a list of flights to the console using the Rich Library

    Consider using Panels, Grids, Tables or any of the more advanced
    features of the library"""

    console.print(flights)


def find_airport_from_iata(iata: str, airport_data: list) -> dict:
    """
    Find an airport from the airport_data given a name
    Should return exactly one airport object
    """

    return {}


def main():
    console.print(" ")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print("Welcome to the Airports Informer Tool")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print(" ")

    airport_data = load_airport_JSON()
    while 1:
        airport_search = get_search()
        find_airports_from_name(airport_search, airport_data)


if __name__ == "__main__":
    main()
