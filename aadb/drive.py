import os

from enum import Enum

from adb import adb_commands
from adb import sign_pycryptodome


class AdbConnectType(Enum):
    IP = 0
    USB = 1


def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AttributeError:
            AdbDrive.device = adb_commands.AdbCommands()
            if AdbConnectType is not None and AdbDrive.connect_type == 'ip':
                AdbDrive.device.ConnectDevice(serial=AdbDrive.connect_ip.encode('utf-8'),
                                              default_timeout_ms=60000,
                                              rsa_keys=[AdbDrive.signer])
            else:
                AdbDrive.device.ConnectDevice(rsa_keys=[AdbDrive.signer])
            func(*args, **kwargs)

    return wrapper


class AdbDrive(object):
    adb_key_path = os.path.expanduser('~/.android/adbkey')
    signer = sign_pycryptodome.PycryptodomeAuthSigner(adb_key_path)
    device = adb_commands.AdbCommands()
    connect_type = None
    connect_ip = None

    def __init__(self, connect_type: AdbConnectType = AdbConnectType.USB, connect_ip: str = '127.0.0.1'):
        self.connect_type = connect_type
        self.connect_ip = connect_ip
        if type(self.connect_type) != AdbConnectType:
            raise RuntimeError('adb connect type was error')

        if connect_type == AdbConnectType.USB:
            self.device.ConnectDevice(rsa_keys=[self.signer])
        elif connect_type == AdbConnectType.IP:
            self.device.ConnectDevice(serial=connect_ip.encode('utf-8'),
                                      default_timeout_ms=60000,
                                      rsa_keys=[self.signer])

    @catch_exception
    def exec(self, cmd: str):
        exec_result = self.device.Shell(command=cmd)
        for result_line in [line for line in exec_result.split('\n') if line]:
            yield result_line

    def reboot(self):
        self.device.Reboot()

    def close(self):
        self.device.Close()
