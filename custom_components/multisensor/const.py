from homeassistant.const import(
    PLATFORM
)

from homeassistant.components.sensor import SensorDeviceClass

DOMAIN = "multisensor"

DEFAULT_NAME = "VTEC"

SENSOR_ID = "Sensor ID"

Platform = [PLATFORM.SENSOR]



SENSOR = {
    'pm10': ['Particulate matter(PM10)']
}