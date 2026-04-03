"""Text entities: NTP server, Canvas file, Canvas server."""
from __future__ import annotations

from homeassistant.components.text import TextEntity
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
        NtpServerText(coordinator),
        CanvasFileText(coordinator),
        CanvasServerText(coordinator),
    ])


class NtpServerText(ClockwiseEntity, TextEntity):
    _attr_name = "NTP Server"
    _attr_icon = "mdi:server"
    _attr_native_max = 128

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "ntpserver")

    @property
    def native_value(self) -> str:
        return self._val("ntpserver")

    async def async_set_value(self, value: str) -> None:
        await self.coordinator.async_set({"ntpServer": value})


class CanvasFileText(ClockwiseEntity, TextEntity):
    _attr_name = "Canvas File"
    _attr_icon = "mdi:file-code"
    _attr_native_max = 128

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "canvasfile")

    @property
    def native_value(self) -> str:
        return self._val("canvasfile")

    async def async_set_value(self, value: str) -> None:
        await self.coordinator.async_set({"canvasFile": value})


class CanvasServerText(ClockwiseEntity, TextEntity):
    _attr_name = "Canvas Server"
    _attr_icon = "mdi:server-network"
    _attr_native_max = 256

    def __init__(self, coordinator: ClockwiseCoordinator) -> None:
        super().__init__(coordinator, "canvasserver")

    @property
    def native_value(self) -> str:
        return self._val("canvasserver")

    async def async_set_value(self, value: str) -> None:
        await self.coordinator.async_set({"canvasServer": value})
