"""Sensor entities: ambient light (LDR), uptime, night brightness level."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
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
        LdrSensor(coordinator),
        UptimeSensor(coordinator),
        NightBrightnessLevelSensor(coordinator),
    ])


class LdrSensor(ClockwiseEntity, SensorEntity):
    _attr_name = "Ambient Light (LDR)"
    _attr_icon = "mdi:brightness-auto"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "raw"

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "ldr")

    @property
    def native_value(self) -> int | None:
        val = self._val("ldr_value")
        return int(val) if val else None

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "ldr_pin": self._val("ldrpin"),
            "auto_bright_min": self._val("autobrightmin"),
            "auto_bright_max": self._val("autobrightmax"),
        }


class UptimeSensor(ClockwiseEntity, SensorEntity):
    """How long the device has been running since last flash/reset."""
    _attr_name = "Uptime"
    _attr_icon = "mdi:timer-outline"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "uptime")

    @property
    def native_value(self) -> str:
        y = self._val("totalyear", "0")
        m = self._val("totalmonth", "0")
        d = self._val("totalday", "0")
        return f"{y}y {m}m {d}d"

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "years": self._val("totalyear"),
            "months": self._val("totalmonth"),
            "days": self._val("totalday"),
        }


class NightBrightnessLevelSensor(ClockwiseEntity, SensorEntity):
    """Night brightness level (1–5). Read-only display; set via number entity."""
    _attr_name = "Night Brightness Level"
    _attr_icon = "mdi:moon-waning-crescent"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "night_level")

    @property
    def native_value(self) -> int | None:
        val = self._val("nightlevel")
        return int(val) if val else None
