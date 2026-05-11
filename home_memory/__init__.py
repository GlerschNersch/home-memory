"""Home Memory — AI narrative digest for Home Assistant."""
import logging
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.http import HomeAssistantView
from homeassistant.components.frontend import async_register_built_in_panel, async_remove_panel

_LOGGER = logging.getLogger(__name__)
DOMAIN = "home_memory"


class HomePanelView(HomeAssistantView):
    """Serve the Home Memory panel HTML directly."""
    url = "/home_memory_panel"
    name = "home_memory_panel"
    requires_auth = False

    def __init__(self, html: str):
        self._html = html

    async def get(self, request):
        from aiohttp.web import Response
        return Response(text=self._html, content_type="text/html")


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    panel_path = Path(__file__).parent / "frontend" / "home-memory-panel.html"
    html = await hass.async_add_executor_job(panel_path.read_text, "utf-8")

    hass.http.register_view(HomePanelView(html))

    async_register_built_in_panel(
        hass,
        component_name="iframe",
        sidebar_title="Home Memory",
        sidebar_icon="mdi:brain",
        frontend_url_path="home-memory",
        config={"url": "/home_memory_panel"},
        require_admin=False,
    )

    _LOGGER.info("Home Memory: panel served at /home_memory_panel")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    async_remove_panel(hass, "home-memory")
    return True
