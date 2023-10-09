import requests

response = requests.get("https://restcountries.com/v3.1/name/germany")
json = response.json()
print(json)
