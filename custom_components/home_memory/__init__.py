"""Home Memory — Smart Home Intelligence dashboard for Home Assistant."""
import logging
import shutil
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)
DOMAIN = "home_memory"
PANEL_URL_PATH = "home-memory"
STATIC_URL = "/home_memory_static"
DATA_STATIC_REGISTERED = f"{DOMAIN}_static_registered"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    try:
        from homeassistant.components.frontend import async_register_built_in_panel
    except ImportError as err:
        _LOGGER.error("Home Memory: could not import frontend module: %s", err)
        return False

    # Ensure frontend directory exists
    frontend_path = Path(__file__).parent / "frontend"
    frontend_path.mkdir(parents=True, exist_ok=True)

    # Copy panel HTML if not already present
    panel_file = frontend_path / "panel.html"
    if not panel_file.exists():
        www_source = Path(hass.config.config_dir) / "www" / "home-memory" / "index.html"
        repo_source = Path(__file__).parent.parent.parent / "index.html"
        if www_source.exists():
            shutil.copy2(www_source, panel_file)
            _LOGGER.info("Home Memory: copied panel from %s", www_source)
        elif repo_source.exists():
            shutil.copy2(repo_source, panel_file)
            _LOGGER.info("Home Memory: copied panel from %s", repo_source)
        else:
            _LOGGER.warning(
                "Home Memory: no panel HTML found. "
                "Copy index.html to /config/www/home-memory/index.html and reload."
            )

    # Only register the static path once per HA lifetime.
    # aiohttp raises RuntimeError if the same GET route is added twice,
    # and it fires before our try/except can catch it.
    if not hass.data.get(DATA_STATIC_REGISTERED):
        try:
            from homeassistant.components.http import StaticPathConfig
            await hass.http.async_register_static_paths([
                StaticPathConfig(
                    url_path=STATIC_URL,
                    path=str(frontend_path),
                    cache_headers=False,
                )
            ])
            hass.data[DATA_STATIC_REGISTERED] = True
            _LOGGER.debug("Home Memory: static path registered at %s", STATIC_URL)
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("Home Memory: failed to register static path: %s", err)
            return False
    else:
        _LOGGER.debug("Home Memory: static path already registered, skipping")

    # Register sidebar panel
    try:
        async_register_built_in_panel(
            hass,
            component_name="iframe",
            sidebar_title="Home Memory",
            sidebar_icon="mdi:brain",
            frontend_url_path=PANEL_URL_PATH,
            config={"url": f"{STATIC_URL}/panel.html"},
            require_admin=False,
        )
    except Exception as err:  # noqa: BLE001
        _LOGGER.error("Home Memory: failed to register panel: %s", err)
        return False

    _LOGGER.info("Home Memory panel registered successfully")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    try:
        from homeassistant.components.frontend import async_remove_panel
        async_remove_panel(hass, PANEL_URL_PATH)
    except Exception as err:  # noqa: BLE001
        _LOGGER.warning("Home Memory: could not remove panel on unload: %s", err)
    # Note: static paths cannot be unregistered from aiohttp at runtime.
    # The DATA_STATIC_REGISTERED flag persists so reloads skip re-registration.
    return True
