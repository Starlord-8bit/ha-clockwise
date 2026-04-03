"""Select entities for Clockwise: clockface, rotation, LED colour order."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CLOCKFACES, DOMAIN, LED_COLOR_ORDER, ROTATIONS
from .coordinator import ClockwiseCoordinator
from .entity import ClockwiseEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: ClockwiseCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ClockfaceSelect(coordinator),
        RotationSelect(coordinator),
        LedColorOrderSelect(coordinator),
    ])


class ClockfaceSelect(ClockwiseEntity, SelectEntity):
    _attr_name = "Clockface"
    _attr_icon = "mdi:clock-outline"
    _attr_options = list(CLOCKFACES.values())

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "clockface")

    @property
    def current_option(self) -> str | None:
        raw = self._val("clockface")
        return CLOCKFACES.get(raw)

    async def async_select_option(self, option: str) -> None:
        key = next((k for k, v in CLOCKFACES.items() if v == option), None)
        if key:
            await self.coordinator.async_set({"clockFace": key})


class RotationSelect(ClockwiseEntity, SelectEntity):
    _attr_name = "Rotation"
    _attr_icon = "mdi:rotate-right"
    _attr_options = list(ROTATIONS.values())

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "rotation")

    @property
    def current_option(self) -> str | None:
        raw = self._val("displayrotation")
        return ROTATIONS.get(raw)

    async def async_select_option(self, option: str) -> None:
        key = next((k for k, v in ROTATIONS.items() if v == option), None)
        if key is not None:
            await self.coordinator.async_set({"displayRotation": key})


class LedColorOrderSelect(ClockwiseEntity, SelectEntity):
    """LED colour order — works with both OG (swapBlueGreen) and Plus (specialLed)."""
    _attr_name = "LED Colour Order"
    _attr_icon = "mdi:palette"
    _attr_options = list(LED_COLOR_ORDER.values())

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "led_color_order")

    def _is_plus_firmware(self) -> bool:
        """Plus firmware exposes 'specialled' header; OG exposes 'swapbluegreen'."""
        return "specialled" in (self.coordinator.data or {})

    @property
    def current_option(self) -> str | None:
        if self._is_plus_firmware():
            raw = self._val("specialled")
        else:
            # OG: swapbluegreen=1 means RBG, 0 means RGB
            raw = "1" if self._val("swapbluegreen") == "1" else "0"
        return LED_COLOR_ORDER.get(raw, "RGB")

    async def async_select_option(self, option: str) -> None:
        key = next((k for k, v in LED_COLOR_ORDER.items() if v == option), "0")
        if self._is_plus_firmware():
            await self.coordinator.async_set({"specialLed": key})
        else:
            # OG only supports RGB/RBG via swapBlueGreen
            await self.coordinator.async_set({"swapBlueGreen": "1" if key == "1" else "0"})
