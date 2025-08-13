from dataclasses import dataclass
from functools import cached_property
from uuid import UUID

from enum import Enum, IntEnum


@dataclass(slots=True, frozen=True)
class Constants:
    EmgResolution = 2.42 / 310.0 / 0xFFFF
    AccResolution = 0.061
    GyroResolution = 4.375


@dataclass(slots=True, frozen=True)
class Pkt:
    SamplesCountData = 8
    ChannelsCountData = 7
    SamplesCountEMG = 32
    ChannelsCountEMG = 1


class Command(Enum):
    SetLed = 0
    AcquisitionStart = 1
    AcquisitionStop = 2
    ConnectionClose = 3
    TurnOff = 4
    Vibro = 5


class SamplingRate(Enum):
    HZ_1000 = 0
    HZ_2000 = 1
    HZ_5000 = 2


class ScaleAccel(Enum):
    G_0 = 0
    G_1 = 1
    G_2 = 2
    G_3 = 3


class ScaleGyro(Enum):
    DPS_125 = 0
    DPS_250 = 1
    DPS_500 = 2
    DPS_1000 = 3


class EventType(Enum):
    BUTTON = 0
    ACTIVITY = 1
    FREEFALL = 2
    ORIENTATION = 3
    START = 4
    CHARGE = 5


UUID_TEMPLATE = "0000{:0>4x}-0000-1000-8000-00805f9b34fb"


class DeviceInformationService(IntEnum):
    MANUFACTURER_NAME = 0x2A29
    MODEL = 0x2A24
    SERIAL = 0x2A25
    FIRMWARE = 0x2A26
    HARDWARE = 0x2A27

    @cached_property
    def uuid(self) -> UUID:
        """Convert the ID to a full UUID and cache."""
        return UUID(UUID_TEMPLATE.format(self.value))

    def __str__(self) -> str:
        """Convert UUID to string value."""
        return str(self.uuid)

