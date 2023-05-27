"""Media platform for zone4-remote integration."""
from __future__ import annotations
from datetime import timedelta
from zone4 import Zone4Manager, Zone4Output
import voluptuous as vol
import serial
import asyncio

from homeassistant.components.media_player import (
    PLATFORM_SCHEMA,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITY_ID, EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import logging

from .const import PORT, ZONE_NAMES

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(PORT): cv.string,
        vol.Optional(ZONE_NAMES, default={"1": "Zone 1", "2": "Zone 2", "3": "Zone 3", "4": "Zone 4"}): cv.schema_with_slug_keys(cv.string)
    }
)

async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the media platform."""
    zone4 = Zone4Manager(config[PORT])
    
    try:
        await zone4.setup() 
        await zone4.request_states()
    except serial.SerialException as e:
        logging.error(f"Zone4 setup: {e}")
        return

    players = [
        Zone4MediaPlayerEntity(config[ZONE_NAMES]["1"], "zone_1", zone4.zone("a"), zone4),
        Zone4MediaPlayerEntity(config[ZONE_NAMES]["2"], "zone_2", zone4.zone("b"), zone4),
        Zone4MediaPlayerEntity(config[ZONE_NAMES]["3"], "zone_3", zone4.zone("c"), zone4),
        Zone4MediaPlayerEntity(config[ZONE_NAMES]["4"], "zone_4", zone4.zone("d"), zone4)
    ]
            
    async def async_update(hass, zone4, players):
        await zone4.update()
        
        for player in players:
            player.async_schedule_update_ha_state(True)

        hass.async_create_task(async_update(hass, zone4, players))


    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, async_update(hass, zone4, players))
    async_add_entities(players, update_before_add=True)

class Zone4MediaPlayerEntity(MediaPlayerEntity):
    """Zone4 Media Player."""

    _attr_media_content_type = MediaType.MUSIC
    _attr_supported_features = (
        MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(self, name: str, unique_id: str, zone: Zone4Output, parent: Zone4) -> None:
        """Initialize Zone4 Media Player."""
        super().__init__()
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._zone = zone
        self._parent = parent
        
        self._attr_source_list = ["A", "B", "C", "D"]
        self._attr_state = MediaPlayerState.PLAYING

    async def async_update(self):
        self._attr_volume_level = self._zone.get_volume() / 79
        self._attr_source = self._zone.get_channel()

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        self._attr_source = source
        await self._zone.set_channel(source)

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level."""
        self._attr_volume_level = volume
        await self._zone.set_volume(volume * 79)

