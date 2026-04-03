"""Select entities for Clockwise: clockface, rotation, LED colour order."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CLOCKFACES, DOMAIN, LED_COLOR_ORDER, ROTATIONS, BRIGHTNESS_METHOD, NIGHT_MODE, AUTO_CHANGE_FACE
from .coordinator import ClockwiseCoordinator
from .entity import ClockwiseEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: ClockwiseCoordinator = hass.data[DOMAIN][entry.entry_id]
    is_plus = "specialled" in (coordinator.data or {})
    entities: list = [
        ClockfaceSelect(coordinator),
        RotationSelect(coordinator),
        LedColorOrderSelect(coordinator),
    ]
    if is_plus:
        entities += [
            BrightnessMethodSelect(coordinator),
            NightModeSelect(coordinator),
            AutoChangeFaceSelect(coordinator),
        ]
    async_add_entities(entities)


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


class BrightnessMethodSelect(ClockwiseEntity, SelectEntity):
    """How brightness is controlled: auto LDR / time-based / fixed."""
    _attr_name = "Brightness Method"
    _attr_icon = "mdi:brightness-auto"
    _attr_options = list(BRIGHTNESS_METHOD.values())

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "brightness_method")

    @property
    def current_option(self) -> str | None:
        return BRIGHTNESS_METHOD.get(self._val("brightmethod"))

    async def async_select_option(self, option: str) -> None:
        key = next((k for k, v in BRIGHTNESS_METHOD.items() if v == option), "0")
        await self.coordinator.async_set({"brightMethod": key})


class NightModeSelect(ClockwiseEntity, SelectEntity):
    """What happens during night hours: nothing / off / big clock."""
    _attr_name = "Night Mode"
    _attr_icon = "mdi:weather-night"
    _attr_options = list(NIGHT_MODE.values())

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "night_mode")

    @property
    def current_option(self) -> str | None:
        return NIGHT_MODE.get(self._val("nightmode"))

    async def async_select_option(self, option: str) -> None:
        key = next((k for k, v in NIGHT_MODE.items() if v == option), "0")
        # nightMode is bundled in nightParam: level,starth,startm,endh,endm,mode
        # We only change the mode, preserve everything else
        data = self.coordinator.data or {}
        param = (
            f"nightLevel={data.get('nightlevel', '1')}"
            f"&nightStarth={data.get('nightstarth', '22')}"
            f"&nightStartm={data.get('nightstartm', '0')}"
            f"&nightEndh={data.get('nightendh', '8')}"
            f"&nightEndm={data.get('nightendm', '0')}"
            f"&nightMode={key}"
        )
        await self.coordinator.async_set_raw(param)


class AutoChangeFaceSelect(ClockwiseEntity, SelectEntity):
    """Auto-change clockface daily: off / sequence / random."""
    _attr_name = "Auto-Change Clockface"
    _attr_icon = "mdi:shuffle-variant"
    _attr_options = list(AUTO_CHANGE_FACE.values())

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "auto_change_face")

    @property
    def current_option(self) -> str | None:
        return AUTO_CHANGE_FACE.get(self._val("autochange"))

    async def async_select_option(self, option: str) -> None:
        key = next((k for k, v in AUTO_CHANGE_FACE.items() if v == option), "0")
        # When enabling, also send faceControl (all faces enabled by default)
        params: dict[str, str] = {"autoChange": key}
        if key != "0":
            params["faceControl"] = self._val("facecontrol") or "1" * 21
        await self.coordinator.async_set(params)
