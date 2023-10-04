**This repository is archived, as I am no longer in possession of such a device. Feel free to fork it, or contact me to transfer the ownership.**
# homeassistant-xiaomi-multifunction-air-monitor
XiaoMi Multifunction Air Monitor component for Home Assistant.

![device_image](https://raw.githubusercontent.com/ALERTua/homeassistant-xiaomi-multifunction-air-monitor/master/images/device_image.jpg)

![card](https://raw.githubusercontent.com/ALERTua/homeassistant-xiaomi-multifunction-air-monitor/master/images/card.png)

## Installation
1. Copy *custom_components* folder from this repositoty to your homeassistant *config* folder.
2. Get the IP of your sensor.
3. Follow [Retrieving the Access Token](https://home-assistant.io/components/vacuum.xiaomi_miio/#retrieving-the-access-token) guide to get the token of your sensor

## Configuration
```yaml
sensor:
  - platform: mi_multifunction_air_quality_monitor
    host: YOUR_SENSOR_IP
    token: YOUR_SENSOR_TOKEN
    device_class: YOUR_DEVICE_CLASS
    name: YOUR_SENSOR_NAME
```
Device class can be:
- zhimi.airmonitor.v1
- cgllc.airmonitor.b1
- cgllc.airmonitor.s1

![entity](https://raw.githubusercontent.com/ALERTua/homeassistant-xiaomi-multifunction-air-monitor/master/images/entity.png)

```yaml
type: vertical-stack
title: XiaoMi Multifunction Air Monitor
cards:
  - type: horizontal-stack
    cards:
      - type: 'custom:mini-graph-card'
        entities:
          - sensor.air_quality_monitor_co2e
      - type: 'custom:mini-graph-card'
        entities:
          - sensor.air_quality_monitor_humidity
      - type: 'custom:mini-graph-card'
        entities:
          - sensor.air_quality_monitor_pm25
      - type: 'custom:mini-graph-card'
        entities:
          - sensor.air_quality_monitor_temperature
  - type: 'custom:entity-attributes-card'
    entity: sensor.xiaomi_multifunction_air_monitor
    filter:
      include:
        - key: sensor.xiaomi_multifunction_air_monitor.*

```


Based on:
- https://github.com/bit3725/homeassistant-mi-air-quality-monitor
- https://github.com/rytilahti/python-miio
