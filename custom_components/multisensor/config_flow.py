from homeassistant import config_entries, core
from homeassistant.const import CONF_NAME, CONF_METHOD, CONF_ID
#import constant from homeassistant
#config_entry and core is the key function of running home assistant

from typing import Any

from vtec_api import SensorID

from .const import DOMAIN, DEFAULT_NAME, SENSOR_ID
#import configuration name and id from .const

import voluptuous as vol
#verify and handle the configuration data


class MultisensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    #define a class inherited from config_entries.Configflow
    #handle config flow

    VERSION = 1
    #plugins version number

    async def async_step_import(self, config: dict[str, Any]):
        #import configuration from config.yaml
        name = config.get(CONF_NAME, DEFAULT_NAME)
        #get config name from file and use default name if there is no name

        self._async_abort_entries_match({CONF_NAME:name})
        #end the config sharing the same name

        config[CONF_NAME] = name
        return await self.async_step_user(user_input = config)
        #return input of users
    
    async def async_step_user(self, user_input: dict[str, Any]):
        #handle input of users

        if user_input is None:
            #give user one form to fill in
            return self.async_show_form(
                step_id = "users",
                data_schema = vol.Schema({
                    vol.Required(CONF_METHOD): str
                })
                #use vol to verify the data type
            )
        if user_input[CONF_METHOD] == SENSOR_ID:
            return await self.async_validate_input()
    
    async def async_validate_input(self, user_input=None):
        #validate the input of users
        errors = {}
        #create a new dic to record all errors
        if user_input:
            id = user_input[CONF_ID]
            method = CONF_ID
            requester = SensorID(None, None, None, id, method)
            #inside the brackets(name,device_class,icon,unique id,method)
            #id,method indicates the id and method to gather from input
        
        Validate = requester.GetData()
        if Validate:
            if Validate["status"] == "ok":
                if "status" in Validate["data"]:
                    if Validate["data"]["status"] == "error":
                        if Validate["data"]["msg"] == "Unknown ID":
                            errors["base"] = "unknow_sensor_id"
                        else:
                            errors["base"] = "server_error"
            elif Validate["status"] == "error":
                if Validate["data"] == "Invalid key":
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
                    CONF_ID: id,
                    CONF_NAME: name
                }
            )
        
        return self.async_show_form

        




    
