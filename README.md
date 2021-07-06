# 一个 python 的异步 adb 包

## 目的

实现这个工具包的目的在于，通过执行想对应的 adb 指令，可以使用 python 来对其日志进行想对应的分析，仅此而已。当然，也可以有更多的应用场景，但是，目前仅仅为了把命令执行后的日志处理更加优雅，当然，需要同时执行多个指令的情况下，这种场景是始终存在的。

## 安装
```shell
pip install aadb
```

## 使用
```python
import aadb
import asyncio


async def main():
    adb = aadb.create_bridge()
    device = (await adb.devices())[0]
    asyncio.create_task(device.logcat(pipeline=lambda x: print(x)))
    await asyncio.sleep(3)
    print(await device.get_properties())
    await asyncio.sleep(3)
    print(await device.list_package())
    await device.shell('dumpsys meminfo', pipeline=lambda x: print(x))

if __name__ == '__main__':
    aadb.start(main())
```