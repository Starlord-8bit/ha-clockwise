"""Switch entities: 24h format."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
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
    async_add_entities([Use24hSwitch(coordinator)])


class Use24hSwitch(ClockwiseEntity, SwitchEntity):
    _attr_name = "24h Format"
    _attr_icon = "mdi:clock-digital"

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "use24h")

    @property
    def is_on(self) -> bool:
        return self._val("use24hformat") == "1"

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_set({"use24hFormat": "1"})

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set({"use24hFormat": "0"})
