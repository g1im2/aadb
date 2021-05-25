from abc import abstractmethod
from enum import Enum
from typing import Dict, List


class Log(object):

    class LogLevel(Enum):
        VERBOSE = (2, "verbose", 'V')
        DEBUG = (3, "debug", 'D')
        INFO = (4, "info", 'I')
        WARN = (5, "warn", 'W')
        ERROR = (6, "error", 'E')
        ASSERT = (7, "assert", 'A')

        def __init__(self, int_priority: int, string_value: str, priority_char: str):
            self.priority_level = int_priority
            self.string_value = string_value
            self.priority_letter = priority_char


class DdmPreferences(object):

    DEFAULT_INITIAL_THREAD_UPDATE = False
    DEFAULT_INITIAL_HEAP_UPDATE = False
    DEFAULT_SELECTED_DEBUG_PORT = 8700
    DEFAULT_DEBUG_PORT_BASE = 8600
    DEFAULT_LOG_LEVEL = Log.LogLevel.ERROR
    DEFAULT_TIMEOUT = 5000
    DEFAULT_PROFILER_BUFFER_SIZE_MB = 8
    DEFAULT_USE_ADBHOST = False
    DEFAULT_ADBHOST_VALUE = "127.0.0.1"

    sThreadUpdate = DEFAULT_INITIAL_THREAD_UPDATE
    sInitialHeapUpdate = DEFAULT_INITIAL_HEAP_UPDATE
    sSelectedDebugPort = DEFAULT_SELECTED_DEBUG_PORT
    sDebugPortBase = DEFAULT_DEBUG_PORT_BASE
    sLogLevel = DEFAULT_LOG_LEVEL
    sTimeOut = DEFAULT_TIMEOUT
    sProfilerBufferSizeMb = DEFAULT_PROFILER_BUFFER_SIZE_MB
    sUseAdbHost = DEFAULT_USE_ADBHOST
    sAdbHostValue = DEFAULT_ADBHOST_VALUE

    @staticmethod
    def get_initial_thread_update() -> bool:
        return DdmPreferences.sThreadUpdate

    @staticmethod
    def set_initial_thread_update(state: bool):
        DdmPreferences.sThreadUpdate = state

    @staticmethod
    def get_initial_heap_update() -> bool:
        return DdmPreferences.sInitialHeapUpdate

    @staticmethod
    def set_initial_heap_update(state: bool):
        DdmPreferences.sInitialHeapUpdate = state

    @staticmethod
    def get_selected_debug_port() -> int:
        return DdmPreferences.sSelectedDebugPort

    @staticmethod
    def set_selected_debug_port(port: int):
        DdmPreferences.sSelectedDebugPort = port

        monitor_thread = MonitorThread.getInstance();
        if monitor_thread is not None:
            monitor_thread.set_debug_selected_port(port)

    @staticmethod
    def get_debug_port_base() -> int:
        return DdmPreferences.sDebugPortBase

    @staticmethod
    def set_debug_port_base(port: int):
        DdmPreferences.sDebugPortBase = port

    @staticmethod
    def get_log_level() -> Log.LogLevel:
        return DdmPreferences.sLogLevel

    @staticmethod
    def set_log_level(value: str):
        log_Level = Log.LogLevel.get_by_string(value)
        Log.set_level(log_Level)

    @staticmethod
    def get_timeout() -> int:
        return DdmPreferences.sTimeOut

    @staticmethod
    def set_timeout(timeout: int):
        DdmPreferences.sTimeOut = timeout

    @staticmethod
    def get_profiler_buffer_size_mb() -> int:
        return DdmPreferences.sProfilerBufferSizeMb

    @staticmethod
    def set_profiler_buffer_size_mb(buffer_size_mb: int):
        DdmPreferences.sProfilerBufferSizeMb = buffer_size_mb

    @staticmethod
    def get_use_adb_host() -> bool:
        return DdmPreferences.sUseAdbHost

    @staticmethod
    def set_use_adb_host(use_adb_host: bool):
        DdmPreferences.sUseAdbHost = use_adb_host

    @staticmethod
    def get_adb_host_value() -> str:
        return DdmPreferences.sAdbHostValue

    @staticmethod
    def set_adb_host_value(adb_host_value: str):
        DdmPreferences.sAdbHostValue = adb_host_value


class Client(object):
    SERVER_PROTOCOL_VERSION = 1

    CHANGE_NAME = 0x0001
    CHANGE_DEBUGGER_STATUS = 0x0002
    CHANGE_PORT = 0x0004
    CHANGE_THREAD_MODE = 0x0008
    CHANGE_THREAD_DATA = 0x0010
    CHANGE_HEAP_MODE = 0x0020
    CHANGE_HEAP_DATA = 0x0040
    CHANGE_NATIVE_HEAP_DATA = 0x0080
    CHANGE_THREAD_STACKTRACE = 0x0100
    CHANGE_HEAP_ALLOCATIONS = 0x0200
    CHANGE_HEAP_ALLOCATION_STATUS = 0x0400
    CHANGE_METHOD_PROFILING_STATUS = 0x0800

    CHANGE_INFO = CHANGE_NAME | CHANGE_DEBUGGER_STATUS | CHANGE_PORT

    INITIAL_BUF_SIZE = 2 * 1024
    MAX_BUF_SIZE = 200 * 1024 * 1024

    WRITE_BUF_SIZE = 256

    ST_INIT = 1
    ST_NOT_JDWP = 2
    ST_AWAIT_SHAKE = 10
    ST_NEED_DDM_PKT = 11
    ST_NOT_DDM = 12
    ST_READY = 13
    ST_ERROR = 20
    ST_DISCONNECTED = 21

    def __init__(self, device: 'Device', channel, pid: int):
        self.device = device
        self.channel = channel

        self.read_buffer = None
        self.write_buffer = None

        self.out_standing_reqs = None
        self.conn_state = self.ST_INIT

        self.client_data = ClientData(pid)

        self.thread_update_enabled = DdmPreferences.get_initial_thread_update()
        self.heap_update_enabled = DdmPreferences.get_initial_heap_update()



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
