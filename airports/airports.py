import json
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

# Instead of using print(), you should use the Console from Rich instead.
console = Console(record=True)
load_dotenv()
AIRLBAS_KEY = os.getenv("AIRLABS_KEY")


def get_search() -> str:
    return Prompt.ask("Search for an an airport")


def load_airport_JSON() -> list:
    """Load airport data from airports.json"""
    f = open("airports.json")
    airport_data = json.load(f)
    return airport_data


def getResults(name: str, data: list):
    return [airport for airport in data if name.lower() in str(airport["name"]).lower()]


def find_airports_from_name(name: str, airport_data: list) -> list:
    """
    Find an airport from the airportData given a name
    Could return one or more airport objects
    """

    airportResults = getResults(name, airport_data)

    while len(airportResults) == 0:
        airport_name = Prompt.ask("No airports match your search. Try again")
        airportResults = getResults(airport_name, airport_data)

    if len(airportResults) > 1:
        possibleChoices = [airport["name"] for airport in airportResults]
        airportChoice = Prompt.ask(
            "Multiple airports found, please choose one: ", choices=possibleChoices
        )
        airport_result = [
            airport
            for airport in airportResults
            if airportChoice.lower() in str(airport["name"]).lower()
        ]
        return airport_result
    return airportResults


def find_airport_from_iata(iata: str, airport_data: list) -> dict:
    """
    Find an airport from the airport_data given a name
    Should return exactly one airport object
    """
    for airport in airport_data:
        if str(iata) in str(airport["iata"]):
            return airport["name"]


def get_flights_from_iata(iata: str, airport_data: list) -> list:
    """Given an IATA get the flights that are departing from that airport from Airlabs"""
    response = requests.get(
        f"https://airlabs.co/api/v9/schedules?dep_iata={iata}&api_key={AIRLBAS_KEY}"
    )
    flight_info = response.json()["response"]
    departing_flights = []
    for flight in flight_info:
        destination_airport = find_airport_from_iata(flight["arr_iata"], airport_data)
        delayed_status = f"{flight['delayed']} minutes"
        if flight["delayed"] == None:
            delayed_status = "No"
        departing_flights.append(
            {
                "flight_iata": flight["flight_iata"],
                "dep_time_utc": flight["dep_time_utc"],
                # "arr_time_utc": flight["arr_time_utc"],
                "arr_airport": destination_airport,
                "delayed": delayed_status,
            }
        )
    return departing_flights


def load_weather_for_location(lat: str, lng: str) -> dict:
    """Given a location, load the current weather for that location"""

    return {}


def render_flights(flights: list) -> None:
    """Render a list of flights to the console using the Rich Library

    Consider using Panels, Grids, Tables or any of the more advanced
    features of the library"""
    table = Table(title="Flights")
    table.add_column("Flight Number", justify="center", style="blue")
    table.add_column("Departure Time", justify="center", style="blue")
    # table.add_column("Arrival Time", justify="center")
    table.add_column("Destination", justify="center", style="purple")
    table.add_column("Delayed?", justify="center", style="green")

    for flight in flights:
        table.add_row(
            flight["flight_iata"],
            flight["dep_time_utc"],
            # flight["arr_time_utc"],
            flight["arr_airport"],
            flight["delayed"],
        )

    console.print(table)
    console.save_html(str(datetime.now()) + ".html")


def main():
    console.print(" ")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print("Welcome to the Airports Informer Tool")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print(" ")

    airport_data = load_airport_JSON()
    while 1:
        airport_search = get_search()
        airport_iata = find_airports_from_name(airport_search, airport_data)[0]["iata"]
        flights = get_flights_from_iata(airport_iata, airport_data)
        render_flights(flights)


if __name__ == "__main__":
    main()
