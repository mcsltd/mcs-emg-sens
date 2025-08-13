import hashlib
import asyncio
import contextlib

from typing import Optional
from bleak import BleakClient, BLEDevice, AdvertisementData, BleakScanner
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher

from constants import Command
from decoder import Decoder
from structures import Settings

from config import BLE_KEY

def get_control_sum(data: bytes, key: bytearray) -> bytes:
    """ Data signing before writing in characteristic """
    hash = hashlib.sha256(data).digest()
    iv = bytes(128 // 8)
    # create encoder
    cipher = Cipher(
        algorithm=algorithms.AES(key), mode=modes.CBC(iv)
    )
    encryptor = cipher.encryptor()
    # encrypt
    sign = encryptor.update(hash) + encryptor.finalize()
    return sign

async def find_device(
        timeout: int | None = None,
        template: str = "EMG-SENS",
) -> tuple[BLEDevice, AdvertisementData] | tuple[None, None]:
    """
    Find ble device on template.
    """
    async with BleakScanner() as scanner:
        with contextlib.suppress(asyncio.TimeoutError):
            async with asyncio.timeout(timeout):
                async for device, advertisement in scanner.advertisement_data():
                    if device is not None and device.name is not None and device.name.startswith(template):
                        return device, advertisement
    return None, None


class EMGSens(BleakClient):

    UUID_CONTROL_SERVICE = "7395ca15-5997-5a1b-a138-75a7a573b8e5"
    UUID_EVENT_SERVICE = "f553739f-9f1f-538d-a7d3-cd987b395eb5"
    UUID_DATA_SERVICE = "a397cc38-e8c3-5d7c-9353-31bae53881ff"
    UUID_BATTERY_SERVICE = "5c979c9f-a1ac-5715-9a1b-f81a581179d9"
    UUID_ACQUISITION_SERVICE = "75851135-953a-7739-c781-5a935531397a"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fs_data = 100 # data acquisition frequency
        self._operation_lock = asyncio.Lock()

    def _check_operation_lock(self) -> None:
        """ Check and print message if lock occupied. """
        if self._operation_lock.locked():
            print("Operation already in progress... Waiting for it to complete.")

    async def setup(self, cmd: Command, settings: Optional[Settings] = None) -> None:
        """ Device control """
        self._check_operation_lock()
        if settings is None:
            settings = b''
        async with self._operation_lock:
            data = cmd.value.to_bytes() + bytes(settings)
            data += get_control_sum(data, key=BLE_KEY)
            await self.write_gatt_char(
                char_specifier=EMGSens.UUID_CONTROL_SERVICE,
                data=data,
            )

    async def get_data(self, settings: Settings, data_queue: asyncio.Queue) -> None:
        """ Subscribe and get data from ble service """
        async def data_handler(_, raw_data: bytearray):
            counter, e_emg, accel, gyro = decoder.decode_data(raw_data)
            # put data in async queue
            await data_queue.put({
                "counter": counter,
                "acceleration": accel,  # in mg
                "gyro": gyro            # in mdps
            })

        await self.setup(cmd=Command.AcquisitionStart, settings=settings)
        decoder = Decoder(settings)
        await self.start_notify(EMGSens.UUID_DATA_SERVICE, data_handler)

    async def stop(self) -> None:
        """ Stop acquisition data """
        self._check_operation_lock()
        if self._operation_lock:
            await self.stop_notify(EMGSens.UUID_DATA_SERVICE)
            await self.setup(cmd=Command.AcquisitionStop)

    async def close(self) -> None:
        """ Close connection """
        self._check_operation_lock()
        if self._operation_lock:
            await self.setup(cmd=Command.ConnectionClose)