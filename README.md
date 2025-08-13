
# Main
The repo contains a class for managing and retrieving data from EMGsens with using bleak and useful scripts.

To run, you need a .env file with a key for signing data and control EMGsens. You need to request it.

```commandline
BLE_KEY=...
```

## Run application

1. Run in command line: `install.bat`
2. Run in command line: `run.bat`

## Components
 * device.py - class EMGsens
 * decoder.py - class for decoding data (gyro, acceleration) from device
 * main.py - gui for control device


## Dependencies

Please, install library:

```commandline
pip install -r requirements.txt
```

App testing and running on Python3.13

OS: windows10