"""Config flow for Clockwise."""
from __future__ import annotations

import aiohttp
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_NAME

from .const import DOMAIN


class ClockwiseConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Clockwise."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip().rstrip("/")
            # Validate: hit /get and check for clockwise-specific headers
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
