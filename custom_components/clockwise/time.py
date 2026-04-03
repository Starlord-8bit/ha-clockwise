"""Time entities for Clockwise: night mode start/end schedule."""
from __future__ import annotations

from datetime import time

from homeassistant.components.time import TimeEntity
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
    async_add_entities([
        NightStartTime(coordinator),
        NightEndTime(coordinator),
    ])


class NightStartTime(ClockwiseEntity, TimeEntity):
    _attr_name = "Night Mode Start"
    _attr_icon = "mdi:weather-night"

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "night_start")

    @property
    def native_value(self) -> time | None:
        try:
            h = int(self._val("nightstarth", "22"))
            m = int(self._val("nightstartm", "0"))
            return time(h, m)
        except (ValueError, OverflowError):
            return None

    async def async_set_value(self, value: time) -> None:
        data = self.coordinator.data or {}
        param = (
            f"nightLevel={data.get('nightlevel', '1')}"
            f"&nightStarth={value.hour}"
            f"&nightStartm={value.minute}"
            f"&nightEndh={data.get('nightendh', '8')}"
            f"&nightEndm={data.get('nightendm', '0')}"
            f"&nightMode={data.get('nightmode', '0')}"
        )
        await self.coordinator.async_set_raw(param)


class NightEndTime(ClockwiseEntity, TimeEntity):
    _attr_name = "Night Mode End"
    _attr_icon = "mdi:weather-sunny"

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "night_end")

    @property
    def native_value(self) -> time | None:
        try:
            h = int(self._val("nightendh", "8"))
            m = int(self._val("nightendm", "0"))
            return time(h, m)
        except (ValueError, OverflowError):
            return None

    async def async_set_value(self, value: time) -> None:
        data = self.coordinator.data or {}
        param = (
            f"nightLevel={data.get('nightlevel', '1')}"
            f"&nightStarth={data.get('nightstarth', '22')}"
            f"&nightStartm={data.get('nightstartm', '0')}"
            f"&nightEndh={value.hour}"
            f"&nightEndm={value.minute}"
            f"&nightMode={data.get('nightmode', '0')}"
        )
        await self.coordinator.async_set_raw(param)
