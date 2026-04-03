# ha-clockwise

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/Starlord-8bit/ha-clockwise)](https://github.com/Starlord-8bit/ha-clockwise/releases)

Home Assistant integration for the [Clockwise](https://clockwise.page/) open-source LED matrix wall clock.

![Clockwise in Home Assistant](docs/ha_screenshot.png)

## Features

- 🕐 **Clockface selection** — switch between all installed clockfaces (Mario, Pac-Man, World Map, Canvas, etc.)
- 💡 **Brightness control** — slider from 0–255
- 🌙 **Canvas support** — set Canvas file + server URL directly from HA
- 🔄 **Rotation** — 0°/90°/180°/270°
- ⏰ **24h format** toggle
- 🎨 **RGB swap** (Blue/Green) for panels with wrong colour order
- 🌐 **NTP server** configuration
- 💡 **Ambient light sensor** (if LDR connected)
- 🔁 **Restart button**
- 📡 **Local polling** — no cloud, no callhome

## Requirements

- Home Assistant 2024.1+
- [Clockwise firmware](https://clockwise.page/) flashed on your ESP32 + HUB75 LED matrix
- Clock and HA on the same network

## Installation

### Via HACS (recommended)

1. Add this repo as a custom repository in HACS:
   - HACS → Integrations → ⋮ → Custom repositories
   - URL: `https://github.com/Starlord-8bit/ha-clockwise`
   - Category: Integration
2. Install **Clockwise LED Clock**
3. Restart Home Assistant

### Manual

Copy `custom_components/clockwise/` into your HA `config/custom_components/` directory and restart.

## Setup

1. Settings → Devices & Services → Add Integration → **Clockwise**
2. Enter the IP address of your clock (e.g. `192.168.1.250`)
3. Done — device and all entities appear automatically

## Entities

| Entity | Type | Description |
|--------|------|-------------|
| Clockface | Select | Switch active clockface |
| Brightness | Number | Display brightness (0–255) |
| Rotation | Select | Display rotation (0°/90°/180°/270°) |
| 24h Format | Switch | Toggle 12h/24h time display |
| Swap Blue/Green | Switch | Fix colour order for RBG panels |
| NTP Server | Text | Change NTP server address |
| Canvas File | Text | Set Canvas clockface JSON filename |
| Canvas Server | Text | Set Canvas JSON server URL |
| Ambient Light (LDR) | Sensor | Raw LDR value (if sensor connected) |
| Restart | Button | Restart the clock |

## Canvas Clockfaces

The Canvas clockface lets you load any JSON-described theme at runtime — no reflashing needed. Point `Canvas Server` at a server hosting your `.json` theme files and set `Canvas File` to the filename.

Community themes: [Clock Club](https://github.com/jnthas/clock-club)

## Compatible Firmware

Tested with [jnthas/clockwise](https://github.com/jnthas/clockwise) v1.4.x.  
The Plus firmware (topyuan.top) exposes a similar API but has a different header format — partial compatibility.

## License

MIT
