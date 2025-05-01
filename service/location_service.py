from typing import List, Dict, Optional
import csv
from model.location import Location


class LocationService:
    def __init__(self):
        self.locations: Dict[str, Location] = {}

    def get_states(self) -> List[Location]:
        # Get all state locations (locations with no state_code)
        result = []
        for loc in self.locations.values():
            if loc.state_code is None:
                result.append(loc)
        return result

    def get_locations_by_state_code(self, state_code: str) -> List[Location]:
        # Get all locations from a specific state
        result = []
        for loc in self.locations.values():
            if loc.state_code == state_code:
                result.append(loc)
        return result

    def get_location_by_code(self, code: str) -> Optional[Location]:
        # Get a location by code
        return self.locations.get(code)

    def get_capitals(self) -> List[Location]:
        # Get all capitals locations
        result = []
        for loc in self.locations.values():
            if loc.is_capital:
                result.append(loc)
        return result

    def load_locations_from_csv(self, file_path: str) -> None:
        # Load locations from csv
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    location = Location(
                        code=row['code'],
                        description=row['description'],
                        state_code=row.get('state_code') if row.get('state_code') else None,
                        is_capital=row.get('is_capital', '').lower() == 'true'
                    )
                    self.locations[location.code] = location
        except Exception as e:
            print(f"Error loading locations from CSV: {e}")

