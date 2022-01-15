# QRCam

[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

This custom component creates cameras displaying qrcodes. The QRCodes can be static or generated from templates.
If you use a template as content the camera will update with a new qr code when the template updates.

**This component will set up the following platforms.**

Platform | Description
-- | --
`qrcam` | Display QRCodes in Camera entites.

## Installation


## Configuration

Example `configuration.yaml` entry:

```
camera:
 - platform: qrcam
   name: "Test Camera"
   content: "Hello World"
```

another a bit more complicated example using a template:

```
camera:
 - platform: qrcam
   name: "Test Camera 2"
   content: "{{states('input_boolean.karl')}}"
   fill_color: "0,255,0"
   back_color: "0,0,0"
```

displaying a wifi qr code (replace {SSID} and {PASSWORD}):

```
camera:
 - platform: qrcam
   name: "WIFI"
   content: "WIFI:S:{SSID};T:WPA;P:{PASSWORD};;"
```

Note that you need a custom sensor for the shopping list example.

Following is configurable:

Name | Description |Required | Type | Default
-- | -- | -- | -- | --
`name` |The name of the Camera| Yes | String | -
`content` | The content that shall be encoded (can be template) | Yes | Template | -
`version` | The "Version" of the qr code (which is basically the size) | No | int between 1 and 40 | Auto
`error_correction` | How much error correction the QRCode should have | No | see Error Corretion | ERROR_CORRECT_M
`box_size` | The size of the Black Boxes in pixel | No | Positive Integer | 10
`border` | Border arround the code | No | Integer > 3 | 4
`fill_color`| RGB Color for the (normaly black) parts of the QRCode | No | String of form "r,g,b" | "0,0,0"
`back_color`| RGB Color for the background of the QRCode | No | String of form "r,g,b" | "255,255,255"
`edge_color`| RGB Color for the edge of the qr code (only used if color_mask is radial or square) | No | String of form "r,b,g" | "0,0,0"
`left_color`| RGB Color for the left side of the qr code (only used if color_mask is horizontal or vertical) | No | String of form "r,g,b" | "0,0,0"
`right_color`| RGB Color for the right side of the qr code (only used if color_mask is horizontal or vertical) | No | String of form "r,g,b" | "0,0,0"
`color_mask`| Mask for the Colors of the QR Code | No | See Color Mask | "solid"
`drawer` | Options on how to render the QR Code | No | See Rendering | "square"

## Error Correction
The error_correction parameter controls the error correction used for the QR Code.
Name | Discription
-- | --
ERROR_CORRECT_L | About 7% or less errors can be corrected.
ERROR_CORRECT_M | About 15% or less errors can be corrected.
ERROR_CORRECT_Q | About 25% or less errors can be corrected.
ERROR_CORRECT_H | About 30% or less errors can be corrected.
***
## Color Mask
![masks](https://github.com/lincolnloop/python-qrcode/blob/master/doc/color_masks.png)
Name | Number in Image
-- | --
`solid`| 1
`radial`| 2
`square`| 3
`horizontal` | 4
`vertical`| 5
 (WIP) | 6

## Drawer
![drawers](https://github.com/lincolnloop/python-qrcode/blob/master/doc/module_drawers.png)
Name | Number in Image
-- | --
`square`| 1
`gapped_square`| 2
`circle`| 3
`rounded`| 4
`vertical_bars`| 5
`horizontal_graphs`| 6

[commits]: https://github.com/Hypercookie/hass-qrcam/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%20%40Hypercookie-blue.svg?style=for-the-badge
