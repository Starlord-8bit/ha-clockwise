"""Data coordinator for Clockwise."""
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ClockwiseCoordinator(DataUpdateCoordinator[dict]):
    """Polls the Clockwise device via GET /get (headers-based API)."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.host = entry.data[CONF_HOST]
        self.entry = entry
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        """Fetch all device state from /get response headers, plus LDR pin read."""
        url = f"http://{self.host}/get"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status != 204:
                        raise UpdateFailed(f"Unexpected status {resp.status}")
                    data = {k.lower(): v for k, v in resp.headers.items()}

                # Also poll LDR pin value (separate endpoint)
                ldr_pin = data.get("ldrpin", "35")
                ldr_val = await self.async_read_pin(int(ldr_pin))
                if ldr_val is not None:
                    data["ldr_value"] = str(ldr_val)

                return data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Cannot reach Clockwise at {self.host}: {err}") from err

    async def async_set(self, params: dict[str, str]) -> None:
        """POST /set with given key=value params."""
        from urllib.parse import urlencode
        await self.async_set_raw(urlencode(params))

    async def async_set_raw(self, body: str) -> None:
        """POST /set with a pre-encoded body string."""
        url = f"http://{self.host}/set"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    data=body,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    if resp.status not in (200, 204):
                        raise UpdateFailed(f"Set failed with status {resp.status}")
            await self.async_request_refresh()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Cannot reach Clockwise at {self.host}: {err}") from err

    async def async_restart(self) -> None:
        """POST /restart."""
        url = f"http://{self.host}/restart"
        async with aiohttp.ClientSession() as session:
            try:
                await session.post(url, timeout=aiohttp.ClientTimeout(total=5))
            except aiohttp.ClientError:
                pass  # device reboots immediately, connection drop is expected

    async def async_read_pin(self, pin: int) -> int | None:
        """GET /read?pin=X, returns pin value from response header."""
        url = f"http://{self.host}/read?pin={pin}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    return int(resp.headers.get("pin", 0))
        except (aiohttp.ClientError, ValueError):
            return None
