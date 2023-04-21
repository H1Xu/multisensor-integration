"""Config flow for ISENSIT integration."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN


class ISENSITFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a ISENSIT config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Skip validation
            return self.async_create_entry(title=user_input["sensor_id"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("sensor_id"): str}
            )
        )
