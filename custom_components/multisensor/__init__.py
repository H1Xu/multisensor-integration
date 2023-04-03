from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
#import objects from home assistant

from .const import Platform
#import Platform constant from const file

import logging
#record all activities carried by this project
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass:HomeAssistant, entry: ConfigEntry):
    #Set up for VTEC multisensor plugin working
    #hass as object contains all status and service of HA
    #config_entry as the admin for all control configuration ports

    await hass.config_entries.async_forward_entry_setups(entry, Platform)
    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True
    #async function as one method to install and unistall to configure admin
    #async_forward will handle all resources to keep plugin running
    #return true to show it has been correctly set up
    #entry.async is only called when uninstalling and delete all resources

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    #listen to all updating versions
    await hass.config_entries.async_reload(entry.entry_id)
    #reload the configuration that plugins will work after updates

