from abc import abstractmethod
from enum import Enum
from typing import Dict, List
from threading import Thread


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


class IStackTraceInfo(object):

    @abstractmethod
    def get_stack_trace(self) -> List[object]:
        pass


class AllocationInfo()


class AndroidDebugBridge(object):
    ADB_VERSION_MICRO_MIN = 20
    ADB_VERSION_MICRO_MAX = -1

    sAdbVersion = "^.*(\\d+)\\.(\\d+)\\.(\\d+)$"

    ADB = "adb"
    DDMS = "ddms"
    SERVER_PORT_ENV_VAR = "ANDROID_ADB_SERVER_PORT"

    ADB_HOST = "127.0.0.1"
    ADB_PORT = 5037

    class IDebugBridgeChangeListener(object):

        @abstractmethod
        def bridge_changed(self, bridge: 'AndroidDebugBridge'):
            pass

    class IDeviceChangeListener(object):

        @abstractmethod
        def device_connected(self, device: 'IDevice'):
            pass

        @abstractmethod
        def device_disconnected(self, device: 'IDevice'):
            pass

        @abstractmethod
        def device_changed(self, device: 'IDevice', change_mask: int):
            pass

    class IClientChangeListener(object):

        @abstractmethod
        def client_changed(self, client: 'Client', change_mask: int):
            pass

    def __init__(self, os_location: str = None):
        self.adb_os_location = os_location

        self.version_check: bool = False
        self.started: bool = False
        self.device_monitor: DeviceMonitor = None
        self.bridge_listeners = list()
        self.device_listeners = list()
        self.client_listeners = list()

        self.__check_adb_version()

    def __check_adb_version(self):
        self.version_check = False

        if self.adb_os_location is None:
            return

        command = []
        command[0] = self.adb_os_location
        command[1] = 'version'
        print(self.DDMS, 'checking {} version'.format(self.adb_os_location))




class MonitorThread(Thread):
    CLIENT_CONNECTED = 1
    CLIENT_READY = 2
    CLIENT_DISCONNECTED = 3
    mQuit = False

    sInstance = None

    def __init__(self):
        super().__init__(name='Monitor')
        self.client_list = list()
        self.handler_map = dict()
        self.new_debug_selected_port = DdmPreferences.get_selected_debug_port()

        self.selector = None
        self.debug_selected_port = -1
        self.selected_client: Client = None

    def create_instance(self) -> 'MonitorThread':
        self.sInstance = MonitorThread()
        return self.sInstance

    def get_instance(self) -> 'MonitorThread':
        return self.sInstance

    def set_debug_selected_port(self, port: int):
        if self.sInstance is None:
            return

        if


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


class HeapSegment(object):
    pass


class ClientData(object):
    PRE_INITIALIZED = '<pre-initialized>'

    class DebuggerStatus(Enum):
        DEFAULT = 0
        WAITING = 1
        ATTACHED = 2
        ERROR = 3

    class AllocationTrackingStatus(Enum):
        UNKNOWN = 0
        OFF = 1
        ON = 2

    class MethodProfilingStatus(Enum):
        UNKNOWN = 0
        OFF = 1
        ON = 2

    HEAP_MAX_SIZE_BYTES = "maxSizeInBytes"
    HEAP_SIZE_BYTES = "sizeInBytes"
    HEAP_BYTES_ALLOCATED = "bytesAllocated"
    HEAP_OBJECTS_ALLOCATED = "objectsAllocated"

    FEATURE_PROFILING = "method-trace-profiling"
    FEATURE_PROFILING_STREAMING = "method-trace-profiling-streaming"
    FEATURE_OPENGL_TRACING = "opengl-tracing"
    FEATURE_VIEW_HIERARCHY = "view-hierarchy"
    FEATURE_HPROF = "hprof-heap-dump"
    FEATURE_HPROF_STREAMING = "hprof-heap-dump-streaming"

    class HeapData(object):

        def clear_heap_data(self):
            pass


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


class MultiLineReceiver(IShellOutputReceiver):

    def __init__(self):
        self.mTrimLines = True
        self.mUnfinishedLine = None
        self.mArray = list()

    def set_trim_line(self, trim: bool):
        self.mTrimLines = trim

    def add_output(self, data: bytes, offset: int, length: int):
        if not self.is_cancelled():
            s = None
        try:
            s = None
        except Exception:
            s = None

        if self.mUnfinishedLine is not None:
            s = self.mUnfinishedLine + s
            self.mUnfinishedLine = None

        self.mArray.clear()
        start = 0

    def flush(self):
        if self.mUnfinishedLine is not None:
            self.process_new_lines(self.mUnfinishedLine)

        self.done()

    def done(self):
        pass

    @abstractmethod
    def is_cancelled(self) -> bool:
        pass

    @abstractmethod
    def process_new_lines(self, lines: List[str]):
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


class Device(IDevice):
    INSTALL_TIMEOUT = 2 * 60 * 1000
    BATTERY_TIMEOUT = 2 * 1000
    GETPROP_TIMEOUT = 2 * 1000

    RE_EMULATOR_SN = "emulator-(\\d+)"

    LOG_TAG = "Device"
    SEPARATOR = '-'
    UNKNOWN_PACKAGE = ""

    def __init__(self):
        self.mSerialNumber = None
        self.mAvdName = None
        self.mState = None

        self.mProperties = dict()
        self.mMountPoints = dict()

        self.mClients = list()
        self.mClientInfo = dict()
        self.mMonitor = None

        self.mSocketChannel = None
        self.mArePropertiesSet = False
        self.mLastBatteryLevel = None
        self.mLastBatteryCheckTime = 0
        self.mName = None

    def get_serial_number(self) -> str:
        pass

    def get_avd_name(self) -> str:
        pass

    def get_state(self) -> IDevice.DeviceState:
        pass

    def get_properties(self) -> Dict[str: str]:
        pass

    def get_property_count(self) -> int:
        pass

    def are_properties_set(self) -> bool:
        pass

    def get_property_sync(self, name: str) -> str:
        pass

    def get_property_cache_or_sync(self, name: str) -> str:
        pass

    def get_mount_point(self, name: str) -> str:
        pass

    def is_online(self) -> bool:
        pass

    def is_emulator(self) -> bool:
        pass

    def is_offline(self) -> bool:
        pass

    def is_bootloader(self) -> bool:
        pass

    def has_clients(self) -> bool:
        pass

    def get_clients(self) -> List[Client]:
        pass

    def get_client(self, application_name: str) -> Client:
        pass

    def get_sync_service(self) -> SyncService:
        pass

    def get_file_listing_service(self) -> FileListingService:
        pass

    def get_screen_shot(self) -> RawImage:
        pass

    def execute_shell_command(self, command: str, receiver: IShellOutputReceiver):
        pass

    def run_event_log_service(self, receiver: LogReceiver):
        pass

    def run_log_service(self, log_name: str, receiver: LogReceiver):
        pass

    def create_forward(self, local_port: int, remote_port: int, namespace: DeviceUnixSocketNamespace = None):
        pass

    def remove_forward(self, local_port: int, remote_port: int, namespace: DeviceUnixSocketNamespace = None):
        pass

    def get_client_name(self, pid: int):
        pass

    def push_file(self, local: str, remote: str):
        pass

    def pull_file(self, remote: str, local: str):
        pass

    def install_package(self, package_file_path: str, reinstall: bool, *extra_args):
        pass

    def sync_package_to_device(self, local_file_path: str):
        pass

    def install_remote_package(self, remote_file_path, reinstall: bool, *extra_args):
        pass

    def remove_remote_package(self, remote_file_path: str):
        pass

    def uninstall_package(self, package_name: str) -> str:
        pass

    def reboot(self, into: str):
        pass

    def get_battery_level(self, freshness_ms: float) -> int:
        pass

    def get_name(self) -> str:
        pass


if __name__ == '__main__':
    print(IDevice.DeviceState.ONLINE.get_state('device'))
