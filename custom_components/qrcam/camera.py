from __future__ import annotations
from numbers import Integral
import qrcode as qrcodegen
import io
import logging
import voluptuous as vol
import re
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.components.camera import (PLATFORM_SCHEMA,SUPPORT_STREAM,Camera)
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType,DiscoveryInfoType
from homeassistant.helpers.reload import async_setup_reload_service
ERROR_CORRECT_VALUES = {"ERROR_CORRECT_L": 1,"ERROR_CORRECT_M":0,"ERROR_CORRECT_Q":3,"ERROR_CORRECT_H":2}
_LOGGER = logging.getLogger(__name__)
from . import DOMAIN,PLATFORMS


def error_correct(value: Any) -> str:
    if value not in ERROR_CORRECT_VALUES:
        raise vol.Invalid("Error Correction Unkown should be one of [\"ERROR_CORRECT_L\",\"ERROR_CORRECT_M\",\"ERROR_CORRECT_Q\",\"ERROR_CORRECT_H\"]")
    else:
        return str(value)
def version(value: Any) -> int:
    if value is None:
        return None
    if value > 40 or value < 1:
        raise vol.Invalid("Error version has to be between 1 and 40")
    return int(value)
def boxSize(value : Any) -> int:
    if type(value) == int and value>0:
        return value
    else:
        raise vol.Invalid("No Float or negative numbers allowed")
def border(value : Any) -> int:
    if type(value) == int and value>=4:
        return value
    else:
        raise vol.Invalid("Value must be greater then 4 and no float")
def color(value : Any) -> tuple(int):
    if(re.match(" *\d{1,3} *, *\d{1,3} *, *\d{1,3} *",str(value))):
        return tuple(map(lambda x : int(x),str(value).replace(" ","").split(",")))
    else :
        raise vol.Invalid("Color did not match '*\d{1,3} *, *\d{1,3} *, *\d{1,3} *'")

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required("content") : cv.template,
    vol.Required(CONF_NAME): cv.string,
    vol.Optional("version", default = None) : version,
    vol.Optional("error_correction",default ="ERROR_CORRECT_M") : error_correct,
    vol.Optional("box_size",default =10) : boxSize,
    vol.Optional("border",default =4) : border,
    vol.Optional("fill_color",default = "0,0,0") : color,
    vol.Optional("back_color",default = "255,255,255") : color
})

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up qr cam"""
    await async_setup_reload_service(hass,DOMAIN,PLATFORMS)
    async_add_entities([QRCAM(config,hass)])

class QRCAM(Camera):
    """QR CAM"""
    def __init__(self,config,hass) -> None:
        super().__init__()
        self._hass = hass
        self._name = config[CONF_NAME]
        self._content = config["content"]
        self._content.hass = self._hass
        self._version = config["version"]
        self._error_correction = config["error_correction"]
        self._box_size = config["box_size"]
        self._border = config["border"]
        self._fill_color = config["fill_color"]
        self._back_color = config["back_color"]
    @property
    def supported_features(self) -> int:
        return 0
    async def async_camera_image(
        self, width: int | None = None, height : int | None = None
    ) -> bytes | None:
        """Still Image"""
        try:
          cont =   self._content.async_render(parse_result=False)
          qr = qrcodegen.QRCode(
            version=self._version,
            error_correction=ERROR_CORRECT_VALUES[self._error_correction],
            box_size=self._box_size,
            border=self._border,
          )
          qr.add_data(cont)
          qr.make(fit=True)
          img = qr.make_image(back_color=self._back_color,fill_color=self._fill_color)
          img_byte_array = io.BytesIO()
          img.save(img_byte_array,format="PNG")
          return img_byte_array.getvalue()
        except TemplateError as err:
           _LOGGER.error("Error parsing template %s: %s", self._still_image_url, err)
           return None

    @property
    def name(self):
        return self._name
    def is_recording(self) -> bool:
        return True
