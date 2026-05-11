"""Config flow for Home Memory."""
import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "home_memory"

class HomeMemoryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Home Memory."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            return self.async_create_entry(title="Home Memory", data={})
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )
