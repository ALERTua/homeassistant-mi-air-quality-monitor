"""Support for XiaoMi Multifunction Air Monitor."""
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_TOKEN, CONF_DEVICE_CLASS, TEMP_CELSIUS)
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.translation import recursive_flatten

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "XiaoMi Multifunction Air Monitor"

ICON = "mdi:cloud"

SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_TOKEN): cv.string,
        vol.Optional(CONF_DEVICE_CLASS): vol.All(
            cv.string, vol.In(["zhimi.airmonitor.v1", "cgllc.airmonitor.b1", "cgllc.airmonitor.s1"])
        ),
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Perform the setup for XiaoMi Multifunction Air Monitor."""
    from miio import AirQualityMonitor, DeviceException

    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)
    device_class = config.get(CONF_DEVICE_CLASS)

    _LOGGER.info("Initializing Xiaomi Mi Multifunction Air Monitor with host %s (token %s...)", host, token[:5])

    entities = []
    try:
        airQualityMonitor = AirQualityMonitor(host, token, model=device_class)
        airQualityMonitorSensor = XiaomiAirQualityMonitorSensor(airQualityMonitor, name)
        entities.append(airQualityMonitorSensor)
    except DeviceException:
        raise PlatformNotReady

    add_entities(entities)


class XiaomiAirQualityMonitorSensor(Entity):
    """Representation of a XiaomiAirQualityMonitorSensor."""

    def __init__(self, airQualityMonitor, name):
        """Initialize the XiaomiAirQualityMonitorSensor."""
        self._state = None
        self._name = name
        self._airQualityMonitor = airQualityMonitor
        self.parse_data()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:cloud'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return TEMP_CELSIUS

    @property
    def device_state_attributes(self):
        """Return the state attributes of the last update."""
        from miio.device import DeviceInfo
        from miio.airqualitymonitor import AirQualityMonitorStatus
        info = self._airQualityMonitor.info()  # type: DeviceInfo
        status = self._airQualityMonitor.status()  # type: AirQualityMonitorStatus
        attrs = {}
        if info:
            attrs.update(info.__dict__.get('data', {}))
        if status:
            attrs.update(status.__dict__.get('data', {}))
        attrs = recursive_flatten('', attrs)
        return attrs

    def parse_data(self):
        from miio import DeviceException
        try:
            self._state = int(self._airQualityMonitor.status().temperature)
        except DeviceException:
            _LOGGER.warning('Fail to get temperature from XiaoMi Multifunction Air Monitor')
            raise PlatformNotReady

    def update(self):
        """Get the latest data and updates the states."""
        self.parse_data()
