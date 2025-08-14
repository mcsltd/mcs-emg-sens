import asyncio
import logging
import numpy as np
from typing import Optional

from PySide6 import QtAsyncio
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from pyqtgraph import LegendItem

from constants import SamplingRate, EventType, Channel
from device import EMGSens, find_device
from structures import Settings
from ui.main_window import Ui_MainWindow

import pyqtgraph as pg

RED = pg.mkPen(color=(255, 0, 0))
GREEN = pg.mkPen(color=(0, 255, 0))

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # emgsens
        self.data_queue = asyncio.Queue()
        self.device: Optional[EMGSens] = None

        # data
        self.time = np.array([])
        self.ax, self.ay, self.az = (np.array([]),) * 3
        self.wx, self.wy, self.wz = (np.array([]),) * 3

        # plots
        self.plotWidget.setLabel("left", "mdps, mg", pen=pg.mkPen(color='k'))
        self.plotWidget.getAxis("left").setPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("left").setTextPen(pg.mkPen(color='k'))
        self.plotWidget.setLabel("bottom", "Time (sec)", pen=pg.mkPen(color='k'))
        self.plotWidget.getAxis("bottom").setPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("bottom").setTextPen(pg.mkPen(color='k'))
        self.plotWidget.addLegend()
        self.plotWidget.setBackground("w")

        self.plot_ax, self.plot_ay, self.plot_az = (
            self.plotWidget.plot(self.time, self.ax, label="ax", pen=GREEN),
            self.plotWidget.plot(self.time, self.ay, label="ay", pen=GREEN),
            self.plotWidget.plot(self.time, self.az, label="az", pen=GREEN)
        )
        self.plot_wx, self.plot_wy, self.plot_wz = (
            self.plotWidget.plot(self.time, self.wx, label="wx", pen=RED),
            self.plotWidget.plot(self.time, self.wy, label="wy", pen=RED),
            self.plotWidget.plot(self.time, self.wz, label="wz", pen=RED)
        )

        # set legends
        self.legend = LegendItem((15, 15), offset=(50, 50))
        self.legend.setParentItem(self.plotWidget.getPlotItem())
        self.legend.addItem(self.plot_ax, name="ax")
        self.legend.addItem(self.plot_ay, name="ay")
        self.legend.addItem(self.plot_az, name="az")

        self.legend.addItem(self.plot_wx, name="wx")
        self.legend.addItem(self.plot_wy, name="wy")
        self.legend.addItem(self.plot_wz, name="wz")


        self.pushButtonConnect.clicked.connect(lambda: asyncio.ensure_future(self.connect_device()))
        self.pushButtonStart.clicked.connect(lambda: asyncio.ensure_future(self.start_device()))
        self.pushButtonStop.clicked.connect(lambda: asyncio.ensure_future(self.stop_device()))

        # for setup scale
        for v in [(0, "±125dps"), (1, "±250dps"), (2, "±500dps"), (3, "±1000dps"), (4, "±2000dps")]:
            self.comboBoxGyroscopeScale.addItem(v[1], userData=v[0])
        for v in [(0, "±2g"), (1, "±4g"), (2, "±8g"), (3, "±16g")]:
            self.comboBoxAccelerometerScale.addItem(v[1], userData=v[0])

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(lambda: asyncio.ensure_future(self.update_plot()))

    async def connect_device(self) -> None:

        ble_device, _ = await find_device()
        self.device = EMGSens(ble_device)

        try:
            await self.device.connect()
        except Exception as exc:
            err_info = QMessageBox.information(
                self, "Connect error",
                f"An error occurred while connect to the device",
                QMessageBox.StandardButton.Ok
            )
        else:
            # set connected device name
            self.labelDeviceName.setText(ble_device.name)

            # deactivate
            self.pushButtonConnect.setEnabled(False)

            # activate
            self.pushButtonStart.setEnabled(True)
            self.comboBoxGyroscopeScale.setEnabled(True)
            self.comboBoxAccelerometerScale.setEnabled(True)


    async def start_device(self) -> None:
        settings = Settings(
                DataRateEMG=SamplingRate.HZ_1000.value,
                AveragingWindowEMG=10,
                FullScaleAccelerometer=self.comboBoxAccelerometerScale.currentData(),
                FullScaleGyroscope=self.comboBoxGyroscopeScale.currentData(),
                EnabledChannels=Channel.X | Channel.Y | Channel.Z | Channel.P | Channel.R | Channel.YAW,
                EnabledEvents=EventType.BUTTON,
                ActivityThreshold=1
            )
        await self.device.get_data(settings=settings, data_queue=self.data_queue)
        self.timer.start()
        # activate
        self.pushButtonStop.setEnabled(True)
        # deactivate
        self.pushButtonStart.setEnabled(False)
        self.comboBoxGyroscopeScale.setEnabled(False)
        self.comboBoxAccelerometerScale.setEnabled(False)

    async def stop_device(self) -> None:
        await self.device.stop()
        self.timer.stop()

        # deactivate
        self.pushButtonStop.setEnabled(False)

        # activate
        self.pushButtonStart.setEnabled(True)
        self.comboBoxGyroscopeScale.setEnabled(True)
        self.comboBoxAccelerometerScale.setEnabled(True)

    async def update_plot(self) -> None:
        if not self.device.is_connected:
            self.timer.stop()
            info = QMessageBox.information(
                self, "Connection lost",
                f"Сonnection to device lost",
                QMessageBox.StandardButton.Ok
            )

        data = await self.data_queue.get()
        self.data_queue.task_done()

        self.ax = np.append(self.ax, data["acceleration"][0, :])
        self.ay = np.append(self.ay, data["acceleration"][1, :])
        self.az = np.append(self.az, data["acceleration"][2, :])

        self.wx = np.append(self.wx, data["gyro"][0, :])
        self.wy = np.append(self.wy, data["gyro"][1, :])
        self.wz = np.append(self.wz, data["gyro"][2, :])

        if len(self.time) == 0:
            self.time = np.arange(1, len(self.ax) + 1) * 0.01
        else:
            self.time = np.append(
                self.time,
                np.arange(1, len(data["acceleration"][0, :]) + 1) / self.device.fs_data + self.time[-1]
            )

        self.plot_ax.setData(self.time, self.ax)
        self.plot_ay.setData(self.time, self.ay)
        self.plot_az.setData(self.time, self.az)

        self.plot_wx.setData(self.time, self.wx)
        self.plot_wy.setData(self.time, self.wy)
        self.plot_wz.setData(self.time, self.wz)

        if self.time[-1] < 3:
            self.plotWidget.setXRange(0, 3)
        else:
            self.plotWidget.setXRange(self.time[-1] - 3, self.time[-1])



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    app = QApplication([])

    window = MainWindow()
    window.showMaximized()

    QtAsyncio.run(handle_sigint=True, debug=True)

