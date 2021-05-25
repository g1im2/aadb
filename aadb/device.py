from abc import abstractmethod
from enum import Enum
from typing import Dict, List


class Client(object):
    pass


class SyncService(object):
    pass


class FileListingService(object):
    pass


class RawImage(object):
    pass


class LogReceiver(object):
    pass


class IShellOutputReceiver(object):

    @abstractmethod
    def add_output(self, data: bytes, offset: int, length: int):
        pass

    @abstractmethod
    def flush(self):
        pass

    @abstractmethod
    def is_cancelled(self) -> bool:
        pass


class IShellEnabledDevice(object):

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def execute_shell_command(self, command: str, receiver: IShellOutputReceiver):
        pass


class IDevice(IShellEnabledDevice):
    PROP_BUILD_VERSION = "ro.build.version.release"
    PROP_BUILD_API_LEVEL = "ro.build.version.sdk"
    PROP_BUILD_CODENAME = "ro.build.version.codename"
    PROP_DEVICE_MODEL = "ro.product.model"
    PROP_DEVICE_MANUFACTURER = "ro.product.manufacturer"

    PROP_DEBUGGABLE = "ro.debuggable"

    FIRST_EMULATOR_SN = "emulator-5554"
    CHANGE_STATE = 0x0001
    CHANGE_CLIENT_LIST = 0x0002
    CHANGE_BUILD_INFO = 0x0004

    PROP_BUILD_VERSION_NUMBER = PROP_BUILD_API_LEVEL

    MNT_EXTERNAL_STORAGE = "EXTERNAL_STORAGE"
    MNT_ROOT = "ANDROID_ROOT"
    MNT_DATA = "ANDROID_DATA"

    class DeviceState(Enum):
        BOOTLOADER = 'bootloader'
        OFFLINE = 'offline'
        ONLINE = 'device'
        RECOVERY = 'recovery'

        def __init__(self, state):
            self.state = state

        def get_state(self, state: str) -> 'DeviceState':
            print(self._member_map_)
            for v in self._member_map_.values():
                if v.state == state:
                    return v
            return None

    class DeviceUnixSocketNamespace(Enum):
        ABSTRACT = 'localabstract'
        FILESYSTEM = 'localfilesystem'
        RESERVED = 'localreserved'

        def __init__(self, dsn_type: str):
            self.__dsn_type = dsn_type

        def get_type(self) -> str:
            return self.__dsn_type

    @abstractmethod
    def get_serial_number(self) -> str:
        pass

    @abstractmethod
    def get_avd_name(self) -> str:
        pass

    @abstractmethod
    def get_state(self) -> DeviceState:
        pass

    @abstractmethod
    def get_properties(self) -> Dict[str: str]:
        pass

    @abstractmethod
    def get_property_count(self) -> int:
        pass

    @abstractmethod
    def are_properties_set(self) -> bool:
        pass

    @abstractmethod
    def get_property_sync(self, name: str) -> str:
        pass

    @abstractmethod
    def get_property_cache_or_sync(self, name: str) -> str:
        pass

    @abstractmethod
    def get_mount_point(self, name: str) -> str:
        pass

    @abstractmethod
    def is_online(self) -> bool:
        pass

    @abstractmethod
    def is_emulator(self) -> bool:
        pass

    @abstractmethod
    def is_offline(self) -> bool:
        pass

    @abstractmethod
    def is_bootloader(self) -> bool:
        pass

    @abstractmethod
    def has_clients(self) -> bool:
        pass

    @abstractmethod
    def get_clients(self) -> List[Client]:
        pass

    @abstractmethod
    def get_client(self, application_name: str) -> Client:
        pass

    @abstractmethod
    def get_sync_service(self) -> SyncService:
        pass

    @abstractmethod
    def get_file_listing_service(self) -> FileListingService:
        pass

    @abstractmethod
    def get_screen_shot(self) -> RawImage:
        pass

    @abstractmethod
    def execute_shell_command(self, command: str, receiver: IShellOutputReceiver):
        pass

    @abstractmethod
    def run_event_log_service(self, receiver: LogReceiver):
        pass

    @abstractmethod
    def run_log_service(self, log_name: str, receiver: LogReceiver):
        pass

    @abstractmethod
    def create_forward(self, local_port: int, remote_port: int, namespace: DeviceUnixSocketNamespace = None):
        pass

    @abstractmethod
    def remove_forward(self, local_port: int, remote_port: int, namespace: DeviceUnixSocketNamespace = None):
        pass

    @abstractmethod
    def get_client_name(self, pid: int):
        pass

    @abstractmethod
    def push_file(self, local: str, remote: str):
        pass

    @abstractmethod
    def pull_file(self, remote: str, local: str):
        pass

    @abstractmethod
    def install_package(self, package_file_path: str, reinstall: bool, *extra_args):
        pass

    @abstractmethod
    def sync_package_to_device(self, local_file_path: str):
        pass

    @abstractmethod
    def install_remote_package(self, remote_file_path, reinstall: bool, *extra_args):
        pass

    @abstractmethod
    def remove_remote_package(self, remote_file_path: str):
        pass

    @abstractmethod
    def uninstall_package(self, package_name: str) -> str:
        pass

    @abstractmethod
    def reboot(self, into: str):
        pass

    @abstractmethod
    def get_battery_level(self, freshness_ms: float) -> int:
        pass


if __name__ == '__main__':
    print(IDevice.DeviceState.ONLINE.get_state('device'))