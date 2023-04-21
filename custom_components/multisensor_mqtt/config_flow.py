"""Config flow for multisensor_mqtt."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for multisensor_mqtt."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_ASSUMED

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Validate the user input
            try:
                await validate_input(self.hass, user_input)
            except InvalidAuthError:
                return self.async_show_form(
                    step_id="user", errors={"base": "invalid_auth"}
                )
            except CannotConnectError:
                return self.async_show_form(
                    step_id="user", errors={"base": "cannot_connect"}
                )
            except Exception:
                return self.async_show_form(
                    step_id="user", errors={"base": "unknown"}
                )

            return self.async_create_entry(
                title=user_input[CONF_HOST], data=user_input
            )

        # Show the form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_PORT, default=1883): cv.positive_int,
                    vol.Required(CONF_USERNAME, default=""): str,
                    vol.Required(CONF_PASSWORD, default=""): str,
                }
            ),
            errors={},
        )


async def validate_input(hass, user_input):
    """Validate the user input allows us to connect."""
    host = user_input[CONF_HOST]
    port = user_input[CONF_PORT]
    username = user_input[CONF_USERNAME]
    password = user_input[CONF_PASSWORD]

    # Test the connection to the broker
    try:
        # This will raise an exception if we cannot connect to the broker
        async with aioMqtt(hass, host, port, username, password):
            pass
    except asyncio.TimeoutError:
        raise CannotConnectError
    except aioMqttException:
        raise InvalidAuthError


class CannotConnectError(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuthError(Exception):
    """Error to indicate there is invalid auth."""


class aioMqtt:
    """Home Assistant aioMqtt client wrapper."""

    def __init__(self, hass, host, port, username, password):
        """Initialize the client."""
        self.hass = hass
        self.client = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    async def __aenter__(self):
        """Async enter."""
        self.client = self.hass.components.mqtt.async_get_client(
            self.hass.data[DOMAIN]["mqtt_config"]
        )

        try:
            await self.client.connect()
        except:
            await self.client.disconnect()
            raise

        return self.client

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Async exit."""
        await self.client.disconnect()

