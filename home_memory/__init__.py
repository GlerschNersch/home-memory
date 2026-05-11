"""Home Memory — AI narrative digest for Home Assistant."""
import logging
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.frontend import async_register_built_in_panel, async_remove_panel
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)
DOMAIN = "home_memory"
PANEL_FILENAME = "home-memory-panel.html"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Ensure the frontend component is loaded before we register anything
    await hass.async_add_executor_job(
        lambda: None  # yield to event loop
    )

    frontend_path = Path(__file__).parent / "frontend"

    # Register the static files directory
    hass.http.register_static_path(
        "/home_memory_static",
        str(frontend_path),
        cache_headers=False,
    )

    # Register the sidebar panel as an iframe pointing to the static HTML
    async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="Home Memory",
        sidebar_icon="mdi:brain",
        frontend_url_path="home-memory",
        config={"url": "/home_memory_static/home-memory-panel.html"},
        require_admin=False,
    )

    _LOGGER.info("Home Memory: panel registered, static path=/home_memory_static")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    async_remove_panel(hass, "home-memory")
    return True
