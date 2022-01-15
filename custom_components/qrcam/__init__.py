"""
The QRCAM Component
This component generates QR Codes inside from Templates
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import Platform

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "qrcam"
PLATFORMS = [Platform.CAMERA]


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""
    # States are in the format DOMAIN.OBJECT_ID.
    # Return boolean to indicate that initialization was successfully.
    return True