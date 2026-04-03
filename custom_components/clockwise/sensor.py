"""Sensor entities: ambient light (LDR)."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import LIGHT_LUX
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import ClockwiseCoordinator
from .entity import ClockwiseEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: ClockwiseCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LdrSensor(coordinator)])


class LdrSensor(ClockwiseEntity, SensorEntity):
    _attr_name = "Ambient Light (LDR)"
    _attr_icon = "mdi:brightness-auto"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "raw"

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "ldr")

    @property
    def native_value(self) -> int | None:
        """LDR is not in /get — it needs a separate /read?pin= call.
        Value is refreshed via coordinator extra data if available."""
        val = self._val("ldr_value")
        return int(val) if val else None

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "ldr_pin": self._val("ldrpin"),
            "auto_bright_min": self._val("autobrightmin"),
            "auto_bright_max": self._val("autobrightmax"),
        }
