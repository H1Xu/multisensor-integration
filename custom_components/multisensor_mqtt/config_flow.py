import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME

from .const import (
    CONF_BROKER_HOST,
    CONF_BROKER_PASSWORD,
    CONF_BROKER_PORT,
    CONF_BROKER_USERNAME,
    DOMAIN,
)

class ThermiqMQTTFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Thermiq MQTT config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize the Thermiq MQTT flow."""
        self.broker_host = None
        self.broker_port = None
        self.broker_username = None
        self.broker_password = None

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            # Validate the user input
            try:
                await self._validate_input(user_input)
            except vol.Invalid as exc:
                errors[CONF_BROKER_HOST] = str(exc)

            if not errors:
                # Input is valid, create the config entry
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data={
                        CONF_BROKER_HOST: user_input[CONF_BROKER_HOST],
                        CONF_BROKER_PORT: user_input.get(CONF_BROKER_PORT),
                        CONF_BROKER_USERNAME: user_input.get(CONF_BROKER_USERNAME),
                        CONF_BROKER_PASSWORD: user_input.get(CONF_BROKER_PASSWORD),
                    },
                )

        # Show the configuration form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_BROKER_HOST): str,
                    vol.Optional(CONF_BROKER_PORT, default=1883): int,
                    vol.Optional(CONF_BROKER_USERNAME): str,
                    vol.Optional(CONF_BROKER_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    async def _validate_input(self, user_input):
        """Validate the user input."""
        broker_host = user_input.get(CONF_BROKER_HOST)
        broker_port = user_input.get(CONF_BROKER_PORT)
        broker_username = user_input.get(CONF_BROKER_USERNAME)
        broker_password = user_input.get(CONF_BROKER_PASSWORD)

        if not broker_host:
            raise vol.Invalid("Missing broker host.")

        if broker_port is not None and (broker_port < 1 or broker_port > 65535):
            raise vol.Invalid("Invalid broker port.")

        self.broker_host = broker_host
        self.broker_port = broker_port
        self.broker_username = broker_username
        self.broker_password = broker_password
