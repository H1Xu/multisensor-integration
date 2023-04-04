import json
import requests
from homeassistant.const import(
    CONF_ID
)

class SensorID:
    def __init__(self, name, id):
        self._name = name
        self._id = id
        self._data = None
        self._error = None  
        try:
            response = requests.get(f"https://api.example.com/sensors/")
            response.raise_for_status()
            self._data = response.json()
        except requests.exceptions.RequestException as exc:
            self._error = f"Error occurred while fetching data: {exc}"
    
    def GetData(self):
        return self._data
    
    def GetError(self):
        return self._error