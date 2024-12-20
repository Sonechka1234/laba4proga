import random
import requests

from models import CountryInfo

class CountyAPI:
    def fetch_country_info(self, country_name: str) -> CountryInfo:
        url = f"https://restcountries.com/v3.1/translation/{country_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                country = data[0]
                return CountryInfo(
                    name=country.get("name", {}).get("common", "Unknown"),
                    capital=country.get("capital", ["Unknown"])[0],
                    region=country.get("region", "Unknown"),
                    area=country.get("area", 0),
                    population=f"{country.get('population', 0):,}",
                    maps_url=country.get("maps", {}).get("googleMaps", "No URL available")
                )
        return None

    def fetch_random_country_info(self) -> CountryInfo:
        url = "https://restcountries.com/v3.1/region/Europe"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                country = random.choice(data)
                return CountryInfo(
                    name=country.get("name", {}).get("common", "Unknown"),
                    capital=country.get("capital", ["Unknown"])[0],
                    region=country.get("region", "Unknown"),
                    area=country.get("area", 0),
                    population=f"{country.get('population', 0):,}",
                    maps_url=country.get("maps", {}).get("googleMaps", "No URL available")
                ) 
        return None