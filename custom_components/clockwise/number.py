"""Number entities for Clockwise: display brightness."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
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
    async_add_entities([BrightnessNumber(coordinator)])


class BrightnessNumber(ClockwiseEntity, NumberEntity):
    _attr_name = "Brightness"
    _attr_icon = "mdi:brightness-5"
    _attr_native_min_value = 0
    _attr_native_max_value = 255
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "brightness")

    @property
    def native_value(self) -> float | None:
        val = self._val("displaybright")
        return float(val) if val else None

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_set({"displayBright": str(int(value))})
