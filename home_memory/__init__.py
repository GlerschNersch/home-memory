"""Home Memory — AI narrative digest for Home Assistant."""
import logging
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.http import StaticPathConfig

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

    hass.components.frontend.async_register_built_in_panel(
        component_name="iframe",
        sidebar_title="Home Memory",
        sidebar_icon="mdi:brain",
        frontend_url_path="home-memory",
        config={"url": f"/home_memory_static/{PANEL_FILENAME}"},
        require_admin=False,
    )

    _LOGGER.info("Home Memory panel registered")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.components.frontend.async_remove_panel("home-memory")
    return True
