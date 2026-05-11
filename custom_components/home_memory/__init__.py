"""Home Memory — Smart Home Intelligence dashboard for Home Assistant."""
import logging
import shutil
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.frontend import async_register_built_in_panel, async_remove_panel
from homeassistant.components.http import StaticPathConfig

_LOGGER = logging.getLogger(__name__)
DOMAIN = "home_memory"
PANEL_URL_PATH = "home-memory"
STATIC_URL = "/home_memory_static"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # The frontend folder sits next to this __init__.py
    frontend_path = Path(__file__).parent / "frontend"
    frontend_path.mkdir(exist_ok=True)

    # If the panel HTML hasn't been copied yet, copy index.html from the repo root www
    # (fallback: use the bundled panel.html if present)
    panel_file = frontend_path / "panel.html"
    if not panel_file.exists():
        # Try to copy from /config/www/home-memory/ if the user placed it there
        www_source = Path(hass.config.config_dir) / "www" / "home-memory" / "index.html"
        repo_source = Path(__file__).parent.parent.parent / "index.html"
        if www_source.exists():
            shutil.copy2(www_source, panel_file)
            _LOGGER.info("Home Memory: copied panel from www/home-memory/index.html")
        elif repo_source.exists():
            shutil.copy2(repo_source, panel_file)
            _LOGGER.info("Home Memory: copied panel from repo root index.html")
        else:
            _LOGGER.warning(
                "Home Memory: panel.html not found in frontend/. "
                "Place index.html at /config/www/home-memory/index.html and reload."
            )

    # Register the static path so HA serves the files
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            url_path=STATIC_URL,
            path=str(frontend_path),
            cache_headers=False,
        )
    ])

    # Register the sidebar panel using the modern API
    async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="Home Memory",
        sidebar_icon="mdi:brain",
        frontend_url_path=PANEL_URL_PATH,
        config={"url": f"{STATIC_URL}/panel.html"},
        require_admin=False,
    )

    _LOGGER.info("Home Memory panel registered at /%s", PANEL_URL_PATH)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    async_remove_panel(hass, PANEL_URL_PATH)
    return True
