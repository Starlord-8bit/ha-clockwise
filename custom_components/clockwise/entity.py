"""Base entity for Clockwise."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ClockwiseCoordinator


class ClockwiseEntity(CoordinatorEntity[ClockwiseCoordinator]):
    """Base entity: ties device_info + unique_id to the coordinator."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: ClockwiseCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_unique_id = f"{coordinator.host}_{key}"

    @property
    def device_info(self) -> DeviceInfo:
        data = self.coordinator.data or {}
        is_plus = "specialled" in data
        if is_plus:
            fw_version = data.get("version", "unknown")
            model = f"ClockWise Plus v{fw_version}"
        else:
            fw_version = data.get("x-cw_fw_version", "unknown")
            model = data.get("x-cw_fw_name", "Clockwise")
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.host)},
            name=self.coordinator.entry.title,
            manufacturer="jnthas" if not is_plus else "MonsterYuan (topyuan.top)",
            model=model,
            sw_version=fw_version,
            configuration_url=f"http://{self.coordinator.host}",
        )

    def _val(self, key: str, default: str = "") -> str:
        return (self.coordinator.data or {}).get(key, default)
