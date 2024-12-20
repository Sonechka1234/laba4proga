from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class CountryInfo:
    name: str
    capital: str
    region: str
    area: int
    population: int 
    maps_url: str
