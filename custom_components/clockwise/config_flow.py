"""Config flow for Clockwise."""
from __future__ import annotations

import aiohttp
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import callback

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN


class ClockwiseConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Clockwise."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip().rstrip("/")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"http://{host}/get",
                        timeout=aiohttp.ClientTimeout(total=8),
                    ) as resp:
                        if resp.status != 204 or "clockface" not in str(resp.headers).lower():
                            errors["base"] = "not_clockwise"
                        else:
                            await self.async_set_unique_id(host)
                            self._abort_if_unique_id_configured()
                            name = user_input.get(CONF_NAME) or "Clockwise"
                            return self.async_create_entry(
                                title=name,
                                data={CONF_HOST: host},
                                options={"scan_interval": DEFAULT_SCAN_INTERVAL},
                            )
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_NAME): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ClockwiseOptionsFlow(config_entry)


class ClockwiseOptionsFlow(OptionsFlow):
    """Handle options: change IP or poll interval after setup."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        current_host = self.config_entry.data[CONF_HOST]
        current_interval = self.config_entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)

        if user_input is not None:
            new_host = user_input[CONF_HOST].strip().rstrip("/")
            new_interval = user_input["scan_interval"]
            # Validate new host if it changed
            if new_host != current_host:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            f"http://{new_host}/get",
                            timeout=aiohttp.ClientTimeout(total=8),
                        ) as resp:
                            if resp.status != 204 or "clockface" not in str(resp.headers).lower():
                                errors["base"] = "not_clockwise"
                except aiohttp.ClientError:
                    errors["base"] = "cannot_connect"

            if not errors:
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data={CONF_HOST: new_host},
                )
                return self.async_create_entry(
                    title="",
                    data={"scan_interval": new_interval},
                )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=current_host): str,
                    vol.Required("scan_interval", default=current_interval): vol.All(
                        vol.Coerce(int), vol.Range(min=30, max=3600)
                    ),
                }
            ),
            errors=errors,
        )
