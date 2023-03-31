import json
import requests
from homeassistant.const import(
    CONF_ID
)

class SensorID(object):

    def __init__(self, id, lng, token, idx, method)