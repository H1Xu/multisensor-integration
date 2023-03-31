from homeassistant import config_entries, core
#from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_NAME, CONF_METHOD, CONF_ID


from .const import DOMAIN, DEFAULT_NAME, SENSOR_ID

import voluptuous as vol


class MultisensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for multisensor integration"""

    VERSION = 1

    async def async_step_import(self, config: dict[str, Any]):
        """Import configuration from config.yaml"""
        name = config.get(CONF_NAME, DEFAULT_NAME)
        self._async_abort_entries_match({CONF_NAME:name})
        config[CONF_NAME] = name
        return await self.async_step_user(user_input = config)
    
    async def async_step_user(self, user_input: dict[str, Any]):
        """Handle the initial step"""
        if user_input is None:
            return self.async_show_form(
                step_id = "user"
            )
        if user_input[CONF_METHOD] == SENSOR_ID:
            return await self.async_validate_input()
    
    async def async_validate_input(self, user_input=None):
        """Validate the input"""
        errors = {}
        if user_input:
            id = user_input[CONF_ID]
            method = CONF_ID
            requester = SensorID(None, None, None, id, method)
        
        Validate = requester.GetData()
        if Validate:
            if Validate["status"] == "ok":
                if "status" in Validate["data"]:
                    if Validate["data"]["status"] == "error":
                        if Validate["data"]["msg"] == "Unknown ID":
                            errors["base"] = "unknow_sensor_id"
                        else:
                            errors["base"] = "server_error"
            elif Validate["status"] == "error"
                if Validate["data"] == "Invalid key"
                    errors["base"] = "invalid_key"
                else:
                    errors["base"] = "server_error"
            else:
                errors["base"] = "server_error"
        else:
            errors["base"] = "server_not_available"
        
        SensorName = requester.GetSensorName()
        name = user_input.get(CONF_NAME, SensorName)

        if not errors:
            await self.async_set_unique_id(name)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title = name,
                data={
                    CONF_ID: id
                    CONF_NAME: name
                }
            )
        
        return self.async_show_form

        




    