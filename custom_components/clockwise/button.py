"""Button entities: restart device."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import ClockwiseCoordinator
from .entity import ClockwiseEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: ClockwiseCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RestartButton(coordinator)])


class RestartButton(ClockwiseEntity, ButtonEntity):
    _attr_name = "Restart"
    _attr_icon = "mdi:restart"

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "restart")

    async def async_press(self) -> None:
        await self.coordinator.async_restart()
