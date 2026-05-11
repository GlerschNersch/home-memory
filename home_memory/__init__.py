"""Home Memory — AI narrative digest for Home Assistant."""
import logging
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.frontend import async_register_built_in_panel, async_remove_panel

_LOGGER = logging.getLogger(__name__)
DOMAIN = "home_memory"
PANEL_FILENAME = "home-memory-panel.html"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    frontend_path = Path(__file__).parent / "frontend"

    await hass.http.async_register_static_paths([
        StaticPathConfig(
            url_path="/home_memory_static",
            path=str(frontend_path),
            cache_headers=False,
        )
    ])

    async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="Home Memory",
        sidebar_icon="mdi:brain",
        frontend_url_path="home-memory",
        config={"url": "/home_memory_static/home-memory-panel.html"},
        require_admin=False,
    )

    _LOGGER.info("Home Memory: panel registered at /home_memory_static/%s", PANEL_FILENAME)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    async_remove_panel(hass, "home-memory")
    return True
