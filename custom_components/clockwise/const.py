"""Constants for the Clockwise integration."""

DOMAIN = "clockwise"
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes — just to catch reboots/external changes

# OG Clockwise v1.4.x clockfaces
CLOCKFACES_OG = {
    "1": "Super Mario",
    "2": "Pac-Man",
    "3": "World Map",
    "4": "Castlevania",
    "5": "Clock Tower",
    "6": "Pokedex",
    "7": "Canvas",
}

# ClockWise Plus v3.x clockfaces (superset)
CLOCKFACES_PLUS = {
    "1": "Super Mario",
    "2": "Pac-Man",
    "3": "World Map",
    "4": "Time In Words",
    "5": "Clock Tower",
    "6": "Pokedex",
    "7": "Retro Computer",
    "8": "Snoopy",
    "9": "Nyan Cat",
    "10": "Transformer",
    "11": "Minecraft Torch",
    "12": "Coffee",
    "13": "Pepsi",
    "14": "Pikachu",
    "15": "Shar Pei Dog",
    "16": "Girl",
    "17": "Kirby",
    "18": "Labubu",
    "19": "Hello Kitty",
    "20": "Twinkle Twinkle",
    "21": "Zootopia",
}

# Combined map (Plus is a superset; OG faces match by index)
CLOCKFACES = CLOCKFACES_PLUS

ROTATIONS = {
    "0": "0°",
    "1": "90°",
    "2": "180°",
    "3": "270°",
}

# LED colour order options (Plus firmware uses specialLed)
LED_COLOR_ORDER = {
    "0": "RGB",
    "1": "RBG",
    "2": "GBR",
}

BRIGHTNESS_METHOD = {
    "0": "Auto (LDR)",
    "1": "Time-based",
    "2": "Fixed",
}

NIGHT_MODE = {
    "0": "Nothing",
    "1": "Turn off display",
    "2": "Big clock",
}

AUTO_CHANGE_FACE = {
    "0": "Off",
    "1": "Sequence",
    "2": "Random",
}
